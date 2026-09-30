#!/usr/bin/env python3
"""Generate research_notes.md and chapter_plan.md from a pre-interviewed session.

Reads guest_profile.json (and pre_interview.md when present) from a session
directory created by pre_interview_cli.py, asks Claude for a research brief and
a four-chapter interview outline, and writes both as Markdown in the shapes
defined in references/artifact-schemas.md.

Requires the Anthropic Python SDK (`pip install anthropic`) and credentials
such as ANTHROPIC_API_KEY. Use --dry-run to inspect the prompt without calling
the API.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


DEFAULT_MODEL = "claude-opus-5-5"
DEFAULT_EFFORT = "high"

CHAPTERS = [
    ("origin", "1. Origin"),
    ("key_choices", "2. Key Choices"),
    ("present", "3. Present"),
    ("philosophy", "4. Philosophy"),
]

RESEARCH_SECTIONS = [
    ("guest_summary", "Guest Summary"),
    ("era_context", "Era Context"),
    ("city_context", "City Context"),
    ("industry_context", "Industry Context"),
    ("public_source_notes", "Public Source Notes"),
    ("deep_follow_up_questions", "Deep Follow-Up Questions"),
    ("contradictions_to_test", "Contradictions To Test"),
    ("claims_to_verify", "Claims To Verify"),
]

# Starter templates written by create_session.py / pre_interview_cli.py. A file
# that still matches its template is safe to overwrite without --force.
STARTER_TEMPLATES = {
    "research_notes.md": "# Research Notes\n\n"
    + "\n\n".join(f"## {title}" for _, title in RESEARCH_SECTIONS)
    + "\n",
    "chapter_plan.md": "# Chapter Plan\n\n"
    + "\n\n".join(
        f"## {title}\n- Goal:\n- Must ask:\n- Exit condition:" for _, title in CHAPTERS
    )
    + "\n",
}

STRING_LIST = {"type": "array", "items": {"type": "string"}}

CHAPTER_SCHEMA = {
    "type": "object",
    "properties": {
        "goal": {"type": "string"},
        "must_ask": STRING_LIST,
        "exit_condition": {"type": "string"},
    },
    "required": ["goal", "must_ask", "exit_condition"],
    "additionalProperties": False,
}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "research_notes": {
            "type": "object",
            "properties": {
                "guest_summary": {"type": "string"},
                "era_context": STRING_LIST,
                "city_context": STRING_LIST,
                "industry_context": STRING_LIST,
                "public_source_notes": STRING_LIST,
                "deep_follow_up_questions": STRING_LIST,
                "contradictions_to_test": STRING_LIST,
                "claims_to_verify": STRING_LIST,
            },
            "required": [key for key, _ in RESEARCH_SECTIONS],
            "additionalProperties": False,
        },
        "chapter_plan": {
            "type": "object",
            "properties": {key: CHAPTER_SCHEMA for key, _ in CHAPTERS},
            "required": [key for key, _ in CHAPTERS],
            "additionalProperties": False,
        },
    },
    "required": ["research_notes", "chapter_plan"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """\
You are the research producer for a longform, biographical interview program. \
The program records how controllable variables shape long-term outcomes: every \
episode asks which variable changed, what it really cost, and which part of the \
lesson transfers to another person. It rejects success theater.

You receive a guest profile and raw producer pre-interview notes. Produce two \
working documents for the host: a research brief and a four-chapter interview \
outline.

Research brief:
- guest_summary: 50 to 80 words (or about 100 to 160 Chinese characters) that \
say who the guest is and which variable makes the story worth recording.
- era_context, city_context, industry_context: background cards on what was \
happening in the years, places, and industries where the guest made key \
choices, and what options were realistically available. Tie each card to a \
specific choice in the profile.
- public_source_notes: kinds of public material worth checking (posts, talks, \
interviews, company records) and what each could confirm. You have no search \
access in this step, so never claim to have read a source or invent titles, \
URLs, or quotes.
- deep_follow_up_questions: five to ten questions that force timestamps, \
cities, people, constraints, and costs out of floating answers.
- contradictions_to_test: tensions between the self-definition, the turning \
points, and the least-wanted question; places where the story sounds polished.
- claims_to_verify: specific claims from the pre-interview that should be \
confirmed before anything is published.

Interview outline, four chapters in this order:
1. origin: family, city, education, and early constraints.
2. key_choices: isolate one to three turning points and test whether they were \
real variables.
3. present: compare the current self-narrative against observed behavior and \
outcomes.
4. philosophy: durable lessons and unresolved questions, without becoming \
generic advice. This is where the least-wanted question is usually handled.
For each chapter give a goal, three to six must-ask questions, and an exit \
condition that says what insight or contradiction must be on the table before \
moving on.

Rules:
- Use only facts present in the input. Anything missing, vague, or inferred is \
marked "unknown" or "needs_confirmation"; general era or industry background \
from your own knowledge is fine but must be phrased as context, not as a fact \
about the guest.
- Respect the guest's boundaries: do not plan questions on off-record or \
forbidden topics, and flag any sensitive topic that needs consent first.
- These are working documents, not public copy. Do not write teaser lines.
- Interview craft is abstract: direct, curious, pressure-testing, never \
humiliating. Do not imitate or name any real host.
- Write the content in the same language as the pre-interview answers.
"""


def load_session(session_dir: Path) -> tuple[dict, str]:
    profile_path = session_dir / "guest_profile.json"
    if not profile_path.exists():
        raise SystemExit(
            f"No guest_profile.json in {session_dir}. Run pre_interview_cli.py first."
        )
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    pre_interview_path = session_dir / "pre_interview.md"
    pre_interview = (
        pre_interview_path.read_text(encoding="utf-8")
        if pre_interview_path.exists()
        else ""
    )
    return profile, pre_interview


def build_user_message(profile: dict, pre_interview: str) -> str:
    parts = [
        "<guest_profile>",
        json.dumps(profile, ensure_ascii=False, indent=2),
        "</guest_profile>",
    ]
    if pre_interview.strip():
        parts += ["<pre_interview>", pre_interview.strip(), "</pre_interview>"]
    parts.append(
        "Write the research brief and the four-chapter interview outline for this guest."
    )
    return "\n\n".join(parts)


def call_claude(client, model: str, effort: str, user_message: str) -> dict:
    with client.beta.messages.stream(
        model=model,
        max_tokens=32000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
        thinking={"type": "adaptive"},
        output_config={
            "effort": effort,
            "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
        },
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason == "refusal":
        raise SystemExit("Claude declined this request; nothing was written.")
    if response.stop_reason == "max_tokens":
        raise SystemExit("Claude's answer was cut off at max_tokens; nothing was written.")
    text = next(block.text for block in response.content if block.type == "text")
    return json.loads(text)


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items if item.strip()) or "- unknown"


def render_research_notes(notes: dict) -> str:
    lines = ["# Research Notes\n"]
    for key, title in RESEARCH_SECTIONS:
        value = notes[key]
        if key == "deep_follow_up_questions":
            body = "\n".join(f"{i}. {q}" for i, q in enumerate(value, 1)) or "- unknown"
        elif isinstance(value, list):
            body = bullets(value)
        else:
            body = value.strip() or "unknown"
        lines.append(f"## {title}\n\n{body}\n")
    return "\n".join(lines)


def render_chapter_plan(plan: dict) -> str:
    lines = ["# Chapter Plan\n"]
    for key, title in CHAPTERS:
        chapter = plan[key]
        must_ask = "\n".join(f"  - {q}" for q in chapter["must_ask"])
        lines.append(
            f"## {title}\n"
            f"- Goal: {chapter['goal']}\n"
            f"- Must ask:\n{must_ask}\n"
            f"- Exit condition: {chapter['exit_condition']}\n"
        )
    return "\n".join(lines)


def check_writable(session_dir: Path, force: bool) -> None:
    for name, template in STARTER_TEMPLATES.items():
        path = session_dir / name
        if force or not path.exists():
            continue
        if path.read_text(encoding="utf-8") != template:
            raise SystemExit(
                f"{path} already has content. Re-run with --force to overwrite it."
            )


def record_meta(session_dir: Path, model: str) -> None:
    meta_path = session_dir / "meta.json"
    meta = (
        json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    )
    meta["research"] = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "model": model,
        "runner": "research_cli",
    }
    meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run(session_dir: Path, client, model: str, effort: str) -> dict:
    profile, pre_interview = load_session(session_dir)
    result = call_claude(client, model, effort, build_user_message(profile, pre_interview))
    (session_dir / "research_notes.md").write_text(
        render_research_notes(result["research_notes"]), encoding="utf-8"
    )
    (session_dir / "chapter_plan.md").write_text(
        render_chapter_plan(result["chapter_plan"]), encoding="utf-8"
    )
    record_meta(session_dir, model)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate research_notes.md and chapter_plan.md with Claude."
    )
    parser.add_argument("session_dir", help="Session directory from pre_interview_cli.py")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Claude model ID")
    parser.add_argument(
        "--effort",
        default=DEFAULT_EFFORT,
        choices=["low", "medium", "high", "xhigh", "max"],
        help="Reasoning effort; defaults to high",
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite files that already have content"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print the prompt without calling the API"
    )
    args = parser.parse_args()

    session_dir = Path(args.session_dir).expanduser().resolve()
    if args.dry_run:
        profile, pre_interview = load_session(session_dir)
        print(SYSTEM_PROMPT)
        print("---")
        print(build_user_message(profile, pre_interview))
        return 0

    check_writable(session_dir, args.force)
    try:
        import anthropic
    except ImportError:
        print("Install the Anthropic SDK first: pip install anthropic", file=sys.stderr)
        return 1

    try:
        run(session_dir, anthropic.Anthropic(), args.model, args.effort)
    except anthropic.AuthenticationError:
        print("Claude API credentials are invalid; check ANTHROPIC_API_KEY.", file=sys.stderr)
        return 1
    except TypeError as error:
        # The SDK raises TypeError when no credentials can be resolved at all.
        if "authentication" not in str(error):
            raise
        print("No Claude API credentials found; set ANTHROPIC_API_KEY.", file=sys.stderr)
        return 1
    except anthropic.APIStatusError as error:
        print(f"Claude API error ({error.status_code}): {error.message}", file=sys.stderr)
        return 1
    except anthropic.APIConnectionError:
        print("Could not reach the Claude API.", file=sys.stderr)
        return 1

    print(f"Written: {session_dir / 'research_notes.md'}")
    print(f"Written: {session_dir / 'chapter_plan.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

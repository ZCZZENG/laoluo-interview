#!/usr/bin/env python3
"""Run a deterministic producer pre-interview and persist session artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


QUESTION_FLOW = [
    {
        "key": "timeline",
        "title": "Timeline",
        "prompt": (
            "先按时间线说：出生/成长城市，以及从小到现在最明显改变你路径的三个阶段。"
        ),
    },
    {
        "key": "family_context",
        "title": "Family and Context",
        "prompt": (
            "原生家庭和成长环境里，哪些约束真实影响了你的选择？可以只说 public-safe 的部分。"
        ),
    },
    {
        "key": "education_path",
        "title": "Education Path",
        "prompt": "教育路径怎么走的？哪一步不是顺理成章，而是你主动调了变量？",
    },
    {
        "key": "turning_points",
        "title": "Turning Points",
        "prompt": (
            "列最多三个转折点：时间、发生了什么、你改了哪个变量、代价是什么、结果是什么。"
        ),
    },
    {
        "key": "self_definition",
        "title": "Self Definition",
        "prompt": "如果只能用一句话定义现在的你，你会怎么说？别包装，尽量具体。",
    },
    {
        "key": "least_wanted_question",
        "title": "Least Wanted Question",
        "prompt": "现在最不想被问的问题是什么？这个问题通常就是正式访谈要处理的核心张力。",
    },
    {
        "key": "boundaries",
        "title": "Boundaries",
        "prompt": "哪些内容不能公开、不能追问、或者必须先确认？",
    },
    {
        "key": "fit_decision",
        "title": "Fit Decision",
        "prompt": "按你的直觉，这个样本现在适合 proceed、delay 还是 stop？为什么？",
    },
]


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    cleaned = re.sub(r"[-\s]+", "-", cleaned)
    return cleaned or "guest"


def session_path(output: str, date: str, guest_name: str) -> Path:
    return Path(output).expanduser().resolve() / f"{date}-{slugify(guest_name)}"


def build_profile(guest_name: str, answers: dict[str, str]) -> dict:
    return {
        "guest": {
            "name": guest_name,
            "public_identity": "",
            "birth_year_or_cohort": "needs_confirmation",
            "growth_city": "needs_confirmation",
            "family_context": {
                "summary": answers.get("family_context", ""),
                "privacy": "internal",
            },
            "education_path": [answers.get("education_path", "")]
            if answers.get("education_path")
            else [],
            "career_path": [],
        },
        "pre_interview_answers": answers,
        "turning_points": [
            {
                "raw_answer": answers.get("turning_points", ""),
                "time": "needs_extraction",
                "event": "needs_extraction",
                "variable_changed": "needs_extraction",
                "cost": "needs_extraction",
                "result": "needs_extraction",
                "evidence": "pre_interview",
                "confidence": "needs_confirmation",
            }
        ]
        if answers.get("turning_points")
        else [],
        "self_definition": answers.get("self_definition", ""),
        "least_wanted_question": answers.get("least_wanted_question", ""),
        "boundaries": {
            "sensitive_topics": [answers.get("boundaries", "")]
            if answers.get("boundaries")
            else [],
            "off_record": [],
            "publication_constraints": [],
        },
        "fit_decision": {
            "status": "needs_review",
            "reason": answers.get("fit_decision", ""),
        },
    }


def write_starter_files(target: Path, guest_name: str, date: str) -> None:
    target.mkdir(parents=True, exist_ok=False)
    session_id = target.name
    (target / "session_memory.json").write_text(
        json.dumps(
            {
                "session_id": session_id,
                "guest_name": guest_name,
                "chapters": [],
                "global_unresolved_threads": [],
                "public_safe_summary": "",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (target / "research_notes.md").write_text(
        "# Research Notes\n\n"
        "## Guest Summary\n\n"
        "## Era Context\n\n"
        "## City Context\n\n"
        "## Industry Context\n\n"
        "## Public Source Notes\n\n"
        "## Deep Follow-Up Questions\n\n"
        "## Contradictions To Test\n\n"
        "## Claims To Verify\n",
        encoding="utf-8",
    )
    (target / "chapter_plan.md").write_text(
        "# Chapter Plan\n\n"
        "## 1. Origin\n- Goal:\n- Must ask:\n- Exit condition:\n\n"
        "## 2. Key Choices\n- Goal:\n- Must ask:\n- Exit condition:\n\n"
        "## 3. Present\n- Goal:\n- Must ask:\n- Exit condition:\n\n"
        "## 4. Philosophy\n- Goal:\n- Must ask:\n- Exit condition:\n",
        encoding="utf-8",
    )
    (target / "transcript.md").write_text("# Transcript\n\n", encoding="utf-8")
    (target / "highlights.md").write_text(
        "# Highlights\n\n"
        "## Public Summary\n\n"
        "## Variables\n\n"
        "## Real Costs\n\n"
        "## Transferable Lessons\n\n"
        "## Strong Moments\n\n"
        "## Teaser Lines\n\n"
        "## Shownotes Seeds\n",
        encoding="utf-8",
    )
    (target / "meta.json").write_text(
        json.dumps(
            {"guest_name": guest_name, "created_at": date, "runner": "pre_interview_cli"},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def run_interview(guest_name: str) -> dict[str, str]:
    print("前采开始。目标是判断样本是否适合，以及最值得深挖的 variable。")
    print("不确定的信息可以写 unknown；不公开的信息可以写 off_record。\n")
    answers: dict[str, str] = {}
    for index, item in enumerate(QUESTION_FLOW, start=1):
        print(f"[{index}/{len(QUESTION_FLOW)}] {item['title']}")
        answer = input(item["prompt"] + "\n> ").strip()
        answers[item["key"]] = answer
        print()
    return answers


def write_outputs(target: Path, guest_name: str, answers: dict[str, str]) -> None:
    pre_interview = ["# Pre-Interview\n"]
    for item in QUESTION_FLOW:
        pre_interview.append(f"## {item['title']}\n")
        pre_interview.append(f"**Question:** {item['prompt']}\n\n")
        pre_interview.append(f"**Answer:** {answers.get(item['key'], '')}\n\n")
    target.joinpath("pre_interview.md").write_text(
        "\n".join(pre_interview), encoding="utf-8"
    )

    target.joinpath("guest_profile.json").write_text(
        json.dumps(build_profile(guest_name, answers), ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    target.joinpath("next_codex_prompt.md").write_text(
        "# Next Codex Prompt\n\n"
        "Use $laoluo-interview to read this session directory, extract a clean "
        "`guest_profile.json`, create `research_notes.md`, and draft a four-chapter "
        f"`chapter_plan.md`: `{target}`\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a producer pre-interview and persist laoluo-interview artifacts."
    )
    parser.add_argument("guest_name", help="Guest name or working title")
    parser.add_argument(
        "--output",
        default="sessions",
        help="Directory where the session folder will be created",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Session date in YYYY-MM-DD format; defaults to today",
    )
    args = parser.parse_args()

    target = session_path(args.output, args.date, args.guest_name)
    write_starter_files(target, args.guest_name, args.date)
    answers = run_interview(args.guest_name)
    write_outputs(target, args.guest_name, answers)
    print(f"Session written: {target}")
    print(f"Continue with: {target / 'next_codex_prompt.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Create a laoluo-interview session workspace with starter artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    cleaned = re.sub(r"[-\s]+", "-", cleaned)
    return cleaned or "guest"


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def build_guest_profile(guest_name: str) -> dict:
    return {
        "guest": {
            "name": guest_name,
            "public_identity": "",
            "birth_year_or_cohort": "unknown",
            "growth_city": "unknown",
            "family_context": {"summary": "unknown", "privacy": "internal"},
            "education_path": [],
            "career_path": [],
        },
        "turning_points": [],
        "self_definition": "",
        "least_wanted_question": "",
        "boundaries": {
            "sensitive_topics": [],
            "off_record": [],
            "publication_constraints": [],
        },
        "fit_decision": {"status": "needs_pre_interview", "reason": ""},
    }


def build_session_memory(session_id: str, guest_name: str) -> dict:
    return {
        "session_id": session_id,
        "guest_name": guest_name,
        "chapters": [],
        "global_unresolved_threads": [],
        "public_safe_summary": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create starter files for a laoluo-interview session."
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

    session_id = f"{args.date}-{slugify(args.guest_name)}"
    session_dir = Path(args.output).expanduser().resolve() / session_id
    session_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        session_dir / "guest_profile.json",
        json.dumps(build_guest_profile(args.guest_name), ensure_ascii=False, indent=2)
        + "\n",
    )
    write_text(
        session_dir / "session_memory.json",
        json.dumps(
            build_session_memory(session_id, args.guest_name),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    write_text(
        session_dir / "research_notes.md",
        "# Research Notes\n\n"
        "## Guest Summary\n\n"
        "## Era Context\n\n"
        "## City Context\n\n"
        "## Industry Context\n\n"
        "## Public Source Notes\n\n"
        "## Deep Follow-Up Questions\n\n"
        "## Contradictions To Test\n\n"
        "## Claims To Verify\n",
    )
    write_text(
        session_dir / "chapter_plan.md",
        "# Chapter Plan\n\n"
        "## 1. Origin\n- Goal:\n- Must ask:\n- Exit condition:\n\n"
        "## 2. Key Choices\n- Goal:\n- Must ask:\n- Exit condition:\n\n"
        "## 3. Present\n- Goal:\n- Must ask:\n- Exit condition:\n\n"
        "## 4. Philosophy\n- Goal:\n- Must ask:\n- Exit condition:\n",
    )
    write_text(session_dir / "transcript.md", "# Transcript\n\n")
    write_text(
        session_dir / "highlights.md",
        "# Highlights\n\n"
        "## Public Summary\n\n"
        "## Variables\n\n"
        "## Real Costs\n\n"
        "## Transferable Lessons\n\n"
        "## Strong Moments\n\n"
        "## Teaser Lines\n\n"
        "## Shownotes Seeds\n",
    )

    print(session_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

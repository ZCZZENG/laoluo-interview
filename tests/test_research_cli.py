"""Tests for research_cli.py using a stubbed Claude client (no network)."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "laoluo-interview" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import create_session  # noqa: E402
import pre_interview_cli  # noqa: E402
import research_cli  # noqa: E402

FAKE_RESULT = {
    "research_notes": {
        "guest_summary": "一位从县城到上海做独立开发的工程师。",
        "era_context": ["2008 年金融危机后的就业收缩"],
        "city_context": ["县城教育资源有限"],
        "industry_context": ["移动互联网红利期"],
        "public_source_notes": ["个人博客：可确认辞职时间"],
        "deep_follow_up_questions": ["辞职那天是哪一年哪一月？", "谁反对你？"],
        "contradictions_to_test": ["自称控制狂，却说转折靠运气"],
        "claims_to_verify": ["needs_confirmation: 2015 年创业"],
    },
    "chapter_plan": {
        key: {
            "goal": f"goal {key}",
            "must_ask": [f"q1 {key}", f"q2 {key}"],
            "exit_condition": f"exit {key}",
        }
        for key, _ in research_cli.CHAPTERS
    },
}


class FakeStream:
    def __init__(self, response):
        self.response = response

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.response


class FakeClient:
    def __init__(self, result=FAKE_RESULT, stop_reason="end_turn"):
        text = json.dumps(result, ensure_ascii=False)
        self.response = SimpleNamespace(
            stop_reason=stop_reason,
            content=[
                SimpleNamespace(type="thinking", thinking=""),
                SimpleNamespace(type="text", text=text),
            ],
        )
        self.calls = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self.stream))

    def stream(self, **kwargs):
        self.calls.append(kwargs)
        return FakeStream(self.response)


def make_session(root: Path) -> Path:
    answers = {item["key"]: f"answer {item['key']}" for item in pre_interview_cli.QUESTION_FLOW}
    target = pre_interview_cli.session_path(str(root), "2026-09-30", "Test Guest")
    pre_interview_cli.write_starter_files(target, "Test Guest", "2026-09-30")
    pre_interview_cli.write_outputs(target, "Test Guest", answers)
    return target


class ResearchCliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_writes_notes_plan_and_meta(self):
        session = make_session(self.root)
        client = FakeClient()
        research_cli.run(session, client, "claude-opus-5-5", "high")

        notes = (session / "research_notes.md").read_text(encoding="utf-8")
        for _, title in research_cli.RESEARCH_SECTIONS:
            self.assertIn(f"## {title}\n", notes)
        self.assertIn("1. 辞职那天是哪一年哪一月？", notes)
        self.assertIn("- needs_confirmation: 2015 年创业", notes)

        plan = (session / "chapter_plan.md").read_text(encoding="utf-8")
        for key, title in research_cli.CHAPTERS:
            self.assertIn(f"## {title}\n- Goal: goal {key}", plan)
            self.assertIn(f"  - q2 {key}", plan)
            self.assertIn(f"- Exit condition: exit {key}", plan)

        meta = json.loads((session / "meta.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["research"]["model"], "claude-opus-5-5")
        self.assertEqual(meta["runner"], "pre_interview_cli")

    def test_request_shape(self):
        session = make_session(self.root)
        client = FakeClient()
        research_cli.run(session, client, "claude-opus-5-5", "high")
        call = client.calls[0]
        self.assertEqual(call["model"], "claude-opus-5-5")
        self.assertEqual(call["thinking"], {"type": "adaptive"})
        self.assertEqual(call["output_config"]["effort"], "high")
        self.assertEqual(call["output_config"]["format"]["type"], "json_schema")
        self.assertEqual(call["fallbacks"], "default")
        user = call["messages"][0]["content"]
        self.assertIn("<guest_profile>", user)
        self.assertIn("<pre_interview>", user)
        self.assertIn("answer least_wanted_question", user)

    def test_refusal_writes_nothing(self):
        session = make_session(self.root)
        before = (session / "research_notes.md").read_text(encoding="utf-8")
        with self.assertRaises(SystemExit):
            research_cli.run(session, FakeClient(stop_reason="refusal"), "m", "high")
        self.assertEqual(before, (session / "research_notes.md").read_text(encoding="utf-8"))

    def test_starter_templates_match_scaffolders(self):
        pre = make_session(self.root)
        for name, template in research_cli.STARTER_TEMPLATES.items():
            self.assertEqual((pre / name).read_text(encoding="utf-8"), template)
        with mock.patch.object(sys, "argv", ["create_session", "Other", "--output", str(self.root)]):
            with redirect_stdout(io.StringIO()) as out:
                create_session.main()
        created = Path(out.getvalue().strip())
        for name, template in research_cli.STARTER_TEMPLATES.items():
            self.assertEqual((created / name).read_text(encoding="utf-8"), template)

    def test_check_writable_protects_edited_files(self):
        session = make_session(self.root)
        research_cli.check_writable(session, force=False)
        (session / "chapter_plan.md").write_text("# edited\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            research_cli.check_writable(session, force=False)
        research_cli.check_writable(session, force=True)

    def test_missing_profile(self):
        with self.assertRaises(SystemExit):
            research_cli.load_session(self.root)


if __name__ == "__main__":
    unittest.main()

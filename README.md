# laoluo-interview

Open-source Codex skill for preparing and running structured longform interviews inspired by direct, biographical podcast craft.

This repo does not clone or impersonate any real person's voice. It packages an interview workflow: producer pre-interview, guest profile extraction, research notes, chapter planning, long-context session memory, transcript drafting, and public highlights.

## Install

Copy or symlink the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/laoluo-interview ~/.codex/skills/
```

Then invoke it in Codex:

```text
Use $laoluo-interview to prepare a pre-interview and chapter plan for this guest.
```

## Create a Session Workspace

```bash
python3 skills/laoluo-interview/scripts/create_session.py "Guest Name" --output sessions
```

This creates:

- `guest_profile.json`
- `research_notes.md`
- `chapter_plan.md`
- `session_memory.json`
- `transcript.md`
- `highlights.md`

## Run an Interactive Pre-Interview

```bash
python3 ~/.codex/skills/laoluo-interview/scripts/pre_interview_cli.py "Guest Name" --output sessions
```

The interactive runner creates a session, asks the producer pre-interview questions, records answers in `pre_interview.md`, updates `guest_profile.json`, and writes `next_codex_prompt.md` for continuing the workflow in Codex.

## Generate Research Notes and a Chapter Plan

After the pre-interview, generate `research_notes.md` and a four-chapter `chapter_plan.md` with the Claude API:

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...
python3 ~/.codex/skills/laoluo-interview/scripts/research_cli.py sessions/<session-id>
```

Options: `--model` (default `claude-opus-5-5`), `--effort` (default `high`), `--force` to overwrite files you already edited, `--dry-run` to print the prompt without calling the API.

## Tests

```bash
python3 -m unittest discover -s tests
```

## Repo Layout

```text
skills/laoluo-interview/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/create_session.py
  scripts/pre_interview_cli.py
  scripts/research_cli.py
tests/
```

## Safety Boundary

Use this as an abstract interview system, not as identity or voice impersonation. Keep sensitive pre-interview facts internal unless the guest explicitly approves public use.

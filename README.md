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

## Repo Layout

```text
skills/laoluo-interview/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/create_session.py
```

## Safety Boundary

Use this as an abstract interview system, not as identity or voice impersonation. Keep sensitive pre-interview facts internal unless the guest explicitly approves public use.

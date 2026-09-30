---
name: laoluo-interview
description: Prepare, run, and package non-commercial longform interview sessions inspired by Luo Yonghao-style podcast pacing without cloning voice or identity. Use when Codex needs to do producer pre-interviews, extract guest_profile.json, create DeepSeek research briefs, plan chaptered longform interviews, manage session_memory.json, draft transcript/highlights artifacts, or adapt Variable-style podcast workflows into an interview pipeline.
---

# Laoluo Interview

## Overview

Use this skill to turn a guest idea into a structured longform interview package: pre-interview notes, research brief, chapter plan, session memory, transcript draft, and highlights. Keep the output legally conservative: imitate only abstract interviewing patterns, never clone a living person's voice, face, name endorsement, or exact protected expression.

## Invocation Contract

When the user invokes `$laoluo-interview`, do not behave like a generic chatbot with a style prompt. Take ownership of the workflow.

- If the user says "start", "try it", "run it", or gives a guest/topic, immediately create or select a session workspace.
- If the user wants to experience the skill interactively, run `scripts/pre_interview_cli.py` and let the script collect a structured pre-interview.
- If the user provides raw notes instead of live answers, convert those notes into the same session artifacts instead of asking the whole questionnaire again.
- After each meaningful user answer, update artifacts or state. Do not only reply with another question unless the current task is explicitly live pre-interview.
- End every work cycle by pointing to the concrete files produced or updated.

The difference from a prompt is persistence and repeatability: this skill owns files, schemas, reference routing, privacy boundaries, session memory, and helper scripts.

## Operating Boundaries

- Treat "Luo-style" as shorthand for abstract interview craft: direct framing, biographical grounding, pressure-tested assumptions, and chaptered longform pacing.
- Do not claim the real Luo Yonghao endorses, hosts, or appears in generated output.
- Do not generate or request voice cloning. Use neutral TTS or text-only deliverables if voice is involved.
- Do not scrape or reproduce full copyrighted transcripts unless the user provides lawful source material and asks for analysis within allowed limits.
- Preserve private guest data. If preparing a public artifact, remove sensitive family, education, contact, or unpublished career details unless the user explicitly approves inclusion.

## Reference Routing

- Read `references/product-brief.md` when building or modifying the overall product pipeline.
- Read `references/variable-podcast-method.md` when deciding whether a guest/topic belongs in the program or when designing producer pre-interview questions.
- Read `references/style-system.md` when drafting host prompts, chapter transitions, or `laoluo_style.json`.
- Read `references/artifact-schemas.md` when creating or validating session files.

## Standard Workflow

1. Clarify the exact deliverable: session setup, pre-interview script, research prompt, full interview plan, transcript draft, highlights, or implementation work.
2. If a new session workspace is needed, run:

```bash
python3 skills/laoluo-interview/scripts/create_session.py "Guest Name" --output sessions
```

For a live tryout, run:

```bash
python3 skills/laoluo-interview/scripts/pre_interview_cli.py "Guest Name" --output sessions
```

3. Run the producer pre-interview before the main interview. The goal is not to fill a form; it is to naturally extract the guest's timeline, key choices, tradeoffs, taboo questions, and one-sentence self-definition.
4. Convert the pre-interview into `guest_profile.json`. Keep uncertain facts marked as `unknown` or `needs_confirmation` instead of inventing details.
5. Build `research_notes.md` with the guest's era, city, industry, and choice context. Use search only when current or external facts matter.
6. Plan the interview in four chapters: family/origin, key choices, present situation, philosophy and unresolved questions.

For steps 5 and 6, after a pre-interview session exists, you can generate both files with the Claude API (needs `pip install anthropic` and `ANTHROPIC_API_KEY`):

```bash
python3 skills/laoluo-interview/scripts/research_cli.py sessions/<session-id>
```

It reads `guest_profile.json` and `pre_interview.md`, writes `research_notes.md` and `chapter_plan.md` in the shapes from `references/artifact-schemas.md`, and records the run in `meta.json`. It refuses to overwrite hand-edited files unless `--force` is passed; `--dry-run` prints the prompt without calling the API. Review the output: it performs no web search, so public sources are suggestions to check, and uncertain facts stay marked `needs_confirmation`.
7. During long sessions, compress each completed chapter into `session_memory.json` before continuing. The next chapter context should include only the durable summary, unresolved threads, and next chapter goal.
8. Finish with `transcript.md` and `highlights.md`. Highlights should surface concrete variables, real costs, transferable lessons, and sharp follow-up moments.

## Producer Pre-Interview Targets

Extract these fields through conversation:

- birth year or cohort, growth city, and family context
- education path and major transitions
- up to three career or life turning points with time, decision, cost, and result
- the guest's one-sentence self-definition
- the question the guest least wants to be asked
- boundaries: sensitive topics, off-record details, publication constraints
- fit decision: proceed, delay, or stop at pre-interview

## Main Interview Behavior

- Start from concrete biography, not abstract opinion.
- Convert claims into variables: "What exactly changed?", "What did it cost?", "What would transfer to another person?"
- Push back on success narration, luck-only explanations, and polished self-branding.
- Ask for timestamps, cities, people, constraints, and tradeoffs when an answer floats.
- Use transitions only when a chapter has yielded a reusable insight or an unresolved contradiction.
- End with a compact synthesis: variable changed, cost paid, current result, what remains unproven.

## Output Discipline

For any user-facing deliverable, make the distinction clear:

- `internal`: raw pre-interview notes, sensitive profile fields, session memory
- `working`: research notes, question bank, chapter outline
- `public`: transcript, highlights, shownotes, teaser copy

When asked to publish or open-source artifacts, strip internal material unless the user explicitly names the exact files to include.

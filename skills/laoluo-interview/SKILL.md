---
name: laoluo-interview
description: Prepare, run, and package non-commercial longform interview sessions inspired by Luo Yonghao-style podcast pacing without cloning voice or identity. Use when Codex needs to do producer pre-interviews, extract guest_profile.json, create DeepSeek research briefs, plan chaptered longform interviews, manage session_memory.json, draft transcript/highlights artifacts, or adapt Variable-style podcast workflows into an interview pipeline.
---

# Laoluo Interview

## Overview

Use this skill to turn a guest idea into a structured longform interview package: pre-interview notes, research brief, chapter plan, session memory, transcript draft, and highlights. Keep the output legally conservative: imitate only abstract interviewing patterns, never clone a living person's voice, face, name endorsement, or exact protected expression.

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

3. Run the producer pre-interview before the main interview. The goal is not to fill a form; it is to naturally extract the guest's timeline, key choices, tradeoffs, taboo questions, and one-sentence self-definition.
4. Convert the pre-interview into `guest_profile.json`. Keep uncertain facts marked as `unknown` or `needs_confirmation` instead of inventing details.
5. Build `research_notes.md` with the guest's era, city, industry, and choice context. Use search only when current or external facts matter.
6. Plan the interview in four chapters: family/origin, key choices, present situation, philosophy and unresolved questions.
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

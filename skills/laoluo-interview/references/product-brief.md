# Product Brief

## Positioning

Build an open-source, non-commercial interview workflow for turning a guest's life choices into a structured longform conversation. The core loop is:

```text
producer pre-interview
  -> guest_profile.json
  -> research_notes.md
  -> chaptered longform interview
  -> session_memory.json compression
  -> transcript.md + highlights.md
```

The skill is meant to help a maker prepare a first-screen promotion or launch moment when a relevant public conversation trend appears. It should be playful and fast, but the outputs still need factual discipline and privacy hygiene.

## Product Logic

The preparation layer exists because freeform LLM interviews drift. Good longform interviewing needs anchors:

- era: what was happening when the guest made key choices
- city: local education, work, family, and industry constraints
- class/family context: treated carefully and privately
- industry context: what options were actually available
- choice sequence: variables changed, costs paid, results observed

The pre-interview replaces a cold intake form. The producer should make a relaxed conversation feel natural while still extracting structured facts.

## Core Pipeline

### Producer pre-interview

Use a warm but precise producer persona. The producer is not the final host. This stage should uncover:

- birth cohort and growth city
- family and education context
- three major turning points at most
- one-sentence self-definition
- the question the guest least wants to answer
- boundaries and sensitive areas

### Guest profile

Generate `guest_profile.json` after the pre-interview. Use explicit uncertainty markers:

- `unknown`
- `needs_confirmation`
- `off_record`
- `public_ok`

### Research layer

Use DeepSeek or another research-capable model/search process to create:

- era background cards
- city/context notes
- industry timeline
- five to ten deep follow-up questions
- likely contradictions or weak spots

### Main interview

Use four chapters by default:

1. family and origin
2. key choices and turning points
3. current situation
4. philosophy, unresolved questions, and future variables

### Long context management

After each chapter:

- summarize what was learned
- record unresolved threads
- record exact claims that need verification
- append durable memory into `session_memory.json`
- continue with only the durable memory and the next chapter goal

## Delivery Targets

- `guest_profile.json`: internal structured profile
- `research_notes.md`: working research brief
- `chapter_plan.md`: ordered interview map
- `session_memory.json`: chapter summaries and unresolved threads
- `transcript.md`: final or simulated transcript
- `highlights.md`: public highlights, teaser lines, and shownotes seeds

## Technical Direction

The full voice app is optional. If implemented, prefer:

- push-to-talk recording
- local faster-whisper for transcription
- DeepSeek-compatible chat model for host reasoning
- neutral TTS such as edge-tts
- no celebrity voice cloning

Package the repeatable process as a Codex skill first. Build a desktop or `.command` launcher only after the text workflow is stable.

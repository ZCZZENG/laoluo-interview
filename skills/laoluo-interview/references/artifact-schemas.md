# Artifact Schemas

Use these schemas as working targets. They are intentionally simple so they can be edited by hand.

## `guest_profile.json`

```json
{
  "guest": {
    "name": "",
    "public_identity": "",
    "birth_year_or_cohort": "unknown",
    "growth_city": "unknown",
    "family_context": {
      "summary": "unknown",
      "privacy": "internal"
    },
    "education_path": [],
    "career_path": []
  },
  "turning_points": [
    {
      "time": "",
      "event": "",
      "variable_changed": "",
      "cost": "",
      "result": "",
      "evidence": "",
      "confidence": "needs_confirmation"
    }
  ],
  "self_definition": "",
  "least_wanted_question": "",
  "boundaries": {
    "sensitive_topics": [],
    "off_record": [],
    "publication_constraints": []
  },
  "fit_decision": {
    "status": "proceed|delay|stop",
    "reason": ""
  }
}
```

## `research_notes.md`

```markdown
# Research Notes

## Guest Summary

## Era Context

## City Context

## Industry Context

## Public Source Notes

## Deep Follow-Up Questions

## Contradictions To Test

## Claims To Verify
```

## `chapter_plan.md`

```markdown
# Chapter Plan

## 1. Origin
- Goal:
- Must ask:
- Exit condition:

## 2. Key Choices
- Goal:
- Must ask:
- Exit condition:

## 3. Present
- Goal:
- Must ask:
- Exit condition:

## 4. Philosophy
- Goal:
- Must ask:
- Exit condition:
```

## `session_memory.json`

```json
{
  "session_id": "",
  "guest_name": "",
  "chapters": [
    {
      "chapter": "",
      "summary": "",
      "variables_found": [],
      "costs_found": [],
      "transferable_lessons": [],
      "unresolved_threads": [],
      "claims_to_verify": []
    }
  ],
  "global_unresolved_threads": [],
  "public_safe_summary": ""
}
```

## `highlights.md`

```markdown
# Highlights

## Public Summary

## Variables

## Real Costs

## Transferable Lessons

## Strong Moments

## Teaser Lines

## Shownotes Seeds
```

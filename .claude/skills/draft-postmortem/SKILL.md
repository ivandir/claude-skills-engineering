---
name: draft-postmortem
description: Draft a blameless incident post-mortem from a timeline and facts. Use after an incident when asked to write a post-mortem, RCA, or incident review.
---

# draft-postmortem

Turn the facts of an incident into a blameless post-mortem draft. The human owns the conclusions; you structure and challenge.

**Inputs:** incident timeline, impact, what was done to resolve it, and any logs/alerts the user provides. Ask for missing facts — never fabricate timestamps, metrics, or causes.
**Output:** a Markdown draft in `docs/postmortems/YYYY-MM-DD-short-title.md` (confirm the location first).

## Procedure

1. Collect facts. List what you were given and what is missing; ask for the missing pieces that matter (start/end time, customer impact, detection method).
2. Build the timeline in UTC, one line per event, marking **detection**, **escalation**, **mitigation** and **resolution**.
3. Separate **trigger** (what set it off) from **root cause(s)** (why the system was vulnerable). Ask "why" repeatedly — stop when you reach something the team can change.
4. Write action items that are specific, owned, and verifiable. Mark each as `prevent`, `detect`, or `mitigate`.
5. Review the draft for blame: replace "X forgot to…" with "the process allowed…".

## Template

```markdown
# Post-mortem: <title>

- **Date:** YYYY-MM-DD   **Duration:** <hh:mm>   **Severity:** SEVn
- **Status:** Draft   **Author:** <name>

## Summary
Two or three sentences: what happened, who was affected, how it was resolved.

## Impact
Who/what was affected, for how long, with numbers where known.

## Timeline (UTC)
| Time | Event |
| --- | --- |

## Root cause
Trigger vs. underlying causes.

## What went well / What went poorly / Where we got lucky

## Action items
| # | Action | Type (prevent/detect/mitigate) | Owner | Due |
| --- | --- | --- | --- | --- |
```

## Rules

- Blameless: describe systems and decisions, not individuals' failings.
- Mark anything uncertain as `TODO(verify)` rather than guessing.
- Do not include customer data, credentials, or internal tokens in the document.

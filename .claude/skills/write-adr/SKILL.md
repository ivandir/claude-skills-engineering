---
name: write-adr
description: Draft an Architecture Decision Record (ADR) from a decision and its context. Use when asked to document an architectural or technical decision, or to write an ADR.
---

# write-adr

Produce a concise, honest ADR that a future engineer can read in two minutes and understand why a decision was made.

**Inputs:** the decision, the context that forced it, and the alternatives considered. Ask for any of these that are missing — do not invent alternatives that weren't actually considered.
**Output:** a new Markdown file in the repo's ADR directory (default `docs/adr/`), numbered sequentially.

## Procedure

1. Find the ADR directory (`docs/adr/`, `docs/decisions/`, `adr/`). If none exists, propose `docs/adr/` and ask before creating it.
2. Find the highest existing number and use the next one: `NNNN-short-kebab-title.md`.
3. Fill in the template below. Keep it to one page.
4. Set **Status** to `Proposed` unless the user says it was already accepted.
5. If this ADR supersedes another, add a `Supersedes` line and tell the user the old ADR's status should be updated to `Superseded by NNNN` (do not edit it without asking).

## Template

```markdown
# NNNN. <Short title in the imperative>

- **Status:** Proposed | Accepted | Deprecated | Superseded by NNNN
- **Date:** YYYY-MM-DD
- **Deciders:** <names/roles>

## Context
What forces are at play? Constraints, requirements, what changed. Facts, not advocacy.

## Decision
We will <decision>. One or two sentences, active voice.

## Alternatives considered
- **<Option A>** — why it was rejected.
- **<Option B>** — why it was rejected.

## Consequences
- Positive: …
- Negative / trade-offs we are accepting: …
- Follow-ups: …
```

## Rules

- State the trade-offs you are accepting, not just the benefits.
- Use today's date from the system, not a guess.
- Do not add sections the template doesn't have.

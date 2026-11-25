# Writing skills

How to add a skill to this library (or your own).

## Anatomy

```markdown
---
name: kebab-case-name            # must equal the folder name
description: What it does. Use when <the situations that should trigger it>.
disable-model-invocation: true   # only for skills that change shared systems
---

# kebab-case-name

One or two sentences on purpose.

**Inputs:** what it needs, and what to ask for if missing.
**Output:** what it produces and where.

## Procedure
1. ...

## Rules
- Hard constraints: what it must never do.
```

## The description is the trigger

Claude decides whether to load a skill from its `description`. Say what the skill does **and when to use it**, in the words a user would actually say ("review a PR", "write an ADR"). Vague descriptions mean the skill never fires, or fires at the wrong time.

## Design rules

1. **Read-only by default.** Analysis skills must say "do not modify code".
2. **Confirm before touching shared state.** Deploys, migrations and anything affecting live data confirm the target by name, show a dry run first, default to non-production, and set `disable-model-invocation: true`.
3. **Never fabricate.** If a fact is missing (timestamps, versions, causes), ask or mark `TODO(verify)`.
4. **Cite evidence.** Findings reference `path:line` and show the trace; say what was *not* checked.
5. **Don't widen permissions.** A skill works inside the engineer's `settings.json`; it must not instruct Claude to bypass it.
6. **No secrets, tokens or internal URLs** in a skill.
7. **Keep it short.** If a skill needs more than about 80 lines, it is probably two skills.

## Promotion process

1. Write it in your own repo and use it for real work.
2. After two people use it successfully, open a PR here.
3. CI must pass (`python scripts/validate.py`), and the PR must add the skill to the README catalog.
4. Review for: clear trigger, documented inputs/outputs, safe defaults, no repo-specific assumptions (or marked `TODO(team)`).
5. Review the library quarterly and delete skills nobody uses.

## Testing a skill

Run it on a real repo with a real task and check the output against the skill's *Rules*. For skills that change shared systems, test against a throwaway environment first.

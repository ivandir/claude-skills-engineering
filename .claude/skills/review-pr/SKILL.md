---
name: review-pr
description: Structured pull request review covering correctness, security, API compatibility and test quality. Use when asked to review a PR, a branch diff, or a set of staged changes.
---

# review-pr

Review code changes the way a careful senior engineer would. Be specific, cite file and line, and separate blocking issues from suggestions.

**Inputs:** a PR number/URL, a branch name, or "the current changes". If none is given, review the diff of the current branch against the default branch.
**Output:** a structured review (format below). Do not post comments or approve anything — report to the user.

## Procedure

1. **Get the diff.** Use `git diff <base>...HEAD` (or `gh pr diff <n>` when a PR is given). Read the PR description for intent.
2. **Understand intent first.** State in one sentence what the change is trying to do. If the description doesn't say, flag that.
3. **Review in this order:**
   1. **Correctness** — logic errors, off-by-one, null/empty handling, concurrency, error paths.
   2. **Security** — input validation, authn/authz, injection, secrets, unsafe deserialization, PII in logs.
   3. **API / contract compatibility** — breaking changes to endpoints, events, schemas, public functions.
   4. **Data & migrations** — reversibility, locking, backfills, indexes.
   5. **Tests** — do they test behavior and the failure path? Would they fail without the change?
   6. **Maintainability** — naming, duplication, unnecessary complexity. Lowest priority.
4. **AI-assisted code:** if the PR says it was AI-assisted (or looks like it), check specifically for plausible-but-wrong logic, architecture that ignores existing patterns, and missing security considerations. Ask "do you understand why this works?" for non-obvious sections.

## Output format

```
## Summary
<one-sentence intent> — <overall: approve / approve with suggestions / changes requested>

## Blocking
- path/to/file.ext:42 — <issue> — <why it matters> — <suggested fix>

## Suggestions
- path/to/file.ext:17 — <suggestion>

## Questions
- <anything unclear that affects the verdict>

## Tests
<what is covered, what is missing>
```

## Rules

- Never invent line numbers. If unsure, quote the code.
- Do not request style changes a linter already enforces.
- If the diff is too large to review well (> ~800 changed lines), say so and recommend splitting it.

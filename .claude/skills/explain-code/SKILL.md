---
name: explain-code
description: Explain an unfamiliar module, service or area of the codebase so a new engineer can orient quickly. Use when asked to explain, walk through, or onboard someone to code.
---

# explain-code

Cut "orientation time" in unfamiliar or poorly documented code. Read-only.

**Inputs:** a file, directory, feature or question ("how does billing retry work?"). Ask what the reader already knows if it is unclear.
**Output:** a written explanation in the structure below. **Do not modify code.**

## Procedure

1. **Find the entry points** — where execution starts for this area (route, handler, job, CLI command, exported function).
2. **Follow the main path** end to end for the common case. Note each module/function touched and what it contributes.
3. **Identify state and boundaries** — where data is stored, what external systems are called, what is cached, what is async.
4. **Find the surprises** — non-obvious behavior, implicit ordering, global state, workarounds, TODO/FIXME comments, anything that looks wrong but is intentional.
5. **Find how to verify** — which tests cover this area, and how to run them.

## Output format

```
## In one paragraph
<what this area does and why it exists>

## Map
- <path:line> — <role>   (entry point → ... → storage/external call)

## How a typical request/job flows
1. ...

## State and dependencies
<databases, queues, caches, third-party calls>

## Gotchas
- <non-obvious thing> (path:line)

## Tests and how to run them
<...>

## What I'm unsure about
<explicitly list guesses>
```

## Rules

- Cite `path:line` for every claim; quote short snippets when a line number would be ambiguous.
- Separate what the code **does** from what you **infer** it is meant to do. Mark inferences.
- If history would help (why it is this way), suggest `git log -p`/`git blame` on specific files rather than guessing.
- Keep it short enough to read in five minutes.

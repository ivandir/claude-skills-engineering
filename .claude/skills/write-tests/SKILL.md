---
name: write-tests
description: Write unit tests for existing code that match the repo's testing conventions. Use when asked to add tests, improve coverage, or write tests for a function, class or module.
---

# write-tests

Writing tests for code that already works is the highest-ROI use of AI assistance we found: it lowers the activation energy, and a reviewable test suite beats a blank file.

**Inputs:** a function, class, file, or module to cover. If none is given, ask.
**Output:** new or extended test files following the repo's existing layout. Run them and report the result.

## Procedure

1. **Learn the conventions.** Read `CLAUDE.md` and two or three existing test files: framework, naming, fixtures, directory layout, how to run a single test.
2. **Read the code under test** and list its behaviors: happy path, boundary values, empty/null input, error paths, and any side effects.
3. **Write tests for behavior, not implementation.** Assert on outputs and observable effects. Avoid asserting on internal calls unless the call *is* the behavior.
4. **Cover failure paths.** Every `raise`/error return gets a test.
5. **Run the tests.** Run only the new tests first, then the surrounding suite. If a test fails, decide whether it found a real bug (report it, do not "fix" the code silently) or the test is wrong (fix the test).
6. **Report:** what is covered, what is deliberately not covered, and any bugs found.

## Rules

- Never weaken or delete an existing test to make a new one pass.
- Do not mock what the repo's conventions say must not be mocked (databases, the router, etc.).
- Use synthetic data only — no real customer data in fixtures.
- Keep tests independent and deterministic: no reliance on test order, wall-clock time, or network.
- If the code is untestable as written, say so and suggest the smallest refactor — do not do it unasked.

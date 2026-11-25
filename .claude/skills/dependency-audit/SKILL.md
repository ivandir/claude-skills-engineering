---
name: dependency-audit
description: Audit project dependencies for known vulnerabilities and outdated packages, triage by real exposure, and propose minimal upgrades. Use when asked to audit, check or update dependencies.
---

# dependency-audit

Find vulnerable and stale dependencies and decide what actually matters. Proposes changes; does not apply major upgrades on its own.

**Inputs:** scope (whole repo by default). **Output:** a triaged report, and — only if the user asks — the minimal upgrade edits.

## Procedure

1. **Detect ecosystems** from manifests/lockfiles (`package-lock.json`, `poetry.lock`, `requirements*.txt`, `go.mod`, `Cargo.lock`, `Gemfile.lock`, `pom.xml`).
2. **Run the native audit tools that are already installed** (read-only): `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `bundle audit`. Do not install tools. State which were unavailable.
3. **List outdated packages** (`npm outdated`, `pip list --outdated`, `go list -u -m all`).
4. **Triage each finding** — do not just paste scanner output:
   - Is the vulnerable package a **direct** or **transitive** dependency? What pulls it in?
   - Is it a **runtime** or **dev/build-only** dependency?
   - Is the **vulnerable code path reachable** from this project? Search for use of the affected API.
   - Is a **fixed version** available, and is the upgrade patch, minor or major?
5. **Propose the minimal fix** per finding: the smallest version bump that resolves it, noting breaking-change risk. For transitive issues, prefer upgrading the parent; use overrides/resolutions only as a stated, temporary workaround.
6. **If the user asks you to apply upgrades:** do one logical group at a time, run the tests after each, and stop on failure. Never apply major-version bumps without asking.

## Output format

```
## Summary
<N vulnerabilities (H/M/L), M outdated; tools run / unavailable>

## Act now
- <package> <current> → <fixed> — <CVE/advisory> — direct|transitive via X — reachable: yes/no/unknown — upgrade: patch|minor|major

## Schedule
- ...

## Ignore (with reason)
- <e.g. dev-only, code path not used>

## Not covered
<ecosystems without an audit tool, private registries, etc.>
```

## Rules

- Never claim a package is "safe" because the scanner is silent — say what the scanner checked.
- Do not weaken lockfile integrity or add blanket ignore rules to silence results.
- Never commit lockfile changes you did not test.

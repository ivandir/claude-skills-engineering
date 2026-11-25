---
name: security-scan
description: Review code or a diff against the OWASP Top 10 and report findings by severity. Use when asked for a security review, security scan, or to check code for vulnerabilities.
---

# security-scan

A structured, read-only security review. It complements — never replaces — automated SAST, dependency scanning and a human security review.

**Inputs:** a path, a diff/PR, or "the current changes". Default scope: the diff against the default branch; if there is none, ask which area to review.
**Output:** a findings report. **Do not modify code.**

## Procedure

1. **Scope and context.** Read `CLAUDE.md` for the data sensitivity and threat context. Identify entry points in scope (routes, handlers, queue consumers, CLI args, file uploads).
2. **Run available scanners (read-only).** If installed, run and summarize: `semgrep`, `gitleaks`/`trufflehog`, `bandit`, `npm audit`/`pip-audit`. Do not install tools. State which were not available.
3. **Manual review against the OWASP Top 10 (2021):**
   - **A01 Broken access control** — missing authz checks, IDOR, path traversal, CORS.
   - **A02 Cryptographic failures** — weak algorithms, hard-coded keys, plaintext sensitive data, bad randomness.
   - **A03 Injection** — SQL/NoSQL/OS command/template/LDAP injection; unsanitized input reaching an interpreter.
   - **A04 Insecure design** — missing rate limits, trust-boundary mistakes, no abuse-case thinking.
   - **A05 Security misconfiguration** — debug on, verbose errors, permissive defaults, open buckets.
   - **A06 Vulnerable components** — known-vulnerable or unmaintained dependencies.
   - **A07 Authentication failures** — weak session handling, credential stuffing exposure, missing MFA hooks.
   - **A08 Integrity failures** — unsafe deserialization, unsigned updates, unpinned CI actions.
   - **A09 Logging failures** — secrets/PII in logs, missing security-event logging.
   - **A10 SSRF** — server fetching user-supplied URLs without allow-listing.
4. **Trace before you claim.** For each suspected issue, follow the data from source to sink in the code. If you cannot show the path, report it as "needs verification", not as a finding.

## Output format

```
## Scope
<what was reviewed; scanners run / not available>

## Findings
### [HIGH|MEDIUM|LOW] <title> — <OWASP category>
- Where: path/to/file.ext:42
- Evidence: <the code, and the source→sink path>
- Impact: <what an attacker can do>
- Fix: <specific remediation>

## Needs verification
- <suspected, path not confirmed>

## Not covered
<what this review did not look at>
```

## Rules

- No false confidence: say what was **not** checked.
- Never print secrets you find; give the file and line and say "credential present".
- Do not run exploits or hit live systems.
- Rate severity by exploitability and impact in *this* context, not by category.

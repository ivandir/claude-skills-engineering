# claude-skills-engineering

A library of 12 [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) for everyday engineering work — review, testing, documentation, incident response, security, infrastructure and release. Each skill is one Markdown file you can copy into a repo and use immediately.

Skills are the most underexplored part of Claude Code: shared runbooks that turn "how our team does X" into something anyone can invoke. This is a working starting library, designed to be forked and tuned to your stack.

> Companion to [How I Set Up Claude Code for a Team of 25](https://ivandir.com/blog/claude-code-team-case-study.html) and [`claude-code-org-setup`](https://github.com/ivandir/claude-code-org-setup).

## Catalog

**Risk:** *read-only* analyzes and reports · *writes files* edits files in your working tree · *shared systems* changes live infrastructure or data (user-invoked only, confirms first).

| Skill | What it does | Risk |
| --- | --- | --- |
| [`review-pr`](.claude/skills/review-pr/SKILL.md) | Structured PR review: correctness, security, API compatibility, tests | read-only |
| [`security-scan`](.claude/skills/security-scan/SKILL.md) | OWASP Top 10 review of code or a diff, with scanners if installed | read-only |
| [`explain-code`](.claude/skills/explain-code/SKILL.md) | Orientation map of an unfamiliar module: entry points, flow, gotchas | read-only |
| [`review-iac-diff`](.claude/skills/review-iac-diff/SKILL.md) | Explain a CDK/Terraform diff: replacements, destroys, IAM and network risk | read-only |
| [`dependency-audit`](.claude/skills/dependency-audit/SKILL.md) | Triage vulnerable/outdated dependencies by real exposure | read-only |
| [`write-tests`](.claude/skills/write-tests/SKILL.md) | Tests for existing code in your repo's conventions | writes files |
| [`scaffold-endpoint`](.claude/skills/scaffold-endpoint/SKILL.md) | New API endpoint following team patterns (customize first) | writes files |
| [`write-adr`](.claude/skills/write-adr/SKILL.md) | Architecture Decision Record from a decision and its context | writes files |
| [`draft-postmortem`](.claude/skills/draft-postmortem/SKILL.md) | Blameless post-mortem draft from a timeline | writes files |
| [`update-changelog`](.claude/skills/update-changelog/SKILL.md) | Keep-a-Changelog entry from commits since the last release | writes files |
| [`deploy`](.claude/skills/deploy/SKILL.md) | Static site to S3 + CloudFront with dry run and confirmation | **shared systems** |
| [`run-migration`](.claude/skills/run-migration/SKILL.md) | Review, apply and verify a DB migration with a rollback plan | **shared systems** |

## Install

Per repo (versioned with the code):

```bash
mkdir -p .claude/skills
cp -r <this-repo>/.claude/skills/review-pr .claude/skills/
```

Across all your repos:

```bash
cp -r <this-repo>/.claude/skills/review-pr ~/.claude/skills/
```

Then ask Claude naturally ("review this PR", "scan the diff for security issues") or invoke by name. Skills that change live systems (`deploy`, `run-migration`) set `disable-model-invocation: true`, so Claude will never start them on its own — you must ask.

## Customize before you roll out

Search for `TODO(team)`. `scaffold-endpoint`, `deploy` and `run-migration` need your framework, bucket/distribution IDs and migration tool. A scaffold skill that doesn't match your repo is worse than none — fill these in or delete the skill.

## Conventions

- **Layout:** `.claude/skills/<name>/SKILL.md` with `name` (matching the folder) and `description` front matter.
- **Every skill documents** its inputs, output, procedure and hard rules.
- **Read-only first.** Skills that analyze never modify; skills that change shared systems confirm before every write and default to non-production.
- **Version breaking changes in the name** (`review-pr-v2`).

Full guidance: [`docs/writing-skills.md`](docs/writing-skills.md).

## Status and testing

CI (`scripts/validate.py`) checks structure on every push: front matter, documented inputs/outputs/rules, a complete README catalog, a safety rule that shared-system skills are user-invoked only, working links, and no credential patterns.

That is **structural** validation. A skill's behaviour depends on your codebase and Claude Code version, so exercise each one on a real repo before you standardize on it. Each skill's *Rules* section is the contract to check for.

## License

[MIT](LICENSE)

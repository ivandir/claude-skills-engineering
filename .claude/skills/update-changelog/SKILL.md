---
name: update-changelog
description: Update CHANGELOG.md in Keep a Changelog format from commits since the last release. Use when asked to update the changelog or prepare release notes.
---

# update-changelog

Turn commit history into a readable changelog entry that describes what changed **for users**, not what each commit did.

**Inputs:** the version number (ask if not given) and the previous release tag (default: latest `git describe --tags --abbrev=0`).
**Output:** an edit to `CHANGELOG.md` (create it from the template if missing). Do not tag, commit or publish.

## Procedure

1. **Gather changes.** `git log <prev-tag>..HEAD --no-merges --format='%h %s%n%b'` and, for PR-based repos, the merged PR titles. Read the existing `CHANGELOG.md` to match its tone and format.
2. **Classify** each user-visible change under **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.
3. **Drop the noise:** formatting, CI tweaks, refactors with no behavior change, dependency bumps that don't affect users (group those as one line if worth mentioning).
4. **Rewrite for readers.** "Fix NPE in order lookup" → "Fixed a crash when looking up an order that has no items." Link PRs/issues where the repo already does.
5. **Flag breaking changes** at the top of the entry, with migration instructions, and recommend a major version bump if the version given disagrees.
6. **Edit the file.** Add `## [<version>] - <today's date from the system>` under `## [Unreleased]`, and update the comparison links at the bottom if the file uses them.
7. **Report** anything ambiguous (commits whose impact you couldn't determine) for the user to decide.

## Template (if no changelog exists)

```markdown
# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]
```

## Rules

- Never invent changes that are not in the history.
- Do not include secrets, internal URLs or customer names.
- One line per change; no commit hashes in the entry unless the file already uses them.

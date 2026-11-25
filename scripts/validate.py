#!/usr/bin/env python3
"""Validate the skill library. No third-party dependencies.

Checks:
  1. Every skill has SKILL.md with `name` (matching its folder) and a useful `description`.
  2. Skills that change shared systems (SHARED_STATE) must set `disable-model-invocation: true`,
     so Claude never runs them on its own initiative.
  3. Every skill documents Inputs/Output and a Rules section.
  4. The README catalog lists every skill, and only real skills.
  5. No credential patterns, and relative Markdown links resolve.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"
SHARED_STATE = {"deploy", "run-migration"}
errors: list[str] = []

FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def err(msg: str) -> None:
    errors.append(msg)


def parse_front_matter(text: str) -> dict[str, str]:
    m = FRONT_MATTER.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def check_skills() -> set[str]:
    names = set()
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        names.add(d.name)
        f = d / "SKILL.md"
        rel = f.relative_to(ROOT)
        if not f.exists():
            err(f"{d.relative_to(ROOT)}: missing SKILL.md")
            continue
        text = f.read_text(encoding="utf-8")
        fm = parse_front_matter(text)
        if not fm:
            err(f"{rel}: missing YAML front matter")
            continue
        if fm.get("name") != d.name:
            err(f"{rel}: name {fm.get('name')!r} != folder {d.name!r}")
        desc = fm.get("description", "")
        if len(desc) < 40:
            err(f"{rel}: description too short to trigger reliably")
        if not re.search(r"\buse\b", desc, re.IGNORECASE):
            err(f"{rel}: description should say when to use the skill")
        if d.name in SHARED_STATE and fm.get("disable-model-invocation") != "true":
            err(f"{rel}: changes shared systems; must set 'disable-model-invocation: true'")
        if "**Inputs" not in text and "**Configuration" not in text:
            err(f"{rel}: missing documented inputs")
        if "**Output" not in text and "## Output" not in text:
            err(f"{rel}: missing documented output")
        if "## Rules" not in text:
            err(f"{rel}: missing '## Rules' section")
    return names


def check_readme_catalog(names: set[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"\|\s*\[`([a-z0-9-]+)`\]\(\.claude/skills/", readme))
    for missing in sorted(names - listed):
        err(f"README.md: skill '{missing}' not listed in the catalog")
    for extra in sorted(listed - names):
        err(f"README.md: catalog lists '{extra}' but no such skill exists")


SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(r"sk-[A-Za-z0-9]{32,}"),
]
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")


def check_files() -> None:
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix not in {".md", ".py", ".yml", ".json"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                err(f"{p.relative_to(ROOT)}: matches credential pattern {pat.pattern!r}")
        if p.suffix != ".md":
            continue
        in_fence = False
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            if in_fence:
                continue
            for target in LINK.findall(line):
                if re.match(r"[a-z]+:", target):
                    continue
                if not (p.parent / target).resolve().exists():
                    err(f"{p.relative_to(ROOT)}:{n}: broken link {target}")


def main() -> int:
    names = check_skills()
    check_readme_catalog(names)
    check_files()
    if errors:
        print("Validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(names)} skills valid; catalog, links and credential checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

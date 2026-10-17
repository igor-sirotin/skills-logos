#!/usr/bin/env python3
"""Validate every <skill>/SKILL.md in the repo and the README skill list."""
import pathlib
import re
import sys

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
README_ENTRY_RE = re.compile(r"^- \*\*([a-z0-9-]+)\*\*", re.M)

root = pathlib.Path(__file__).resolve().parents[2]
errors = []


def check_skill(path):
    rel = path.relative_to(root)
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if parts[0] != "" or len(parts) < 3:
        return errors.append(f"{rel}: must start with a '---' front matter block")
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return errors.append(f"{rel}: front matter is not valid YAML: {e}")
    if not isinstance(meta, dict):
        return errors.append(f"{rel}: front matter must be a mapping")

    name = meta.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"{rel}: name must be kebab-case, at most 64 chars, got {name!r}")
    elif name != path.parent.name:
        errors.append(f"{rel}: name {name!r} does not match directory {path.parent.name!r}")

    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{rel}: description must be a non-empty string")
    elif len(desc) > 1024:
        errors.append(f"{rel}: description is {len(desc)} chars, limit is 1024")

    if not parts[2].strip():
        errors.append(f"{rel}: body is empty")


skills = sorted(p.parent.name for p in root.glob("*/SKILL.md"))
if not skills:
    errors.append("no */SKILL.md found")
for name in skills:
    check_skill(root / name / "SKILL.md")

listed = README_ENTRY_RE.findall((root / "README.md").read_text(encoding="utf-8"))
for name in sorted(set(skills) - set(listed)):
    errors.append(f"README.md: skill {name!r} is not listed")
for name in sorted(set(listed) - set(skills)):
    errors.append(f"README.md: lists {name!r}, which does not exist")

for e in errors:
    print("::error::" + " ".join(e.split()))
print(f"checked {len(skills)} skill(s), {len(errors)} error(s)")
sys.exit(1 if errors else 0)

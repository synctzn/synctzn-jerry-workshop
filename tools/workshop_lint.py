#!/usr/bin/env python3
"""Small dependency-free linter for Jerry workshop skill cards."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED = ("name", "description", "version", "status")
SECRET_PATTERNS = (
    re.compile(r"github_pat_[A-Za-z0-9_]+", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9]+", re.I),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.I),
)


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def lint(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    metadata = frontmatter(text)
    if not metadata:
        errors.append("missing or malformed YAML frontmatter")
    for key in REQUIRED:
        if not metadata.get(key):
            errors.append(f"missing frontmatter field: {key}")
    if metadata.get("status") not in {"starter", "tested", "PR", "merged", "adopted"}:
        errors.append("status must be starter, tested, PR, merged, or adopted")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append("secret-like text detected")
    if "skills/" in str(path) and "## Limits" not in text:
        errors.append("skill card must include a Limits section")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    for path in args.paths:
        try:
            errors = lint(path)
        except OSError as exc:
            errors = [str(exc)]
        if errors:
            failed = True
            print(f"FAIL {path}: {'; '.join(errors)}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

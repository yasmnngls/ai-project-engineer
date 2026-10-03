#!/usr/bin/env python3
"""Validate ARCHITECTURE.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADINGS = [
    "## Status",
    "## Read this first",
    "## Containers",
    "## Modules",
    "## Contracts",
    "## UI boundary",
    "## Decisions",
    "## Last change",
]
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def heading_body(text: str, heading: str) -> str:
    if heading not in text:
        return ""
    rest = text.split(heading, 1)[1]
    lines = []
    for line in rest.splitlines()[1:]:
        if line.startswith("## "):
            break
        lines.append(line)
    return "\n".join(lines).strip()


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if not first.startswith("# Architecture"):
        errors.append("First line must start with '# Architecture'")
    for heading in HEADINGS:
        body = heading_body(text, heading)
        if heading not in text:
            errors.append(f"Missing heading {heading!r}")
        elif not body:
            errors.append(f"{heading} is empty")
    last = heading_body(text, "## Last change")
    if last and not DATE.search(last):
        errors.append("## Last change must include a YYYY-MM-DD date")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1] if len(argv) > 1 else "ARCHITECTURE.md")
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: architecture file is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

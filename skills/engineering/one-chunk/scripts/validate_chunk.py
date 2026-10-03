#!/usr/bin/env python3
"""Validate docs/foundation/12-chunk.md."""

from __future__ import annotations

import sys
from pathlib import Path

HEADINGS = [
    "## Beat",
    "## Build step",
    "## Done when",
    "## Test",
    "## Not in this chunk",
    "## Files",
]
BEATS = {"contract", "shell", "wire"}


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


def first_line(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if first != "# Chunk":
        errors.append("First line must be '# Chunk'")
    bodies = {heading: heading_body(text, heading) for heading in HEADINGS}
    for heading, body in bodies.items():
        if heading not in text:
            errors.append(f"Missing heading {heading!r}")
        elif not body:
            errors.append(f"{heading} is empty")
    beat = first_line(bodies["## Beat"])
    if beat not in BEATS:
        errors.append("## Beat must be contract, shell, or wire")
    test = bodies["## Test"]
    if beat == "wire" and "safeParse" in test and "see" not in test.lower():
        errors.append("A wire test must assert what the user sees")
    if beat == "wire" and not any(token in test.lower() for token in ("render", "screen", "user sees", "user can see")):
        errors.append("A wire test must say what the user sees")
    if beat == "shell" and "Automated test waits for the wire beat." not in test:
        errors.append("Shell test line must say the automated test waits for the wire beat")
    if beat == "contract" and "safeParse" not in test:
        errors.append("Contract test must name safeParse")
    files = bodies["## Files"]
    if files and not any(line.strip().startswith("- ") for line in files.splitlines()):
        errors.append("## Files needs a bullet list of paths")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1] if len(argv) > 1 else "docs/foundation/12-chunk.md")
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: chunk file is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

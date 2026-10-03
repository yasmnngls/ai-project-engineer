#!/usr/bin/env python3
"""Validate docs/foundation/09-assumption-trials.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

FIELDS = [
    "- Claim:",
    "- Left alone:",
    "- Kill test:",
    "- Result that flips it:",
    "- If it flips:",
    "- Expensive after:",
]
NONE = "No assumptions. There is nothing to try."
BLOCK = re.compile(r"(?m)^### (A\d+)\b")


def split_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(BLOCK.finditer(text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[start:end]))
    return blocks


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if first != "# Assumption trials":
        errors.append("First line must be '# Assumption trials'")
    if "## Trials" not in text:
        errors.append("Missing heading '## Trials'")
    blocks = split_blocks(text)
    has_none = NONE in text
    if not blocks and not has_none:
        errors.append(f"Add at least one '### A1' block, or the line: {NONE}")
    if blocks and has_none:
        errors.append("Remove the no-assumptions line when trials exist")
    for trial_id, body in blocks:
        for field in FIELDS:
            if field not in body:
                errors.append(f"{trial_id} missing {field!r}")
        if "[assumption]" not in body:
            errors.append(f"{trial_id} claim must keep the [assumption] tag")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1] if len(argv) > 1 else "docs/foundation/09-assumption-trials.md")
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: assumption trials are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

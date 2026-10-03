#!/usr/bin/env python3
"""Validate docs/foundation/10-refusals.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

FIELDS = ["- They ask:", "- We say:", "- Owns:", "- If it becomes real:"]
BANNED = re.compile(r"unfortunately|at this time|we value", re.IGNORECASE)
NONE = "Nothing is excluded."
BLOCK = re.compile(r"(?m)^### (R\d+)\b")


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
    if first != "# Refusals":
        errors.append("First line must be '# Refusals'")
    if "## Catalog" not in text:
        errors.append("Missing heading '## Catalog'")
    if BANNED.search(text):
        errors.append("Remove apology language: unfortunately, at this time, we value")
    blocks = split_blocks(text)
    has_none = NONE in text
    if not blocks and not has_none:
        errors.append(f"Add at least one '### R1' block, or the line: {NONE}")
    if blocks and has_none:
        errors.append("Remove the nothing-excluded line when refusals exist")
    for refusal_id, body in blocks:
        for field in FIELDS:
            if field not in body:
                errors.append(f"{refusal_id} missing {field!r}")
        we_say = "\n".join(line for line in body.splitlines() if line.startswith("- We say:"))
        if we_say and "FR-" not in we_say and "/" not in we_say:
            errors.append(f"{refusal_id} 'We say' must name a screen or an FR id")
    if "## Asked now" in text:
        asked = text.split("## Asked now", 1)[1].split("## Catalog", 1)[0]
        if not re.search(r"Verdict:\s*(refuse|change the pack)\b", asked):
            errors.append("Asked now needs 'Verdict: refuse' or 'Verdict: change the pack'")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1] if len(argv) > 1 else "docs/foundation/10-refusals.md")
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: refusals are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

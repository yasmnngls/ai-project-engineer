#!/usr/bin/env python3
"""Validate docs/foundation/11-drift.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

KINDS = {"contradiction", "gap", "hardened"}
FIELDS = ["- Kind:", "- Spec:", "- Code:", "- What to do:"]
CLEAR = "None. The code still matches the pack."
BLOCK = re.compile(r"(?m)^### (D\d+)\b")
KIND_RE = re.compile(r"^- Kind:\s*(contradiction|gap|hardened)\b", re.MULTILINE)


def split_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(BLOCK.finditer(text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[start:end]))
    return blocks


def verdict(text: str) -> str | None:
    if "## Verdict" not in text:
        return None
    body = text.split("## Verdict", 1)[1].split("## Findings", 1)[0]
    for line in body.splitlines():
        word = line.strip()
        if word:
            return word
    return ""


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if first != "# Drift":
        errors.append("First line must be '# Drift'")
    found = verdict(text)
    if found not in {"clear", "drift"}:
        errors.append("Verdict must be the single word 'clear' or 'drift'")
    if "## Findings" not in text:
        errors.append("Missing heading '## Findings'")
    blocks = split_blocks(text)
    if found == "clear":
        if blocks:
            errors.append("A clear verdict has no D blocks")
        if CLEAR not in text:
            errors.append(f"Clear findings must contain: {CLEAR}")
    if found == "drift":
        if CLEAR in text:
            errors.append("Remove the clear-findings line when verdict is drift")
        if not blocks:
            errors.append("Drift needs at least one '### D1' finding")
    for finding_id, body in blocks:
        for field in FIELDS:
            if field not in body:
                errors.append(f"{finding_id} missing {field!r}")
        kind = KIND_RE.search(body)
        if not kind:
            errors.append(f"{finding_id} kind must be contradiction, gap, or hardened")
        code_lines = [line for line in body.splitlines() if line.startswith("- Code:")]
        if code_lines:
            code = code_lines[0].split(":", 1)[1].strip()
            if code != "No product code yet." and "/" not in code and "." not in Path(code).name:
                errors.append(f"{finding_id} code must be a path or 'No product code yet.'")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1] if len(argv) > 1 else "docs/foundation/11-drift.md")
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: drift report is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

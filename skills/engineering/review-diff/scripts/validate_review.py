#!/usr/bin/env python3
"""Validate docs/reviews/<YYYY-MM-DD>-<short-ref>.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADINGS = [
    "## Fixed point",
    "## Files",
    "## Checks",
    "## Standards",
    "## Spec",
    "## Verdict",
]
VERDICTS = {"ship", "fix"}
RESULTS = {"pass", "fail"}
SMELLS = {
    "Mysterious Name",
    "Duplicated Code",
    "Feature Envy",
    "Data Clumps",
    "Primitive Obsession",
    "Repeated Switches",
    "Shotgun Surgery",
    "Divergent Change",
    "Speculative Generality",
    "Message Chains",
    "Middle Man",
    "Refused Bequest",
}
VALIDATORS = [
    (lambda p: p.startswith("src/contracts/"), "validate_contracts.py"),
    (lambda p: p.startswith("src/features/"), "validate_shell.py"),
    (lambda p: p == "docs/foundation/12-chunk.md", "validate_chunk.py"),
    (lambda p: p == "ARCHITECTURE.md", "validate_architecture.py"),
    (lambda p: p == "PROJECT-STATE.md", "validate_project_state.py"),
]
FILENAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$")
SHA = re.compile(r"\b[0-9a-f]{7,40}\b")
DIFF = re.compile(r"`git diff \S+\.\.\.HEAD`")
FILE_ITEM = re.compile(r"^- `([^`]+)`$")
FINDING = re.compile(r"^- \[(hard|judgement)\] `([^`:]+):(\d+)(?:-\d+)?` — (.+?) Source: (.+)$")
SPEC_SOURCE = re.compile(r"\bN?FR-\d{3}\b|12-chunk\.md|#\d+")


def heading_body(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}[ \t]*$", text, re.MULTILINE)
    if not match:
        return ""
    lines = []
    for line in text[match.end():].splitlines()[1:]:
        if line.startswith("## "):
            break
        lines.append(line)
    return "\n".join(lines).strip()


def table_rows(body: str) -> list[list[str]]:
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    return rows[1:]


def product_root(path: Path) -> Path | None:
    parent = path.resolve().parent
    if parent.name == "reviews" and parent.parent.name == "docs":
        return parent.parent.parent
    return None


def check_findings(
    heading: str,
    body: str,
    files: set[str],
    root: Path | None,
    empty: set[str],
) -> tuple[list[str], int, list[str]]:
    errors: list[str] = []
    hard = 0
    sources: list[str] = []
    if body in empty:
        return errors, hard, sources
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    for line in lines:
        match = FINDING.match(line)
        if not match:
            errors.append(f"{heading}: not a finding: {line[:60]!r}")
            continue
        severity, ref, number, _what, source = match.groups()
        source = source.strip()
        sources.append(source)
        if severity == "hard":
            hard += 1
        if ref not in files:
            errors.append(f"{heading}: {ref} is not listed under ## Files")
        if int(number) < 1:
            errors.append(f"{heading}: {ref}:{number} needs a line number from 1")
        if root and (root / ref).is_file():
            count = len((root / ref).read_text(encoding="utf-8").splitlines())
            if int(number) > count:
                errors.append(f"{heading}: {ref} has {count} lines, not {number}")
        if heading == "## Standards":
            smell = source.rstrip(".") in SMELLS
            if not smell and "`" not in source:
                errors.append(f"{heading}: Source must be a backticked standard file or a smell name")
            if smell and severity == "hard":
                errors.append(f"{heading}: {source.rstrip('.')} is a smell, so it is a judgement call")
        if heading == "## Spec" and not SPEC_SOURCE.search(source):
            errors.append(f"{heading}: Source must cite an FR or NFR id, 12-chunk.md, or an issue number")
    return errors, hard, sources


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if first != "# Review":
        errors.append("First line must be '# Review'")
    if not FILENAME.match(path.name):
        errors.append("File name must be <YYYY-MM-DD>-<short-ref>.md in lowercase")

    positions = []
    bodies = {}
    for heading in HEADINGS:
        match = re.search(rf"^{re.escape(heading)}[ \t]*$", text, re.MULTILINE)
        if not match:
            errors.append(f"Missing heading {heading!r}")
            continue
        positions.append(match.start())
        bodies[heading] = heading_body(text, heading)
        if not bodies[heading]:
            errors.append(f"{heading} is empty")
    if positions != sorted(positions):
        errors.append("Headings must be in order: " + ", ".join(HEADINGS))

    fixed = bodies.get("## Fixed point", "")
    if fixed and not SHA.search(fixed):
        errors.append("## Fixed point needs the resolved SHA, 7 to 40 lowercase hex characters")
    if fixed and not DIFF.search(fixed):
        errors.append("## Fixed point needs the backticked command `git diff <ref>...HEAD`")

    files: set[str] = set()
    for line in bodies.get("## Files", "").splitlines():
        if not line.strip():
            continue
        match = FILE_ITEM.match(line.strip())
        if match:
            files.add(match.group(1))
        else:
            errors.append(f"## Files: each line is a backticked path in a bullet: {line.strip()[:60]!r}")

    checks = bodies.get("## Checks", "")
    rows = table_rows(checks)
    failed = False
    if checks and not rows:
        errors.append("## Checks needs a Command | Result table with at least one row")
    commands = []
    for cells in rows:
        if len(cells) < 2:
            errors.append(f"Checks row needs Command and Result: {cells}")
            continue
        command, result = cells[0], cells[1]
        if not (command.startswith("`") and command.endswith("`")):
            errors.append(f"Checks command must be backticked: {command}")
        if result not in RESULTS:
            errors.append(f"Checks result must be pass or fail: {command}")
        failed = failed or result == "fail"
        commands.append(command)
    if rows and not any("git diff --check" in command for command in commands):
        errors.append("## Checks needs a `git diff --check <ref>...HEAD` row")

    root = product_root(path)
    standard_errors, standard_hard, _ = check_findings(
        "## Standards", bodies.get("## Standards", ""), files, root, {"None."}
    )
    spec_errors, spec_hard, spec_sources = check_findings(
        "## Spec", bodies.get("## Spec", ""), files, root, {"None.", "No spec available."}
    )
    errors += standard_errors + spec_errors

    needed = {script for path_ in files for test, script in VALIDATORS if test(path_)}
    if any("12-chunk.md" in source for source in spec_sources):
        needed.add("validate_chunk.py")
    for script in sorted(needed):
        if not any(script in command for command in commands):
            errors.append(f"## Checks needs a {script} row for the files in this diff")

    verdict = bodies.get("## Verdict", "")
    if verdict and verdict not in VERDICTS:
        errors.append("## Verdict must be the single word ship or fix")
    if verdict == "ship" and failed:
        errors.append("Verdict must be fix when a check failed")
    if verdict == "ship" and standard_hard + spec_hard:
        errors.append("Verdict must be fix when a [hard] finding exists")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: validate_review.py docs/reviews/<YYYY-MM-DD>-<short-ref>.md")
        return 2
    path = Path(argv[1])
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: review is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

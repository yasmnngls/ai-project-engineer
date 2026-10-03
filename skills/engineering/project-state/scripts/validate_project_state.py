#!/usr/bin/env python3
"""Validate PROJECT-STATE.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADINGS = [
    "## Status",
    "## Current focus",
    "## Done",
    "## In progress",
    "## Blocked",
    "## Known issues",
    "## Next actions",
    "## Sources of truth",
    "## Read for",
    "## Last updated",
]
LISTS = ["## Done", "## In progress", "## Blocked", "## Known issues"]
STATUSES = {"foundation", "building", "shipping", "maintenance", "paused"}
REQUIRED_DOMAINS = ["Product", "Architecture", "Data", "UI", "Current work"]
STATE_FILE = "PROJECT-STATE.md"
MAX_READ = 5
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}\b")
TICKED = re.compile(r"`([^`]+)`")


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


def check_path(root: Path, ref: str) -> str | None:
    if ref.startswith("mcp:"):
        return None if len(ref) > 4 else "mcp source needs a server name"
    target = root / ref
    if ref.endswith("/"):
        return None if target.is_dir() else f"{ref} is not a directory"
    return None if target.exists() else f"{ref} does not exist"


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    root = path.parent
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if first != "# Project state":
        errors.append("First line must be '# Project state'")

    bodies = {heading: heading_body(text, heading) for heading in HEADINGS}
    for heading, body in bodies.items():
        if not re.search(rf"^{re.escape(heading)}[ \t]*$", text, re.MULTILINE):
            errors.append(f"Missing heading {heading!r}")
        elif not body:
            errors.append(f"{heading} is empty")

    status = bodies["## Status"]
    if status and re.split(r"[\s.,]", status, 1)[0] not in STATUSES:
        errors.append("## Status must start with " + ", ".join(sorted(STATUSES)))

    for heading in LISTS:
        body = bodies[heading]
        if not body or body == "None.":
            continue
        if not all(line.strip().startswith("- ") for line in body.splitlines() if line.strip()):
            errors.append(f"{heading} must be a bullet list or 'None.'")

    actions = [line for line in bodies["## Next actions"].splitlines() if re.match(r"^\d+\.\s+\S", line.strip())]
    if bodies["## Next actions"] and not 1 <= len(actions) <= 5:
        errors.append("## Next actions needs one to five numbered items")

    sources = table_rows(bodies["## Sources of truth"])
    seen: dict[str, int] = {}
    for cells in sources:
        if len(cells) < 3:
            errors.append(f"Sources of truth row needs Domain, Source, and Update when: {cells}")
            continue
        domain, source, update = cells[0], cells[1], cells[2]
        seen[domain] = seen.get(domain, 0) + 1
        refs = TICKED.findall(source)
        if source != "missing" and not refs:
            errors.append(f"{domain}: Source must be backticked paths, `mcp:<server>`, or missing")
        if not update:
            errors.append(f"{domain}: Update when is empty")
        for ref in refs:
            problem = check_path(root, ref)
            if problem:
                errors.append(f"{domain}: {problem}")
    for domain in REQUIRED_DOMAINS:
        if domain not in seen:
            errors.append(f"## Sources of truth is missing the {domain} row")
    for domain, count in seen.items():
        if count > 1:
            errors.append(f"{domain} has {count} rows. One domain has one winner")
    current = next((cells for cells in sources if cells and cells[0] == "Current work"), None)
    if current and len(current) > 1 and current[1] != f"`{STATE_FILE}`":
        errors.append(f"Current work source must be `{STATE_FILE}`")

    reads = table_rows(bodies["## Read for"])
    if bodies["## Read for"] and not reads:
        errors.append("## Read for needs a table with at least one task")
    for cells in reads:
        if len(cells) < 2:
            errors.append(f"Read for row needs Task and Read: {cells}")
            continue
        task, refs = cells[0], TICKED.findall(cells[1])
        if not refs or refs[0] != STATE_FILE:
            errors.append(f"Read for {task}: start with `{STATE_FILE}`")
        if len(refs) - 1 > MAX_READ:
            errors.append(f"Read for {task}: at most {MAX_READ} sources after `{STATE_FILE}`")
        for ref in refs[1:]:
            problem = check_path(root, ref)
            if problem:
                errors.append(f"Read for {task}: {problem}")

    if bodies["## Last updated"] and not DATE.match(bodies["## Last updated"]):
        errors.append("## Last updated must start with YYYY-MM-DD")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1] if len(argv) > 1 else STATE_FILE)
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: project state is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

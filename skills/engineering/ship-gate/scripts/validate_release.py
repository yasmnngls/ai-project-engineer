#!/usr/bin/env python3
"""Validate docs/releases/<version>.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADINGS = [
    "## Version",
    "## Verdict",
    "## Checks",
    "## Shipped",
    "## Not shipped",
    "## Env",
    "## Rollback",
    "## Risks open",
]
OPTIONAL_LISTS = ["## Not shipped", "## Env", "## Risks open"]
VERDICTS = {"ship", "hold"}
RESULTS = {"pass", "fail"}
EXCLUDED = {"later", "out", "cut"}
VERSION = re.compile(r"^(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?|\d{4}-\d{2}-\d{2})$")
FR = re.compile(r"\bFR-\d{3}\b")
TICKED = re.compile(r"`([^`]+)`")
PATH = re.compile(r"/|\.\w+$")
ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")
SECRETS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{8,}"), "an sk- key"),
    (re.compile(r"://[^/\s:@]+:[^@\s]+@"), "a URL with a user and password"),
    (re.compile(r"\b[0-9a-fA-F]{32,}\b"), "a long hex string"),
    (re.compile(r"[A-Za-z0-9+/]{32,}={0,2}"), "a long base64 string"),
]


def heading_match(text: str, heading: str) -> re.Match[str] | None:
    return re.search(rf"^{re.escape(heading)}[ \t]*$", text, re.MULTILINE)


def heading_body(text: str, heading: str, level: str = "## ") -> str:
    match = heading_match(text, heading)
    if not match:
        return ""
    lines = []
    for line in text[match.end():].splitlines()[1:]:
        if line.startswith(level) or (level == "### " and line.startswith("## ")):
            break
        lines.append(line)
    return "\n".join(lines).strip()


def bullets(body: str) -> list[str]:
    return [line.strip()[2:] for line in body.splitlines() if line.strip().startswith("- ")]


def is_list(body: str) -> bool:
    return all(line.strip().startswith("- ") for line in body.splitlines() if line.strip())


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


def prd_scope(prd: Path) -> tuple[set[str], dict[str, str]]:
    text = prd.read_text(encoding="utf-8")
    statuses: dict[str, str] = {}
    blocks = list(re.finditer(r"(?m)^### (FR-\d{3})\b", text))
    for index, match in enumerate(blocks):
        end = blocks[index + 1].start() if index + 1 < len(blocks) else len(text)
        body = text[match.end():end].split("\n## ", 1)[0]
        status = re.search(r"(?m)^- Status:\s*(\w+)", body)
        statuses[match.group(1)] = status.group(1).lower() if status else ""
    excluded = {fr for fr, status in statuses.items() if status in EXCLUDED}
    for heading in ("### Later", "### Out"):
        excluded.update(FR.findall(heading_body(text, heading, "### ")))
    return excluded, statuses


def validate(path: Path, root: Path, prd: Path | None, slice_: Path | None) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    text = path.read_text(encoding="utf-8-sig")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if first != "# Release":
        errors.append("First line must be '# Release'")

    positions = []
    bodies = {heading: heading_body(text, heading) for heading in HEADINGS}
    for heading, body in bodies.items():
        match = heading_match(text, heading)
        if not match:
            errors.append(f"Missing heading {heading!r}")
            continue
        positions.append(match.start())
        if not body:
            errors.append(f"{heading} is empty")
    if positions != sorted(positions):
        errors.append("Headings must be in order: " + ", ".join(h[3:] for h in HEADINGS))

    version = bodies["## Version"]
    if version and not VERSION.match(version):
        errors.append("## Version must be semver like 1.4.0 or a date like 2026-10-04")
    elif version and version != path.stem:
        errors.append(f"## Version {version} does not match the file name {path.name}")

    verdict = bodies["## Verdict"]
    if verdict and verdict not in VERDICTS:
        errors.append("## Verdict must be the single word ship or hold")

    rows = table_rows(bodies["## Checks"])
    if bodies["## Checks"] and not rows:
        errors.append("## Checks needs a table with at least one command")
    failed = []
    for cells in rows:
        if len(cells) < 2:
            errors.append(f"Checks row needs Command and Result: {cells}")
            continue
        command, result = cells[0], cells[1].lower()
        if not TICKED.fullmatch(command):
            errors.append(f"Checks command must be backticked: {command}")
        if result not in RESULTS:
            errors.append(f"Checks result for {command} must be pass or fail")
        if result == "fail":
            failed.append(command)
    if failed and verdict == "ship":
        errors.append(f"Verdict must be hold while a check fails: {', '.join(failed)}")

    shipped_body = bodies["## Shipped"]
    if shipped_body and not is_list(shipped_body):
        errors.append("## Shipped must be a bullet list")
    shipped: set[str] = set()
    for bullet in bullets(shipped_body):
        ids = FR.findall(bullet)
        refs = [ref for ref in TICKED.findall(bullet) if PATH.search(ref)]
        if len(ids) != 1:
            errors.append(f"Shipped bullet must name one FR-###: {bullet}")
        if not refs:
            errors.append(f"Shipped bullet needs a backticked test or route path: {bullet}")
        for ref in refs:
            if not (root / ref).exists():
                errors.append(f"Shipped path does not exist under {root}: {ref}")
        shipped.update(ids)

    for heading in OPTIONAL_LISTS:
        body = bodies[heading]
        if body and body != "None." and not is_list(body):
            errors.append(f"{heading} must be a bullet list or 'None.'")
    not_shipped = set(FR.findall(bodies["## Not shipped"]))
    for fr in sorted(shipped & not_shipped):
        errors.append(f"{fr} is in both Shipped and Not shipped")

    env = bodies["## Env"]
    if env and env != "None.":
        if "=" in env:
            errors.append("## Env lists names only. Remove the '=' assignment")
        names = TICKED.findall(env)
        if not names:
            errors.append("## Env must backtick each variable name")
        for name in names:
            if not ENV_NAME.match(name):
                errors.append(f"## Env name must be UPPER_SNAKE: {name}")
        rest = TICKED.sub(lambda m: "" if ENV_NAME.match(m.group(1)) else m.group(1), env)
        for pattern, label in SECRETS:
            if pattern.search(rest):
                errors.append(f"## Env contains what looks like {label}. Write the name, never the value")

    rollback = bodies["## Rollback"]
    if rollback:
        if len([line for line in rollback.splitlines() if line.strip()]) != 1:
            errors.append("## Rollback must be one line with one step")
        if not TICKED.search(rollback):
            errors.append("## Rollback must backtick the command, tag, or setting to use")

    if prd:
        if not prd.is_file():
            errors.append(f"Missing PRD: {prd}")
        else:
            excluded, statuses = prd_scope(prd)
            for fr in sorted(shipped | not_shipped):
                if fr not in statuses:
                    errors.append(f"{fr} is not a requirement in {prd.name}")
            for fr in sorted(shipped & excluded):
                errors.append(f"{fr} is later, out, or cut in {prd.name} and cannot ship")
            for fr in sorted(set(statuses) - shipped - not_shipped):
                errors.append(f"{fr} from {prd.name} is in neither Shipped nor Not shipped")

    if slice_:
        if not slice_.is_file():
            errors.append(f"Missing MVP slice: {slice_}")
        else:
            forbidden = set(FR.findall(heading_body(slice_.read_text(encoding="utf-8"), "## Do not build")))
            for fr in sorted(shipped & forbidden):
                errors.append(f"{fr} is in Do not build in {slice_.name} and cannot ship")
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--prd", type=Path, help="path to docs/foundation/01-prd.md")
    parser.add_argument("--slice", dest="slice_", type=Path, help="path to docs/foundation/07-mvp-slice.md")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="product root for Shipped paths")
    args = parser.parse_args(argv[1:])
    errors = validate(args.file, args.root, args.prd, args.slice_)
    if errors:
        print(f"{args.file}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{args.file}: release file is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

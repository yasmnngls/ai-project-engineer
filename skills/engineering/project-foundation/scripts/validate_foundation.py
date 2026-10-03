#!/usr/bin/env python3
"""Validate a project-foundation pack.

The headings and checks below are the contract. Keep
references/output-contract.md in sync with this file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "00-brief.md",
    "01-prd.md",
    "02-personas.md",
    "03-user-journeys.md",
    "04-sitemap.md",
    "05-system-design.md",
    "06-data-and-api.md",
    "07-mvp-slice.md",
    "08-risks.md",
]

TITLE_PREFIX = {
    "README.md": "# Project foundation",
    "00-brief.md": "# Brief:",
    "01-prd.md": "# PRD:",
    "02-personas.md": "# Personas",
    "03-user-journeys.md": "# User journeys",
    "04-sitemap.md": "# Sitemap",
    "05-system-design.md": "# System design",
    "06-data-and-api.md": "# Data and API",
    "07-mvp-slice.md": "# MVP slice",
    "08-risks.md": "# Risks",
}

EXACT_HEADINGS = {
    "README.md": ["## Pack", "## How to use this"],
    "00-brief.md": ["## Problem", "## User", "## Promise", "## MVP", "## Non-goals"],
    "01-prd.md": [
        "## Problem",
        "## Users",
        "## Success",
        "## Scope",
        "### In",
        "### Out",
        "### Later",
        "## Requirements",
        "## Non-functional requirements",
        "## Constraints",
    ],
    "03-user-journeys.md": ["## J1 ", "## J2 ", "## J3 "],
    "04-sitemap.md": ["## Map", "## Routes"],
    "05-system-design.md": [
        "## Context",
        "## Containers",
        "## Critical sequence",
        "## Decisions",
        "## Not designed yet",
    ],
    "06-data-and-api.md": ["## Entities", "## API"],
    "07-mvp-slice.md": ["## Build order", "## Done when", "## Do not build"],
    "08-risks.md": ["## Assumptions", "## Risks", "## Open questions"],
}

PREFIX_HEADINGS = {
    "02-personas.md": ["## P1 "],
    "03-user-journeys.md": ["## J1 ", "## J2 ", "## J3 "],
}

FR_FIELDS = [
    "- User:",
    "- Status:",
    "- Trigger:",
    "- Behavior:",
    "- Acceptance:",
    "- Screens:",
    "- Journey:",
]
PERSONA_FIELDS = ["- Role:", "- Job:", "- Context:", "- Success:"]
JOURNEY_FIELDS = ["- Persona:", "- Job:", "- Starts:", "- Succeeds when:"]
ROUTE_RE = re.compile(r"^(?:/|cmd:|api:)\S*$")
FR_HEADING_RE = re.compile(r"^### (FR-\d+)\b")
NFR_HEADING_RE = re.compile(r"^### (NFR-\d+)\b")
PROVENANCE_RE = re.compile(r"\[(stated|assumption|inferred)\]")
BANNED_RE = re.compile(r"\b(todo|tbd)\b|lorem ipsum", re.IGNORECASE)
STATUS_RE = re.compile(r"^- Status:\s*(in|later|cut)\b", re.MULTILINE)


def heading_level(line: str) -> int | None:
    match = re.match(r"^(#{1,6})\s+\S", line)
    if not match:
        return None
    return len(match.group(1))


def find_heading(lines: list[str], token: str, prefix: bool) -> int | None:
    for index, line in enumerate(lines):
        stripped = line.strip()
        if prefix:
            if stripped.startswith(token):
                return index
        elif stripped == token:
            return index
    return None


def section_body(lines: list[str], start: int) -> str:
    level = heading_level(lines[start].strip()) or 6
    body: list[str] = []
    for line in lines[start + 1 :]:
        current = heading_level(line.strip())
        if current is not None and current <= level:
            break
        body.append(line)
    return "\n".join(body).strip()


def table_data_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    header_seen = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            header_seen = False
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if not header_seen:
            header_seen = True
            rows.append(cells)
            continue
        rows.append(cells)
    if not rows:
        return []
    return rows[1:]


def table_column(text: str, header_name: str) -> list[str]:
    header_index = None
    values: list[str] = []
    header_seen = False
    column = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            header_seen = False
            column = None
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if not header_seen:
            header_seen = True
            for index, cell in enumerate(cells):
                if cell.lower() == header_name.lower():
                    column = index
                    header_index = index
                    break
            continue
        if column is not None and column < len(cells):
            values.append(cells[column])
    if header_index is None:
        return []
    return values


def split_h3(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^### .+$", text))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(0), text[start:end]))
    return sections


def validate(pack: Path) -> list[str]:
    errors: list[str] = []
    if not pack.is_dir():
        return [f"Missing pack directory: {pack}"]

    texts: dict[str, str] = {}
    for name in REQUIRED_FILES:
        path = pack / name
        if not path.is_file():
            errors.append(f"Missing file: {name}")
            continue
        texts[name] = path.read_text(encoding="utf-8")

    if errors:
        return errors

    for name, text in texts.items():
        if BANNED_RE.search(text):
            errors.append(f"{name}: replace placeholder text (todo, tbd, or lorem ipsum)")
        first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
        prefix = TITLE_PREFIX[name]
        if not first.startswith(prefix):
            errors.append(f"{name}: first line must start with {prefix!r}")

    lines_by_file = {name: text.splitlines() for name, text in texts.items()}

    for name, headings in EXACT_HEADINGS.items():
        lines = lines_by_file[name]
        for heading in headings:
            if heading in PREFIX_HEADINGS.get(name, []):
                continue
            index = find_heading(lines, heading, prefix=False)
            if index is None:
                errors.append(f"{name}: missing heading {heading!r}")
                continue
            if not section_body(lines, index):
                errors.append(f"{name}: heading {heading!r} is empty")

    for name, headings in PREFIX_HEADINGS.items():
        lines = lines_by_file[name]
        for heading in headings:
            index = find_heading(lines, heading, prefix=True)
            if index is None:
                errors.append(f"{name}: missing heading starting with {heading!r}")
                continue
            if not section_body(lines, index):
                errors.append(f"{name}: heading starting with {heading!r} is empty")

    persona_text = texts["02-personas.md"]
    for match in re.finditer(r"(?m)^## (P\d+ .+)$", persona_text):
        heading = f"## {match.group(1)}"
        lines = persona_text.splitlines()
        index = find_heading(lines, heading, prefix=False)
        body = section_body(lines, index) if index is not None else ""
        for field in PERSONA_FIELDS:
            if field not in body:
                errors.append(f"02-personas.md: {heading} missing {field!r}")

    prd = texts["01-prd.md"]
    fr_sections = [
        (match.group(1), body)
        for heading, body in split_h3(prd)
        if (match := FR_HEADING_RE.match(heading))
    ]
    if not fr_sections:
        errors.append("01-prd.md: add at least one '### FR-001' requirement")
    statuses: dict[str, str] = {}
    for fr_id, body in fr_sections:
        for field in FR_FIELDS:
            if field not in body:
                errors.append(f"01-prd.md: {fr_id} missing {field!r}")
        status = STATUS_RE.search(body)
        if status:
            statuses[fr_id] = status.group(1)
        else:
            errors.append(f"01-prd.md: {fr_id} status must be in, later, or cut")

    nfr_sections = [
        (match.group(1), body)
        for heading, body in split_h3(prd)
        if (match := NFR_HEADING_RE.match(heading))
    ]
    if not nfr_sections:
        errors.append("01-prd.md: add at least one '### NFR-001' requirement")
    for nfr_id, body in nfr_sections:
        if "- Acceptance:" not in body:
            errors.append(f"01-prd.md: {nfr_id} missing '- Acceptance:'")

    journeys = texts["03-user-journeys.md"]
    journey_lines = journeys.splitlines()
    for token in ("## J1 ", "## J2 ", "## J3 "):
        index = find_heading(journey_lines, token, prefix=True)
        if index is None:
            continue
        body = section_body(journey_lines, index)
        heading = journey_lines[index].strip()
        for field in JOURNEY_FIELDS:
            if field not in body:
                errors.append(f"03-user-journeys.md: {heading} missing {field!r}")
        steps_index = find_heading(body.splitlines(), "### Steps", prefix=False)
        if steps_index is None:
            errors.append(f"03-user-journeys.md: {heading} missing '### Steps'")
            continue
        steps = section_body(body.splitlines(), steps_index)
        rows = table_data_rows(steps)
        if len(rows) < 3:
            errors.append(f"03-user-journeys.md: {heading} needs at least 3 step rows")
        screens = table_column(steps, "Screen")
        if not screens:
            errors.append(f"03-user-journeys.md: {heading} steps table needs a Screen column")
        for screen in screens:
            if screen not in texts["04-sitemap.md"]:
                errors.append(
                    f"03-user-journeys.md: screen {screen!r} is not in 04-sitemap.md"
                )

    routes = table_column(
        section_body(
            texts["04-sitemap.md"].splitlines(),
            find_heading(texts["04-sitemap.md"].splitlines(), "## Routes", False) or 0,
        ),
        "Route",
    )
    if len(routes) < 3:
        errors.append("04-sitemap.md: Routes table needs at least 3 routes")
    for route in routes:
        if not ROUTE_RE.match(route):
            errors.append(
                f"04-sitemap.md: route {route!r} must start with /, cmd:, or api:"
            )

    if "```mermaid" not in texts["05-system-design.md"]:
        errors.append("05-system-design.md: add a mermaid diagram")

    for section_name, label in (("## Entities", "entity"), ("## API", "API")):
        lines = texts["06-data-and-api.md"].splitlines()
        index = find_heading(lines, section_name, prefix=False)
        body = section_body(lines, index) if index is not None else ""
        if not re.search(r"(?m)^### \S", body):
            errors.append(f"06-data-and-api.md: {section_name} needs at least one ### {label}")

    mvp_lines = texts["07-mvp-slice.md"].splitlines()
    build_index = find_heading(mvp_lines, "## Build order", prefix=False)
    build_body = section_body(mvp_lines, build_index) if build_index is not None else ""
    numbered = re.findall(r"(?m)^\d+\.\s+\S", build_body)
    if len(numbered) < 3:
        errors.append("07-mvp-slice.md: Build order needs at least 3 numbered steps")

    mvp_text = texts["07-mvp-slice.md"]
    journey_text = texts["03-user-journeys.md"]
    for fr_id, status in statuses.items():
        if fr_id not in mvp_text:
            errors.append(f"07-mvp-slice.md: cite {fr_id}")
        if status == "in" and fr_id not in journey_text:
            errors.append(f"03-user-journeys.md: in-scope {fr_id} is missing from a journey")

    questions = section_body(
        texts["08-risks.md"].splitlines(),
        find_heading(texts["08-risks.md"].splitlines(), "## Open questions", False) or 0,
    )
    question_count = len(re.findall(r"(?m)^\d+\.\s+\S", questions))
    if question_count > 7:
        errors.append("08-risks.md: keep open questions to 7 or fewer")

    combined = "\n".join(texts.values())
    if not PROVENANCE_RE.search(combined):
        errors.append(
            "Tag decisions with [stated], [assumption], or [inferred] in the pack"
        )
    assumed = any(PROVENANCE_RE.search(text) and "[assumption]" in text for text in texts.values())
    if assumed and "[assumption]" not in texts["08-risks.md"]:
        errors.append("08-risks.md: list every [assumption] in ## Assumptions")

    return errors


def main(argv: list[str]) -> int:
    pack = Path(argv[1] if len(argv) > 1 else "docs/foundation")
    errors = validate(pack)
    if errors:
        print(f"{pack}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{pack}: foundation pack is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

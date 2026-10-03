#!/usr/bin/env python3
"""Validate docs/bugs/<slug>.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADINGS = [
    "## Symptom",
    "## Loop",
    "## Minimised",
    "## Hypotheses",
    "## Probes",
    "## Cause",
    "## Fix",
    "## Regression test",
    "## Cleanup",
    "## Prevention",
]
VERDICTS = ["[confirmed]", "[ruled out]", "[untested]"]
NO_SEAM = "No correct seam:"
NO_LOGS = "No debug logs added."
TAG = re.compile(r"\[DEBUG-[0-9a-fA-F]{4,}\]")
EMPTY_WORDS = ("returned nothing", "came back empty", "empty", "no matches")
FENCE = re.compile(r"^(```+|~~~+)")
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "coverage", "docs", "examples"}
SOURCE_SUFFIXES = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro",
    ".py", ".rb", ".go", ".rs", ".java", ".kt", ".swift", ".cs", ".php",
    ".css", ".scss", ".html", ".sql", ".sh", ".ps1",
}
SECRET_VALUE = r"(?!<REDACTED>|\$|%|process\.env|os\.environ)[^\s\"'`,;}&]+"
SECRETS = [
    ("Bearer token", re.compile(rf"\bBearer\s+{SECRET_VALUE}")),
    ("sk- key", re.compile(r"\bsk-[A-Za-z0-9_-]{8,}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("cookie", re.compile(rf"(?i)\bcookie:\s*[^=\s]+={SECRET_VALUE}")),
    (
        "credential assignment",
        re.compile(
            rf"(?i)\b(?:password|passwd|passphrase|secret|token|api[_-]?key)[\"']?\s*[=:]\s*[\"']?{SECRET_VALUE}"
        ),
    ),
]


def section_lines(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line.strip()):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            current = line.strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def fenced_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    block: list[str] | None = None
    for line in lines:
        if FENCE.match(line.strip()):
            if block is None:
                block = []
            else:
                blocks.append(block)
                block = None
        elif block is not None:
            block.append(line)
    return blocks


def heading_order(text: str) -> list[str]:
    found = []
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line.strip()):
            fenced = not fenced
        elif not fenced and line.strip() in HEADINGS:
            found.append(line.strip())
    return found


def check_hypotheses(body: str, errors: list[str]) -> tuple[set[int], int | None]:
    items = re.findall(r"^\s*(\d+)\.\s+(.+)$", body, re.MULTILINE)
    if not 3 <= len(items) <= 5:
        errors.append(f"## Hypotheses needs three to five numbered items, found {len(items)}")
    numbers: set[int] = set()
    confirmed: list[int] = []
    for number, item in items:
        n = int(number)
        numbers.add(n)
        if not re.search(r"\bIf\b", item) or not re.search(r"\bthen\b", item, re.IGNORECASE):
            errors.append(f"Hypothesis {n} must state 'If ... then ...'")
        verdicts = [verdict for verdict in VERDICTS if verdict in item]
        if len(verdicts) != 1 or not item.rstrip().endswith(verdicts[0]):
            errors.append(f"Hypothesis {n} must end with one of {', '.join(VERDICTS)}")
        if "[confirmed]" in item:
            confirmed.append(n)
    if items and len(confirmed) != 1:
        errors.append(f"## Hypotheses needs exactly one [confirmed], found {len(confirmed)}")
    return numbers, confirmed[0] if len(confirmed) == 1 else None


def check_probes(body: str, numbers: set[int], confirmed: int | None, errors: list[str]) -> None:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if lines and not all(line.startswith("- ") for line in lines):
        errors.append("## Probes must be a bullet list")
    probed: set[int] = set()
    for line in lines:
        match = re.match(r"^- H(\d+):\s+\S", line)
        if not match:
            errors.append(f"Probe must start with 'H<n>:': {line}")
            continue
        n = int(match.group(1))
        if n not in numbers:
            errors.append(f"Probe names H{n}, which is not a hypothesis")
        probed.add(n)
    if confirmed is not None and confirmed not in probed:
        errors.append(f"Confirmed hypothesis H{confirmed} has no probe")


def check_regression(body: str, root: Path | None, errors: list[str]) -> None:
    first = next((line.strip() for line in body.splitlines() if line.strip()), "")
    if first.startswith(NO_SEAM):
        if not first[len(NO_SEAM):].strip():
            errors.append(f"'{NO_SEAM}' needs a reason on the same line")
        return
    match = re.match(r"^`([^`]+)`", first)
    if not match:
        errors.append(f"## Regression test must start with a backticked test path or '{NO_SEAM}'")
        return
    test_path = match.group(1)
    lowered = body.lower()
    if not re.search(r"\bred\b", lowered) or not re.search(r"\bgreen\b", lowered):
        errors.append("## Regression test must say it went red before the fix and green after")
    if "src/contracts/" in test_path.replace("\\", "/") and "safeParse" not in body:
        errors.append("A regression test in src/contracts/ must be a safeParse rejection")
    if root is not None and not (root / test_path).is_file():
        errors.append(f"Regression test {test_path} does not exist under {root}")


def check_cleanup(body: str, errors: list[str]) -> None:
    if body.strip() == NO_LOGS:
        return
    lowered = body.lower()
    if not TAG.search(body) or not any(word in lowered for word in EMPTY_WORDS):
        errors.append(f"## Cleanup must name the [DEBUG-xxxx] tag and say the search returned nothing, or be '{NO_LOGS}'")


def check_secrets(text: str, errors: list[str]) -> None:
    for number, line in enumerate(text.splitlines(), 1):
        for label, pattern in SECRETS:
            if pattern.search(line):
                errors.append(f"Line {number}: unredacted {label}. Write <REDACTED>")
                break


def leftover_tags(root: Path, skip: Path) -> list[str]:
    in_examples = "examples" in root.resolve().parts
    skip_dirs = SKIP_DIRS - {"examples"} if in_examples else SKIP_DIRS
    found = []
    for file in sorted(root.rglob("*")):
        relative = file.relative_to(root)
        if any(part in skip_dirs for part in relative.parts[:-1]):
            continue
        if not file.is_file() or file.suffix not in SOURCE_SUFFIXES or file.resolve() == skip:
            continue
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if "[DEBUG-" in line:
                found.append(f"{relative.as_posix()}:{number}")
    return found


def check_known_issues(root: Path, path: Path, errors: list[str]) -> None:
    state = root / "PROJECT-STATE.md"
    if not state.is_file():
        return
    known = "\n".join(section_lines(state.read_text(encoding="utf-8")).get("## Known issues", []))
    if path.name in known:
        errors.append(f"PROJECT-STATE.md ## Known issues still names {path.name}")


def validate(path: Path, root: Path | None) -> list[str]:
    if not path.is_file():
        return [f"Missing file: {path}"]
    if root is not None and not root.is_dir():
        return [f"--root is not a directory: {root}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    first = text.lstrip().splitlines()[0].strip() if text.strip() else ""
    if first != "# Diagnosis":
        errors.append("First line must be '# Diagnosis'")

    sections = section_lines(text)
    bodies = {heading: "\n".join(sections.get(heading, [])).strip() for heading in HEADINGS}
    for heading, body in bodies.items():
        if heading not in sections:
            errors.append(f"Missing heading {heading!r}")
        elif not body:
            errors.append(f"{heading} is empty")
    order = [heading for heading in heading_order(text) if heading in HEADINGS]
    present = [heading for heading in HEADINGS if heading in order]
    if order != present:
        errors.append("Headings must appear once each, in the order of references/diagnosis.md")

    loop_blocks = fenced_blocks(sections.get("## Loop", []))
    command = ""
    if len(loop_blocks) < 2:
        errors.append("## Loop needs a fenced block with the command and a fenced block with the red output")
    if loop_blocks:
        command_lines = [line.strip() for line in loop_blocks[0] if line.strip()]
        if len(command_lines) != 1:
            errors.append("## Loop's first fenced block must hold exactly one command line")
        else:
            command = command_lines[0]
    if len(loop_blocks) >= 2 and not any(line.strip() for line in loop_blocks[1]):
        errors.append("## Loop's red output block is empty")

    numbers, confirmed = check_hypotheses(bodies["## Hypotheses"], errors)
    if bodies["## Probes"]:
        check_probes(bodies["## Probes"], numbers, confirmed, errors)

    fix_blocks = fenced_blocks(sections.get("## Fix", []))
    if bodies["## Fix"] and command and not any(command in "\n".join(block) for block in fix_blocks):
        errors.append("## Fix needs a fenced block that re-runs the ## Loop command unchanged")

    if bodies["## Regression test"]:
        check_regression(bodies["## Regression test"], root, errors)
    if bodies["## Cleanup"]:
        check_cleanup(bodies["## Cleanup"], errors)
    check_secrets(text, errors)

    if root is not None:
        for location in leftover_tags(root, path.resolve()):
            errors.append(f"Leftover [DEBUG- tag at {location}")
        check_known_issues(root, path, errors)
    return errors


def main(argv: list[str]) -> int:
    args = argv[1:]
    root: Path | None = None
    if "--root" in args:
        index = args.index("--root")
        if index + 1 >= len(args):
            print("usage: validate_diagnosis.py <docs/bugs/slug.md> [--root <repo-root>]")
            return 2
        root = Path(args[index + 1])
        del args[index:index + 2]
    if len(args) != 1:
        print("usage: validate_diagnosis.py <docs/bugs/slug.md> [--root <repo-root>]")
        return 2
    path = Path(args[0])
    errors = validate(path, root)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{path}: diagnosis file is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

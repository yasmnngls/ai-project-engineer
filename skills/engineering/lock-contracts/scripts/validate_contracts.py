#!/usr/bin/env python3
"""Validate a src/contracts directory."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ANY = re.compile(r"\bany\b")


def validate(directory: Path) -> list[str]:
    if not directory.is_dir():
        return [f"Missing directory: {directory}"]
    errors: list[str] = []
    files = sorted(path for path in directory.glob("*.ts") if path.is_file())
    tsx = list(directory.glob("*.tsx"))
    if tsx:
        errors.append("Contracts must not include TSX")
    names = {path.name for path in files}
    if "index.ts" not in names:
        errors.append("Missing index.ts")
    if "results.ts" not in names:
        errors.append("Missing results.ts")
    schema_files = [path for path in files if path.name not in {"index.ts"}]
    if not any("z.object" in path.read_text(encoding="utf-8") for path in schema_files):
        errors.append("At least one schema file must call z.object")
    for path in files:
        text = path.read_text(encoding="utf-8")
        if ANY.search(text):
            errors.append(f"{path.name} uses any")
        if path.name != "index.ts" and 'from "zod"' not in text and "from 'zod'" not in text:
            errors.append(f"{path.name} must import zod")
    if "index.ts" in names:
        index = (directory / "index.ts").read_text(encoding="utf-8")
        if "from \"./" not in index and "from './" not in index:
            errors.append("index.ts must re-export the schema modules")
    if "results.ts" in names:
        results = (directory / "results.ts").read_text(encoding="utf-8")
        if "discriminatedUnion" not in results:
            errors.append("results.ts must use z.discriminatedUnion")
        if "z.literal(true)" not in results or "z.literal(false)" not in results:
            errors.append("results.ts must discriminate on ok true and ok false")
    return errors


def main(argv: list[str]) -> int:
    directory = Path(argv[1] if len(argv) > 1 else "src/contracts")
    errors = validate(directory)
    if errors:
        print(f"{directory}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{directory}: contracts are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

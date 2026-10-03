#!/usr/bin/env python3
"""Validate a feature shell: state.ts and view.tsx."""

from __future__ import annotations

import sys
from pathlib import Path

STATUSES = ("idle", "loading", "ready", "error")


def validate(directory: Path) -> list[str]:
    if not directory.is_dir():
        return [f"Missing directory: {directory}"]
    errors: list[str] = []
    state_path = directory / "state.ts"
    view_path = directory / "view.tsx"
    if not state_path.is_file():
        errors.append("Missing state.ts")
    if not view_path.is_file():
        errors.append("Missing view.tsx")
    if errors:
        return errors
    state = state_path.read_text(encoding="utf-8")
    view = view_path.read_text(encoding="utf-8")
    if "fetch(" in state or 'from "react"' in state or "from 'react'" in state:
        errors.append("state.ts must be a pure model: no React and no fetch")
    for status in STATUSES:
        if f'"{status}"' not in state:
            errors.append(f'state.ts missing status "{status}"')
    if "isLoading" in state or "isError" in state:
        errors.append("state.ts must not add isLoading or isError beside status")
    if "fetch(" in view:
        errors.append("view.tsx must not fetch")
    if 'from "zod"' in view or "from 'zod'" in view:
        errors.append("view.tsx must not import zod")
    if "Props" not in view:
        errors.append("view.tsx must name a Props type")
    lowered = view.lower()
    if "skeleton" not in lowered:
        errors.append("view.tsx needs a skeleton branch")
    if "usereducedmotion" not in lowered:
        errors.append("view.tsx must use useReducedMotion")
    if "<button" not in lowered:
        errors.append("view.tsx needs a real button for the primary action")
    return errors


def main(argv: list[str]) -> int:
    directory = Path(argv[1] if len(argv) > 1 else "src/features")
    errors = validate(directory)
    if errors:
        print(f"{directory}: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{directory}: shell is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

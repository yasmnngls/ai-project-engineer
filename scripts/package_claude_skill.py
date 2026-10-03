#!/usr/bin/env python3
"""Zip each skill for a claude.ai custom-skill upload.

Each archive contains <skill-name>/SKILL.md. Output is dist/<skill-name>.zip.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills" / "engineering"
DIST = ROOT / "dist"


def package(skill: Path) -> Path:
    out = DIST / f"{skill.name}.zip"
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(skill.rglob("*")):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            archive.write(path, Path(skill.name) / path.relative_to(skill))
    return out


def main() -> None:
    found = sorted(path.parent for path in SKILLS.glob("*/SKILL.md"))
    if not found:
        raise SystemExit(f"No skills under {SKILLS}")
    DIST.mkdir(parents=True, exist_ok=True)
    for skill in found:
        print(package(skill))


if __name__ == "__main__":
    main()

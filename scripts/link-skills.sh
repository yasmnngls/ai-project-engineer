#!/usr/bin/env bash
set -euo pipefail

# Maintainer script. Links promoted skills into the local harness directories:
#   ~/.claude/skills
#   ~/.agents/skills
#   ~/.cursor/skills
# Each entry is a symlink into this repo, so a git pull keeps them current.
# Re-run after adding, removing, or renaming a skill.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.cursor/skills")

names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills/engineering" -name SKILL.md -print0)

for DEST in "${DESTS[@]}"; do
  if [ -L "$DEST" ]; then
    resolved="$(readlink -f "$DEST")"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo ($resolved)." >&2
        echo "Remove it and re-run. The script will recreate it as a real directory." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip $name ($DEST already has a real directory)" >&2
      continue
    fi

    ln -sfn "$src" "$target"
    echo "linked $name -> $src ($DEST)"
  done
done

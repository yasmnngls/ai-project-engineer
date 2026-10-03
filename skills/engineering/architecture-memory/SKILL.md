---
name: architecture-memory
description: >
  Creates or updates ARCHITECTURE.md so later sessions read the system
  instead of reconstructing it from chat. Also installs the craft constraints
  for Cursor and Claude when those files are missing. Use when the user says
  "architecture", "remember this decision", "write ARCHITECTURE.md",
  "memory file", "before you build", or starts implementation after a
  project-foundation pack. Use before lock-contracts, state-shell, and
  one-chunk if ARCHITECTURE.md does not exist. Invoke with /architecture-memory.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator.
icon: book-open
color: cyan
---

# Architecture memory

Chat forgets containers and decisions. The file does not.

Write `ARCHITECTURE.md` at the root of the product repo. Do not overwrite this skill marketplace's own `ARCHITECTURE.md` unless the user asked to change the skill system. You can tell that repo by `.claude-plugin/marketplace.json` next to `skills/engineering/`.

## Do this

1. Read `docs/foundation/05-system-design.md`, `06-data-and-api.md`, and `07-mvp-slice.md`. If they are missing, say to run `/project-foundation` and stop.
2. Read `ARCHITECTURE.md` if it already exists. Keep decisions that are still true. Do not rewrite history into a cleaner story.
3. Read `references/architecture.md` and write the file with those headings.
4. If `.cursor/rules/craft.mdc` is missing, write it with the frontmatter in `references/architecture.md` and the body of `assets/constraints.md`.
5. If `CLAUDE.md` is missing, write a short file that points at `ARCHITECTURE.md` and then includes `assets/constraints.md`. If either file exists and does not mention `ARCHITECTURE.md`, append one sentence telling the next session to read it. Do not replace a file the project already owns.
6. Run:

```bash
python3 scripts/validate_architecture.py <product-root>/ARCHITECTURE.md
```

7. Reply with the path and the `## Last change` line. Do not paste the file.

## Do not

- Do not invent containers the system design does not name.
- Do not put component code in `ARCHITECTURE.md`.
- Do not open `examples/` and copy them.

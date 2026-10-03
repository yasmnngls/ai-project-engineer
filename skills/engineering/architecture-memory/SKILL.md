---
name: architecture-memory
description: >
  Architecture memory: creates or updates ARCHITECTURE.md so later sessions
  read the system instead of reconstructing it from chat, and installs the
  Cursor and Claude craft rules when missing. Use when the user records a
  decision, asks for ARCHITECTURE.md, or starts implementation after a
  project-foundation pack and the file does not exist yet. Invoke with
  /architecture-memory.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator.
icon: book-open
color: cyan
---

# Architecture memory

Chat forgets containers and decisions. The file does not.

Write `ARCHITECTURE.md` at the root of the product repo. This skill marketplace's own `ARCHITECTURE.md` changes only when the user asked to change the skill system. You can tell that repo by `.claude-plugin/marketplace.json` next to `skills/engineering/`.

## Do this

1. Read `docs/foundation/05-system-design.md`, `06-data-and-api.md`, and `07-mvp-slice.md`. If they are missing, say to run `/project-foundation` and stop.
2. Read `ARCHITECTURE.md` if it already exists. Keep decisions that are still true, in the words they were recorded.
3. Read `references/architecture.md` and write the file with those headings. Name only the containers the system design names. The file holds structure and decisions, not component code.
4. If `.cursor/rules/craft.mdc` is missing, write it with the frontmatter in `references/architecture.md` and the body of `assets/constraints.md`.
5. If `CLAUDE.md` is missing, write a short file that points at `ARCHITECTURE.md` and then includes `assets/constraints.md`. If either file exists and does not mention `ARCHITECTURE.md`, append one sentence telling the next session to read it, and leave the rest of that file as it is. The step is done when both files exist and mention `ARCHITECTURE.md`.
6. Run, and fix the file until it prints `architecture file is valid`:

```bash
python3 scripts/validate_architecture.py <product-root>/ARCHITECTURE.md
```

7. Reply with the path and the `## Last change` line. The file stays in the repo.

## Guardrails

- Never open `examples/` to copy from it. Write from this product's foundation pack.

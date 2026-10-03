---
name: project-foundation
description: >
  Writes the foundation pack for a new product in one pass: brief, PRD,
  personas, user journeys, sitemap, system design, data model and API, MVP
  build slice, and risks. Use when the user starts a new project, kicks off
  a product, says "new project", "greenfield", "write a PRD", "product spec",
  "site map", "sitemap", "information architecture", "user journey", "user
  flow", "system design", "architecture", "scope the MVP", or asks for the
  docs an AI engineer needs before building. Also use when a repo is empty
  or nearly empty and the user describes a product to build.   Works in Cursor
  and Claude. Invoke with /project-foundation, or with
  /ai-project-engineer:project-foundation when this skill is installed as the
  Claude Code plugin.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the pack validator.
icon: rocket
color: blue
---

# Project foundation

Write the spec pack an AI engineer builds from. Do the whole pack in one pass. Put it in `docs/foundation/` at the root of the project being founded.

This skill is the same folder in Cursor, Claude Code, and claude.ai. Use the file tools and shell those products give you. Do not change the pack because the host changed.

Paths in this skill are relative to the directory that contains this `SKILL.md`.

## Do this

1. Read `references/writing-rules.md` and `references/output-contract.md`.
2. Look at the repo you are founding. If it already has code or a README, read enough to see what is already true. Tag those facts `[inferred]`.
3. Apply the ask gate in `references/writing-rules.md`. If the gate says ask, ask in one message and stop. Do not draft the pack in that turn.
4. Write all ten files. Before each file, read the reference named for it in the output contract. Use the headings verbatim.
5. Run the validator from this skill directory:

```bash
python3 scripts/validate_foundation.py <project-root>/docs/foundation
```

6. If it reports problems, fix the files and run it again. Do not finish while it fails. If Python is unavailable, check the pack against `references/output-contract.md` by hand and say the script did not run.
7. Reply with the short closeout in writing-rules. Do not paste the pack into chat.

## Revisions

When the user changes a decision, update every file that cites it in the same pass. Keep existing `FR-` and `NFR-` ids. Add the next number for a new requirement. Mark a dropped requirement `cut` instead of deleting it.

## Companion skills

Do not write these in the kickoff pass. They run after the pack exists.

- `architecture-memory` writes `ARCHITECTURE.md` and the craft rules.
- `one-chunk` implements a single beat: contract, shell, or wire.
- `lock-contracts` writes the Zod schemas before any UI.
- `state-shell` splits one screen into a state model and a presentational view.
- `assumption-trial` writes a kill test for each load-bearing assumption.
- `say-no` writes the refusal for each excluded capability.
- `spec-drift` compares later code to this pack.

## Do not

- Do not write the pack into this repository's `examples/` directory.
- Do not open `examples/field-notes`. It is a validator fixture, not a template.
- Do not invent a second product, a marketing site, or a backlog beyond the pack.
- Do not start implementing the product in the same turn unless the user asked to build after the pack exists.

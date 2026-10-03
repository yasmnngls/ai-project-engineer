---
name: project-foundation
description: >
  Foundation pack for a new product, written in one pass: brief, PRD,
  personas, user journeys, sitemap, system design, data model and API, MVP
  build slice, and risks. Use when the user starts a new project, asks for
  any of those documents, or describes a product to build in an empty repo.
  Invoke with /project-foundation, or with
  /ai-project-engineer:project-foundation when this skill is installed as the
  Claude Code plugin.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the pack validator.
icon: rocket
color: blue
---

# Project foundation

Write the spec pack an AI engineer builds from. Do the whole pack in one pass. Put it in `docs/foundation/` at the root of the project being founded. The pack is the same in every host.

Paths in this skill are relative to the directory that contains this `SKILL.md`.

## Do this

1. Read `references/writing-rules.md` and `references/output-contract.md`.
2. Look at the repo you are founding. If it already has code or a README, read enough to see what is already true. Every fact taken from it is tagged `[inferred]`.
3. Apply the ask gate in `references/writing-rules.md`. If the gate says ask, send every question in one message and end the turn. The pack is drafted in the turn after the answers.
4. Write all ten files. Before each file, read the reference named for it in the output contract. Use the headings verbatim. The step is done when all ten files exist.
5. Run the validator from this skill directory:

```bash
python3 scripts/validate_foundation.py <project-root>/docs/foundation
```

6. Fix the files and run it again until it prints `foundation pack is valid`. If Python is unavailable, check the pack against `references/output-contract.md` by hand and say the script did not run.
7. Reply with the short closeout in writing-rules. The pack stays in its files.

## Revisions

When the user changes a decision, update every file that cites it in the same pass. Keep existing `FR-` and `NFR-` ids. Add the next number for a new requirement. Mark a dropped requirement `cut` instead of deleting it.

## Companion skills

These run in later turns, after the pack exists.

- `architecture-memory` writes `ARCHITECTURE.md` and the craft rules.
- `one-chunk` implements a single beat: contract, shell, or wire.
- `lock-contracts` writes the Zod schemas before any UI.
- `state-shell` splits one screen into a state model and a presentational view.
- `assumption-trial` writes a kill test for each load-bearing assumption.
- `say-no` writes the refusal for each excluded capability.
- `spec-drift` compares later code to this pack.

## Guardrails

- Write only the ten pack files for the product the user described. End the turn after the closeout. Build the product only when the user asks, after the pack exists.
- Never open `examples/field-notes` or write into this repository's `examples/`. It is a validator fixture, not a template.

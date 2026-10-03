---
name: one-chunk
description: >
  One chunk: implements exactly one beat of the foundation MVP, contract,
  shell, or wire, then stops. Use when the user asks for the next slice or
  step, or to build a screen or flow the pack already split into steps.
  Invoke with /one-chunk.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 validates the chunk file. Needs a project-foundation pack.
icon: rocket
color: green
---

# One chunk

"Build the dashboard" is how a session drifts. This skill does the next beat and stops.

## Do this

1. Read `ARCHITECTURE.md`. If it is missing, run `architecture-memory` and stop.
2. Read `docs/foundation/07-mvp-slice.md` and `docs/foundation/12-chunk.md` if that file exists.
3. Choose the beat. If `12-chunk.md` names an unfinished beat, do that beat. If the file is missing, the beat is `contract` for build-order step 1. If the named beat's files already exist and typecheck, advance one beat: `contract` to `shell`, `shell` to `wire`, `wire` to the next build step's `contract`. Advance at most one beat per turn. The step is done when one build step and one beat are chosen.
4. Read `references/chunk.md`. Update `12-chunk.md` before writing code. The step is done when the file names the beat and its definition of done.
5. Do the beat:
   - `contract`: follow `lock-contracts` for the entities that step stores. The test is a `safeParse` rejection of the invalid payload, in a `*.test.ts` next to the schema. No UI.
   - `shell`: follow `state-shell` for the route that step shows. `## Test` says `Automated test waits for the wire beat.`
   - `wire`: pass the contract's parsed result into the shell. Add one test that renders the view and asserts text the user can see. A reducer unit test or an assertion on private functions is not this test.
6. Update `ARCHITECTURE.md` `## Last change`. If `PROJECT-STATE.md` exists, follow `project-state` for the end of the session.
7. Run:

```bash
python3 scripts/validate_chunk.py <product-root>/docs/foundation/12-chunk.md
```

Then run the beat's own validator and the typecheck. The step is done when this script prints `chunk file is valid`, the beat's validator prints valid, and the typecheck exits 0.

8. Reply with the build step, the beat, what is true now, and the next beat. Stop.

## Guardrails

- Never copy this repository's `examples/`. Build from this product's pack.

---
name: project-state
description: >
  Project state: creates or updates PROJECT-STATE.md, the file a session
  reads first and writes last, with status, focus, progress, next actions,
  and which document or MCP server wins for each domain. Use at the start or
  end of a session, on a handoff, or when opening an existing repo that has
  no foundation pack. Invoke with /project-state.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator.
icon: compass
color: purple
---

# Project state

The next session should not reconstruct the project from chat, and it should not trust a README line because it found it first. `PROJECT-STATE.md` says what is true now and which source wins when two files disagree.

Write it at the root of the product repo. The skill marketplace itself gets none. You can tell that repo by `.claude-plugin/marketplace.json` next to `skills/engineering/`.

## Start of a session

1. Read `PROJECT-STATE.md`. If it is missing, go to Adopt.
2. Find the task's row in `## Read for`. Read only those sources and the code the task touches.
3. When two sources disagree, the row for that domain in `## Sources of truth` wins. If the winner contradicts the code, the code is what runs. Say so in the reply, and fix the source at the end of the session.
4. Work on `## Current focus`. If the user asks for something else, do it, and update the focus at the end.

## Adopt

Use this when `PROJECT-STATE.md` does not exist.

1. Inspect before writing: the package manifest, the source tree, the tests, the existing docs, env examples, and CI. List the MCP servers this session can reach.
2. Pick one source per domain, from sources you opened. Prefer what already exists: `docs/foundation/` from `project-foundation`, `ARCHITECTURE.md` from `architecture-memory`, `src/contracts/` from `lock-contracts`. If an MCP server owns the domain, such as an issue tracker for work or a design tool for UI, the source is `mcp:<server>`. If nothing owns the domain, write `missing` and leave it without a new document. The step is done when every domain has exactly one winner or `missing`.
3. Write `## Done` from what the code and its passing checks prove. Anything you could not verify goes under `## In progress` or `## Known issues`.

## End of a session

1. For each domain the session changed, update that row's source in the same turn, as `Update when` says. If the source is `mcp:<server>`, write through that server when this session can. Otherwise name the change in the reply. MCP-owned content stays in its server.
2. Move an item to `## Done` only after its test, typecheck, or lint ran and passed in this session. Name the check. A plan or a diff alone leaves it in progress.
3. Rewrite `## Current focus` and `## Next actions` for the next session. Action 1 is the next thing to do, not a theme.
4. Read `references/state.md` and keep its headings.
5. Run:

```bash
python3 scripts/validate_project_state.py <product-root>/PROJECT-STATE.md
```

The validator fails when a backticked path in either table does not exist. Fix the row, or write `missing`. The step is done when it prints `project state is valid`.

6. Reply with the status line, the current focus, and next action 1. The file stays in the repo.

## With the other skills

- `one-chunk` owns the current beat in `docs/foundation/12-chunk.md`. `## Current focus` names that file. It does not restate the beat's definition of done.
- `architecture-memory` owns structure. Point the Architecture row at `ARCHITECTURE.md` when it exists.
- `spec-drift` reports where the code and the pack disagree. A contradiction it finds belongs under `## Known issues` until it is fixed.

## Guardrails

- Never open `examples/` to copy from it. Write from this repo's own sources.

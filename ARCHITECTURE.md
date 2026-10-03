# Architecture

## Status

Skill marketplace at 1.4.0, published at https://github.com/yasmnngls/ai-project-engineer. This repository distributes Cursor and Claude skills. It is not the product those skills build.

## Read this first

Run the skills in this order once a product repo exists:

1. `project-foundation` writes `docs/foundation/`.
2. `architecture-memory` writes `ARCHITECTURE.md` and the craft rules in that product repo.
3. `one-chunk` performs a single beat of the MVP build order.
4. On a `contract` beat, `lock-contracts` writes Zod schemas before any UI.
5. On a `shell` beat, `state-shell` writes a pure state model and a presentational view.
6. On a `wire` beat, connect the shell to the contracts and add one test of what the user sees.

`assumption-trial`, `say-no`, and `spec-drift` read the pack. They do not replace steps 3 to 6.

`project-state` opens and closes each session through `PROJECT-STATE.md`. In an existing repo without a pack, it runs first and points each domain at what already exists.

`review-diff` writes `docs/reviews/` after a beat or a branch. `diagnose` writes `docs/bugs/` for one bug. `ship-gate` writes `docs/releases/` before a release.

## Containers

None. Nothing here serves HTTP. The distributable unit is the repository root: Claude and Cursor manifests, `skills/engineering/`, docs, one Cursor rule, and Python validators.

## Modules

- `skills/engineering/<name>/` is one skill. `SKILL.md` is the procedure. `references/` is the file shape. `scripts/validate_*.py` is the contract.
- `docs/engineering/<name>.md` is the human-facing page for that skill.
- `examples/` holds fixtures the validators accept. Skills must not copy a fixture into a product repo.
- `rules/craft.mdc` applies when a product file matching `*.ts` or `*.tsx` is in context.
- `scripts/package_claude_skill.py` zips each skill for claude.ai. The zip root is the skill folder.
- `scripts/link-skills.sh` symlinks the engineering skills into local harness directories.
- `.claude-plugin/plugin.json` lists the promoted skills. `.claude-plugin/marketplace.json` publishes this repo as that one plugin, with source `./`.
- `.cursor-plugin/marketplace.json` publishes the same plugin for Cursor, with source `.`.

## Contracts

A skill is unfinished without a validator and a fixture that passes it. Headings in the reference and checks in the script are the same contract. Do not add a skill that only leaves advice in chat.

Product code that the skills generate is validated in `examples/site-log/`. Those TypeScript files are a fixture for Site Log, typechecked with `tsc`. They are not a running app.

## UI boundary

This repo has no interface. Product views take props and do not fetch, parse, or decide. That split is enforced by `state-shell`, not by a component library.

## Decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Layout | `skills/<bucket>/<name>/SKILL.md` | Same shape as a public skills repo, so `npx skills add` and a Claude plugin can both install it. |
| Hosts | One skill folder for Cursor and Claude | The procedure is the same. Manifests differ. |
| Memory | `ARCHITECTURE.md` in the product repo | Agents reread a short file instead of reconstructing the system from chat. |
| Session state | `PROJECT-STATE.md` with one source of truth per domain | A session trusts the winning source, not the first file it finds. MCP servers can own a domain without being copied into docs. |
| Review | Checks before judgement, Standards and Spec kept apart | A failing typecheck is a fact and a smell is an opinion. Merging the axes lets one hide the other. |
| Bugs | A red loop before any hypothesis | A theory without a loop that fails on the symptom cannot be confirmed or ruled out. |
| Doc templates | None. One state file points at existing sources | A blank `DATABASE.md` or `SECURITY.md` competes with the code and goes stale. A missing domain is written as `missing`. |
| Boundaries | Zod schemas before UI | Invalid payloads and impossible UI states fail before a component exists. |
| Chunks | One beat per turn: contract, shell, or wire | A session that builds a whole feature rewrites its own constraints. |
| Examples | Fixtures, never templates | Copying Site Log into an unrelated product is a failed skill run. |
| Repository | https://github.com/yasmnngls/ai-project-engineer | Canonical public source for the marketplace. |

## Last change

2026-10-04 Added `project-state`, `diagnose`, `review-diff`, and `ship-gate`, each with a validator and a fixture under `examples/`.

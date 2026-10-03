# Changelog

## 1.4.0

- `project-state` keeps `PROJECT-STATE.md`, the file a session reads first and writes last. It names one source of truth per domain, which may be an MCP server, the files to update when that domain changes, and at most five sources to read per task.
- `project-state` adopts an existing repo that has no foundation pack.
- `one-chunk` hands the end of the session to `project-state` when `PROJECT-STATE.md` exists.
- `diagnose` writes `docs/bugs/<slug>.md`. The validator checks for a red loop, three to five falsifiable hypotheses with one confirmed, a fix that re-runs the loop, the regression test file, no leftover `[DEBUG-` tags, and no stale known issue.
- `review-diff` runs the pack validators and project checks before judgement, keeps Standards and Spec separate, scopes Spec to the current chunk, and writes a `ship` or `fix` verdict the validator ties to the findings.
- `ship-gate` writes `docs/releases/<version>.md`. Every PRD requirement is shipped with a path that exists or listed as not shipped, `later` and Do-not-build work cannot ship, and env lists names only.
- Every skill description lists one trigger per distinct case, and `## Do not` lists became at most two `## Guardrails`.

## 1.3.0

- Skills live in `skills/engineering/`, with a docs page per skill under `docs/engineering/`.
- The repo root is the Claude Code plugin and the Cursor marketplace entry.
- Install with `npx skills add yasmnngls/ai-project-engineer`, or with the Claude marketplace command in the README.

## 1.2.0

- `architecture-memory` keeps `ARCHITECTURE.md` as the file later sessions read.
- `lock-contracts` writes Zod schemas and discriminated results before UI.
- `state-shell` builds one screen as a state union plus a presentational view.
- `one-chunk` implements a single beat of the MVP: contract, shell, or wire.

## 1.1.0

- `assumption-trial` writes a kill test for each load-bearing assumption.
- `say-no` writes the refusal for each excluded capability.
- `spec-drift` compares the code to the pack and reports only contradictions, gaps, and hardened assumptions.

## 1.0.0

- Kickoff skill that writes a ten-file foundation pack.
- Cursor marketplace plugin and Claude Code marketplace plugin from the same skill folder.
- Pack validator and a field-notes fixture.

---
name: ship-gate
description: >
  Gates a release before it deploys: runs every check the project defines,
  proves each shipped requirement with a test or route, lists env var names,
  one rollback step, and what is not in the release, then records the
  verdict. Use before a release or deploy, or when the user asks whether
  the build is shippable. Invoke with /ship-gate.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator. Reads a project-foundation pack when one exists.
icon: package
color: green
---

# Ship gate

A release is a claim that the build works. The gate proves the claim, or writes `hold` and names the check that failed.

Write `docs/releases/<version>.md` in the product repo. This skill marketplace is not a product repo. You can tell it by `.claude-plugin/marketplace.json` next to `skills/engineering/`.

## Do this

1. Pick the version: the one the user named, else `version` in `package.json`, else today's date as `YYYY-MM-DD`.
2. Read `PROJECT-STATE.md`, `docs/foundation/01-prd.md`, `07-mvp-slice.md`, `08-risks.md`, and `09-assumption-trials.md` where they exist.
3. Run every check the project defines: the `typecheck`, `lint`, `test`, and `build` scripts in `package.json`, with the repo's package manager. Then run the validator of each pack skill whose output exists, such as `lock-contracts` for `src/contracts/` and `project-state` for `PROJECT-STATE.md`. Record each exact command and whether it passed. Any failure makes the verdict `hold`.
4. For each requirement you would call shipped, open the test or route that proves it. A requirement with nothing to open goes under `## Not shipped`. So does every `later`, `out`, or `cut` requirement and everything in Do not build.
5. Collect env var names from the code and `.env.example`.
6. Write the rollback: the one action that restores the previous release. For a first release, it is the action that takes this release down.
7. Copy into `## Risks open` each assumption from `08-risks.md` whose trial has no result.
8. Read `references/release.md` and write the file. Run from the product root:

```bash
python3 scripts/validate_release.py docs/releases/<version>.md --prd docs/foundation/01-prd.md --slice docs/foundation/07-mvp-slice.md
```

Leave out `--prd` and `--slice` when the repo has no pack. Fix failures and run it again.

9. Follow `project-state` for the end of the session. On `ship`, set `## Status` to `shipping` and add the release to `## Done`, naming the checks that passed. On `hold`, put the failing check under `## Known issues`. If the product repo has `CHANGELOG.md`, add the version with the shipped requirements.
10. Reply with the version, the verdict, and either the first failing check or the rollback step. Do not paste the file.

## Guardrails

- The gate reports. Deploy only when the user asked for the deploy in this conversation and the verdict is `ship`.
- `## Env` holds names. Write `TEAM_PASSPHRASE`, never its value, even when the value is in `.env`.

## With the other skills

- `spec-drift` finds a `later` capability built into the code. The gate refuses to list it as shipped.
- `assumption-trial` writes the trials. An untested one stays in `## Risks open` until its result is in.
- `project-state` owns `PROJECT-STATE.md`. The gate changes only its status, Done, and Known issues.

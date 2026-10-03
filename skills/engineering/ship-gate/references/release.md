# Release file

```markdown
# Release

## Version

0.1.0

## Verdict

ship

## Checks

| Command | Result |
| --- | --- |
| `npm run typecheck` | pass |
| `npm test` | pass |

## Shipped

- FR-001 Add a site. `src/contracts/site.test.ts`

## Not shipped

- FR-007 photo attachments. Later in the PRD.

## Env

- `TEAM_PASSPHRASE` the shared unlock value.

## Rollback

Redeploy tag `v0.0.9` with `vercel rollback`.

## Risks open

- One SQLite file is enough for the first team. No trial has run.
```

Write the file at `docs/releases/<version>.md` in the product repo.

`## Checks` has one row per command that ran in this session, with the exact command in backticks. A script the project does not define gets no row.

`## Shipped` cites the file a person opens to check the requirement: its test, its route, or the contract or screen that enforces its acceptance. Prefer the test.

`## Rollback` is the one action that puts the previous release back. For a first release, it is the action that takes this one down.

Rules the validator checks:

- The first line is `# Release`. Every heading is present, in this order, and non-empty.
- `## Version` is semver like `1.4.0` or a date like `2026-10-04`, and it matches the file name.
- `## Verdict` is the single word `ship` or `hold`. It is `hold` when any check is `fail`.
- `## Checks` is a table with at least one row. Each Command is backticked. Each Result is `pass` or `fail`.
- Every `## Shipped` bullet names one `FR-###` and at least one backticked path. A path is a backticked value with a `/` or a file extension. Every path exists relative to `--root`, which defaults to the current directory.
- `## Shipped` is bullets. `## Not shipped`, `## Env`, and `## Risks open` are bullets or the single line `None.`
- An FR id is never in both `## Shipped` and `## Not shipped`.
- `## Env` backticks UPPER_SNAKE names only. It has no `=` and nothing that looks like a secret: `sk-` keys, long hex or base64 strings, or `://user:pass@` URLs.
- `## Rollback` is one line with at least one backticked command, tag, or setting.
- With `--prd`, every FR id in the file exists in the PRD. No shipped FR has status `later`, `out`, or `cut`, or sits under the PRD's Later or Out scope. Every PRD requirement is in `## Shipped` or `## Not shipped`.
- With `--slice`, no shipped FR is named in the slice's `## Do not build`.

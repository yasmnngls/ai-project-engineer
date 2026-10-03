# Review shape

Write `docs/reviews/<YYYY-MM-DD>-<short-ref>.md`. `<short-ref>` is lowercase letters, digits, and hyphens, such as `step4-shell` or `pr-42`.

```markdown
# Review

## Fixed point

- Ref: `main`
- SHA: `{git rev-parse <ref>, 7 to 40 hex characters}`
- Diff: `git diff main...HEAD`
- Beat: {the ## Beat word from docs/foundation/12-chunk.md, or none}

## Files

- `src/features/visit/state.ts`

## Checks

| Command | Result |
| --- | --- |
| `git diff --check main...HEAD` | pass |
| `python3 <skills>/state-shell/scripts/validate_shell.py src/features/visit` | pass |
| `npm run typecheck` | fail |

## Standards

- [judgement] `src/features/visit/view.tsx:137` — {what is wrong, one or two sentences}. Source: Duplicated Code

## Spec

- [hard] `src/features/visit/state.ts:70` — {what is wrong}. Source: FR-004 Acceptance, "{quoted line}"

## Verdict

fix
```

## Rules the validator checks

- The first line is `# Review`. The headings above appear in that order, and none is empty.
- `## Fixed point` holds the resolved SHA and the backticked command `git diff <ref>...HEAD`.
- `## Files` is the output of `git diff --name-only <ref>...HEAD`, one backticked path per bullet.
- `## Checks` is a table. Each command is backticked. Each result is `pass` or `fail`. One row is `git diff --check <ref>...HEAD`.
- A file in `## Files` needs its pack validator in `## Checks`:

| Path | Validator |
| --- | --- |
| `src/contracts/...` | `validate_contracts.py` |
| `src/features/...` | `validate_shell.py` |
| `docs/foundation/12-chunk.md` | `validate_chunk.py` |
| `ARCHITECTURE.md` | `validate_architecture.py` |
| `PROJECT-STATE.md` | `validate_project_state.py` |

  A Spec finding that cites `12-chunk.md` also needs a `validate_chunk.py` row.
- A finding is one line: `- [hard] ` or `- [judgement] `, then a backticked `path:line` from `## Files`, then ` — `, what is wrong, and `Source:`.
- A Standards source is a backticked standard file with its rule, or a smell name from `smells.md`. A smell is always `[judgement]`.
- A Spec source cites an FR or NFR id, `12-chunk.md` with its heading, or an issue number such as `#42`.
- `## Standards` with no findings is `None.` `## Spec` with no findings is `None.`, or `No spec available.` when there is no PRD, chunk, or issue.
- `## Verdict` is `ship` or `fix`. It is `fix` when any check is `fail` or any finding is `[hard]`.

When the file sits in `docs/reviews/` of a product repo, the validator also checks that each cited line exists.

## Severity

- `[hard]`: a failing check, a documented rule the diff breaks, an acceptance line the diff contradicts, or code listed under `## Not in this chunk`.
- `[judgement]`: a smell, a partial requirement, or behaviour the beat may or may not own. Say which beat should own it.

Order findings by file, then line. Keep the two axes apart. The verdict is the only line that reads both.

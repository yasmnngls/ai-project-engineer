# Project state file

```markdown
# Project state

## Status

{foundation | building | shipping | maintenance | paused}. {One sentence on what exists today.}

## Current focus

{The one build step, beat, or bug the next session works on. Name `docs/foundation/12-chunk.md` when it exists.}

## Done

- {Verified work. Name the check that passed.}

## In progress

- {Started and not verified. Name the file.}

## Blocked

- {What is blocked, and who or what unblocks it.}

## Known issues

- {A defect or a drift finding that is not fixed yet.}

## Next actions

1. {The next concrete step.}

## Sources of truth

| Domain | Source | Update when |
| --- | --- | --- |
| Product | `docs/foundation/01-prd.md` | A requirement is added, cut, or changes acceptance |
| Architecture | `ARCHITECTURE.md` | A container, module, contract directory, or decision changes |
| Data | `src/contracts/` | An entity, field, or payload changes |
| UI | `mcp:figma` | A route, screen state, or shared primitive changes |
| Current work | `PROJECT-STATE.md` | Every session that changes the repo |

## Read for

| Task | Read |
| --- | --- |
| UI | `PROJECT-STATE.md`, `ARCHITECTURE.md`, `docs/foundation/04-sitemap.md` |
| Data | `PROJECT-STATE.md`, `ARCHITECTURE.md`, `src/contracts/` |

## Last updated

YYYY-MM-DD {one sentence}
```

The values in the tables are examples of shape. Use the sources this repo actually has.

Rules the validator checks:

- The first line is `# Project state`. Every heading is present and non-empty.
- `## Status` starts with `foundation`, `building`, `shipping`, `maintenance`, or `paused`.
- `## Done`, `## In progress`, `## Blocked`, and `## Known issues` are bullet lists, or the single line `None.`
- `## Next actions` has one to five numbered items.
- `## Sources of truth` has exactly one row each for Product, Architecture, Data, UI, and Current work. More domains are allowed, such as AI behavior or Security. No domain appears twice.
- A Source cell is backticked repo paths, backticked `mcp:<server>` names, or the word `missing`. Current work is `PROJECT-STATE.md`. Every row has an `Update when`.
- Every `## Read for` row starts with `PROJECT-STATE.md` and names at most five sources.
- Every backticked path in either table exists relative to the directory that holds `PROJECT-STATE.md`. A path ending in `/` must be a directory.
- `## Last updated` starts with a calendar date.

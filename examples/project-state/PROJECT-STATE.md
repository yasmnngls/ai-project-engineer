# Project state

## Status

building. Field Notes has its foundation pack, the visit contracts, and the visit screen shell. Nothing is wired to a server yet.

## Current focus

Build step 4, wire beat: pass the parsed submit result into the visit shell. The beat is defined in `../chunk/12-chunk.md`.

## Done

- Visit, site, and result contracts. `validate_contracts.py` and `tsc --noEmit` passed.
- Visit state union and presentational view. `validate_shell.py` and `tsc --noEmit` passed.

## In progress

None.

## Blocked

- The production passphrase. The office manager sets it before the first deploy.

## Known issues

- FR-005 lists only submitted visits, and no contract filters drafts yet.

## Next actions

1. Write the submit server action that returns the `SubmitResult` union.
2. Pass that result into the visit view and add one test that asserts the confirmation text the user sees.
3. Update `ARCHITECTURE.md` `## Last change`, then this file.

## Sources of truth

| Domain | Source | Update when |
| --- | --- | --- |
| Product | `../field-notes/01-prd.md` | A requirement is added, cut, or changes acceptance |
| Architecture | `../field-notes/05-system-design.md` | A container, module, or decision changes |
| Data | `../site-log/src/contracts/` | An entity, field, or payload changes |
| UI | `../site-log/src/features/visit/` | A route, screen state, or shared primitive changes |
| Risks | `../field-notes/08-risks.md` | An assumption is tested or a new risk appears |
| Tasks | `mcp:github` | An issue opens, closes, or changes scope |
| Current work | `PROJECT-STATE.md` | Every session that changes the repo |

## Read for

| Task | Read |
| --- | --- |
| UI | `PROJECT-STATE.md`, `../field-notes/04-sitemap.md`, `../site-log/src/features/visit/` |
| Data | `PROJECT-STATE.md`, `../field-notes/06-data-and-api.md`, `../site-log/src/contracts/` |
| Next beat | `PROJECT-STATE.md`, `../chunk/12-chunk.md`, `../field-notes/07-mvp-slice.md` |

## Last updated

2026-10-04 Recorded the shell beat for build step 4 and set the wire beat as the focus.

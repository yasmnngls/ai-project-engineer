# Output contract

Write these files in `docs/foundation/`. The validator script is the check. Headings below must match it character for character.

| File | First line | Reference to read first |
| --- | --- | --- |
| `README.md` | `# Project foundation` | this file |
| `00-brief.md` | `# Brief: {name}` | `references/brief.md` |
| `01-prd.md` | `# PRD: {name}` | `references/prd.md` |
| `02-personas.md` | `# Personas` | `references/personas.md` |
| `03-user-journeys.md` | `# User journeys` | `references/journeys.md` |
| `04-sitemap.md` | `# Sitemap` | `references/sitemap.md` |
| `05-system-design.md` | `# System design` | `references/system-design.md` |
| `06-data-and-api.md` | `# Data and API` | `references/data-api.md` |
| `07-mvp-slice.md` | `# MVP slice` | `references/mvp-and-risks.md` |
| `08-risks.md` | `# Risks` | `references/mvp-and-risks.md` |

## Required headings

`README.md`: `## Pack`, `## How to use this`

`00-brief.md`: `## Problem`, `## User`, `## Promise`, `## MVP`, `## Non-goals`

`01-prd.md`: `## Problem`, `## Users`, `## Success`, `## Scope`, `### In`, `### Out`, `### Later`, `## Requirements`, `## Non-functional requirements`, `## Constraints`

`02-personas.md`: `## P1 {name}` and `- Role:`, `- Job:`, `- Context:`, `- Success:`

`03-user-journeys.md`: `## J1 {name}`, `## J2 {name}`, `## J3 {name}`. Each has `- Persona:`, `- Job:`, `- Starts:`, `- Succeeds when:`, and `### Steps` with a table of at least 3 rows. The table includes a `Screen` column. Every screen string appears in the sitemap.

`04-sitemap.md`: `## Map`, `## Routes`. The routes table has a `Route` column and at least 3 rows. Each route starts with `/`, `cmd:`, or `api:`.

`05-system-design.md`: `## Context`, `## Containers`, `## Critical sequence`, `## Decisions`, `## Not designed yet`, and at least one `mermaid` fence.

`06-data-and-api.md`: `## Entities` and `## API`, each with at least one `###` block.

`07-mvp-slice.md`: `## Build order` (at least 3 numbered steps), `## Done when`, `## Do not build`. Every `FR-` id appears in this file.

`08-risks.md`: `## Assumptions`, `## Risks`, `## Open questions` (7 numbered questions maximum).

## Identifiers

- Functional requirements: `### FR-001` upward, stable across revisions.
- Non-functional: `### NFR-001` upward. At least one.
- Each FR includes `- User:`, `- Status:`, `- Trigger:`, `- Behavior:`, `- Acceptance:`, `- Screens:`, `- Journey:`.
- Status is `in`, `later`, or `cut`.
- Every `in` requirement appears in `03-user-journeys.md`.

## README body

`## Pack` links the other nine files. `## How to use this` tells the next session to build the MVP slice and to update every file that cites a decision when it changes.

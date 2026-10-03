# Risks

## Assumptions

- The technician types their name on each visit because the shared passphrase does not identify a person. [assumption]
- One Next.js process and one SQLite file are enough for the first team. [assumption]
- Office readers can read submitted visits and cannot comment or edit them. [assumption]
- Checklist items are defined on the site, and a visit copies them when it starts. [assumption]
- One passphrase covers the whole deployment, not one passphrase per depot. [assumption]

## Risks

| Risk | What breaks if it is true | Mitigation in the MVP |
| --- | --- | --- |
| Several depots share one deployment but need different passphrases | Anyone with the passphrase sees every team's visits | One deployment is one team. A second team is out of scope. |
| The site has no network at submit time | FR-004 cannot finish | The technician sees the server error and retries. Offline queue is FR-008. |
| Two people edit one draft | The last save wins | Acceptable for the MVP. The submitted visit is then locked. |

## Open questions

None. The assumptions above are enough to build the MVP.

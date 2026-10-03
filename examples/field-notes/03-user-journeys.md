# User journeys

## J1 Submit a visit before leaving

- Persona: P1, then P2 reads the result
- Job: Leave a visit record the office can trust.
- Starts: The technician is unlocked and a site already exists.
- Succeeds when: The visit is submitted and P2 can read it from the list.

### Steps

| # | User action | Screen | System response | Requirements |
| --- | --- | --- | --- | --- |
| 1 | Technician starts a visit for a site | /visits/new | App creates a draft whose checklist matches the site | FR-002 |
| 2 | Technician checks every item, types a name, and writes a note | /visits/:id | App stores the draft | FR-003 |
| 3 | Technician taps Submit | /visits/:id | App locks the visit and records the submit time | FR-004 |
| 4 | Office reader opens the list and the visit | / | App shows the submitted visit and hides drafts | FR-005 |

## J2 First run with no sites

- Persona: P1
- Job: Get into the app and create the first site.
- Starts: The browser has no session, and the team has no sites.
- Succeeds when: The passphrase is accepted and the new site is saved with a checklist.

### Steps

| # | User action | Screen | System response | Requirements |
| --- | --- | --- | --- | --- |
| 1 | Technician opens the app | /unlock | App shows the passphrase form | FR-006 |
| 2 | Technician enters the team passphrase | /unlock | App sets a session and opens an empty visit list | FR-006 |
| 3 | Technician adds a site name, address, and one checklist item | /sites/new | App saves the site | FR-001 |
| 4 | Technician opens the site | /sites/:id | App shows the site and its checklist | FR-001 |

## J3 Submit rejected, then recovered

- Persona: P1
- Job: Submit a complete visit after a rejected attempt.
- Starts: A draft is open and the note is empty.
- Succeeds when: The first submit is rejected and the second submit locks the visit.

### Steps

| # | User action | Screen | System response | Requirements |
| --- | --- | --- | --- | --- |
| 1 | Technician opens the draft and leaves the note empty | /visits/:id | App keeps the draft editable | FR-003 |
| 2 | Technician taps Submit | /visits/:id | App rejects the submit and indicates the empty note | FR-004 |
| 3 | Technician writes the note and taps Submit again | /visits/:id | App locks the visit | FR-004 |

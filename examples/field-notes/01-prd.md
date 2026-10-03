# PRD: Site Log

## Problem

Technicians finish a site visit without a record the office can trust. The record has to exist before they drive away. [stated]

## Users

P1, the field technician, writes the visit. P2, the office reader, reads submitted visits and does not change them. [stated]

## Success

A tester can unlock the app, add a site with two checklist items, submit a visit that checks both items and includes a name and a note, and see that visit on the submitted list. A visit with an empty note or an unchecked required item cannot be submitted. A submitted visit cannot be edited. [stated]

## Scope

### In

FR-001, FR-002, FR-003, FR-004, FR-005, FR-006.

### Out

User accounts, comments, customer signatures, invoicing, a native app, and more than one team in the same deployment.

### Later

FR-007 photo attachments. FR-008 offline submit.

## Requirements

### FR-001 Add a site

- User: P1 field technician [stated]
- Status: in
- Trigger: Technician saves the new-site form.
- Behavior: The app stores the site name, address, and at least one checklist item.
- Acceptance: Save is rejected when the name, address, or checklist is empty. A saved site appears on the site page with its checklist in order.
- Screens: /sites/new, /sites/:id
- Journey: J2

### FR-002 Start a visit

- User: P1 field technician [stated]
- Status: in
- Trigger: Technician chooses a site and starts a visit.
- Behavior: The app creates a draft visit for that site, copied from the site's current checklist.
- Acceptance: Starting a visit opens the draft. The draft's checklist matches the site at start time. Later edits to the site checklist do not change this draft.
- Screens: /visits/new, /visits/:id
- Journey: J1

### FR-003 Record the checklist, name, and note

- User: P1 field technician [stated]
- Status: in
- Trigger: Technician edits an open draft.
- Behavior: The app stores which checklist items are checked, the name the technician typed, and the note.
- Acceptance: A reload of the draft shows the same checks, name, and note. The name is free text because there is no account. [assumption]
- Screens: /visits/:id
- Journey: J1

### FR-004 Submit a visit

- User: P1 field technician [stated]
- Status: in
- Trigger: Technician taps Submit on an open draft.
- Behavior: The app locks the visit and marks it submitted, with the submit time.
- Acceptance: Submit succeeds only when every checklist item is checked, the name is non-empty, and the note is non-empty. Otherwise the draft stays open and the missing fields are indicated. A submitted visit cannot be edited.
- Screens: /visits/:id
- Journey: J1

### FR-005 Read submitted visits

- User: P2 office reader [stated]
- Status: in
- Trigger: Reader opens the visit list or a submitted visit.
- Behavior: The app shows submitted visits with site, checklist, name, note, and submit time. Drafts are not on this list.
- Acceptance: A visit appears on the list only after FR-004 succeeds. Opening it shows the stored checklist and note. The reader cannot submit or edit.
- Screens: /, /visits/:id
- Journey: J1

### FR-006 Unlock with the team passphrase

- User: P1 and P2 [stated]
- Status: in
- Trigger: Someone opens the app without a session.
- Behavior: The app asks for the team passphrase and then sets a session cookie.
- Acceptance: A wrong passphrase stays on the unlock screen. A correct passphrase opens the visit list. The passphrase is the single shared value configured for the deployment. [stated]
- Screens: /unlock
- Journey: J2

### FR-007 Attach a photo

- User: P1 field technician
- Status: later
- Trigger: Technician adds a photo to a draft.
- Behavior: The app stores an image on the visit.
- Acceptance: Not in the MVP. No upload control is shown.
- Screens: /visits/:id
- Journey: none

### FR-008 Submit offline

- User: P1 field technician
- Status: later
- Trigger: Technician submits with no network.
- Behavior: The app queues the visit and sends it later.
- Acceptance: Not in the MVP. Submit requires a response from the server.
- Screens: /visits/:id
- Journey: none

## Non-functional requirements

### NFR-001 Phone width

- Acceptance: Unlock, new site, and visit screens are usable at 390px width without horizontal scrolling.

### NFR-002 Locked after submit

- Acceptance: After FR-004, the visit's checklist, name, note, and submit time do not change through the UI or the submit action.

## Constraints

One shared team passphrase, no user accounts, no photo upload, and no offline queue. [stated]

The app is one Next.js server and one SQLite file. [assumption]

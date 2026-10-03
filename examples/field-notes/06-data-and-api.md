# Data and API

## Entities

### Site

- Owns: FR-001
- Fields: id text required, name text required, address text required, created_at timestamp required

### ChecklistItem

- Owns: FR-001, FR-002
- Fields: id text required, site_id text required, label text required, position integer required

### Visit

- Owns: FR-002, FR-003, FR-004, FR-005
- Fields: id text required, site_id text required, technician_name text required on submit, note text required on submit, status text required (`draft` or `submitted`), created_at timestamp required, submitted_at timestamp nullable

### VisitCheck

- Owns: FR-002, FR-003, FR-004
- Fields: visit_id text required, checklist_item_id text required, label text required, checked boolean required

The visit check copies the label at start time so a later edit to the site checklist does not change an open or submitted visit.

## API

### unlockTeam

- Actor: P1 or P2
- Input: passphrase
- Output: session cookie
- Errors: passphrase does not match the configured value
- Requirements: FR-006

### createSite

- Actor: P1
- Input: name, address, checklist labels in order
- Output: site id
- Errors: name, address, or checklist empty
- Requirements: FR-001

### startVisit

- Actor: P1
- Input: site id
- Output: draft visit id and copied checks
- Errors: site not found
- Requirements: FR-002

### saveVisitDraft

- Actor: P1
- Input: visit id, checks, technician name, note
- Output: saved draft
- Errors: visit is already submitted; visit not found
- Requirements: FR-003

### submitVisit

- Actor: P1
- Input: visit id
- Output: submitted visit with submitted_at
- Errors: any check unchecked; name empty; note empty; visit already submitted; visit not found
- Requirements: FR-004

### listSubmittedVisits

- Actor: P2
- Input: none
- Output: submitted visits only, newest first
- Errors: session missing
- Requirements: FR-005

### getVisit

- Actor: P1 or P2
- Input: visit id
- Output: visit, copied checks, and site name
- Errors: visit not found; session missing
- Requirements: FR-005

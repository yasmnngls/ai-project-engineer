# Refusals

## Catalog

### R1 Photos

- They ask: Can I attach a picture of the panel?
- We say: The visit on /visits/:id stores the checklist and the note (FR-004). A photo is not on that screen.
- Owns: FR-007 in 01-prd.md and 07-mvp-slice.md
- If it becomes real: Move FR-007 from later to in, and add the object storage named in Not designed yet.

### R2 Offline submit

- They ask: The basement has no signal. Can it send the visit later?
- We say: Submit on /visits/:id waits for the server (FR-004). The draft stays open until that response arrives.
- Owns: FR-008 in 01-prd.md and 07-mvp-slice.md
- If it becomes real: Move FR-008 from later to in, and add the local queue named in Not designed yet.

### R3 Separate logins

- They ask: Can each technician have their own login?
- We say: /unlock takes the one team passphrase (FR-006), and the visit stores a typed name. There is no account screen.
- Owns: 01-prd.md ### Out
- If it becomes real: A new FR replaces the shared passphrase, and the session cookie has to identify a person.

### R4 Comments

- They ask: Can the office write back on the visit?
- We say: After FR-004, /visits/:id is locked. The office reads it and does not write on it.
- Owns: 07-mvp-slice.md Do not build
- If it becomes real: A new FR adds a second writer on a submitted visit.

### R5 An installable app

- They ask: Is there an app to install on the phone?
- We say: The product is the phone page at / (FR-005). There is nothing to install.
- Owns: 00-brief.md Non-goals
- If it becomes real: A second client. The server actions in 06-data-and-api.md stay the API.

### R6 Invoicing and signatures

- They ask: Can the customer sign, and can we turn the visit into an invoice?
- We say: A submitted visit is the checklist, the name, and the note (FR-004). It does not collect a signature or create an invoice.
- Owns: 00-brief.md Non-goals and 01-prd.md ### Out
- If it becomes real: Two new FRs. Neither has a seam in the current data model.

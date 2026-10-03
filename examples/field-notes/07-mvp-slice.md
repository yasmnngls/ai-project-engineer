# MVP slice

## Build order

1. Passphrase form, session cookie, and a locked `/unlock` gate. FR-006.
2. Create a site with an ordered checklist and open the site page. FR-001.
3. Start a draft from a site and save checks, name, and note. FR-002, FR-003.
4. Submit the draft, reject incomplete drafts, and refuse further edits. FR-004.
5. Show only submitted visits on `/`, and open a read-only visit for the office. FR-005.

## Done when

- A wrong passphrase never leaves `/unlock`, and the right passphrase opens `/`.
- A site without a name, address, or checklist item does not save.
- A new draft's checklist matches the site at start time.
- Reloading a draft keeps the checks, name, and note.
- Submit fails while a check is off or the name or note is empty, and the draft stays editable.
- Submit succeeds only when every check is on and the name and note are filled, then the visit no longer accepts edits.
- `/` lists that visit and does not list drafts.
- Unlock, new site, and visit screens fit a 390px-wide phone without horizontal scrolling.

## Do not build

FR-007 photo attachments. FR-008 offline submit. User accounts, comments, signatures, invoicing, a native app, and a second team in the same database.

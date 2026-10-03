# Sitemap

## Map

```text
/unlock
/
  /sites/new
  /sites/:id
  /visits/new
  /visits/:id
```

Someone without a session only sees `/unlock`. After unlock, `/` is the submitted-visit list. Sites and drafts are reached from that list.

## Routes

| Route | Screen | User | Purpose | Empty | Error | Requirements |
| --- | --- | --- | --- | --- | --- | --- |
| /unlock | Unlock | P1, P2 | Enter the team passphrase | The form is the whole screen | Wrong passphrase stays here and says the passphrase was not accepted | FR-006 |
| / | Submitted visits | P2 | Read visits that have been submitted | No submitted visits yet, with a way to add a site | List fails to load and offers a retry | FR-005 |
| /sites/new | New site | P1 | Add a site and its checklist | The form is blank | Save blocked when name, address, or checklist is empty | FR-001 |
| /sites/:id | Site | P1 | See a site and start a visit | A site always has one checklist item, so the checklist is never empty | Unknown site id says the site was not found | FR-001, FR-002 |
| /visits/new | Start visit | P1 | Pick a site and create a draft | No sites yet, with a link to /sites/new | Create fails and the choice remains | FR-002 |
| /visits/:id | Visit | P1, P2 | Edit a draft, submit it, or read a submitted visit | Not used: a visit always has a site and a checklist | Submit rejected until every item is checked and the name and note are filled; unknown id says the visit was not found | FR-003, FR-004, FR-005 |

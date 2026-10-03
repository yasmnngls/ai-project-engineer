# Assumption trials

## Trials

### A1 Typed name

- Claim: The technician types their name on each visit because the shared passphrase does not identify a person. [assumption]
- Left alone: `Visit.technician_name` stays required free text. No person table.
- Kill test: Ask one office reader to match five typed names from last week's notes to the technicians who were on those sites.
- Result that flips it: They cannot match at least two of the five, or two technicians share a name the office would confuse.
- If it flips: FR-006 no longer ends at a shared cookie. A person id becomes required, and accounts leave `### Out`.
- Expensive after: Build order step 3, when the draft stores the name.

### A2 One SQLite file

- Claim: One Next.js process and one SQLite file are enough for the first team. [assumption]
- Left alone: The Decisions row stays one process and one database file.
- Kill test: Ask the office how many technicians submit a visit in the same fifteen minutes, and whether those phones talk to more than one server.
- Result that flips it: More than one server must accept submits at the same time.
- If it flips: No FR changes status. The SQLite container is replaced by a server database.
- Expensive after: Build order step 1, when the session and the database file are the app.

### A3 Office cannot comment

- Claim: Office readers can read submitted visits and cannot comment or edit them. [assumption]
- Left alone: `/visits/:id` is read-only after submit. Comments stay in Do not build.
- Kill test: Show one office reader a submitted note that is wrong and ask what they do next.
- Result that flips it: They need to write on the visit itself. A phone call or a separate message does not count.
- If it flips: Comments leave Do not build and need a new FR. A submitted visit gains a second writer.
- Expensive after: Build order step 5, when the office view is read-only.

### A4 Checklist copied at start

- Claim: Checklist items are defined on the site, and a visit copies them when it starts. [assumption]
- Left alone: `VisitCheck` stores the label from start time. Later site edits do not change the draft.
- Kill test: Ask one technician whether the checklist changes while they are still on the site.
- Result that flips it: They edit the site checklist and expect the open visit to change with it.
- If it flips: The acceptance on FR-002 changes. The copied label on `VisitCheck` goes away.
- Expensive after: Build order step 3, when the draft stores its own checks.

### A5 One passphrase for the deployment

- Claim: One passphrase covers the whole deployment, not one passphrase per depot. [assumption]
- Left alone: FR-006 checks a single configured value. Every session sees every visit.
- Kill test: Ask whether two depots would share this deployment, and whether each may see the other's visits.
- Result that flips it: They share a deployment and must not see each other's visits, or they need different passphrases.
- If it flips: FR-006 is no longer one configured value. "One team per deployment" leaves the risks table and becomes scope.
- Expensive after: Build order step 1, when the passphrase gate is the front door.

# Chunk file

```markdown
# Chunk

## Beat

shell

## Build step

{The numbered line from 07-mvp-slice.md, copied.}

## Done when

{What a person can observe when this beat is finished. One to three sentences.}

## Test

{Contract: the invalid payload safeParse rejects, and the field that fails.}
{Shell: Automated test waits for the wire beat.}
{Wire: the user-visible assertion, including the text they read.}

## Not in this chunk

{The next beat, the later build steps, and the pack's Do not build list that this step tempts.}

## Files

- src/contracts/visit.ts
```

`## Beat` is the single word `contract`, `shell`, or `wire` on its own line.

`## Files` lists paths this beat owns. It does not list the rest of the app.

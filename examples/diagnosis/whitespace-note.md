# Diagnosis

## Symptom

"I hit Submit with just a few spaces in the note and it went through. The office sees a visit with a blank note." Reported by P1 against FR-004, which says the note must be non-empty.

## Loop

```bash
curl -s -X POST http://localhost:3000/api/visits/v_204/submit -H "Cookie: site_log_session=<REDACTED>" -H "Content-Type: application/json" -d "{\"technicianName\":\"Ana\",\"note\":\"   \"}"
```

```text
{"ok":true,"data":{"id":"v_204","siteId":"s_12","status":"submitted","technicianName":"Ana","note":"   ","submittedAt":"2026-10-03T18:02:11.000Z", ...}}
```

FR-004 expects `{"ok":false,"error":"note_empty"}`. The loop is red: the server accepted a note of three spaces, which is the blank note the office saw.

## Minimised

The submit action with draft `v_204` and a note of `"   "`. The checklist is fully checked and the name is `Ana`. Changing the note to `"x"` turns the loop green, and so does removing the spaces.

- Cut: the browser form. The `curl` call reproduces it without the UI.
- Cut: the second checklist item. One checked item is enough.
- Cut: a newline-only note. Three spaces is the smallest case that stays red.

## Hypotheses

1. If `submittedVisitSchema` checks the note with `z.string().min(1)`, which counts spaces, then `submittedVisitSchema.safeParse` accepts `"   "`, and adding `.trim()` before `.min(1)` turns the loop green. [confirmed]
2. If the submit action writes the draft without parsing it, then an empty note `""` is accepted too, and a log at the parse call never prints. [ruled out]
3. If the form trims on blur but sends the raw textarea value on Submit, then the request body from the UI differs from what the form shows, and the `curl` loop with a trimmed body goes green. [ruled out]
4. If SQLite stores the note padded to a fixed width, then the stored value differs from the request value, and reading the row back shows extra spaces for `"x"`. [untested]

## Probes

- H2: Added `console.log("[DEBUG-7c1e] parse", result.success)` at the parse call in `src/features/visit/actions.ts`, then sent `""`. It printed `false` and the loop returned `note_empty`. The schema runs.
- H3: The `curl` loop already bypasses the form, and it is still red. The form is not the cause.
- H1: In a Node REPL, `submittedVisitSchema.shape.note.safeParse("   ").success` was `true`. With `.trim().min(1)` it was `false`. One change, opposite verdicts.

## Cause

`submittedVisitSchema.note` is `z.string().min(1)` in `src/contracts/visit.ts`. Zod counts whitespace as length, so three spaces pass `min(1)`. The submit action trusts the schema's verdict, so it locks the visit with a blank note.

## Fix

`note` and `technicianName` in `submittedVisitSchema` became `z.string().trim().min(1)` in `src/contracts/visit.ts`. A name of only spaces had the same hole.

```bash
curl -s -X POST http://localhost:3000/api/visits/v_204/submit -H "Cookie: site_log_session=<REDACTED>" -H "Content-Type: application/json" -d "{\"technicianName\":\"Ana\",\"note\":\"   \"}"
{"ok":false,"error":"note_empty"}
```

## Regression test

`src/contracts/visit.test.ts`

The bug crosses the submit payload boundary, so the seam is the contract. The test is a `safeParse` rejection of a whitespace-only note and name. It went red on the old schema and green after `.trim()`.

## Cleanup

Removed the `[DEBUG-7c1e]` log from `src/features/visit/actions.ts`. `rg -F "[DEBUG-7c1e]" src` returned nothing.

## Prevention

Every required free-text field in `src/contracts/` should use `z.string().trim().min(1)`. The contract test for each required string should include a whitespace-only case, so the next schema gets it at its contract beat.

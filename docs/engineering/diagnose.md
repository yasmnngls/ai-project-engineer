# diagnose

## What it does

Diagnoses one bug into `docs/bugs/<slug>.md`. It builds a command that goes red on the reported symptom, shrinks the repro, ranks three to five falsifiable hypotheses, probes them one variable at a time, and writes a regression test before the fix. The validator checks the file and the repo: one confirmed hypothesis, the same loop re-run green, the test file present, and no `[DEBUG-` log left in source.

## When to reach for it

Someone reports something broken, throwing, wrong, or slower than it was. Or the current focus in `PROJECT-STATE.md` is a known issue.

## Common questions

**Why build the loop before reading the code?** A theory without a red command cannot be tested. The loop turns each hypothesis into a yes or no.

**Where does the regression test go?** At the seam where the bug happens. A bad payload is a `safeParse` rejection next to the schema in `src/contracts/`, the same test shape `lock-contracts` writes.

**What if no test can reach the bug?** The file says `No correct seam:` and why. That is the finding, and `## Prevention` names the module that needs to change.

**What happens to the known issue?** If `PROJECT-STATE.md` exists, the bug is listed under `## Known issues` while it is open. The validator fails until the fixed bug leaves that list.

## It's working if

The reply names the cause, the regression test or the missing seam, and the prevention. The validator passes with `--root`, and the loop command in `## Fix` is the one in `## Loop`.

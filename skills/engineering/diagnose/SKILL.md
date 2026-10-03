---
name: diagnose
description: >
  Diagnoses a bug into docs/bugs/<slug>.md: a red loop, ranked falsifiable
  hypotheses, probes, a regression test before the fix, and cleanup. Use
  when the user reports something broken, throwing, or wrong, when
  something got slower, or when the current focus in PROJECT-STATE.md is a
  known issue. Invoke with /diagnose.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 validates the diagnosis file.
icon: bug
color: red
---

# Diagnose

A bug is found by a loop, not by reading code. This skill builds the loop first and writes every step into `docs/bugs/<slug>.md` in the product repo, so the next session can check the work instead of trusting it.

Read `references/diagnosis.md` before writing the file. Write each section when its step is done, in order.

## Redact

Write `<REDACTED>` in place of every token, cookie, key, and password you show. Build loops against environment variables, such as `$SITE_LOG_PASSPHRASE`, so the secret stays in the environment. Quote only the output lines that carry the signal. If the redacted output is not enough, say so and ask the user.

## Do this

1. Read `ARCHITECTURE.md` and `PROJECT-STATE.md` if they exist. Pick a short kebab-case slug. Write `## Symptom` with the user's exact words or the exact error. If `PROJECT-STATE.md` exists, add a `## Known issues` bullet that names `docs/bugs/<slug>.md`.

2. Build the loop. This is the skill. The loop is one command that drives the real code path and goes red on the user's symptom. Try these in order:
   - a failing test at the seam that reaches the bug
   - a `curl` against the running dev server
   - a CLI run on a fixture input, diffed against a known-good output
   - a headless browser script that asserts on the DOM or the network
   - a captured payload or trace replayed through the code path
   - a throwaway harness that calls the one function with mocked dependencies
   - a property loop over many random inputs
   - `git bisect run` between a good and a bad commit

   Then tighten it: seconds, not minutes; the same verdict every run; an assertion on the exact symptom. For a flaky bug, raise the reproduction rate until it is red most runs. For a slow path, the loop is a timing harness with a threshold.

   The step is done when you have run the command and seen it go red on this symptom. Write it into `## Loop`: the command in one fenced block, the red output in the next.

   If you cannot build a red loop, stop. List what you tried and ask for an environment that reproduces it, a redacted captured artifact, or permission to add temporary instrumentation.

3. Minimise. Cut inputs, callers, config, data, and steps one at a time. Re-run the loop after each cut. The step is done when removing any remaining element turns the loop green. Write what is left, and what you cut, into `## Minimised`.

4. Write three to five ranked hypotheses into `## Hypotheses`. Each one says: If {cause}, then {one change} turns the loop green, or {another change} makes it worse. A hypothesis without a prediction is a guess; sharpen it or drop it. Show the list to the user. If they re-rank it, follow their order. If they are away, follow yours.

5. Probe in rank order. Each probe changes one variable and tests one prediction. Prefer a debugger or a REPL. When you add a log, tag it with one tag for this whole diagnosis, `[DEBUG-` plus four random hex characters and `]`, at the boundary that separates two hypotheses. Write each probe into `## Probes` as `- H{n}: {what changed}. {what the loop did}.` Mark every hypothesis `[confirmed]`, `[ruled out]`, or `[untested]`. Stop probing when one is confirmed.

6. Write `## Cause`: the confirmed mechanism, in the code's terms.

7. Write the regression test before the fix, at a correct seam. A correct seam reproduces the bug the way the call site triggers it. A test at a shallower seam passes while the bug survives.
   - If the bug crosses a data boundary, the seam is the contract. Follow `lock-contracts`: the test is a `safeParse` rejection of the minimised payload, in a `*.test.ts` next to the schema in `src/contracts/`.
   - Run the test and watch it go red. Apply the fix. Watch it go green.
   - If no correct seam exists, that is the finding. Write `No correct seam:` and the reason, and carry it into `## Prevention`.

   Write the test path into `## Regression test` with one line on how it went red, then green.

8. Re-run the loop command from step 2, unchanged. Write `## Fix`: what changed, in which file, then the same command and its green output in one fenced block.

9. Clean up. Remove every tagged log and throwaway harness, then search the repo for the tag. Write `## Cleanup` with the tag and the search that came back empty, or `No debug logs added.`

10. Write `## Prevention`: what would have caught this earlier. If the answer is an architecture change, name the module and the change. If `PROJECT-STATE.md` exists, remove the bug's `## Known issues` bullet and follow `project-state` for the end of the session.

11. Run:

```bash
python3 scripts/validate_diagnosis.py <product-root>/docs/bugs/<slug>.md --root <product-root>
```

With `--root`, the validator fails on any `[DEBUG-` tag left in source, a missing test file, or a `## Known issues` bullet that still names this file. Fix the repo, not the check.

12. Reply with the cause, the regression test path or the missing seam, and the prevention. Link the file instead of pasting it.

## Guardrails

- A hypothesis comes after a red loop. When you catch yourself reading code to build a theory, return to step 2.
- Write the bug from this repo's own symptom. `examples/` holds fixtures for the validator, not diagnoses to copy.

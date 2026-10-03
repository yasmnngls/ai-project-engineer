# assumption-trial

## What it does

Turns each load-bearing assumption in the foundation pack into a kill test: one check that could flip the claim before it is expensive to undo. Output is `docs/foundation/09-assumption-trials.md`.

## When to reach for it

The pack exists and someone asks whether we are sure, or what would change our mind, before building.

## Common questions

**Does it rewrite the PRD?** No. It reads the pack and writes the trials file.

**What if nothing is assumed?** The file says there are no assumptions to try.

## It's working if

Each trial names the claim, what is left alone, the kill test, the result that flips it, and what happens if it flips.

# spec-drift

## What it does

Compares the product code to the foundation pack. It reports only three kinds of drift: a forbidden capability that was built, an in-scope requirement with nothing to point at, or an assumption the code now treats as a setting. Output is `docs/foundation/11-drift.md`.

## When to reach for it

Code exists and someone asks whether it still matches the spec.

## Common questions

**Is this a style review?** No. Naming, formatting, and bug hunts are out of scope.

**What if the code still matches?** The verdict is `clear`, and the finding says the code still matches the pack.

## It's working if

The verdict is the single word `clear` or `drift`, and every finding names the spec line and the code path.

# review-diff

## What it does

Reviews the diff since a fixed point. It runs the pack validators for the touched files and the project's typecheck, lint, and test scripts first. Then it judges two axes apart: Standards, against the repo's rules and a smell baseline, and Spec, against the current chunk and its FR ids. Output is `docs/reviews/<YYYY-MM-DD>-<short-ref>.md` with the verdict `ship` or `fix`.

## When to reach for it

Someone asks to review a branch, a PR, or the changes since a ref, or a one-chunk beat is about to close.

## Common questions

**How is this different from spec-drift?** `spec-drift` compares the whole repo to the whole pack. This review reads only the diff and the current beat. When it finds pack-level drift, it points to `/spec-drift`.

**Can a review ship with a failing check?** No. A failing check or a `[hard]` finding makes the verdict `fix`. The validator enforces it.

**Why are smells never hard?** They are judgement calls. A documented repo rule can be hard, and it overrides the smell baseline.

## It's working if

The Checks table shows every validator the touched paths need, each finding cites a `path:line` from the diff and a source, and the reply names the worst finding in each axis without ranking them against each other.

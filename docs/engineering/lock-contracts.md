# lock-contracts

## What it does

Writes Zod schemas in `src/contracts/` for the data the current beat stores. Draft and submitted records are different schemas. Action results are a union on `ok`.

## When to reach for it

The chunk beat is `contract`, or someone asks to define the types before UI.

## Common questions

**Can it add a screen?** No. A contract beat has no UI.

**What does the test check?** A `safeParse` rejection of an invalid payload, next to the schema.

## It's working if

`src/contracts/` exports the schemas, the invalid payload fails `safeParse`, and no view file was added in the same turn.

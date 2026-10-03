---
name: lock-contracts
description: >
  Contracts first: writes Zod schemas and discriminated result unions for the
  foundation pack's data and API before any UI exists. Use when the user asks
  to define types or lock a payload, or when one-chunk's beat is contract.
  For a screen, use state-shell. Invoke with /lock-contracts.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 validates the files. Typecheck with the project's TypeScript. Needs a project-foundation pack.
icon: shield
color: blue
---

# Lock contracts

A component that invents its props will invent a second product. Schemas come first.

Write `src/contracts/` in the product repo. This turn writes schemas only. UI waits for a shell beat.

## Do this

1. Read `ARCHITECTURE.md`. If it is missing, run `architecture-memory` first and stop after that file exists.
2. Read `docs/foundation/06-data-and-api.md` and the Decisions table in `05-system-design.md`. If the data file is missing, say to run `/project-foundation` and stop.
3. Read `references/schemas.md`. Write one module per entity, `results.ts` for action results, and `index.ts` that re-exports them. Add only fields the data file stores, plus ids and timestamps that file already names. The step is done when every entity in the data file has a module.
4. Use the Zod already in the project. If none is installed, add `zod` and import from `"zod"`.
5. Make impossible combinations unrepresentable. A submitted record cannot share a shape with a draft if their required fields differ. Each action returns a discriminated union on `ok`, not a thrown string and not a nullable data field.
6. Update `ARCHITECTURE.md` `## Contracts` and `## Last change`.
7. Run:

```bash
python3 scripts/validate_contracts.py <product-root>/src/contracts
```

Then typecheck the project. The step is done when the script prints `contracts are valid` and the typecheck exits 0.

8. Reply with the schema names and the action results. The modules stay in their files.

## Guardrails

- Every payload field is a named, typed key. Never use `any`, a blanket `passthrough`, or a single `Record<string, unknown>` as the payload.
- Never open `examples/site-log` to copy Site Log into another product.

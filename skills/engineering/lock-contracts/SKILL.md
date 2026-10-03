---
name: lock-contracts
description: >
  Writes Zod schemas and discriminated result unions for the foundation
  pack's data and API before any UI exists. Use when the user says
  "define the types", "Zod", "contracts first", "schema before UI",
  "lock the payload", or when one-chunk's beat is contract. Do not use
  to build screens. Invoke with /lock-contracts.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 validates the files. Typecheck with the project's TypeScript. Needs a project-foundation pack.
icon: shield
color: blue
---

# Lock contracts

A component that invents its props will invent a second product. Schemas come first.

Write `src/contracts/` in the product repo. Do not add a React component in this turn.

## Do this

1. Read `ARCHITECTURE.md`. If it is missing, run `architecture-memory` first and stop after that file exists.
2. Read `docs/foundation/06-data-and-api.md` and the Decisions table in `05-system-design.md`. If the data file is missing, say to run `/project-foundation` and stop.
3. Read `references/schemas.md`. Write one module per entity, `results.ts` for action results, and `index.ts` that re-exports them.
4. Use the Zod already in the project. If none is installed, add `zod` and import from `"zod"`.
5. Make impossible combinations unrepresentable. A submitted record cannot share a shape with a draft if their required fields differ. Each action returns a discriminated union on `ok`, not a thrown string and not a nullable data field.
6. Update `ARCHITECTURE.md` `## Contracts` and `## Last change`.
7. Run:

```bash
python3 scripts/validate_contracts.py <product-root>/src/contracts
```

Then typecheck the project. Fix both before finishing.

8. Reply with the schema names and the action results. Do not build UI. Do not paste the modules.

## Do not

- Do not use `any`, a blanket `passthrough`, or a single `Record<string, unknown>` as the payload.
- Do not add fields the data file does not store, except ids and timestamps that file already names.
- Do not open `examples/site-log` and copy Site Log into another product.

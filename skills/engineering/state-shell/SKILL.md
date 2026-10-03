---
name: state-shell
description: >
  State shell: builds one screen as a typed state model plus a presentational
  view that receives props and shows a skeleton. Use when the user asks for
  one screen or an empty shell with state kept apart from UI, or when
  one-chunk's beat is shell. Invoke with /state-shell.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 validates the feature folder. Needs locked contracts for the data that screen shows.
icon: beaker
color: purple
---

# State shell

Build one route from the sitemap. Leave the rest of the product alone.

## Do this

1. Read `ARCHITECTURE.md` and `src/contracts/index.ts`. If contracts for this screen do not exist, run `lock-contracts` and stop.
2. Pick the one route the user named. If they did not name one, use the route in the current `docs/foundation/12-chunk.md`. If that file is missing, use the first screen in the current build-order step and write that choice into `12-chunk.md` only when `one-chunk` is already the active beat. Otherwise ask which route, in one line, and stop. The step is done when exactly one route is chosen.
3. Read `references/shell.md`. Write `src/features/<screen>/state.ts` and `view.tsx`. The reducer lives in `state.ts`.
4. The view imports the state type and nothing from Zod. It receives data through props and does not call `fetch`. Status is a discriminated union that includes `idle`, `loading`, `ready`, and `error`. That union is the only loading, error, and data state, with no `isLoading`, `isError`, or nullable `data` beside it.
5. The ready branch has a visible label, a skeleton exists for loading, the primary action has a keyboard path, and one motion transition checks reduced motion.
6. Update `ARCHITECTURE.md` `## UI boundary` and `## Last change`.
7. Run:

```bash
python3 scripts/validate_shell.py <product-root>/src/features/<screen>
```

Then typecheck. The step is done when the script prints `shell is valid` and the typecheck exits 0.

8. Reply with the route, the status variants, and the primary action's key. Network wiring waits for the wire beat.

## Guardrails

- Build from the project's existing elements. Never install a component library.
- Never copy `examples/site-log`. Build from this product's contracts and sitemap.

---
name: state-shell
description: >
  Builds one screen as a typed state model plus a presentational view.
  The view receives props, shows a skeleton, and does not fetch or parse.
  Use when the user says "empty shell", "separate state from UI",
  "presentational component", "just the screen", or when one-chunk's beat
  is shell. Invoke with /state-shell.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 validates the feature folder. Needs locked contracts for the data that screen shows.
icon: beaker
color: purple
---

# State shell

Build one route from the sitemap. Leave the rest of the product alone.

## Do this

1. Read `ARCHITECTURE.md` and `src/contracts/index.ts`. If contracts for this screen do not exist, run `lock-contracts` and stop.
2. Pick the one route the user named. If they did not name one, use the route in the current `docs/foundation/12-chunk.md`. If that file is missing, use the first screen in the current build-order step and write that choice into `12-chunk.md` only when `one-chunk` is already the active beat. Otherwise ask which route, in one line, and stop.
3. Read `references/shell.md`. Write `src/features/<screen>/state.ts` and `view.tsx`.
4. The view imports the state type and nothing from Zod. It does not call `fetch`. Status is a discriminated union that includes `idle`, `loading`, `ready`, and `error`.
5. The ready branch has a visible label, a skeleton exists for loading, the primary action has a keyboard path, and one motion transition checks reduced motion.
6. Update `ARCHITECTURE.md` `## UI boundary` and `## Last change`.
7. Run:

```bash
python3 scripts/validate_shell.py <product-root>/src/features/<screen>
```

Then typecheck. Fix both before finishing.

8. Reply with the route, the status variants, and the primary action's key. Do not wire the network in this turn.

## Do not

- Do not add `isLoading`, `isError`, or `data` nullable as a second source of truth.
- Do not put the reducer in the view file.
- Do not install a component library.
- Do not copy `examples/site-log`.

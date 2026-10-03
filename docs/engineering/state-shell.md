# state-shell

## What it does

Builds one route as `state.ts` plus `view.tsx`. Status is a union (`idle`, `loading`, `ready`, `error`, and the extras that beat needs). The view takes props, shows a skeleton, and does not fetch or parse.

## When to reach for it

The chunk beat is `shell`, or someone asks for the screen without wiring it up.

## Common questions

**Where does the data come from?** It does not. The wire beat passes a parsed result in later.

**What about motion and the keyboard?** The view has a reduced-motion path and a keyboard path for the primary action.

## It's working if

The view compiles from props alone, the skeleton is the loading branch, and the chunk test line still says the automated test waits for the wire beat.

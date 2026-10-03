# one-chunk

## What it does

Implements exactly one beat of the MVP build order: `contract`, `shell`, or `wire`. It writes `docs/foundation/12-chunk.md` before the code, then stops.

## When to reach for it

Someone says to build the next slice, a screen, or a flow the pack already split into steps.

## Common questions

**Can one turn do the contract and the screen?** No. The next beat waits for the next turn.

**What is the test on a shell beat?** The chunk file says the automated test waits for the wire beat. The user-visible test arrives with `wire`.

## It's working if

The reply names the build step, the beat, what is true now, and the next beat. The following build-order step is untouched.

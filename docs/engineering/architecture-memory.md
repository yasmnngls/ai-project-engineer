# architecture-memory

## What it does

Writes `ARCHITECTURE.md` at the product root so the next session reads containers, modules, contracts, and decisions instead of reconstructing them from chat. If the craft rule or `CLAUDE.md` is missing, it adds them.

## When to reach for it

The foundation pack exists and implementation is about to start. Also when a container, module, or decision changes.

## Common questions

**Will it overwrite a product's existing architecture file?** It keeps decisions that are still true. It does not rewrite history into a cleaner story.

**Will it edit this skills repo?** Only if you asked to change the skill system. It recognizes this repo by `.claude-plugin/marketplace.json` next to `skills/engineering/`.

## It's working if

`ARCHITECTURE.md` has a dated `## Last change` line, and the reply names that path instead of pasting the file.

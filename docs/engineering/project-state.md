# project-state

## What it does

Keeps `PROJECT-STATE.md` at the product root: status, current focus, done, in progress, blocked, and next actions. It also records which document or MCP server wins for each domain, which files to update when that domain changes, and what to read for each kind of task.

## When to reach for it

At the start of a session, at the end of one, or when you open an existing repo that never had a foundation pack.

## Common questions

**Does it replace `ARCHITECTURE.md` or the foundation pack?** No. It points at them. `## Sources of truth` names one winner per domain, and that winner is often a file another skill writes.

**What if a domain lives in an MCP server?** The source is `mcp:<server>`, such as `mcp:github` for issues or `mcp:figma` for design. The skill does not copy that content into the repo.

**Why not read every doc each session?** `## Read for` caps each task at five sources after `PROJECT-STATE.md`, so a UI task does not load the database notes.

## It's working if

A new session reads `PROJECT-STATE.md`, opens only its task's row, and starts on next action 1. Every item under `## Done` names the check that passed. The validator finds no stale path.

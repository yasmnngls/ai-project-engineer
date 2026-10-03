# Architecture file

```markdown
# Architecture

## Status

{What exists today, in two sentences. Tag a guess with [assumption].}

## Read this first

{The order a session should touch this repo. Name the foundation pack and the contract directory.}

## Containers

{The deployable pieces from the system design. What each owns. What it must not own.}

## Modules

{Folders that exist, or that the next chunk will add. One line each. No future platform.}

## Contracts

{Where Zod schemas live, and which pack file they must agree with. `docs/foundation/06-data-and-api.md` is the source until code exists. After code exists, `src/contracts/` is the source and the pack is updated when they diverge.}

## UI boundary

{State lives in a reducer or hook. Views take props. Name the feature folder if one exists.}

## Decisions

| Decision | Choice | Why |
| --- | --- | --- |
| | | [{tag}] |

## Last change

YYYY-MM-DD {one sentence}
```

Every heading is required and non-empty. `## Last change` starts with a calendar date.

Cursor rule frontmatter, used only when `.cursor/rules/craft.mdc` is missing:

```markdown
---
description: When editing application TypeScript, read ARCHITECTURE.md, keep Zod contracts ahead of UI, and ship one verifiable chunk.
globs: "**/*.{ts,tsx}"
alwaysApply: false
---
```

The body under that frontmatter is `assets/constraints.md`, unchanged.

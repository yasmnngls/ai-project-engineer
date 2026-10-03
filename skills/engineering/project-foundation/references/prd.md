# PRD

The PRD is the numbered source of truth. Journeys, screens, and the MVP slice cite its ids. They do not invent parallel requirements.

## Shape

```markdown
# PRD: {Product name}

## Problem

## Users

## Success

{The observable outcome of the MVP. Prefer a check a tester can run over a growth metric.} [{tag}]

## Scope

### In

### Out

### Later

## Requirements

### FR-001 {verb phrase}

- User:
- Status: in
- Trigger:
- Behavior:
- Acceptance:
- Screens:
- Journey:

## Non-functional requirements

### NFR-001 {name}

- Acceptance:

## Constraints

{Stack, platform, compliance, and anything the repo already fixed.} [{tag}]
```

## Requirement rules

- One behavior per `FR-`. Split "create and submit" if their acceptance tests differ.
- Acceptance names the inputs that pass and the inputs that are rejected.
- `Screens:` uses the same route tokens as the sitemap (`/visits/:id`, `cmd:visit`, `api:submit`).
- `Journey:` cites `J1`, `J2`, or `J3` for status `in`. Use `none` for `later` or `cut`.
- `### In` is the list of `in` ids. `### Later` is the list of `later` ids. `### Out` is what will not be designed.
- Non-functional requirements are testable limits: viewport, latency budget, retention, who can read data. At least one.
- Constraints record the stack in a sentence and why that sentence is `[stated]`, `[inferred]`, or `[assumption]`.

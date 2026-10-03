# System design

Design the MVP, not the platform it might become.

```markdown
# System design

## Context

{Who talks to the product, and which external systems exist. One mermaid flowchart.}

## Containers

{The deployable pieces. Prefer one application and one database. Name the process, what it owns, and what it must not own.}

## Critical sequence

{The J1 submit path as a mermaid sequence diagram. Participants match the containers.}

## Decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Stack | | [{tag}] |

## Not designed yet

{Capabilities from scope Later and Out, and the seam where they would attach later.}
```

Include at least one mermaid fence. Two diagrams are enough: context and the critical sequence.

Decisions that need a row when they apply: stack, auth, file storage, and where state lives. Each row has a provenance tag in the Why cell.

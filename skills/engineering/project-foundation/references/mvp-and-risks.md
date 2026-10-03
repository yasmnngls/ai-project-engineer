# MVP slice and risks

The slice is the next session's build order. Risks hold the assumptions the pack depends on.

```markdown
# MVP slice

## Build order

1. {First vertical slice a person can see.}
2. 
3. 

## Done when

{The acceptance checks for every status `in` requirement, in tester language.}

## Do not build

{Every `later` and `cut` id, plus the tempting extras from scope Out.}
```

Build order is sequence, not a restatement of the PRD. Earlier steps should leave something a person can open. Cite `FR-` ids in the steps. Every FR id in the PRD appears somewhere in this file.

```markdown
# Risks

## Assumptions

- {decision} [assumption]

## Risks

| Risk | What breaks if it is true | Mitigation in the MVP |
| --- | --- | --- |
| | | |

## Open questions

None. The assumptions above are enough to build the MVP.
```

If you truly cannot assume something without changing the MVP, replace the "None" line with a numbered list of at most 7 questions. Do not also assume the answer in another file.

If the pack contains no assumptions, write: `No assumptions. Every decision in this pack was stated by the user or inferred from the repo.`

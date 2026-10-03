# Refusal shape

```markdown
# Refusals

## Asked now

- Verdict: refuse
- They ask: {the request from this conversation, in their words}
- We say: {one or two sentences. Name what exists instead.}
- Owns: {file and FR id or heading}
- If it becomes real: {the status change and the seam already named in Not designed yet}

## Catalog

### R1 {capability}

- They ask: {the sentence a person would actually say}
- We say:
- Owns:
- If it becomes real:
```

`## Asked now` is omitted when nobody has just requested an excluded thing.

`We say` is what the person hears. Two sentences maximum. It names a screen or an `FR-` id.

`Owns` points at the pack file that already excludes the capability.

`If it becomes real` is a spec change, not an implementation plan. It says which id moves from `later`, `out`, or `cut` to `in`, or that a new id is required.

If the pack excludes nothing, the file is only:

```markdown
# Refusals

## Catalog

Nothing is excluded.
```

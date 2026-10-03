# User journeys

Three journeys, each tied to screens and requirement ids.

- `J1` is the primary success path. It must include the moment the user finishes the job.
- `J2` is the first run, when the important collection is empty.
- `J3` is a failure and the recovery. Validation, a rejected submit, or a missing permission. Not a second happy path.

```markdown
# User journeys

## J1 {Name}

- Persona: P1
- Job:
- Starts:
- Succeeds when:

### Steps

| # | User action | Screen | System response | Requirements |
| --- | --- | --- | --- | --- |
| 1 | | /route | | FR-001 |
| 2 | | /route | | FR-002 |
| 3 | | /route | | FR-003 |
```

Repeat that shape for `J2` and `J3`.

The `Screen` cell is the route token from the sitemap, copied exactly. The `Requirements` cell cites one or more `FR-` ids. Every status `in` requirement appears in at least one row across the three journeys.

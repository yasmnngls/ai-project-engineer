# Data and API

Model only what an `in` requirement stores or reads. A `later` requirement does not get a table.

```markdown
# Data and API

## Entities

### {Entity}

- Owns: {the requirement ids}
- Fields: {name, type, and whether it is required}

## API

### {actionOrRoute}

- Actor:
- Input:
- Output:
- Errors:
- Requirements: FR-001
```

Field lists are concrete (`name text required`, `submitted_at timestamp nullable`). Relationships are a field (`site_id`) or a sentence under the entity.

Each API block is a server action, command, or HTTP route the MVP actually calls. Errors include the rejection named in the requirement's acceptance. Do not document a generic CRUD surface for entities nothing calls.

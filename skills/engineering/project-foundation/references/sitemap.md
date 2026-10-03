# Sitemap

The sitemap is the set of places a person or a caller can be. Screens in journeys must be copied from here.

```markdown
# Sitemap

## Map

{A fenced text tree, or a mermaid flowchart, of how someone moves.}

## Routes

| Route | Screen | User | Purpose | Empty | Error | Requirements |
| --- | --- | --- | --- | --- | --- | --- |
| / | {name} | P1 | | {what they see with no data} | {what they see when the action fails} | FR-001 |
```

Route tokens:

- Web screen: `/path` or `/things/:id`
- CLI: `cmd:name`
- HTTP API with no screen: `api:name`

Use at least three routes. Every `in` requirement appears in the Requirements column of the route where it happens. Empty and error are specific to that screen. "N/A" is allowed only when the screen cannot be empty or cannot fail, and the cell says why in a few words.

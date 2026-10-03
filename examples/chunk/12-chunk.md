# Chunk

## Beat

shell

## Build step

4. Submit the draft, reject incomplete drafts, and refuse further edits. FR-004.

## Done when

The visit screen shows a skeleton while loading, then the checklist, name, and note. Submit is unavailable while the visit is still loading. Cmd+Enter or Ctrl+Enter submits from the form.

## Test

Automated test waits for the wire beat.

## Not in this chunk

The server action, the database write, photos, and offline submit. The wire beat is next.

## Files

- src/features/visit/state.ts
- src/features/visit/view.tsx

# Schema shape

One file per entity. `results.ts` holds action results. `index.ts` only re-exports.

```ts
import { z } from "zod";

export const draftVisitSchema = z.object({
  status: z.literal("draft"),
  submittedAt: z.null(),
});

export const submittedVisitSchema = z.object({
  status: z.literal("submitted"),
  submittedAt: z.string().datetime(),
});

export const visitSchema = z.discriminatedUnion("status", [
  draftVisitSchema,
  submittedVisitSchema,
]);

export type Visit = z.infer<typeof visitSchema>;
```

Action results use the same discriminator everywhere:

```ts
export const submitVisitResultSchema = z.discriminatedUnion("ok", [
  z.object({ ok: z.literal(true), data: submittedVisitSchema }),
  z.object({
    ok: z.literal(false),
    error: z.enum(["unchecked", "name_empty", "note_empty", "already_submitted", "not_found"]),
  }),
]);
```

The `error` enum entries are the failures named in the API section of the pack, in snake_case. Do not add a generic `"unknown"` error to avoid deciding.

Imports use the extension style the repo already uses. A new NodeNext repo uses `.js` extensions in relative imports.

`index.ts` exports every public schema and type. It does not define a new shape.

import { z } from "zod";

import { siteSchema } from "./site.js";
import { submittedVisitSchema } from "./visit.js";

export const unlockResultSchema = z.discriminatedUnion("ok", [
  z.object({ ok: z.literal(true), data: z.object({ unlocked: z.literal(true) }) }),
  z.object({ ok: z.literal(false), error: z.enum(["passphrase_rejected"]) }),
]);

export const createSiteResultSchema = z.discriminatedUnion("ok", [
  z.object({ ok: z.literal(true), data: siteSchema }),
  z.object({
    ok: z.literal(false),
    error: z.enum(["name_empty", "address_empty", "checklist_empty"]),
  }),
]);

export const submitVisitResultSchema = z.discriminatedUnion("ok", [
  z.object({ ok: z.literal(true), data: submittedVisitSchema }),
  z.object({
    ok: z.literal(false),
    error: z.enum([
      "unchecked",
      "name_empty",
      "note_empty",
      "already_submitted",
      "not_found",
    ]),
  }),
]);

export type UnlockResult = z.infer<typeof unlockResultSchema>;
export type CreateSiteResult = z.infer<typeof createSiteResultSchema>;
export type SubmitVisitResult = z.infer<typeof submitVisitResultSchema>;

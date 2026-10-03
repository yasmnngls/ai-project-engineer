import { z } from "zod";

const visitCheckSchema = z.object({
  checklistItemId: z.string().min(1),
  label: z.string().min(1),
  checked: z.boolean(),
});

const visitBase = {
  id: z.string().min(1),
  siteId: z.string().min(1),
  checks: z.array(visitCheckSchema).min(1),
  createdAt: z.string().datetime(),
};

export const draftVisitSchema = z.object({
  ...visitBase,
  status: z.literal("draft"),
  technicianName: z.string(),
  note: z.string(),
  submittedAt: z.null(),
});

export const submittedVisitSchema = z.object({
  ...visitBase,
  status: z.literal("submitted"),
  technicianName: z.string().min(1),
  note: z.string().min(1),
  submittedAt: z.string().datetime(),
});

export const visitSchema = z.discriminatedUnion("status", [
  draftVisitSchema,
  submittedVisitSchema,
]);

export type DraftVisit = z.infer<typeof draftVisitSchema>;
export type SubmittedVisit = z.infer<typeof submittedVisitSchema>;
export type Visit = z.infer<typeof visitSchema>;

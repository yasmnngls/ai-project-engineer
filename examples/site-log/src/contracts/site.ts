import { z } from "zod";

export const checklistItemSchema = z.object({
  id: z.string().min(1),
  siteId: z.string().min(1),
  label: z.string().min(1),
  position: z.number().int().nonnegative(),
});

export const siteSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  address: z.string().min(1),
  checklist: z.array(checklistItemSchema).min(1),
  createdAt: z.string().datetime(),
});

export type ChecklistItem = z.infer<typeof checklistItemSchema>;
export type Site = z.infer<typeof siteSchema>;

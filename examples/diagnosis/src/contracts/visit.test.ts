import { describe, expect, it } from "vitest";

import { submittedVisitSchema } from "./visit.js";

const submitted = {
  id: "v_204",
  siteId: "s_12",
  status: "submitted",
  checks: [{ checklistItemId: "c_1", label: "Breaker panel labelled", checked: true }],
  createdAt: "2026-10-03T17:40:00.000Z",
  technicianName: "Ana",
  note: "Replaced the cracked cover.",
  submittedAt: "2026-10-03T18:02:11.000Z",
};

describe("submittedVisitSchema", () => {
  it("rejects a whitespace-only note", () => {
    const result = submittedVisitSchema.safeParse({ ...submitted, note: "   " });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0]?.path).toEqual(["note"]);
  });

  it("rejects a whitespace-only technician name", () => {
    const result = submittedVisitSchema.safeParse({ ...submitted, technicianName: "  " });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0]?.path).toEqual(["technicianName"]);
  });
});

import type { DraftVisit, SubmittedVisit, Visit } from "../../contracts/visit.js";

export type VisitState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "ready"; visit: DraftVisit; name: string; note: string }
  | { status: "submitting"; visit: DraftVisit; name: string; note: string }
  | { status: "done"; visit: SubmittedVisit }
  | { status: "error"; message: string };

export type VisitEvent =
  | { type: "load" }
  | { type: "loaded"; visit: Visit }
  | { type: "fail"; message: string }
  | { type: "name"; value: string }
  | { type: "note"; value: string }
  | { type: "toggle"; checklistItemId: string }
  | { type: "submit" }
  | { type: "submitted"; visit: SubmittedVisit }
  | { type: "retry" };

export function reduceVisit(state: VisitState, event: VisitEvent): VisitState {
  switch (state.status) {
    case "idle":
      return event.type === "load" ? { status: "loading" } : state;
    case "loading":
      if (event.type === "fail") {
        return { status: "error", message: event.message };
      }
      if (event.type !== "loaded") {
        return state;
      }
      if (event.visit.status === "submitted") {
        return { status: "done", visit: event.visit };
      }
      return {
        status: "ready",
        visit: event.visit,
        name: event.visit.technicianName,
        note: event.visit.note,
      };
    case "ready":
      if (event.type === "name") {
        return { ...state, name: event.value };
      }
      if (event.type === "note") {
        return { ...state, note: event.value };
      }
      if (event.type === "toggle") {
        return {
          ...state,
          visit: {
            ...state.visit,
            checks: state.visit.checks.map((check) =>
              check.checklistItemId === event.checklistItemId
                ? { ...check, checked: !check.checked }
                : check,
            ),
          },
        };
      }
      if (event.type === "submit") {
        return { status: "submitting", visit: state.visit, name: state.name, note: state.note };
      }
      return state;
    case "submitting":
      if (event.type === "submitted") {
        return { status: "done", visit: event.visit };
      }
      if (event.type === "fail") {
        return { status: "error", message: event.message };
      }
      return state;
    case "done":
      return state;
    case "error":
      return event.type === "retry" ? { status: "loading" } : state;
    default:
      return assertNever(state);
  }
}

function assertNever(value: never): never {
  throw new Error(`Unhandled visit state: ${JSON.stringify(value)}`);
}

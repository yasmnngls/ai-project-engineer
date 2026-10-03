import { useEffect, useRef } from "react";
import { motion, useReducedMotion } from "framer-motion";

import type { VisitState } from "./state.js";

export type VisitViewProps = {
  state: VisitState;
  onName: (value: string) => void;
  onNote: (value: string) => void;
  onToggle: (checklistItemId: string) => void;
  onSubmit: () => void;
  onRetry: () => void;
};

export function VisitView({ state, onName, onNote, onToggle, onSubmit, onRetry }: VisitViewProps) {
  const reduceMotion = useReducedMotion();
  const noteRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (state.status === "ready") {
      noteRef.current?.focus();
    }
  }, [state.status]);

  switch (state.status) {
    case "idle":
    case "loading":
      return (
        <section aria-busy={state.status === "loading"} className="grid gap-3">
          <p className="text-sm text-neutral-500">
            {state.status === "loading" ? "Opening the visit" : "Visit not loaded"}
          </p>
          <VisitSkeleton pulse={reduceMotion !== true} />
        </section>
      );
    case "error":
      return (
        <section role="alert" className="grid gap-3">
          <p>{state.message}</p>
          <button
            type="button"
            onClick={onRetry}
            className="w-fit rounded-md bg-neutral-900 px-3 py-2 text-sm text-white"
          >
            Try again
          </button>
        </section>
      );
    case "done":
      return (
        <section className="grid gap-2">
          <h1 className="text-lg font-medium tracking-tight">Visit submitted</h1>
          <p className="text-sm text-neutral-700">{state.visit.note}</p>
        </section>
      );
    case "ready":
    case "submitting": {
      const pending = state.status === "submitting";
      return (
        <motion.form
          className="grid gap-4"
          initial={reduceMotion ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={reduceMotion ? { duration: 0 } : { type: "spring", stiffness: 420, damping: 34 }}
          onSubmit={(event) => {
            event.preventDefault();
            onSubmit();
          }}
          onKeyDown={(event) => {
            if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
              event.preventDefault();
              onSubmit();
            }
          }}
        >
          <fieldset className="grid gap-2" disabled={pending}>
            <legend className="text-sm font-medium">Checklist</legend>
            {state.visit.checks.map((check) => (
              <label key={check.checklistItemId} className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={check.checked}
                  onChange={() => onToggle(check.checklistItemId)}
                />
                {check.label}
              </label>
            ))}
          </fieldset>
          <label className="grid gap-1 text-sm">
            Your name
            <input
              value={state.name}
              onChange={(event) => onName(event.target.value)}
              className="rounded-md border border-neutral-300 px-2 py-1.5"
              autoComplete="name"
            />
          </label>
          <label className="grid gap-1 text-sm">
            Note
            <textarea
              ref={noteRef}
              value={state.note}
              onChange={(event) => onNote(event.target.value)}
              rows={4}
              className="rounded-md border border-neutral-300 px-2 py-1.5"
            />
          </label>
          <div className="flex items-center justify-between gap-3">
            <p className="text-xs text-neutral-500">Cmd+Enter or Ctrl+Enter submits.</p>
            <button
              type="submit"
              disabled={pending}
              className="rounded-md bg-neutral-900 px-3 py-2 text-sm text-white disabled:opacity-60"
            >
              {pending ? "Submitting" : "Submit visit"}
            </button>
          </div>
        </motion.form>
      );
    }
    default:
      return assertNever(state);
  }
}

function VisitSkeleton({ pulse }: { pulse: boolean }) {
  const bar = pulse ? "h-3 animate-pulse rounded bg-neutral-200" : "h-3 rounded bg-neutral-200";
  return (
    <div className="grid gap-2" aria-hidden="true">
      <div className={`${bar} w-2/3`} />
      <div className={`${bar} w-full`} />
      <div className={`${bar} skeleton w-5/6`} />
    </div>
  );
}

function assertNever(value: never): never {
  throw new Error(`Unhandled visit view state: ${JSON.stringify(value)}`);
}

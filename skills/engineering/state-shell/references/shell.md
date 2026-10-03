# Shell shape

`state.ts` is free of JSX and of `fetch`. It exports the status union and a pure reducer.

```ts
export type FeatureState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "ready"; /* fields the view may render */ }
  | { status: "error"; message: string };

export type FeatureEvent =
  | { type: "load" }
  | { type: "loaded" }
  | { type: "fail"; message: string };

export function reduceFeature(state: FeatureState, event: FeatureEvent): FeatureState {
  return state;
}
```

Illegal events return the same state. They do not throw and they do not coerce a loading screen into a submitted record.

`submitting` and `done` are allowed extra variants when the screen needs them. A boolean beside `status` is not.

`view.tsx` exports a props type and a component. It imports `type` from `./state` only. The switch on `state.status` ends in an `assertNever` default so a new variant fails typecheck.

Loading renders a skeleton, not a blank page. Error renders the message and a control that calls the retry prop. Ready renders the fields from props. The component does not import Zod and does not call `fetch`.

Motion: one entrance on the ready surface, with `useReducedMotion`. When motion is reduced, the transition duration is 0. Use `motion/react` if the `motion` package is installed, otherwise `framer-motion`.

Keyboard: the primary action runs on a stated key, usually Meta+Enter or Ctrl+Enter for submit, and the control is a real `button`.

Focus: when status becomes `ready`, move focus to the first field. That effect does not load data.

Tailwind utilities style the screen. Do not add a CSS framework.

---
name: assumption-trial
description: >
  Assumption trial: turns each load-bearing assumption in a
  project-foundation pack into a kill test, one check that could flip the
  claim before it is expensive to undo. Use when the user challenges the
  pack's assumptions or asks what would change the plan, once
  docs/foundation exists. Invoke with /assumption-trial.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator. Needs a project-foundation pack.
icon: beaker
color: yellow
---

# Assumption trial

A foundation pack is allowed to assume. This skill decides which assumptions are safe to build on, and which need a kill test first.

Write `docs/foundation/09-assumption-trials.md` in the project that holds the pack. This turn writes only that file.

## Do this

1. Read `docs/foundation/08-risks.md`, `01-prd.md`, `05-system-design.md`, and `07-mvp-slice.md`. If `08-risks.md` is missing, say to run `/project-foundation` and stop.
2. Keep an assumption only when flipping it would change the primary user, what is in or out, the stack, or what is stored. Drop wording assumptions. The step is done when every kept assumption names which of those four it would change.
3. Read `references/trial.md`. Write one `### A` block per remaining assumption. Copy the claim from the risks file word for word.
4. A kill test that takes longer than build-order step 1 is not a kill test. Mark that assumption accepted for the MVP and say which step makes it expensive.
5. Run this skill's validator:

```bash
python3 scripts/validate_trials.py <project-root>/docs/foundation/09-assumption-trials.md
```

6. Fix failures and run it again until it prints `assumption trials are valid`. Then reply with how many trials there are and which single trial to run before build-order step 1. The file stays in the repo.

## Guardrails

- A kill test is one check against the product's own claim. Never propose a survey, a landing page, or a research plan.
- Never open `examples/`. The fixture is not the user's product.

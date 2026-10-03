---
name: assumption-trial
description: >
  Turns each load-bearing assumption in a project-foundation pack into a
  kill test: one check that could flip the claim before it is expensive to
  undo. Use when the user asks "are we sure", "challenge the assumptions",
  "what would change our mind", "kill test", "before we build", or
  "assumption trial". Use after docs/foundation exists. Do not use to write
  the original PRD. Invoke with /assumption-trial.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator. Needs a project-foundation pack.
icon: beaker
color: yellow
---

# Assumption trial

A foundation pack is allowed to assume. This skill decides which assumptions are safe to build on, and which need a kill test first.

Write `docs/foundation/09-assumption-trials.md` in the project that holds the pack. Do not edit the other pack files. Do not implement the product.

## Do this

1. Read `docs/foundation/08-risks.md`, `01-prd.md`, `05-system-design.md`, and `07-mvp-slice.md`. If `08-risks.md` is missing, say to run `/project-foundation` and stop.
2. Keep an assumption only when flipping it would change the primary user, what is in or out, the stack, or what is stored. Drop wording assumptions.
3. Read `references/trial.md`. Write one `### A` block per remaining assumption. Copy the claim from the risks file. Do not soften it.
4. A kill test that takes longer than build-order step 1 is not a kill test. Mark that assumption accepted for the MVP and say which step makes it expensive.
5. Run this skill's validator:

```bash
python3 scripts/validate_trials.py <project-root>/docs/foundation/09-assumption-trials.md
```

6. Fix failures and run it again. Then reply with how many trials there are and which single trial to run before build-order step 1. Do not paste the file.

## Do not

- Do not add requirements, personas, or a new product idea.
- Do not propose a survey, a landing page, or a research plan.
- Do not open `examples/`. The fixture is not the user's product.

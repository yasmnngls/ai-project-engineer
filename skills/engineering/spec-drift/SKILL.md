---
name: spec-drift
description: >
  Spec drift: compares the code to a project-foundation pack and reports only
  real drift: a later or out-of-scope capability that was built, an in-scope
  requirement with nothing to point at, or an assumption the code now treats
  as a setting. Use when the user asks whether the code still matches the
  pack. For a style review, use review-diff. For a bug, use diagnose.
  Invoke with /spec-drift.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator. Needs a project-foundation pack and the project code.
icon: git-branch
color: orange
---

# Spec drift

A missing abstraction is not drift. Drift is a promise the pack already wrote down, broken or abandoned in the code.

Write `docs/foundation/11-drift.md`. Product code changes in this turn only when the user asked you to fix the drift.

## Do this

1. If `docs/foundation/01-prd.md` is missing, say to run `/project-foundation` and stop.
2. Read scope in the PRD, the decisions in `05-system-design.md`, Do not build in `07-mvp-slice.md`, the assumptions in `08-risks.md`, and the routes in `04-sitemap.md`.
3. Search the project for product code: pages, handlers, components, models, and the dependency manifest. Ignore `docs/foundation/`, `examples/`, `node_modules/`, `vendor/`, `dist/`, and `.git/`.
4. Read `references/finding.md`. Record a finding only when it is a contradiction, a gap, or a hardened assumption. The step is done when every finding is one of the three kinds in What counts.
5. If the repo has no product code yet, write exactly one gap for the whole MVP.
6. Run, and fix the file until it prints `drift report is valid`:

```bash
python3 scripts/validate_drift.py <project-root>/docs/foundation/11-drift.md
```

7. Reply with the verdict and the one finding to deal with first. If the verdict is clear, say that and stop. The file stays in the repo.

## What counts

- **Contradiction.** The code implements something marked `later`, `out`, `cut`, or Do not build. Or the dependency manifest, auth, or storage disagrees with the Decisions table.
- **Gap.** An `in` requirement has no route, action, or test a reader can open. No product code at all is a single gap, with code `No product code yet.`
- **Hardened.** An `[assumption]` now has a setting, screen, or column that lets someone change it as if the pack had decided it was a feature.

## What does not count

Formatting, names, comments, folder layout, test coverage percentages, and ideas the pack never mentioned.

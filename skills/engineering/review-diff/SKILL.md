---
name: review-diff
description: >
  Reviews the diff since a fixed point. Runs the pack validators and the
  project's checks first, then judges Standards and Spec separately against
  the current chunk, and writes docs/reviews/ with a ship or fix verdict.
  Use when the user asks to review a branch, a PR, or the changes since a
  ref, or before closing a one-chunk beat. Invoke with /review-diff.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validators. Needs git. Reads a project-foundation pack when one exists.
icon: eye
color: red
---

# Review diff

Run the machines before the judgement. A typecheck failure is a fact. A smell is an opinion. The file keeps them apart.

Write `docs/reviews/<YYYY-MM-DD>-<short-ref>.md` in the product repo.

## Do this

1. Pin the fixed point. Use the ref the user gave. If they gave none, use the merge-base with the default branch and say so. Run `git rev-parse <ref>`, `git diff --name-only <ref>...HEAD`, and `git log <ref>..HEAD --oneline`. If the ref does not resolve or the diff is empty, say so and stop.
2. Run the deterministic pass. Read `references/review.md` for which pack validator each touched path needs. Run each one from the sibling skill folders, such as `../state-shell/scripts/validate_shell.py <product-root>/src/features/<screen>`. Run `git diff --check <ref>...HEAD`. Read `package.json` `scripts` and run `typecheck`, `lint`, and `test` when they exist, with the package manager the lockfile names. Record every command and its `pass` or `fail`.
3. Gather the Standards sources: `.cursor/rules/craft.mdc`, `CLAUDE.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, and any coding standards file the repo has. Read `references/smells.md`.
4. Gather the Spec sources: `docs/foundation/12-chunk.md` for the beat, Done when, and Not in this chunk, and the FR ids that its Build step names in `docs/foundation/01-prd.md`. With no pack, use an issue number from the commit messages or a spec path the user gave. With none of these, Spec is `No spec available.`
5. Review the two axes in parallel subagents when the host has them. Otherwise review Standards, write it, then review Spec. Give each axis the diff command, the commit list, the failing checks, and only its own sources. Paste `references/smells.md` into the Standards brief.
   - **Standards.** Every place the diff breaks a documented rule, cited by file and rule. Then any baseline smell in the diff. Repo rules override the baseline. Skip what the checks already caught.
   - **Spec.** This axis is diff-scoped. Report Done when lines the diff leaves unmet, acceptance lines it contradicts, and scope creep: code for the next beat, a later build step, or anything under Not in this chunk. Quote the line. When a finding is pack-level drift, such as a `later` FR built anywhere in the repo, write it once and point to `/spec-drift`.
6. Write the review with the headings in `references/review.md`. Copy each axis's findings under its own heading. The verdict is `fix` when a check failed or a finding is `[hard]`. Otherwise it is `ship`.
7. Run:

```bash
python3 scripts/validate_review.py <product-root>/docs/reviews/<YYYY-MM-DD>-<short-ref>.md
```

Fix the file until it passes.

8. Reply with the verdict, the failing checks, and the worst finding in each axis. Pick no winner across axes. Do not paste the file.

## Hard guardrails

- Leave product code unchanged in this turn. The fixes are the next turn's beat.
- Do not open `examples/` and copy them into the review.

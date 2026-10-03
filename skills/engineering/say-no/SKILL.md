---
name: say-no
description: >
  Say no: writes the exact refusal for every capability the foundation pack
  excluded, in the words a person would hear if they asked for it. Use when
  the user asks for the refusals, or when someone asks for a feature the pack
  marked later, out, or do-not-build. Needs docs/foundation. Invoke with
  /say-no.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator. Needs a project-foundation pack.
icon: shield
color: red
---

# Say no

The pack already lists what not to build. This skill writes the sentence that says no, naming the thing the product does instead.

Write `docs/foundation/10-refusals.md`. This turn writes the refusal and leaves the capability out of the MVP. Other pack files change only when the user explicitly said to update the spec.

## Do this

1. Read `00-brief.md` non-goals, `01-prd.md` Out and Later, `07-mvp-slice.md` Do not build, and `05-system-design.md` Not designed yet. If those files are missing, say to run `/project-foundation` and stop.
2. One refusal per capability. Photos mentioned in three files are one refusal, not three. The step is done when each excluded capability appears exactly once.
3. If the user just asked for a capability, put it first as `## Asked now` with `Verdict: refuse` or `Verdict: change the pack`. Default is refuse. A `change the pack` verdict edits nothing by itself.
4. Read `references/refusal.md` and write the file.
5. Each refusal names a screen or an `FR-` id from this pack, so it could not be said about any other product.
6. Run, and fix the file until it prints `refusals are valid`:

```bash
python3 scripts/validate_refusals.py <project-root>/docs/foundation/10-refusals.md
```

7. Reply with the asked-now verdict when there is one. Otherwise reply with how many refusals you wrote and the sentence for the request nearest to the MVP. The file stays in the repo.

## Guardrails

- State the no plainly, then what the product does instead. Never apologize or write "unfortunately", "at this time", or "we value".
- Never open `examples/`. Write from this product's pack.

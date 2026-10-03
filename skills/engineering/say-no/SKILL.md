---
name: say-no
description: >
  Writes the exact refusal for every capability the foundation pack excluded,
  in the words a person would hear if they asked for it. Use when the user
  says "what do we say no to", "write the refusals", "they asked for",
  "the stakeholder wants", "scope creep", "don't build that", or names a
  feature the pack marked later, out, or do-not-build. Use after
  docs/foundation exists. Invoke with /say-no.
compatibility: Cursor, Claude Code, and claude.ai. Python 3 runs the validator. Needs a project-foundation pack.
icon: shield
color: red
---

# Say no

The pack already lists what not to build. This skill writes the sentence that says no, naming the thing the product does instead.

Write `docs/foundation/10-refusals.md`. Do not implement the request. Do not change other pack files unless the user explicitly said to update the spec.

## Do this

1. Read `00-brief.md` non-goals, `01-prd.md` Out and Later, `07-mvp-slice.md` Do not build, and `05-system-design.md` Not designed yet. If those files are missing, say to run `/project-foundation` and stop.
2. One refusal per capability. Photos mentioned in three files are one refusal, not three.
3. If the user just asked for a capability, put it first as `## Asked now` with `Verdict: refuse` or `Verdict: change the pack`. Default is refuse. `change the pack` does not edit the pack in this turn unless they also asked for the spec update.
4. Read `references/refusal.md` and write the file.
5. A refusal that could be said about any product is a failed line. Name a screen or an `FR-` id from this pack.
6. Run:

```bash
python3 scripts/validate_refusals.py <project-root>/docs/foundation/10-refusals.md
```

7. Reply with the asked-now verdict when there is one. Otherwise reply with how many refusals you wrote and the sentence for the request nearest to the MVP. Do not paste the file.

## Do not

- Do not apologize, and do not write "at this time" or "we value".
- Do not add the excluded capability to the MVP.
- Do not open `examples/`.

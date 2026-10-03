# Invocation

Every `SKILL.md` under `skills/engineering/` is model-invoked. The model may reach for it when the description matches, and a person may still type the slash command.

This repo does not set `disable-model-invocation`. A new project, a contract beat, or a drift question should be able to pick the skill up without a memorized command.

`one-chunk` is the session that builds. On a `contract` beat it follows `lock-contracts`. On a `shell` beat it follows `state-shell`. Those two stay separate skills so a turn that only needs types, or only a screen, can run them alone.

Do not call another skill by a relative path into its folder. Name the skill and follow its `SKILL.md`.

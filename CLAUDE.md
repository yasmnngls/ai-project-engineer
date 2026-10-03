# AI Project Engineer

Skills live in bucket folders under `skills/`:

- `engineering/`: the promoted set. Every skill here is listed in the top-level `README.md`, in `skills/engineering/README.md`, in `.claude-plugin/plugin.json`, and as a page under `docs/engineering/`.

This repository is a skill marketplace, not a product app. Before adding or renaming a skill, a validator, a manifest, or an example, read `ARCHITECTURE.md`. Update `ARCHITECTURE.md` in the same turn when that structure changes.

Do not add a product UI here. In a product repo, the installed skills require Zod contracts before UI, presentational components that only receive props, and one build beat per turn.

Install commands in `README.md` match this layout: Claude Code installs the plugin from this repo, and `npx skills add yasmnngls/ai-project-engineer` copies the skill folders. See `.agents/invocation.md` for how a skill is reached.

Each skill entry in `README.md` links the skill name to its `SKILL.md`.

To relink every engineering skill into `~/.claude/skills`, `~/.agents/skills`, and `~/.cursor/skills`, run `scripts/link-skills.sh`.

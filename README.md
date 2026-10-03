# AI Project Engineer

Skills for the start of a product, and for the beats after it. `project-foundation` writes the pack an engineer builds from: a brief, PRD, personas, user journeys, sitemap, system design, data model and API, MVP slice, and risks. The later skills keep that pack coherent: a living architecture file, Zod contracts before UI, one presentational screen, one verifiable chunk, kill tests, refusal lines, and a spec-drift check.

They are small and composable. Hack on them. The files in your project are yours.

Two ways in. The Claude Code plugin installs the set as a bundle. `npx skills` copies the skill folders into your project so you can edit them. Installing both leaves you with every skill twice.

## Install

### Claude Code

```text
/plugin marketplace add yasmnngls/ai-project-engineer
/plugin install ai-project-engineer@ai-project-engineer
/reload-plugins
```

The catalog is `.claude-plugin/marketplace.json`. A skill command is `/ai-project-engineer:<skill-name>`.

From a local checkout:

```text
/plugin marketplace add ./path-to-this-repo
/plugin install ai-project-engineer@ai-project-engineer
```

### Cursor, Codex, and other agents

```bash
npx skills@latest add yasmnngls/ai-project-engineer
```

Pick the skills you want. After that, `/project-foundation` and the other names work without the plugin prefix.

Cursor can also add `https://github.com/yasmnngls/ai-project-engineer` as a marketplace and install **AI Project Engineer**. The catalog is `.cursor-plugin/marketplace.json`.

### claude.ai

Package one zip per skill, then upload each zip under Customize, Skills. Code execution has to be on, because each skill runs a Python check.

```bash
python3 scripts/package_claude_skill.py
```

That writes `dist/<skill-name>.zip`. The zip root is the skill folder, with `SKILL.md` inside it. claude.ai skills stay on claude.ai. They do not sync to Claude Code or Cursor.

### Maintainers of this repo

```bash
bash scripts/link-skills.sh
```

That symlinks `skills/engineering/*` into `~/.claude/skills`, `~/.agents/skills`, and `~/.cursor/skills`.

## Use it

Open the product repo and describe the job:

```text
/project-foundation
Field technicians need a phone page to record a site visit before they drive away. The office reads submitted visits. First version has no accounts.
```

If the user and the job are already named, the skill writes `docs/foundation/` in that turn. If either is missing, it asks once and waits.

| File | What it decides |
| --- | --- |
| `README.md` | Index for the next session |
| `00-brief.md` | Problem, user, promise, MVP, non-goals |
| `01-prd.md` | Numbered requirements and acceptance |
| `02-personas.md` | The people those requirements name |
| `03-user-journeys.md` | Success, first run, and one recovery |
| `04-sitemap.md` | Routes, empty states, and errors |
| `05-system-design.md` | Containers and the critical sequence |
| `06-data-and-api.md` | Entities and the calls the MVP makes |
| `07-mvp-slice.md` | Build order for the next session |
| `08-risks.md` | Assumptions, risks, and at most seven open questions |

Facts the user stated, facts read from the repo, and choices the skill made are tagged `[stated]`, `[inferred]`, and `[assumption]`.

Build in beats after that. A session that tries to ship a whole feature goes back to the current beat.

## Reference

These skills live in `skills/engineering/`. Each one is model-invoked: you can type it, and the model can reach for it when the task fits. Human-facing pages are under `docs/engineering/`.

- **[project-foundation](./skills/engineering/project-foundation/SKILL.md)**: Writes the ten-file foundation pack before any product code.
- **[architecture-memory](./skills/engineering/architecture-memory/SKILL.md)**: Writes `ARCHITECTURE.md` and the craft rules the next session reads.
- **[one-chunk](./skills/engineering/one-chunk/SKILL.md)**: Implements one beat of the MVP: contract, shell, or wire.
- **[lock-contracts](./skills/engineering/lock-contracts/SKILL.md)**: Writes Zod schemas and discriminated results before UI.
- **[state-shell](./skills/engineering/state-shell/SKILL.md)**: Builds one screen as a state union plus a presentational view.
- **[assumption-trial](./skills/engineering/assumption-trial/SKILL.md)**: Writes a kill test for each load-bearing assumption.
- **[say-no](./skills/engineering/say-no/SKILL.md)**: Writes the refusal for each excluded capability.
- **[spec-drift](./skills/engineering/spec-drift/SKILL.md)**: Compares the code to the pack and reports contradictions, gaps, and hardened assumptions.

The order once a product repo exists:

1. `project-foundation` writes `docs/foundation/`.
2. `architecture-memory` writes `ARCHITECTURE.md`.
3. `one-chunk` performs a single beat.
4. On a `contract` beat, `lock-contracts` writes the schemas.
5. On a `shell` beat, `state-shell` writes the state model and the view.
6. On a `wire` beat, connect the shell to the contracts and add one test of what the user sees.

`assumption-trial`, `say-no`, and `spec-drift` read the pack. They do not replace steps 3 to 6.

## Check a pack

```bash
python3 skills/engineering/project-foundation/scripts/validate_foundation.py docs/foundation
```

`examples/field-notes` is a finished pack for a site-visit log. It exists so the validator has a known-good fixture. The skill is instructed not to copy it into a new project.

```bash
python3 skills/engineering/project-foundation/scripts/validate_foundation.py examples/field-notes
python3 skills/engineering/assumption-trial/scripts/validate_trials.py examples/field-notes/09-assumption-trials.md
python3 skills/engineering/say-no/scripts/validate_refusals.py examples/field-notes/10-refusals.md
python3 skills/engineering/spec-drift/scripts/validate_drift.py examples/drift-found/11-drift.md
python3 skills/engineering/architecture-memory/scripts/validate_architecture.py ARCHITECTURE.md
python3 skills/engineering/lock-contracts/scripts/validate_contracts.py examples/site-log/src/contracts
python3 skills/engineering/state-shell/scripts/validate_shell.py examples/site-log/src/features/visit
python3 skills/engineering/one-chunk/scripts/validate_chunk.py examples/chunk/12-chunk.md
```

## Layout

```text
.claude-plugin/          Claude Code plugin and marketplace
.cursor-plugin/          Cursor marketplace
skills/engineering/      one folder per skill
docs/engineering/        human-facing page per skill
examples/                validator fixtures, not templates
rules/craft.mdc          constraints for product TypeScript
scripts/link-skills.sh   symlink skills into local harnesses
```

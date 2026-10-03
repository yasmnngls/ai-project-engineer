# Diagnosis file

`docs/bugs/<slug>.md` in the product repo.

````markdown
# Diagnosis

## Symptom

{The user's exact words, or the exact error message. Quoted, not paraphrased.}

## Loop

```bash
{one command}
```

```text
{The red output you observed. Secrets written as <REDACTED>.}
```

{One sentence: why this output is the user's symptom.}

## Minimised

{What is left. Every remaining element turns the loop green when removed.}

- Cut: {an input, caller, config, or step that was not load-bearing}

## Hypotheses

1. If {cause}, then {one change} turns the loop green. [confirmed]
2. If {cause}, then {one change} turns the loop green. [ruled out]
3. If {cause}, then {one change} makes it worse. [untested]

## Probes

- H2: {the one variable changed}. {what the loop did}.
- H1: {the one variable changed}. {what the loop did}.

## Cause

{The confirmed mechanism, in the code's terms.}

## Fix

{What changed, in which file.}

```bash
{the same command as ## Loop}
{its green output}
```

## Regression test

`src/contracts/visit.test.ts`

{One line: it went red before the fix and green after.}

## Cleanup

Searched for `[DEBUG-7c1e]` with `rg -F "[DEBUG-7c1e]"`. It returned nothing.

## Prevention

{What would have caught this earlier. An architecture change names the module.}
````

Rules the validator checks:

- The first line is `# Diagnosis`. Every heading is present, non-empty, and in this order.
- `## Loop` has at least two fenced blocks. The first holds exactly one non-blank line: the command. The second holds the red output.
- `## Hypotheses` has three to five numbered items. Each contains `If` and `then`, and ends with exactly one of `[confirmed]`, `[ruled out]`, or `[untested]`. Exactly one is `[confirmed]`.
- `## Probes` is a bullet list. Each bullet starts with `H{n}:` for a hypothesis that exists. The confirmed hypothesis has at least one probe.
- `## Fix` has a fenced block that contains the `## Loop` command, unchanged.
- `## Regression test` starts with a backticked path, or with `No correct seam:` and a reason. A path to `src/contracts/` needs the word `safeParse` in the section. A path needs the words `red` and `green`.
- `## Cleanup` names a `[DEBUG-xxxx]` tag and says the search returned nothing, empty, or no matches. Or it is the line `No debug logs added.`
- The file has no unredacted secret: `Bearer` tokens, cookie values, `sk-` keys, GitHub and AWS keys, Slack tokens, or `password`, `passphrase`, `secret`, `token`, and `api_key` assignments. A value of `<REDACTED>` or an environment variable such as `$TOKEN` passes.

With `--root <product-root>`, it also checks:

- The regression test path exists under the root.
- No source file under the root contains `[DEBUG-`. It skips `.git`, `node_modules`, `dist`, `build`, `.next`, `coverage`, `docs`, and `examples`, unless the root is itself inside `examples`.
- If `PROJECT-STATE.md` exists at the root, its `## Known issues` does not name this file.

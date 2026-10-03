# ship-gate

## What it does

Gates a release before it deploys. It runs every check the project defines, proves each shipped requirement with a test or route, lists env var names, one rollback step, and what is not in the release. It writes `docs/releases/<version>.md` with the verdict `ship` or `hold`, then updates `PROJECT-STATE.md`.

## When to reach for it

Someone says to ship, cut a release, tag a version, or asks whether the build is ready to deploy.

## Common questions

**Does it deploy?** Only when you asked for the deploy and the verdict is `ship`. Otherwise it reports the gate and stops.

**What if one check fails?** The verdict is `hold`, and the failing command goes under Known issues in `PROJECT-STATE.md`.

**Can a `later` requirement ship?** No. The validator fails when a shipped FR is `later`, `out`, or `cut` in the PRD, or sits in Do not build.

**Where do secrets go?** Nowhere in the release file. `## Env` lists names like `TEAM_PASSPHRASE`, and the validator rejects anything that looks like a value.

## It's working if

The reply names the version, the verdict, and the rollback step or the first failing check. Every shipped FR points at a file you can open.

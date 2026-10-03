# Writing rules

Write the pack so a later agent session can build the MVP without asking what the product is.

## Ask gate

These four facts matter:

1. Primary user
2. Job they are finishing
3. What the first version must make true
4. A hard constraint, if one exists (platform, stack, compliance, offline)

Ask only when fact 1 or fact 2 is missing, and the user did not say to assume, proceed, or draft it.

If you ask: one message, the missing facts only, then stop. No outline, no partial pack.

If both the user and the job are known, write the pack now. Unknown constraints become labeled assumptions. Do not stop to offer stack options.

## Provenance

Tag any sentence that is a decision or a fact about the user, scope, or stack:

- `[stated]` — the user said it in this conversation
- `[inferred]` — it is already true in the repo
- `[assumption]` — you chose it so the pack could be finished

Every `[assumption]` that changes the user, scope, data, or stack must also appear in `08-risks.md`.

## Voice

- Use concrete nouns from this product. Name the person and the object they change.
- Requirements are testable. "Works well" is not acceptance.
- Numbers are either stated by the user or marked `[assumption]`.
- Pick one stack when the repo and the user have not. Record it once. Do not list alternatives.
- Do not add accounts, billing, admin, notifications, native apps, or a second service unless a requirement needs them. If you include one, the PRD says why.
- Open questions are only decisions that would change the MVP. Cap them at 7. Everything else is an assumption or out of scope.
- No placeholder words (`TODO`, `TBD`), no lorem, no "seamless", no "delightful".

## Closeout

After the validator passes, reply in four lines:

1. Product in one sentence.
2. MVP in one sentence.
3. `docs/foundation/` and that the validator passed.
4. The first numbered step from `07-mvp-slice.md`.

Then stop.

# Drift

## Verdict

drift

## Findings

### D1 Photo control on the visit

- Kind: contradiction
- Spec: FR-007 is later, and 07-mvp-slice.md says not to build photo attachments.
- Code: app/visits/photo-button.tsx
- What to do: Remove the control, or move FR-007 to in and update the pack before keeping it.

### D2 Passphrase is now a setting

- Kind: hardened
- Spec: 08-risks.md assumes one passphrase for the whole deployment.
- Code: app/settings/passphrase-form.tsx
- What to do: Remove the settings screen, or change the assumption and FR-006 before shipping it.

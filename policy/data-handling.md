# Data Handling

- Collect only what is needed.
- Prefer hashes, identifiers, counts and redacted samples over full sensitive records.
- Never commit credentials, session tokens, API keys, private keys, raw cookies, customer records or forensic images to this repository.
- Use a secrets manager or encrypted evidence store for sensitive material.
- Maintain chain-of-custody where evidence could be used in legal/HR/regulatory processes.
- Record timezone and clock source for incident evidence.
- Apply retention and deletion requirements from the engagement/incident plan.
- Sanitise examples before sharing with an AI service that is not approved for the data classification.

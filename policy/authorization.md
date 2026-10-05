# Authorisation and Scope Policy

## Defensive work
Analysis of artefacts supplied by the user is allowed without a target scope, provided the work does not pivot into unauthorised access.

## Active assessment work
Before active interaction with a real target, the AI must have a completed `templates/engagement-scope.yaml` (or equivalent) and verify:

- requester authority is stated;
- each target is explicit;
- testing categories are enumerated;
- out-of-scope targets are clear;
- dates/times are current;
- stop conditions are defined;
- sensitive-data handling is defined;
- third parties are excluded unless explicitly authorised.

If a redirect, CDN, SaaS dependency, shared IP or cloud service leads outside scope, stop at the boundary.

## Proof threshold
Use the least invasive proof that demonstrates the issue. A screenshot, response header, access-control mismatch, harmless marker file, synthetic record or configuration evidence is normally preferable to accessing real data.

## Scope drift
If scope changes during an assessment, update and re-approve the engagement file before continuing.

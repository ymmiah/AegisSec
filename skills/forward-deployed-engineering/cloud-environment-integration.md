# Cloud Environment Integration

**Skill ID:** `fde-cloud-environment-integration`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-CSF, CIS-v8.1, Zero-Trust

## Outcomes

- Deploy or integrate security capabilities safely across AWS, Azure or GCP
- Use cloud-native identity, networking, logging and secret management
- Avoid broad standing privileges

## Method

1. Confirm account/subscription/project boundaries and regions.
2. Map deployment identity and least-privilege permissions.
3. Review network egress/ingress, private connectivity and service endpoints.
4. Use managed secret/key services and avoid static credentials.
5. Enable required audit and operational telemetry.
6. Validate with a pilot scope before wider rollout.

## Safety / quality guardrails

- Cloud credentials do not prove authorisation; require defined customer scope.
- Avoid organisation-wide policy changes unless explicitly approved.
- Do not expose management interfaces or data stores publicly for convenience.

## Output format

Return: `cloud scope → identity → network → data/secrets → deployment plan → telemetry → pilot validation → rollout/rollback`.

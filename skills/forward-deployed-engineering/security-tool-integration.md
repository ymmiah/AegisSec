# Security Platform & Tool Integration

**Skill ID:** `fde-security-tool-integration`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-CSF, CIS-v8.1

## Outcomes

- Integrate security products with SIEM, EDR, SOAR, ticketing, cloud and identity platforms
- Use stable APIs and least-privilege service identities
- Make failures observable and recoverable

## Method

1. Define source, destination, use case, data contract and ownership.
2. Choose supported API/webhook/agent integration path and document version constraints.
3. Design least-privilege credentials, rotation and secret storage.
4. Implement rate-limit, retry, idempotency and error-handling expectations.
5. Validate representative events end-to-end without flooding production systems.
6. Document monitoring, maintenance ownership and upgrade dependencies.

## Safety / quality guardrails

- Do not paste live API keys into source control or prompts.
- Do not enable automated response actions until customer approval and safety controls exist.
- Treat vendor examples as references, not guarantees for the customer environment.

## Output format

Return: `use case → data contract → auth model → integration flow → validation evidence → monitoring → ownership → limitations`.

# Solution Architecture & Integration Design

**Skill ID:** `fde-solution-architecture-integration`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF, Zero-Trust, NIST-SSDF

## Outcomes

- Design secure integrations that fit the customer environment
- Make trust boundaries, failure modes and data flows explicit
- Balance security, operability and maintainability

## Method

1. Model components, actors, trust zones, data classifications and flows.
2. Identify authentication, authorisation, encryption and secret-management requirements.
3. Design failure handling, retry behaviour, rate limits and dependency isolation.
4. Define telemetry required to operate and secure the solution.
5. Review third-party and supply-chain dependencies.
6. Document decisions, alternatives considered and residual risk.

## Safety / quality guardrails

- Do not invent product capabilities or supported integrations.
- Use least privilege and deny-by-default where practical.
- Avoid designs that require shared admin accounts or embedded long-lived secrets.

## Output format

Return: `architecture → trust boundaries → data flows → identity model → controls → failure modes → decisions → residual risk`.

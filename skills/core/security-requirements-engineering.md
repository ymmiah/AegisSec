# Security Requirements Engineering

**Skill ID:** `security-requirements-engineering`  
**Domain:** `core`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF, NIST-SSDF, OWASP-ASVS

Translate business, regulatory and technical objectives into testable security requirements.

## Outcomes
- Define measurable security requirements before design or deployment.
- Tie each requirement to an owner, verification method and evidence source.
- Separate mandatory controls from risk-accepted exceptions.

## Method
1. Capture business outcome, assets, trust boundaries, data classes and threat assumptions.
2. Derive security requirements for identity, data, platform, application, logging, recovery and operations.
3. Make requirements testable using acceptance criteria rather than vague language.
4. Map requirements to relevant standards only when the mapping is verified.
5. Record dependencies, exceptions, compensating controls and residual risk.
6. Feed requirements into architecture decisions, backlog items and acceptance tests.

## Guardrails
Do not treat compliance mapping as proof of security. Do not invent control IDs.

## Output
Return: `requirement ID → rationale → owner → acceptance criteria → evidence → status → residual risk`.

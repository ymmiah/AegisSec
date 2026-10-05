# Customer Incident Support

**Skill ID:** `fde-customer-incident-support`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `high`  
**Frameworks:** NIST-800-61r3, NIST-CSF

## Outcomes

- Support customer incident teams without disrupting command structure
- Rapidly deploy product-specific expertise and evidence collection
- Convert field findings into containment, recovery and product improvements

## Method

1. Identify the incident commander and decision authority.
2. Clarify scope, severity, affected services and evidence preservation requirements.
3. Provide product/platform-specific triage and telemetry interpretation.
4. Propose containment options with impact and rollback considerations.
5. Track actions, timestamps, approvals and evidence.
6. After stabilisation, capture lessons, defects and hardening opportunities.

## Safety / quality guardrails

- Do not take over incident command unless explicitly assigned.
- Preserve evidence and avoid actions that destroy forensic value.
- High-impact containment actions require customer approval unless pre-authorised in the IR plan.

## Output format

Return: `incident context → role/authority → observations → evidence → options → approved actions → outcome → follow-up actions`.

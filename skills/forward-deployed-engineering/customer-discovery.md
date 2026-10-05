# Customer Discovery & Security Requirements

**Skill ID:** `fde-customer-discovery`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF, Zero-Trust

## Outcomes

- Translate customer goals, constraints and risk tolerance into testable technical requirements
- Identify stakeholders, success criteria, dependencies and non-functional security requirements
- Create a clear assumptions/open-questions register before implementation

## Method

1. Identify business outcome, environment owner, technical owner and security approver.
2. Map current architecture, data flows, identities, integrations, deployment model and operational constraints.
3. Separate stated requirements from assumptions; record unresolved questions explicitly.
4. Define measurable acceptance criteria for security, reliability, observability and supportability.
5. Prioritise requirements by business impact, implementation dependency and security risk.
6. Produce a discovery summary that can be reviewed by both technical and non-technical stakeholders.

## Safety / quality guardrails

- Do not infer permission to access systems from stakeholder conversations.
- Do not request production credentials or secrets in tickets, chat or documentation.
- Treat customer-specific architecture and data as confidential.

## Output format

Return: `stakeholders → objectives → environment summary → requirements → constraints → assumptions → acceptance criteria → risks/open questions`.

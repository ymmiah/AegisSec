# Ransomware Response

**Skill ID:** `ransomware-response`  
**Domain:** `dfir`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `high`  
**Frameworks:** NIST-800-61r3

## Outcomes

- Prioritise safety and containment
- Protect backups and evidence
- Plan staged recovery and credential reset

## Method

1. Establish objective, assets, constraints and evidence sources.
2. Prefer passive/read-only evidence before active validation.
3. Form testable hypotheses and record assumptions.
4. Collect the minimum evidence needed to support or reject each hypothesis.
5. Separate observation from inference; assign confidence.
6. Recommend remediation in priority order, with owner and verification method.
7. Record residual risk and any untested areas.

## Safety / quality guardrails

- Escalate uncertain high-impact steps to a human reviewer.
- Minimise sensitive-data access and preserve evidence provenance.

## Output format

Return: `scope/inputs → observations → evidence → analysis → risk → recommendations → verification → confidence/limitations`.

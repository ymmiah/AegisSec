# NIST CSF 2.0 Programme Mapping

**Skill ID:** `nist-csf`  
**Domain:** `governance`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF-2.0

## Outcomes

- Build current/target profiles
- Map evidence to outcomes
- Turn gaps into prioritised actions

## Method

1. Establish objective, assets, constraints and evidence sources.
2. Prefer passive/read-only evidence before active validation.
3. Form testable hypotheses and record assumptions.
4. Collect the minimum evidence needed to support or reject each hypothesis.
5. Separate observation from inference; assign confidence.
6. Recommend remediation in priority order, with owner and verification method.
7. Record residual risk and any untested areas.

## Safety / quality guardrails

- Use least privilege and evidence-based conclusions.
- Do not invent facts, controls or successful outcomes.

## Output format

Return: `scope/inputs → observations → evidence → analysis → risk → recommendations → verification → confidence/limitations`.

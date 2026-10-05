# GCP Security Review

**Skill ID:** `gcp-security`  
**Domain:** `cloud`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** CIS, NIST-CSF

## Outcomes

- Review IAM and org policies
- Assess service exposure and keys
- Validate logging and security controls

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

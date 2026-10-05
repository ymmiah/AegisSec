# Web Application Security Testing

**Skill ID:** `web-security-testing`  
**Domain:** `red-team`  
**Default mode:** `ASSESSMENT`  
**Operational risk:** `medium`  
**Frameworks:** OWASP-Top10-2025, ASVS-5.0

## Outcomes

- Test access control, input handling and security configuration
- Use benign proofs
- Map verified findings to remediation

## Method

1. Establish objective, assets, constraints and evidence sources.
2. Prefer passive/read-only evidence before active validation.
3. Form testable hypotheses and record assumptions.
4. Collect the minimum evidence needed to support or reject each hypothesis.
5. Separate observation from inference; assign confidence.
6. Recommend remediation in priority order, with owner and verification method.
7. Record residual risk and any untested areas.

## Safety / quality guardrails

- Require a valid engagement scope before active target interaction.
- Use rate-limited, non-destructive validation and stop after sufficient proof.
- Escalate uncertain high-impact steps to a human reviewer.
- Minimise sensitive-data access and preserve evidence provenance.

## Output format

Return: `scope/inputs → observations → evidence → analysis → risk → recommendations → verification → confidence/limitations`.

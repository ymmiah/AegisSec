# Applied Cryptography Review

**Skill ID:** `cryptography-review`  
**Domain:** `appsec`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** ASVS-5.0, NIST

## Outcomes

- Review algorithm/mode/key lifecycle choices
- Identify custom-crypto risks
- Recommend proven libraries and rotation

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

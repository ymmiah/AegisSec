# Kubernetes Security

**Skill ID:** `kubernetes-security`  
**Domain:** `devsecops`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** CIS, NIST-CSF

## Outcomes

- Review RBAC, admission, network policies and secrets
- Minimise pod privileges
- Secure control plane and audit logs

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

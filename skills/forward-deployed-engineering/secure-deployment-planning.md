# Secure Deployment Planning

**Skill ID:** `fde-secure-deployment-planning`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-SSDF, CIS-v8.1

## Outcomes

- Create a safe, reversible production deployment plan
- Build security checks and human approval into release execution
- Minimise blast radius and downtime

## Method

1. Define target state, components, dependencies and change boundary.
2. Break deployment into reversible stages with pre-checks and post-checks.
3. Specify least-privilege execution identities and secret handling.
4. Define backup/snapshot, rollback, abort thresholds and communications.
5. Plan canary/pilot rollout where feasible.
6. Require explicit approval before state-changing production steps.

## Safety / quality guardrails

- Never treat a deployment plan as authorisation to execute it.
- Do not disable security controls merely to make a deployment succeed.
- Stop when rollback criteria or customer stop conditions are met.

## Output format

Return: `target state → prerequisites → staged plan → approvals → validation → rollback → communications → residual risk`.

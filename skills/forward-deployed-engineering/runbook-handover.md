# Runbook, Handover & Customer Enablement

**Skill ID:** `fde-runbook-handover`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF

## Outcomes

- Transfer operational ownership cleanly
- Ensure customer teams can operate, troubleshoot and secure the deployment
- Reduce dependency on undocumented field knowledge

## Method

1. Document architecture, owners, dependencies and support boundaries.
2. Create normal-operation, failure, escalation, backup/restore and rollback procedures.
3. Document key dashboards, alerts and health checks.
4. Provide role-based enablement for administrators, SOC, engineering and support.
5. Verify the customer can perform critical tasks independently.
6. Record open risks, technical debt and future maintenance actions.

## Safety / quality guardrails

- Remove or redact secrets from all handover material.
- Do not claim handover complete while critical ownership is unresolved.
- Keep customer-specific documentation in approved storage only.

## Output format

Return: `system summary → ownership → runbooks → dashboards/alerts → troubleshooting → escalation → training evidence → open actions`.

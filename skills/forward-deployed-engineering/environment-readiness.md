# Environment Readiness Assessment

**Skill ID:** `fde-environment-readiness`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF, CIS-v8.1

## Outcomes

- Assess whether an environment is ready for secure deployment
- Identify missing prerequisites before implementation begins
- Reduce failed deployments caused by identity, network, logging or change-control gaps

## Method

1. Inventory required accounts, roles, network paths, DNS, certificates, APIs, data sources and destinations.
2. Confirm supported platform versions and deployment constraints.
3. Check least-privilege access design and secret-storage approach.
4. Confirm logging, backup, rollback, health-check and monitoring prerequisites.
5. Identify organisational prerequisites such as CAB/change windows and incident contacts.
6. Return a readiness decision: ready, ready-with-actions, or blocked.

## Safety / quality guardrails

- Prefer read-only checks.
- Do not create accounts, firewall rules or production resources without approved change authority.
- Clearly distinguish hard blockers from recommendations.

## Output format

Return: `scope → prerequisite matrix → evidence → blockers → required actions → readiness decision → owner/date`.

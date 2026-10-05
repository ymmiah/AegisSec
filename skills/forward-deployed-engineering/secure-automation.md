# Secure Automation & Orchestration

**Skill ID:** `fde-secure-automation`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-SSDF, CIS-v8.1

## Outcomes

- Automate repetitive field engineering tasks safely
- Build idempotent, observable and reversible workflows
- Prevent automation from silently expanding privileges or blast radius

## Method

1. Define the manual workflow, inputs, outputs and failure states before automating.
2. Use scoped service identities and central secret management.
3. Make operations idempotent where possible and add dry-run/plan modes.
4. Add structured logs, audit context, timeout, retry and rate limiting.
5. Require approval gates for production state changes or security-response actions.
6. Test in non-production and document rollback plus ownership.

## Safety / quality guardrails

- Never hard-code customer secrets.
- Do not automate destructive or high-impact actions without explicit human approval.
- Fail closed when scope, identity or target selection is ambiguous.

## Output format

Return: `workflow → trust model → automation design → safeguards → test results → approval gates → rollback → operating runbook`.

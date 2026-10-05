# Production Troubleshooting & Root-Cause Analysis

**Skill ID:** `fde-production-troubleshooting`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-CSF

## Outcomes

- Restore service safely while preserving evidence
- Distinguish symptoms from root cause
- Produce a reproducible fix and prevention plan

## Method

1. Confirm impact, timeline, scope and recent changes.
2. Collect low-impact evidence: health checks, logs, metrics, configuration and dependency status.
3. Form and rank hypotheses; test the least invasive first.
4. Use controlled changes with owner approval and rollback.
5. Validate recovery against agreed success criteria.
6. Document root cause, contributing factors and preventive actions.

## Safety / quality guardrails

- Do not make untracked emergency changes.
- Preserve relevant evidence when the issue may be a security incident.
- Escalate to incident response when compromise is plausible.

## Output format

Return: `impact → timeline → evidence → hypotheses → tests → root cause → fix → verification → prevention actions`.

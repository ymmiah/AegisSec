# Change, Release & Rollback Management

**Skill ID:** `fde-change-release-management`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-SSDF, NIST-CSF

## Outcomes

- Deliver controlled changes into customer environments
- Make every production change attributable, reviewable and reversible
- Reduce deployment-related outages and security regressions

## Method

1. Define change owner, approver, window, affected assets and dependencies.
2. Document pre-change validation and backup/snapshot state.
3. Separate implementation steps from verification steps.
4. Specify rollback trigger, rollback procedure and maximum tolerated impact.
5. Capture actual execution timestamps and deviations.
6. Close with verification evidence and post-change monitoring.

## Safety / quality guardrails

- No production change without customer-authorised change path.
- Avoid bundling unrelated changes into one release.
- Do not proceed when rollback is impossible unless risk is explicitly accepted.

## Output format

Return: `change record → approvals → pre-checks → implementation → verification → rollback → monitoring → closure evidence`.

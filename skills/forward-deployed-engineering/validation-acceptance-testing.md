# Validation & Acceptance Testing

**Skill ID:** `fde-validation-acceptance-testing`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-SSDF, NIST-CSF

## Outcomes

- Prove the deployed solution meets agreed functional and security requirements
- Create objective evidence for customer acceptance
- Identify residual gaps before handover

## Method

1. Turn requirements into explicit test cases with expected results.
2. Prioritise security, identity, failure-mode, logging and recovery tests.
3. Use representative non-sensitive test data.
4. Record actual result and evidence for every acceptance criterion.
5. Classify failures as blocker, defect, limitation or enhancement.
6. Obtain customer acceptance or document outstanding actions.

## Safety / quality guardrails

- Do not mark tests passed without evidence.
- Do not use production-sensitive data when synthetic data is sufficient.
- Escalate any discovered vulnerability through the agreed security process.

## Output format

Return: `acceptance criteria → test cases → evidence/results → defects → residual risk → sign-off/outstanding actions`.

# Detection Content Deployment

**Skill ID:** `fde-detection-content-deployment`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** MITRE-ATT&CK, NIST-CSF

## Outcomes

- Move detection logic from development into customer environments safely
- Tune content to local telemetry and reduce false positives
- Maintain versioned and testable detection-as-code workflows

## Method

1. Confirm detection objective, ATT&CK behaviour and required data sources.
2. Validate field mapping and telemetry quality before deployment.
3. Test logic on historical or synthetic benign/adversary-like samples.
4. Tune thresholds and exclusions with documented rationale.
5. Deploy progressively and monitor alert quality.
6. Version control the rule and document rollback and ownership.

## Safety / quality guardrails

- Do not suppress alerts merely to achieve a low false-positive rate.
- Do not run unsafe adversary emulation on production solely to test a rule.
- Record known blind spots and unvalidated assumptions.

## Output format

Return: `detection objective → data requirements → rule → test evidence → tuning → deployment → monitoring → rollback/ownership`.

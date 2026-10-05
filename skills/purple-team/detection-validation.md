# Detection Validation & Regression Testing

**Skill ID:** `detection-validation`  
**Domain:** `purple-team`  
**Default mode:** `LAB`  
**Operational risk:** `medium`  
**Frameworks:** MITRE-ATT&CK

## Outcomes

- Create benign/synthetic test events
- Verify telemetry and alert logic end to end
- Maintain repeatable regression tests

## Method

1. Define the intelligence/control question and decision it must support.
2. Collect only relevant approved sources and record provenance.
3. Corroborate important claims and state confidence.
4. Translate results into defensive actions, detections, mitigations or prioritisation.
5. Record gaps, assumptions, expiry/review date and next evidence needed.

## Safety / quality guardrails

- Use only a declared lab, synthetic event source, or explicitly approved purple-team environment.
- Do not convert validation into stealth, persistence or uncontrolled real-world exploitation.
- Escalate high-impact changes to a human reviewer.
- Minimise sensitive-data access and preserve evidence provenance.

## Output format

Return: `question → sources/evidence → assessment → confidence → defensive implications → recommended actions → review/expiry`.

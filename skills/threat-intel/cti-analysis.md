# Cyber Threat Intelligence Analysis

**Skill ID:** `cti-analysis`  
**Domain:** `threat-intel`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** MITRE-ATT&CK, NIST-CSF

## Outcomes

- Assess source reliability and information confidence
- Turn reporting into relevant defensive hypotheses
- Separate actor attribution from observed behaviour

## Method

1. Define the intelligence/control question and decision it must support.
2. Collect only relevant approved sources and record provenance.
3. Corroborate important claims and state confidence.
4. Translate results into defensive actions, detections, mitigations or prioritisation.
5. Record gaps, assumptions, expiry/review date and next evidence needed.

## Safety / quality guardrails

- Use source confidence and evidence provenance.
- Do not invent attribution, indicators or framework mappings.

## Output format

Return: `question → sources/evidence → assessment → confidence → defensive implications → recommended actions → review/expiry`.

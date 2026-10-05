# Threat Campaign Analysis

**Skill ID:** `campaign-analysis`  
**Domain:** `threat-intel`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** MITRE-ATT&CK

## Outcomes

- Build timelines from public and internal evidence
- Cluster behaviour cautiously
- Create defensive detection and hunting priorities

## Method

1. Define the intelligence/control question and decision it must support.
2. Collect only relevant approved sources and record provenance.
3. Corroborate important claims and state confidence.
4. Translate results into defensive actions, detections, mitigations or prioritisation.
5. Record gaps, assumptions, expiry/review date and next evidence needed.

## Safety / quality guardrails

- Escalate high-impact changes to a human reviewer.
- Minimise sensitive-data access and preserve evidence provenance.

## Output format

Return: `question → sources/evidence → assessment → confidence → defensive implications → recommended actions → review/expiry`.

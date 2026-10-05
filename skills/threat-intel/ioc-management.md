# IOC & Observable Management

**Skill ID:** `ioc-management`  
**Domain:** `threat-intel`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** STIX/TAXII, NIST-CSF

## Outcomes

- Normalise and enrich observables
- Apply expiry/confidence/context
- Avoid treating stale indicators as permanent truth

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

# Telemetry & Observability Onboarding

**Skill ID:** `fde-telemetry-observability-onboarding`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF, MITRE-ATT&CK

## Outcomes

- Make deployed security solutions observable
- Confirm required security and operational events reach the intended destination
- Detect gaps, parsing failures and blind spots early

## Method

1. Define required telemetry by security use case and operational SLO.
2. Map log/event sources, transport, parsing, enrichment and retention.
3. Validate timestamps, host/user identifiers and field normalisation.
4. Check end-to-end delivery with benign representative events.
5. Measure volume, latency, loss and duplication.
6. Create health indicators and ownership for telemetry failures.

## Safety / quality guardrails

- Avoid generating harmful test activity merely to produce logs.
- Minimise sensitive data in telemetry and follow retention requirements.
- Do not claim coverage when a source or path has not been validated.

## Output format

Return: `required telemetry → source map → pipeline → validation → gaps → health metrics → ownership → retention/privacy notes`.

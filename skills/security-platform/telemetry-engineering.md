# Security Telemetry Engineering

**Skill ID:** `telemetry-engineering`  
**Domain:** `security-platform`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** MITRE-ATT&CK, NIST-CSF

Engineer high-quality security telemetry before writing detections.

Map required events to threat hypotheses; define schemas, time synchronisation, identity/asset context, retention, redaction, quality checks and coverage gaps.

## Output
Return: `data source → event → required fields → quality test → retention → privacy handling → detections enabled`.

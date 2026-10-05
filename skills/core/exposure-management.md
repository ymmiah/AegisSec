# Continuous Exposure Management

**Skill ID:** `exposure-management`  
**Domain:** `core`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-CSF, CIS-v8.1, MITRE-ATT&CK

Prioritise externally and internally exposed weaknesses by realistic business impact instead of scanner volume.

## Outcomes
- Correlate assets, vulnerabilities, identities, reachability and business criticality.
- Identify exploitable exposure chains and remediation choke points.
- Drive measurable risk reduction.

## Method
1. Build an authoritative asset and ownership view.
2. Ingest vulnerability, configuration, cloud, identity and attack-surface findings.
3. De-duplicate and validate material exposures.
4. Score by exploitability, reachability, privilege, blast radius, asset value and active threat intelligence.
5. Group related weaknesses into exposure paths rather than independent tickets.
6. Prioritise fixes that break multiple paths.
7. Verify remediation and monitor recurrence.

## Output
Return: `exposure → affected assets → path → business impact → priority → fix → verification`.

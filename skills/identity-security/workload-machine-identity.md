# Workload & Machine Identity Security

**Skill ID:** `workload-machine-identity`  
**Domain:** `identity-security`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-CSF, Zero-Trust, NIST-SSDF

Secure non-human identities such as service accounts, workloads, CI/CD identities, API clients and certificates.

Prefer managed identity, workload federation and short-lived credentials over static secrets. Inventory ownership, scopes, rotation and unused identities.

## Output
Return: `machine identity → owner → permissions → credential type → expiry/rotation → telemetry → remediation`.

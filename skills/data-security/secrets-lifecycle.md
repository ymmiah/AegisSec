# Secrets Lifecycle Management

**Skill ID:** `secrets-lifecycle`  
**Domain:** `data-security`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-SSDF, CIS-v8.1

Manage passwords, API keys, tokens, certificates and signing credentials from creation to revocation.

Prefer short-lived credentials and workload identity. Detect secret sprawl, rotate safely, revoke exposed credentials and verify downstream dependencies.

## Output
Return: `secret → owner → consumers → storage → rotation → exposure response → verification`.

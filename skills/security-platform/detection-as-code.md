# Detection as Code

**Skill ID:** `detection-as-code`  
**Domain:** `security-platform`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** MITRE-ATT&CK, MITRE-D3FEND

Manage detection logic using version control, review, tests, deployment gates and rollback.

Require reproducible test fixtures, false-positive expectations, data prerequisites, owner and version. Separate detection logic from environment-specific deployment configuration.

## Output
Return: `detection → threat mapping → data dependency → test cases → deployment → monitoring → rollback`.

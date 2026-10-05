# Secure CI/CD Build Runners

**Skill ID:** `secure-build-runners`  
**Domain:** `devsecops`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-SSDF, SLSA

Harden hosted and self-hosted build runners against secret theft, cross-job persistence and untrusted code.

Prefer ephemeral runners, minimal network reachability, workload identity, isolated caches, protected secrets and restricted privileged execution.

## Output
Return: `runner trust boundary → workload → credentials → isolation → egress → cleanup → verification`.

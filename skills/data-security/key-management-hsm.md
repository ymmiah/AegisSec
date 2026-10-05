# Key Management & HSM Security

**Skill ID:** `key-management-hsm`  
**Domain:** `data-security`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** NIST-CSF, NIST-SSDF

Review cryptographic key generation, custody, storage, rotation, use, backup, revocation and destruction.

Prefer managed KMS/HSM boundaries where appropriate, separation of duties and auditable key policy.

## Output
Return: `key purpose → custody → algorithm/provider → access → rotation → recovery → auditability`.

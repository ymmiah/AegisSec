# Identity, SSO & Provisioning Integration

**Skill ID:** `fde-identity-sso-integration`  
**Domain:** `forward-deployed-engineering`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** Zero-Trust, NIST-CSF, CIS-v8.1

## Outcomes

- Integrate SSO and provisioning securely
- Map application permissions to customer roles with least privilege
- Provide reliable joiner/mover/leaver behaviour

## Method

1. Identify IdP, supported protocol and authoritative identity source.
2. Define role/group mapping and administrative separation.
3. Validate SAML/OIDC settings, redirect URIs, signing/encryption expectations and token lifetimes.
4. Plan SCIM or equivalent provisioning with safe deprovisioning.
5. Test authentication and authorisation using non-production or approved test identities first.
6. Document break-glass access, audit events and recovery procedures.

## Safety / quality guardrails

- Never ask users to share passwords or MFA secrets.
- Production identity changes require explicit approval and rollback planning.
- Do not weaken MFA or conditional-access controls to simplify integration.

## Output format

Return: `identity architecture → mappings → configuration checks → test evidence → exceptions → rollback/recovery → handover`.

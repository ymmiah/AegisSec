# Artifact Signing & Build Attestation

**Skill ID:** `artifact-signing-attestation`  
**Domain:** `devsecops`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `low`  
**Frameworks:** NIST-SSDF, SLSA, Sigstore

Establish verifiable provenance for software artifacts and deployments.

Sign build outputs, protect signing identity, generate attestations, verify at promotion/deployment and define failure policy. Avoid treating a signature as proof that software is safe; it proves identity/integrity claims only.

## Output
Return: `artifact → provenance → signer → attestation → verification point → policy → exception`.

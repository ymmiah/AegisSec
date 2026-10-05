# SBOM Pipeline

AegisSec treats the Software Bill of Materials as a security input, not as a compliance artefact only.

## Pipeline

1. Produce or ingest CycloneDX/SPDX.
2. Extract package name, version and Package URL where available.
3. Query OSV in batches.
4. Normalise CVE/GHSA/OSV identifiers.
5. Enrich unique CVEs with GitHub Advisory, NVD, CISA KEV and EPSS.
6. Add asset/runtime context.
7. Prioritise and route findings.
8. Create remediation work and preserve evidence.
9. Re-scan after the change.
10. Close only after verification.

Package URLs are preferred because they reduce ecosystem/name ambiguity.

## Example generic inventory

```json
{
  "components": [
    {
      "name": "lodash",
      "version": "4.17.20",
      "purl": "pkg:npm/lodash@4.17.20",
      "direct": true
    }
  ]
}
```

# Release Validation — AegisSec AI v1.1.1

Release date: **5 October 2026**

## Validation gates

- **115** security-native AegisSec skill IDs are unique and every indexed file exists.
- All-in-one senior layer contains exactly **64** indexed skills and **64** router entries.
- Every senior specialist has an individual `SKILL.md`.
- Every senior source reference resolves to an entry in `skills/SOURCES.md`.
- Required mode/risk metadata is valid.
- JSON and JSON Schema files parse successfully.
- YAML policy, configuration, template and workflow files parse successfully.
- Manifest skill counts match the indexes.
- Upstream skills cannot override AegisSec policy.
- `skip_check_allowed` remains false for the guarded upstream integration.
- Python helpers and the vulnerability-intelligence package compile.
- Repository and vulnerability-intelligence unit tests pass.
- Approved brand assets and dependency-free GitHub Pages frontend files are present.
- OSV-Scanner reusable workflows are pinned to an existing reviewed release.

## Expected catalogues

- AegisSec native security catalogue: **115 skills**.
- All-in-one senior catalogue: **64 skills**.
- Optional guarded upstream catalogue at pinned review: **818 reported skills / 34 domains**.

## Vulnerability-intelligence checks

- OSV, GitHub Advisory Database, NVD, CISA KEV and FIRST EPSS connector configuration parses.
- CycloneDX and SPDX parsing has automated unit coverage.
- CVE/GHSA/OSV correlation and deduplication paths have automated unit coverage.
- Risk urgency floors and context-aware prioritisation have automated unit coverage.
- OSV-Scanner v2 JSON ingestion has automated unit coverage.
- Production remediation remains gated by AegisSec change-control policy.

## Stable release status

The v1.1.1 package is considered **stable when all local validation commands below pass**:

```bash
python -m pip install -r requirements.txt
python scripts/aegissec.py validate
python scripts/aegissec.py catalog
python scripts/aegissec.py senior-status
python scripts/vuln_intel.py show-config
python -m unittest discover -s tests -v
python -m compileall -q aegissec_vuln scripts tests
```

`upstream-status` may return a non-zero status when the optional third-party skill package has not been installed; that is expected and does not invalidate the native release.

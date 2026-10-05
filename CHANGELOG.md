# Changelog

## 1.0.0 Stable — 2026-10-05

First stable release of **AegisSec AI v1**. This release consolidates the complete development line into one tested, production-oriented repository.

### Security-native platform

- 115 curated AegisSec security-native skills with explicit modes and risk tiers.
- Red Team, Blue Team, SOC, DFIR, AppSec, DevSecOps, Cloud, IAM, Threat Intelligence, Purple Team, AI Security, GRC and reporting coverage.
- Forward Deployed Security Engineer, Identity Security Engineer, Security Platform Engineer and Data Security Engineer roles.
- Governed lifecycle: `DISCOVER → PLAN → APPROVE → EXECUTE → VERIFY → CLOSE`.
- Policy precedence, action-risk classification, capability controls, production-change gates, evidence integrity and human approval for consequential actions.

### Vulnerability intelligence

- OSV-based dependency/package discovery.
- GitHub Advisory Database, NVD, CISA KEV and FIRST EPSS enrichment connectors.
- CycloneDX JSON, SPDX JSON and generic component inventory support.
- CVE/GHSA/OSV normalisation and deduplication.
- Context-aware P0–P4 prioritisation using CVSS, EPSS, KEV, reachability, internet exposure, asset criticality and privilege context.
- OSV-Scanner v2 repository ingestion and GitHub Actions workflows.

### Senior all-in-one layer

- 64 portable senior specialist `SKILL.md` files.
- Machine-readable `skills/router.json` and `skills/skills-index.json`.
- AI/agent engineering, software engineering, cloud, Kubernetes, data/ML, research, design, SRE, QA, architecture, browser/computer-use and FDE coverage.

### Guarded upstream integration

- Optional reviewed integration with `mukul975/Anthropic-Cybersecurity-Skills` (818 reported skills / 34 domains at the pinned review).
- Upstream knowledge remains subordinate to AegisSec scope, authorisation and approval policy.
- Reviewed upstream commit provenance is stored in `upstream/source.lock.json`.

### Brand, frontend and documentation

- Approved AegisSec AI logo, icon and hero artwork.
- Responsive dependency-free GitHub Pages frontend under `docs/`.
- In-depth README, architecture, framework, capability, brand and vulnerability-intelligence documentation.

### Validation

- Repository structure validator.
- JSON/JSON Schema and YAML parsing checks.
- Python compilation checks.
- 10 automated repository and vulnerability-intelligence unit tests.
- Stable release metadata normalised to `1.0.0`.

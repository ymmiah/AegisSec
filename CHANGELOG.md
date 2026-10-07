# Changelog

## 1.1.1 — 2026-10-07

### Added — purple-team skills

- **`aegissec-adversary-emulation-plan`** — build an authorised, MITRE ATT&CK-mapped purple-team emulation plan: least-impact techniques to emulate under an engagement scope, the detection each step should trigger, and a hand-off to detection validation. Produces a plan and expected detections, never exploitation how-to.
- **`aegissec-attack-technique-coverage`** — map detections, findings and controls to the ATT&CK matrix and report where coverage is strong, partial or blind, ranked by relevance. Read-only; tests nothing.
- Operational skills: 8 → 10; total Agent Skills: 72 → 74.

## 1.1.0 — 2026-10-06

Highlights: actionable vulnerability fix plans, 72 Agent Skills, a governed runtime harness over any LLM (incl. NVIDIA NIM), imported security/DevSecOps personas, and hardened API/credential handling.

### Added — every-agent/every-skill smoke test

- `tests/test_all_agents_skills.py` loads all 18 harness agents and drives the governed loop, loads all 8 operational + 115 native + 64 senior skills, and runs every harness tool (network tools stubbed so CI stays fast and hermetic). Runs in the `validate` gate.

### Security — hardened every outbound API call

- All outbound HTTP (LLM providers and the OSV/GitHub/NVD/CISA/EPSS connectors) now goes through `aegissec_vuln/securehttp.py`: TLS enforced and verified (never disableable); plain HTTP only to loopback/private hosts, never remote, so bearer keys are never sent in cleartext; `Authorization`/API-key headers stripped on cross-host redirect; secrets redacted from error text; `AEGISSEC_CA_BUNDLE` to trust an inspecting proxy; bounded timeouts. Keys come from the environment, ride in headers only, and are never logged or persisted. Covered by `tests/test_securehttp.py` and documented in `SECURITY.md`.

### Added — runtime harness (security chatbot over any LLM)

- **`aegissec_agent/`**, a pure-standard-library runtime harness that runs AegisSec as a governed security agent over any LLM. Run it as a CLI (`scripts/aegissec_agent.py`) or embed it with `from aegissec_agent import Harness`.
- **Provider-agnostic**: Anthropic Messages API, OpenAI, **NVIDIA NIM** (the NVIDIA API catalog or a self-hosted NIM container, `--provider nvidia`, `NVIDIA_API_KEY`) and any OpenAI-compatible endpoint, over the standard library; a stub provider runs the whole loop offline for tests.
- **Policy enforced in the loop**: every tool call clears a gate driven by `tools/action-risk.yaml` — low-risk read-only/intelligence tools run; scope-gated actions need a passing engagement scope; approval-gated actions need a human; destructive actions are denied; unknown actions fail closed.
- **Tools**: list/read skills, list/read files (sandboxed to a workdir), dependency scan with fix plan, CVE enrichment, scope check. Shipped tools are read-only and advisory.
- **Personas**: `aegissec-operator` plus 17 **security and DevSecOps/SRE** specialists imported from `msitarzewski/agency-agents` (MIT) into `agents/community/`, recorded with checksums in `upstream/agency-agents.lock.json` and subordinate to AegisSec policy.
- `validate` now checks `agents/index.json` against the files and verifies imported personas against the upstream lock. README and `docs/runtime-harness.md` document it.

### Added — Agent Skills for any AI

- **8 operational Agent Skills** in `skills/aegissec/`, installable into Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and 70+ other agents with `npx skills add ymmiah/AegisSec`: `aegissec` (operating rules and routing), `aegissec-vuln-scan`, `aegissec-fix-plan-pr`, `aegissec-cve-triage`, `aegissec-scope-check`, `aegissec-finding-report`, `aegissec-ci-setup`, `aegissec-wordpress-review`. They fetch the toolkit on first use, so they work in any repository.
- `validate` now enforces the Agent Skills specification for every `SKILL.md`, plus links between skills and to toolkit files. All 72 skills also pass the official `agentskills validate`.
- README: "AegisSec skills for AI agents" with install commands for coding agents and guidance for chat apps (ChatGPT, Claude.ai, Gemini, Grok).

### Changed

- The 64 senior `SKILL.md` files now carry a `description` (taken from the index and its triggers) and keep their other fields under `metadata`. They previously had no description and failed the Agent Skills specification, so agents could not discover them.
- **`check-scope` enforces all eight `AGENTS.md` scope requirements.** It previously checked five and accepted an expired window. It now also requires a named owner, non-placeholder targets, a valid start/end window that includes the current time, data-handling details and a real emergency contact.

### Added — actionable vulnerability reports

- **Fix plan**: findings are grouped into one upgrade action per package, ordered by priority, naming the version that clears every fixable finding on it. Flags major-version upgrades, known-exploited issues, indirect dependencies and findings with no published fix. Each finding links to its plan step.
- **Deadlines and owner**: `remediation_sla_days` in the configuration turns priority into a fix-by date (defaults P0 2, P1 7, P2 30, P3 90, P4 180 days); the owner comes from the asset context.
- **Report redesign**: a one-screen summary, then the fix plan, then detail for P0–P2; P3/P4 collapse into a table; long warnings are shortened.
- **`--baseline`**: compares with a previous JSON result, marks findings new or existing, and lists what was resolved.
- **`--fail-on P0..P4` and `--new-only`**: exit code 3 for CI gating, optionally only on newly introduced findings.
- **SARIF 2.1.0** (`--format sarif`, `--sarif-out`) for the GitHub Security tab.
- **`--json-out` / `--markdown-out`** to write several formats in one run; **`repo --from-osv-json`** to reuse output from the official OSV-Scanner action.
- **`examples/github-actions/aegissec-dependency-scan.yml`**: reusable weekly workflow that publishes to the Security tab, keeps one fix-plan issue current (closing it when clean), caches the baseline, and gates pull requests on new findings. Verified end to end on live data.
- README: new "How to use AegisSec" section with the human/AI partner model; engine, risk, playbook and usage docs updated.

### Fixed

- Restored the GitHub Actions workflows that the web upload had dropped: `validate.yml` (release gates on Python 3.11–3.13, including manifest integrity), `osv-scanner.yml` and `osv-scanner-scheduled.yml` (pinned to `google/osv-scanner-action` v2.6.0 by commit), and a read-only `upstream-audit.yml` drift check.
- Restored `engagements/.gitkeep` so the engagement scope folder referenced by the agent adapters exists.
- Regenerated `MANIFEST.sha256`; every listed file now exists and verifies.
- Vulnerability scans failed against the live OSV API (HTTP 400) whenever a component had a versioned purl, because the version was sent twice. The OSV query now sends the version only once; a regression test covers pinned, scoped, unpinned and name-based queries.
- Live scans under-prioritised every finding (all P3, confidence low — including Log4Shell). OSV's batch endpoint returns only IDs, so findings had no CVE aliases, severity or fixed versions and EPSS, CISA KEV and NVD enrichment never ran. The OSV connector now fetches each full record (cached per ID); a regression test reproduces the live API shape.
- GitHub Advisory enrichment crashed on every CVE (`'str' object has no attribute 'get'`) because the REST API returns `first_patched_version` as a string. Both shapes are now accepted, and CVSS is read from `cvss_severities` (v4, then v3) before the legacy `cvss` field.
- NVD enrichment was rate-limited (HTTP 429) on real scans. Requests are now paced to NVD's public limits (6.5 s apart without `NVD_API_KEY`, 0.7 s with one) and a 429 waits for the window to clear before one retry.
- Remediation recommended older-branch fixes (for example Log4j 2.3.1 for an installed 2.14.1). `target_versions` now lists only genuine upgrades, lowest first, with a new `recommended_version`, also shown in the Markdown report.
- Upgrade advice could name a version still inside another advisory's affected range for the same CVE (seen live: lodash 4.17.23 vs 4.18.0). Affected ranges are now tracked per package through deduplication and the lowest version outside every range is recommended.
- `aegissec.py vuln-*` shortcuts now forward every scanner option.
- `aegissec risk` with no action now lists the known actions instead of exiting with a usage error.

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

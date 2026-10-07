# AegisSec AI v1.1.1 — Release

**Status:** Stable

AegisSec AI v1.1.1 adds two purple-team skills (adversary-emulation planning and ATT&CK coverage mapping) on top of v1.1.0, which brought actionable vulnerability reporting, Agent Skills usable by any AI, a governed runtime harness, imported security/DevSecOps personas, NVIDIA NIM support, and hardened API/credential handling.

## What's new

**v1.1.1** — `aegissec-adversary-emulation-plan` (authorised, ATT&CK-mapped purple-team planning with expected detections) and `aegissec-attack-technique-coverage` (map detections/findings/controls to ATT&CK and report gaps). Operational skills 8 → 10; total 72 → 74.

### v1.1.0

- **Actionable vulnerability reports** — per-package fix plan with deadlines and owner, baseline diff, `--fail-on` CI gate, SARIF for the GitHub Security tab, and a reusable weekly scan workflow. (Fixed the live-API bugs that made the scanner under-report.)
- **72 Agent Skills** installable into Claude Code, Codex, Cursor, Gemini CLI, Copilot and 70+ tools via `npx skills`; all pass the official validator.
- **Runtime harness** (`aegissec_agent/`) — AegisSec as a governed security chatbot over any LLM, with the scope and approval gates enforced in the loop. Providers: Anthropic, OpenAI, **NVIDIA NIM**, any OpenAI-compatible endpoint.
- **17 security + DevSecOps/SRE personas** imported from agency-agents (MIT), subordinate to policy.
- **Hardened API/credential handling** — TLS enforced and verified, keys in headers only and never logged, no cleartext to remote hosts, auth stripped on cross-host redirect.
- **Full scope gate** — `check-scope` enforces all eight AGENTS.md requirements.

## Verified

- 74 Agent Skills (10 operational + 64 senior) · 115 native security skills · 18 harness agents · 7 harness tools
- 63/63 unit tests, including an every-agent/every-skill smoke test
- All 72 skills pass the official `agentskills validate`
- Python compilation, JSON/YAML parsing, repository validation, manifest integrity
- Agents, skills and tools exercised end to end (offline, with a stub LLM)

See [`CHANGELOG.md`](CHANGELOG.md) for the full list, [`docs/release-validation.md`](docs/release-validation.md) for the gates and [`README.md`](README.md) for setup and usage.

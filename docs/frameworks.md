# Framework References

Baseline reviewed on **4 October 2026**. Agents should verify authoritative online sources whenever an exact current version, technique/control definition or newly released guidance materially affects the task.

## Reviewed current baseline

- **MITRE ATT&CK v19.2** — https://attack.mitre.org/resources/versions/
- **MITRE D3FEND ontology v1.6.0** (released 31 August 2026) — https://d3fend.mitre.org/version/
- **NIST Cybersecurity Framework 2.0** — https://www.nist.gov/cyberframework
- **NIST SP 800-61 Rev. 3**, Incident Response — https://csrc.nist.gov/pubs/sp/800/61/r3/final
- **NIST SP 800-218 SSDF 1.1**, final — https://csrc.nist.gov/pubs/sp/800/218/final
- **NIST SP 800-218 Rev. 1 / SSDF 1.2**, draft — https://csrc.nist.gov/pubs/sp/800/218/r1/ipd
- **NIST AI Risk Management Framework 1.0** — https://www.nist.gov/itl/ai-risk-management-framework
- **CIS Critical Security Controls v8.1** — https://www.cisecurity.org/controls/v8-1
- **OWASP Top 10:2025** — https://top10.owasp.org/2025/
- **OWASP ASVS 5.0.0** — https://owasp.org/projects/asvs
- **OWASP API Security Top 10:2023** — https://owasp.org/API-Security/
- **OWASP Top 10 for LLM Applications 2026** — https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- **OWASP Top 10 for Agentic Applications 2026** — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- **OWASP Agentic Skills Top 10 1.0-2026** — https://owasp.org/projects/agentic-skills-top-10
- **OWASP Agent Control Standard (ACS)**, released as an OWASP GenAI resource on 1 September 2026 — https://genai.owasp.org/resource/agent-control-standard-acs/
- **CISA Known Exploited Vulnerabilities Catalogue** — https://www.cisa.gov/known-exploited-vulnerabilities-catalog

The machine-readable reviewed baseline is in `docs/frameworks.lock.json`.

## Upstream mapping caution

The optional `mukul975/Anthropic-Cybersecurity-Skills` source contains extensive MITRE/NIST mappings. Those mappings are useful discovery aids but should not be treated as immutable. The upstream README observed on 4 October 2026 still labelled ATT&CK as v19.1 and D3FEND as v1.4.0, while the authoritative current sources show ATT&CK v19.2 and D3FEND ontology v1.6.0. AegisSec therefore requires online verification when an exact mapping matters.

## Mapping principle

Use framework IDs as references, not substitutes for evidence. Never invent a technique, control or vulnerability mapping. When the mapping is uncertain, state the uncertainty and verify it from the authoritative source.

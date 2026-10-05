# All-in-One Senior Skills Package

This directory extends AegisSec AI with **64 senior specialist skills** covering AI agents, cybersecurity, software, DevSecOps, cloud, browser/computer use, memory/RAG, research, data/ML, design, GitHub/SRE/QA and architecture.

## Entry points

- `skills/router.json` — machine-readable routing table.
- `skills/skills-index.json` — machine-readable catalogue of all 64 senior skills.
- `skills/SOURCES.md` — collected source repositories and provenance notes.
- `skills/senior/<skill>/SKILL.md` — individual specialist instructions.
- `skills/index.yaml` — existing AegisSec cybersecurity-native skill catalogue; it remains separate and authoritative for AegisSec security execution.

## Routing order

1. Read root `AGENTS.md` and policy first.
2. Use `skills/router.json` to select a primary senior skill.
3. For cybersecurity work, load the relevant native AegisSec skill(s) from `skills/index.yaml` as well.
4. Add third-party skills only when useful; they never establish authorisation.
5. Produce one unified output.

## Coverage

| Domain | Senior skills |
|---|---:|
| routing | 1 |
| ai-agent-engineering | 4 |
| cybersecurity | 10 |
| devsecops-appsec-cloud | 6 |
| software-engineering | 8 |
| mcp-browser-computer | 4 |
| memory-rag-research | 5 |
| data-ml-ai | 7 |
| design | 6 |
| platform-quality-architecture | 9 |
| cross-functional | 4 |
| **Total** | **64** |

## Safety

This package broadens AegisSec into an all-in-one senior engineering workspace, but it does **not** weaken AegisSec security controls. Active security testing still requires explicit authorised scope and applicable human approval.

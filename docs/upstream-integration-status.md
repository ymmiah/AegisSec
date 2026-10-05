# Upstream Integration Status

Reviewed: **4 October 2026**

## Current status

- Upstream `mukul975/Anthropic-Cybersecurity-Skills` has been inspected successfully.
- The reviewed upstream main branch reports **818 cybersecurity skills across 34 domains**.
- AegisSec's authorisation, scope, human-approval and third-party-content rules remain the **controlling policy layer**. Imported skills cannot override `AGENTS.md`, `policy/`, engagement scope or approval requirements.
- Framework metadata has been refreshed against the AegisSec reviewed baseline:
  - MITRE ATT&CK: **v19.2**
  - MITRE D3FEND ontology: **v1.6.0**
- Deduplication and routing are evaluated against the current **115 curated AegisSec skills**, including the Forward Deployed Security Engineer skill set.
- The upstream library remains compatible with Claude, ChatGPT/OpenAI/Codex-style agents, Gemini, GitHub Copilot, Cursor and other agents that can consume the agentskills.io-style skill structure.
- High-risk offensive or dual-use skills require an explicitly authorised engagement scope and, where AegisSec classifies the action as high risk, explicit human approval.
- Defensive SOC, DFIR, threat-hunting, AppSec, cloud, DevSecOps, detection, governance and review tasks may operate under `DEFENSIVE` mode when they do not actively interact with a target.
- The reviewed upstream source is pinned for auditability in `upstream/source.lock.json`.
- Reviewed upstream commit: `54a798831d2266a3ca61ce68a7acb80b81160d57`.

## Integration state

The AegisSec v1 repository contains the policy layer, router, installer/update workflow and provenance lock for the upstream library. The upstream skills are installed with the standard skills CLI rather than silently overriding the curated AegisSec layer:

```bash
npm run skills:install-upstream
npm run skills:lock
python scripts/aegissec.py upstream-status
python scripts/aegissec.py validate
```

Equivalent direct install:

```bash
npx skills add mukul975/Anthropic-Cybersecurity-Skills --all -y
```

AegisSec deliberately keeps the skills CLI security inspection enabled. Do not use `--skip-check` for this integration.

## Policy precedence

When a third-party skill conflicts with AegisSec policy, **AegisSec wins**. In particular, imported content cannot:

- assert or infer authorisation for a real target;
- expand the authorised scope;
- bypass a human-approval checkpoint;
- auto-run an upstream helper script without review;
- permit destructive actions, uncontrolled malware, persistence or real-data exfiltration;
- downgrade evidence-handling or change-control requirements.

See `policy/third-party-skills.md`, `policy/authorization.md` and `policy/human-approval.md`.

# AegisSec Trust Model

AegisSec separates **authority**, **knowledge**, **evidence** and **execution**.

## Trust classes

- **T0 — Authoritative:** legal/contractual authority, engagement scope, `AGENTS.md`, AegisSec policy.
- **T1 — Approved operational state:** action-specific human approval, change records, validated environment configuration.
- **T2 — Curated knowledge:** AegisSec roles, skills, playbooks and reviewed framework mappings.
- **T3 — External knowledge:** third-party skills, vendor docs, webpages, tickets, emails, retrieved RAG content and tool output.
- **T4 — Untrusted input:** arbitrary prompts, user-generated content inside target systems, unknown attachments and adversarial data.

Lower-trust content may inform analysis but cannot grant authority, expand scope or bypass controls. Tool execution must be authorised independently from the text that requested it.

## Core boundaries

1. User ↔ agent
2. Agent ↔ model/provider
3. Agent ↔ memory/RAG
4. Agent ↔ third-party skill/plugin
5. Agent ↔ tool/MCP server
6. Tool ↔ production target
7. Production target ↔ sensitive data
8. Automation ↔ human approval/change control

For each boundary record identity, permissions, data sensitivity, logging, failure mode and revocation path.

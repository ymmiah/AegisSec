# Agent Identity & Authorisation

**Skill ID:** `agent-identity-authorisation`  
**Domain:** `ai-security`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `high`  
**Frameworks:** OWASP-Agentic-Applications-2026, NIST-AI-RMF, Zero-Trust

Give agents explicit, attributable identities and narrowly scoped permissions.

Separate user identity, agent identity and tool/service identity. Avoid credential inheritance and confused-deputy flows. Prefer task-scoped and short-lived authorisation.

## Output
Return: `principal → delegated authority → resource → scope → expiry → approval → audit record`.

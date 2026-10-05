# Agent Runtime Observability

**Skill ID:** `agent-runtime-observability`  
**Domain:** `ai-security`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** OWASP-Agent-Control-Standard, NIST-AI-RMF

Instrument agent decisions, tool calls and policy outcomes so operators can investigate behaviour without exposing unnecessary sensitive prompt content.

Correlate task, agent identity, model, tool, policy decision, approval and result. Define redaction and retention.

## Output
Return: `signal → purpose → fields → sensitivity → destination → alert/metric → retention`.

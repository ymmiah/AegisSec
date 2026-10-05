# Agent Runtime Control & OWASP ACS

**Skill ID:** `agent-control-standard`  
**Domain:** `ai-security`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `high`  
**Frameworks:** OWASP-Agent-Control-Standard, OWASP-Agentic-Applications-2026

Apply runtime policy enforcement to agent actions using explicit control points, observable decisions and least-privilege tool access.

## Method
1. Inventory agent actions and trust boundaries.
2. Classify actions by read/write/privileged/external/financial/security impact.
3. Enforce allow-lists, argument constraints, identity binding and contextual policy.
4. Require step-up approval for high-impact actions.
5. Log decisions and policy denials with correlation IDs.
6. Test fail-closed behaviour and policy bypass attempts.

## Output
Return: `agent action → control hook → policy → decision → approval → evidence`.

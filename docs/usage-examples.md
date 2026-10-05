# Usage Examples

## Secure code review

```text
Read AGENTS.md, roles/appsec-engineer.md and skills/appsec/secure-code-review.md.
Review the files I provide. Focus on access control, injection, secrets, cryptography and business logic.
Return only evidence-supported findings using templates/finding.md.
```

## SOC triage

```text
Read AGENTS.md, roles/soc-analyst.md and playbooks/soc-triage.md.
Analyse the supplied alert and logs. Build a timeline, state confidence, list containment options and identify the extra telemetry needed before escalation.
```

## Authorised assessment

```text
Read AGENTS.md and engagements/customer-a.yaml first. Refuse any target outside that file.
Use playbooks/authorised-pentest.md and the web/API skills. Prefer safe proof and stop once a vulnerability is demonstrated.
```

## AI agent security

```text
Read AGENTS.md, roles/ai-security.md and playbooks/ai-agent-security-review.md.
Threat-model this agent, its MCP/tools, memory, RAG sources and approvals. Produce abuse cases, guardrails, logging requirements and test cases using synthetic data.
```

## Forward-deployed customer implementation

```text
Read AGENTS.md, roles/forward-deployed-security-engineer.md and playbooks/forward-deployed-security-engagement.md.
Help deploy this security capability into the customer's authorised environment. Start with discovery and readiness, then produce the architecture, staged implementation, validation, rollback and handover plan.
```

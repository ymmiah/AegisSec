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

## Dependency fix plan (scan → pull request)

```text
Read AGENTS.md and playbooks/continuous-vulnerability-management.md.
Run scripts/vuln_intel.py repo . with .github/aegissec-context.yaml and show me the fix plan.
Then open a pull request for step 1 only, run the tests, and re-scan with the previous
result as --baseline to prove the findings are resolved. Do not merge.
```

## Weekly report for a client or manager

```text
Read the latest AegisSec fix-plan issue in this repository. Summarise in five lines for a
non-technical owner: what is urgent, the deadline, what was fixed since last week, and what
decision you need from them.
```

## Triage one alert

```text
Read AGENTS.md and roles/appsec-engineer.md. Enrich CVE-2021-44228 for
.github/aegissec-context.yaml. Is our usage actually reachable? What is the smallest safe
fix, how do we roll it back, and what evidence would show it worked?
```

# AegisSec Problem Registry

> Source of truth for the problem cards on the [AegisSec site](index.html). Agents: when a request matches a problem below, load its playbook and skills. `AGENTS.md` and `policy/` still decide what you're allowed to do.

Every entry maps a **real-world security problem** to files that already exist in this repository. Every path below is checked before release.

**Hard rule for every entry:** no target + no scope + no authorisation = no active testing. Consequential actions (production changes, containment, credential rotation, account disabling) wait for human approval.

## How to use an entry

1. Find the problem that matches yours.
2. Run the **Start with** command, or open the file it names.
3. Follow the playbook's steps through `DISCOVER → PLAN → APPROVE → EXECUTE → VERIFY → CLOSE`.
4. Deliver evidence plus a fix plan or report (see `templates/`).

## Index

| # | Problem | Who it hurts | Category |
| ---: | --- | --- | --- |
| 1 | [Our dependencies have a pile of CVEs and nobody knows what to fix first](#01-dependency-vulns) | Dev, AppSec, DevSecOps | Vulnerability |
| 2 | [A scary CVE is trending. Does it actually affect us?](#02-one-cve) | AppSec, SOC, Dev | Vulnerability |
| 3 | [Vulnerable code keeps getting merged. We need a PR / CI security gate](#03-pr-gate) | DevSecOps, Dev, Platform | DevSecOps |
| 4 | [We need a security review of an app or a risky pull request](#04-code-review) | AppSec, Dev | AppSec |
| 5 | [We've been asked to pentest a web app. How do we do it safely and legally?](#05-pentest-plan) | Red Team, AppSec, Consultant | Offensive (authorised) |
| 6 | [The SOC is drowning in alerts. Is this one real?](#06-soc-triage) | SOC, Blue Team | Detection & Response |
| 7 | [Someone reported a phishing email. Who clicked, and what do we do?](#07-phishing) | SOC, IT, DFIR | Detection & Response |
| 8 | [We think we have an active incident or ransomware](#08-ransomware-ir) | DFIR, IR Lead, Leadership | Detection & Response |
| 9 | [Is our AWS / Azure / GCP account set up securely?](#09-cloud-review) | Cloud, Platform, GRC | Cloud & Identity |
| 10 | [Too many admins, stale accounts and unknown service principals](#10-iam-review) | Identity, IT, GRC | Cloud & Identity |
| 11 | [Our WordPress site / plugin needs hardening before it gets hacked](#11-wordpress) | Dev, Agency, SMB | AppSec |
| 12 | [We're shipping an AI agent / MCP server. What can go wrong?](#12-ai-agent) | AI Eng, AppSec, Platform | AI Security |
| 13 | [Can we trust this third-party agent skill / prompt pack?](#13-third-party-skills) | AI Eng, AppSec, GRC | AI Security |
| 14 | [Would our detections actually catch a real attacker?](#14-purple-team) | Purple Team, Detection Eng, SOC | Purple Team |
| 15 | [We suspect something is in the network that no alert has caught](#15-threat-hunt) | Threat Hunter, SOC, CTI | Detection & Response |
| 16 | [Thousands of findings across tools, and no idea which ones lead to the crown jewels](#16-exposure) | Security Lead, Vuln Mgmt, Cloud | Exposure |
| 17 | [We need to push a security fix to production without breaking things](#17-prod-change) | SRE, Platform, Change Mgr | Governance |
| 18 | [Findings are scattered. We need a report leadership and engineers will both read](#18-reporting) | Consultant, GRC, Security Lead | Governance |

<a id="01-dependency-vulns"></a>

## 01. Our dependencies have a pile of CVEs and nobody knows what to fix first

**Who it hurts:** Dev, AppSec, DevSecOps  ·  **Category:** Vulnerability

**AegisSec answer:** Scan the repo or SBOM through OSV, enrich with GitHub Advisory, NVD, CISA KEV and EPSS, weigh it against your asset context, and get one ordered fix plan: one upgrade per package, with a priority, deadline and owner.

**Workflow:**

1. Scan repo / SBOM
2. Enrich with KEV + EPSS
3. Prioritise P0–P4 with context
4. Fix plan → PR
5. Re-scan to verify

**Start with:**

```bash
python scripts/vuln_intel.py repo . --context examples/vulnerability-intelligence/context.yaml --format markdown
```

**Files in this repo:**

- [`scripts/vuln_intel.py`](../scripts/vuln_intel.py)
- [`playbooks/continuous-vulnerability-management.md`](../playbooks/continuous-vulnerability-management.md)
- [`skills/aegissec/aegissec-vuln-scan/SKILL.md`](../skills/aegissec/aegissec-vuln-scan/SKILL.md)
- [`skills/aegissec/aegissec-fix-plan-pr/SKILL.md`](../skills/aegissec/aegissec-fix-plan-pr/SKILL.md)
- [`docs/vulnerability-intelligence.md`](../docs/vulnerability-intelligence.md)

**Guardrail:** Read-only scan. Upgrades go through a normal reviewed PR.

<a id="02-one-cve"></a>

## 02. A scary CVE is trending. Does it actually affect us?

**Who it hurts:** AppSec, SOC, Dev  ·  **Category:** Vulnerability

**AegisSec answer:** Enrich the identifier with public intelligence, then check whether the vulnerable version and code path are present, reachable and exposed. You get a decision (patch, mitigate, isolate or accept) with the evidence behind it.

**Workflow:**

1. Enrich CVE / GHSA
2. Confirm component + version
3. Check reachability + exposure
4. Decide patch / mitigate / accept
5. Define how to verify the fix

**Start with:**

```bash
python scripts/vuln_intel.py enrich CVE-2024-3094
```

**Files in this repo:**

- [`playbooks/vulnerability-triage.md`](../playbooks/vulnerability-triage.md)
- [`skills/aegissec/aegissec-cve-triage/SKILL.md`](../skills/aegissec/aegissec-cve-triage/SKILL.md)
- [`skills/threat-intel/vulnerability-intelligence.md`](../skills/threat-intel/vulnerability-intelligence.md)

**Guardrail:** Public intelligence only. No exploit attempts against your systems.

<a id="03-pr-gate"></a>

## 03. Vulnerable code keeps getting merged. We need a PR / CI security gate

**Who it hurts:** DevSecOps, Dev, Platform  ·  **Category:** DevSecOps

**AegisSec answer:** Drop one workflow into the repo: a weekly scan, results in the GitHub Security tab (SARIF), one fix-plan issue that keeps itself up to date, and a pull-request gate that fails only on new findings at or above your threshold.

**Workflow:**

1. Copy the workflow + context file
2. Pick a --fail-on threshold
3. Baseline the current findings
4. Block new P0/P1 findings on PRs
5. Review the CI/CD hardening checklist

**Start with:**

```bash
cp examples/github-actions/aegissec-dependency-scan.yml .github/workflows/
```

**Files in this repo:**

- [`examples/github-actions/aegissec-dependency-scan.yml`](../examples/github-actions/aegissec-dependency-scan.yml)
- [`examples/github-actions/aegissec-context.yaml`](../examples/github-actions/aegissec-context.yaml)
- [`skills/aegissec/aegissec-ci-setup/SKILL.md`](../skills/aegissec/aegissec-ci-setup/SKILL.md)
- [`playbooks/ci-cd-security-review.md`](../playbooks/ci-cd-security-review.md)
- [`skills/devsecops/ci-cd-security.md`](../skills/devsecops/ci-cd-security.md)

**Guardrail:** Changes to branch protection and production deploy gates need human approval.

<a id="04-code-review"></a>

## 04. We need a security review of an app or a risky pull request

**Who it hurts:** AppSec, Dev  ·  **Category:** AppSec

**AegisSec answer:** Threat-model the critical business actions, then review authentication, authorisation, input handling, secrets and dependencies. Verified gaps are mapped to OWASP Top 10 / ASVS and ranked by exploitability and impact.

**Workflow:**

1. Map data flows + trust boundaries
2. Threat-model critical actions
3. Review auth, input, secrets, deps
4. Map to OWASP / ASVS
5. Prioritised findings + fixes

**Start with:**

```bash
python scripts/aegissec_agent.py --agent security-appsec-engineer
```

**Files in this repo:**

- [`playbooks/application-security-review.md`](../playbooks/application-security-review.md)
- [`skills/appsec/secure-code-review.md`](../skills/appsec/secure-code-review.md)
- [`skills/appsec/authentication-review.md`](../skills/appsec/authentication-review.md)
- [`examples/sample-defensive-code-review/README.md`](../examples/sample-defensive-code-review/README.md)

**Guardrail:** Static, defensive review. No testing of live systems without a scope.

<a id="05-pentest-plan"></a>

## 05. We've been asked to pentest a web app. How do we do it safely and legally?

**Who it hurts:** Red Team, AppSec, Consultant  ·  **Category:** Offensive (authorised)

**AegisSec answer:** Nothing active happens until a complete engagement scope passes check-scope: owner, explicit targets, permitted and prohibited actions, a time window that includes now, data handling, emergency contact, stop conditions and confirmed authority. Then you test the agreed categories with benign proof and report.

**Workflow:**

1. Fill in the engagement scope
2. check-scope must pass
3. Passive baseline, then rate-limited discovery
4. Benign proof only, stop at sufficient evidence
5. Executive + technical report, then retest

**Start with:**

```bash
cp templates/engagement-scope.yaml engagements/acme.yaml && python scripts/aegissec.py check-scope engagements/acme.yaml
```

**Files in this repo:**

- [`playbooks/authorised-pentest.md`](../playbooks/authorised-pentest.md)
- [`templates/engagement-scope.yaml`](../templates/engagement-scope.yaml)
- [`skills/aegissec/aegissec-scope-check/SKILL.md`](../skills/aegissec/aegissec-scope-check/SKILL.md)
- [`skills/red-team/web-security-testing.md`](../skills/red-team/web-security-testing.md)
- [`skills/red-team/engagement-planning.md`](../skills/red-team/engagement-planning.md)

**Guardrail:** Hard gate: no target + no scope + no authorisation = no active testing.

<a id="06-soc-triage"></a>

## 06. The SOC is drowning in alerts. Is this one real?

**Who it hurts:** SOC, Blue Team  ·  **Category:** Detection & Response

**AegisSec answer:** Validate the alert source and data quality, enrich it with identity, endpoint, network and cloud context, build a short timeline, then call it benign, suspicious or malicious with a confidence level and a recommended next step.

**Workflow:**

1. Validate source + time range
2. Check false-positive conditions
3. Enrich + build a timeline
4. Verdict + confidence
5. Contain / escalate / close, then tune the detection

**Start with:**

```bash
python scripts/aegissec_agent.py --agent security-senior-secops
```

**Files in this repo:**

- [`playbooks/soc-triage.md`](../playbooks/soc-triage.md)
- [`skills/blue-team/soc-triage.md`](../skills/blue-team/soc-triage.md)
- [`roles/soc-analyst.md`](../roles/soc-analyst.md)
- [`skills/blue-team/detection-engineering.md`](../skills/blue-team/detection-engineering.md)

**Guardrail:** Containment actions on production assets need human approval.

<a id="07-phishing"></a>

## 07. Someone reported a phishing email. Who clicked, and what do we do?

**Who it hurts:** SOC, IT, DFIR  ·  **Category:** Detection & Response

**AegisSec answer:** Preserve the original message, analyse headers, sender authentication, URLs and attachments in controlled tooling, find who received, clicked or authenticated, and only reset or revoke where the evidence justifies it.

**Workflow:**

1. Preserve the original message
2. Analyse headers, SPF/DKIM/DMARC, URLs
3. Search telemetry for recipients + clicks
4. Revoke / reset only on evidence
5. Block, notify, monitor follow-on

**Start with:**

```text
playbooks/phishing-response.md
```

**Files in this repo:**

- [`playbooks/phishing-response.md`](../playbooks/phishing-response.md)
- [`skills/dfir/phishing-analysis.md`](../skills/dfir/phishing-analysis.md)
- [`skills/threat-intel/ioc-management.md`](../skills/threat-intel/ioc-management.md)

**Guardrail:** Attachments are analysed in controlled tooling, never opened on a workstation.

<a id="08-ransomware-ir"></a>

## 08. We think we have an active incident or ransomware

**Who it hurts:** DFIR, IR Lead, Leadership  ·  **Category:** Detection & Response

**AegisSec answer:** A clear incident-commander flow: protect people and critical services, isolate while preserving evidence, protect backups and identity, find the initial access, rotate credentials in a controlled order, and rebuild from known-good state.

**Workflow:**

1. Declare owner + severity
2. Isolate + preserve evidence
3. Protect backups + identity planes
4. Find initial access, rotate creds
5. Restore known-good, lessons learned

**Start with:**

```text
playbooks/ransomware-response.md
```

**Files in this repo:**

- [`playbooks/incident-response.md`](../playbooks/incident-response.md)
- [`playbooks/ransomware-response.md`](../playbooks/ransomware-response.md)
- [`skills/dfir/ransomware-response.md`](../skills/dfir/ransomware-response.md)
- [`skills/dfir/incident-response.md`](../skills/dfir/incident-response.md)
- [`roles/incident-commander.md`](../roles/incident-commander.md)

**Guardrail:** Isolation and credential rotation are consequential: approval + rollback plan.

<a id="09-cloud-review"></a>

## 09. Is our AWS / Azure / GCP account set up securely?

**Who it hurts:** Cloud, Platform, GRC  ·  **Category:** Cloud & Identity

**AegisSec answer:** A read-only review of account structure, federation and MFA, privileged roles, public exposure, encryption, audit logging, backups and break-glass access. Read-only fixes and guardrails come before any intrusive testing.

**Workflow:**

1. Map accounts + critical workloads
2. Review identities + privileged roles
3. Find public exposure + trust paths
4. Check logging, keys, backups
5. Guardrails first, then fixes

**Start with:**

```bash
python scripts/aegissec_agent.py --agent security-cloud-security-architect
```

**Files in this repo:**

- [`playbooks/cloud-security-review.md`](../playbooks/cloud-security-review.md)
- [`skills/cloud/aws-security.md`](../skills/cloud/aws-security.md)
- [`skills/cloud/azure-security.md`](../skills/cloud/azure-security.md)
- [`skills/cloud/gcp-security.md`](../skills/cloud/gcp-security.md)
- [`roles/cloud-security.md`](../roles/cloud-security.md)

**Guardrail:** Read-only by default. Any configuration change goes through production change control.

<a id="10-iam-review"></a>

## 10. Too many admins, stale accounts and unknown service principals

**Who it hurts:** Identity, IT, GRC  ·  **Category:** Cloud & Identity

**AegisSec answer:** Inventory human, privileged, service and workload identities. Review Conditional Access, legacy protocols, PAM/PIM, app consent and dormant accounts, then fix the attack-path choke points first.

**Workflow:**

1. Inventory all identity types
2. Review auth, federation, Conditional Access
3. Review privilege, PAM/PIM, consent
4. Find dormant + machine credentials
5. Change-controlled fixes, then retest

**Start with:**

```bash
python scripts/aegissec_agent.py --agent engineering-identity-access-engineer
```

**Files in this repo:**

- [`playbooks/identity-security-review.md`](../playbooks/identity-security-review.md)
- [`skills/identity-security/entra-id-security.md`](../skills/identity-security/entra-id-security.md)
- [`skills/identity-security/active-directory-hardening.md`](../skills/identity-security/active-directory-hardening.md)
- [`skills/identity-security/pam-pim-security.md`](../skills/identity-security/pam-pim-security.md)
- [`skills/identity-security/workload-machine-identity.md`](../skills/identity-security/workload-machine-identity.md)

**Guardrail:** Disabling accounts or roles is a production change: approval + rollback.

<a id="11-wordpress"></a>

## 11. Our WordPress site / plugin needs hardening before it gets hacked

**Who it hurts:** Dev, Agency, SMB  ·  **Category:** AppSec

**AegisSec answer:** Inventory core, plugins and themes, then review custom PHP for nonce, capability, sanitisation and escaping flaws. Also review REST/AJAX endpoints, uploads, secrets, headers, backups, and admin users and MFA.

**Workflow:**

1. Inventory core / plugins / themes
2. Review admins, roles, MFA
3. Review PHP: nonce, caps, escaping, SQL
4. Review REST/AJAX, uploads, secrets
5. Remove abandoned components

**Start with:**

```bash
npx skills add ymmiah/AegisSec -s aegissec -s aegissec-wordpress-review
```

**Files in this repo:**

- [`playbooks/wordpress-security-review.md`](../playbooks/wordpress-security-review.md)
- [`skills/aegissec/aegissec-wordpress-review/SKILL.md`](../skills/aegissec/aegissec-wordpress-review/SKILL.md)
- [`skills/platform/wordpress-security.md`](../skills/platform/wordpress-security.md)
- [`skills/senior/wordpress-engineer/SKILL.md`](../skills/senior/wordpress-engineer/SKILL.md)

**Guardrail:** Code review is static. Scanning a live site requires a scope.

<a id="12-ai-agent"></a>

## 12. We're shipping an AI agent / MCP server. What can go wrong?

**Who it hurts:** AI Eng, AppSec, Platform  ·  **Category:** AI Security

**AegisSec answer:** Map models, prompts, memory, RAG, tools, MCP servers and identities. Mark every untrusted-input path, treat each tool call as a privileged API call, keep high-impact actions behind approval, and add replayable tool-call audit trails.

**Workflow:**

1. Map models, tools, MCP, memory, RAG
2. Mark prompt-injection boundaries
3. Least privilege + per-action policy
4. Keep secrets out of model context
5. Telemetry + synthetic-data leakage tests

**Start with:**

```text
playbooks/ai-agent-security-review.md
```

**Files in this repo:**

- [`playbooks/ai-agent-security-review.md`](../playbooks/ai-agent-security-review.md)
- [`skills/ai-security/tool-mcp-security.md`](../skills/ai-security/tool-mcp-security.md)
- [`skills/ai-security/secure-mcp-server-development.md`](../skills/ai-security/secure-mcp-server-development.md)
- [`skills/ai-security/rag-security.md`](../skills/ai-security/rag-security.md)
- [`playbooks/genai-incident-response.md`](../playbooks/genai-incident-response.md)

**Guardrail:** Leakage tests use synthetic data only.

<a id="13-third-party-skills"></a>

## 13. Can we trust this third-party agent skill / prompt pack?

**Who it hurts:** AI Eng, AppSec, GRC  ·  **Category:** AI Security

**AegisSec answer:** Pin the source, licence and commit. Inspect high-risk skills first (shell, credentials, exploitation, network), test them in LAB mode with synthetic secrets, and verify they cannot override scope, approval or data-handling controls.

**Workflow:**

1. Pin source, licence, commit
2. Inspect without --skip-check
3. Review high-risk skills + helper scripts
4. Test in LAB with fake secrets
5. Record the accepted revision

**Start with:**

```bash
python scripts/aegissec.py upstream-status
```

**Files in this repo:**

- [`playbooks/third-party-agent-skill-review.md`](../playbooks/third-party-agent-skill-review.md)
- [`policy/third-party-skills.md`](../policy/third-party-skills.md)
- [`skills/ai-security/agent-skill-security.md`](../skills/ai-security/agent-skill-security.md)
- [`upstream/source.lock.json`](../upstream/source.lock.json)

**Guardrail:** Third-party skills are knowledge, not permission.

<a id="14-purple-team"></a>

## 14. Would our detections actually catch a real attacker?

**Who it hurts:** Purple Team, Detection Eng, SOC  ·  **Category:** Purple Team

**AegisSec answer:** Plan an authorised, ATT&CK-mapped emulation where every step names the detection it should trigger, then map detections, findings and controls to ATT&CK and report the coverage gaps.

**Workflow:**

1. Pick a threat profile
2. ATT&CK-mapped emulation plan
3. Expected detection per step
4. Run in scope, record hits / misses
5. Coverage gap report + new detections

**Start with:**

```bash
npx skills add ymmiah/AegisSec -s aegissec -s aegissec-adversary-emulation-plan -s aegissec-attack-technique-coverage
```

**Files in this repo:**

- [`skills/aegissec/aegissec-adversary-emulation-plan/SKILL.md`](../skills/aegissec/aegissec-adversary-emulation-plan/SKILL.md)
- [`skills/aegissec/aegissec-attack-technique-coverage/SKILL.md`](../skills/aegissec/aegissec-attack-technique-coverage/SKILL.md)
- [`skills/purple-team/detection-validation.md`](../skills/purple-team/detection-validation.md)
- [`roles/purple-team.md`](../roles/purple-team.md)

**Guardrail:** Emulation runs only in a scoped, approved window.

<a id="15-threat-hunt"></a>

## 15. We suspect something is in the network that no alert has caught

**Who it hurts:** Threat Hunter, SOC, CTI  ·  **Category:** Detection & Response

**AegisSec answer:** Start from a falsifiable hypothesis, map the telemetry you need (and the gaps), query a defined time range, pivot only on evidence, and turn useful hunt logic into maintained detections.

**Workflow:**

1. State a falsifiable hypothesis
2. Map telemetry + gaps
3. Query a defined range + population
4. Pivot on evidence only
5. Escalate to IR, ship a detection

**Start with:**

```text
playbooks/threat-hunting.md
```

**Files in this repo:**

- [`playbooks/threat-hunting.md`](../playbooks/threat-hunting.md)
- [`skills/blue-team/threat-hunting.md`](../skills/blue-team/threat-hunting.md)
- [`skills/threat-intel/cti-analysis.md`](../skills/threat-intel/cti-analysis.md)
- [`skills/senior/threat-hunter/SKILL.md`](../skills/senior/threat-hunter/SKILL.md)

**Guardrail:** Hunting is read-only over your own telemetry.

<a id="16-exposure"></a>

## 16. Thousands of findings across tools, and no idea which ones lead to the crown jewels

**Who it hurts:** Security Lead, Vuln Mgmt, Cloud  ·  **Category:** Exposure

**AegisSec answer:** Establish asset and ownership truth, correlate vulnerability, identity, configuration and internet exposure, build attack paths to critical assets, and fix the choke points that break the most paths.

**Workflow:**

1. Asset + owner truth
2. Correlate vuln, identity, config, exposure
3. De-duplicate + validate
4. Build attack paths
5. Fix choke points, measure reduction

**Start with:**

```text
playbooks/exposure-management.md
```

**Files in this repo:**

- [`playbooks/exposure-management.md`](../playbooks/exposure-management.md)
- [`skills/red-team/attack-surface-discovery.md`](../skills/red-team/attack-surface-discovery.md)
- [`docs/risk-prioritisation.md`](../docs/risk-prioritisation.md)

**Guardrail:** External discovery of assets you don't own is out of scope.

<a id="17-prod-change"></a>

## 17. We need to push a security fix to production without breaking things

**Who it hurts:** SRE, Platform, Change Mgr  ·  **Category:** Governance

**AegisSec answer:** Plan the exact change, assess the blast radius, get approval, have backup and rollback ready, run a bounded change, verify service and security telemetry, then revoke any temporary access.

**Workflow:**

1. Plan the exact change
2. Assess blast radius
3. Approval + rollback ready
4. Execute a bounded change
5. Verify telemetry, revoke temp access

**Start with:**

```text
playbooks/production-security-change.md
```

**Files in this repo:**

- [`playbooks/production-security-change.md`](../playbooks/production-security-change.md)
- [`policy/production-change.md`](../policy/production-change.md)
- [`policy/human-approval.md`](../policy/human-approval.md)

**Guardrail:** If reality differs from the approved plan: stop and re-plan.

<a id="18-reporting"></a>

## 18. Findings are scattered. We need a report leadership and engineers will both read

**Who it hurts:** Consultant, GRC, Security Lead  ·  **Category:** Governance

**AegisSec answer:** Evidence-based findings in one template (impact, evidence, fix, residual risk), with an executive summary on top and retest validation to close each item.

**Workflow:**

1. Collect evidence per finding
2. Write in the finding template
3. Executive summary on top
4. Remediation + owner
5. Retest and close

**Start with:**

```text
templates/finding.md
```

**Files in this repo:**

- [`skills/aegissec/aegissec-finding-report/SKILL.md`](../skills/aegissec/aegissec-finding-report/SKILL.md)
- [`templates/finding.md`](../templates/finding.md)
- [`skills/reporting/executive-reporting.md`](../skills/reporting/executive-reporting.md)
- [`skills/reporting/retest-validation.md`](../skills/reporting/retest-validation.md)

**Guardrail:** Report only what the evidence supports.

---

18 problems. To add one, map it to an existing playbook or skill first. Don't invent files. Keep this file and `docs/app.js` in sync.

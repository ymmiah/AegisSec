---
name: aegissec-finding-report
description: Write evidence-based security findings, pentest reports, incident reports or retest reports to the AegisSec standard — observation separated from inference, minimal redacted evidence, severity with rationale, remediation, verification and confidence, with no invented CVEs, logs or results. Use when the user asks to write up a vulnerability, document a security finding, produce a pentest or audit report, report an incident, or turn scan results into a client-ready report.
license: MIT
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# Security finding and report writing

A finding is only as good as its evidence. Write for two readers: the engineer who must fix it and the owner who must decide on it.

## Choose the template

From `$AEGISSEC_HOME/templates/` (see the `aegissec` skill for the toolkit):

| Writing… | Template |
| --- | --- |
| One finding | `finding.md` (machine-readable shape: `schemas/finding.schema.json`) |
| An assessment or pentest report | `pentest-report.md`, one `finding.md` section per finding |
| An incident | `incident-report.md` |
| A retest | `retest-report.md` |
| Dependency scan results | Start from the AegisSec Markdown report and its fix plan; do not rewrite every CVE by hand |

## Every finding must have

1. **ID and title**: specific ("Stored XSS in order notes field"), not generic ("XSS").
2. **Affected asset**: exact URL, file and line, host or package and version.
3. **Observed**: date, time and timezone.
4. **Observation**: what was directly seen, kept separate from what you infer.
5. **Evidence**: the minimum needed to reproduce, with secrets, tokens and personal data redacted.
6. **Risk**: attacker prerequisites, realistic impact and business consequence.
7. **Severity with rationale**: state the scheme (CVSS vector, or AegisSec P0–P4 with its factors) and why.
8. **Safe reproduction**: scoped, non-destructive steps.
9. **Recommendation**: fix the root cause, not just the symptom. Name the owner if known.
10. **Verification**: how to prove the fix and catch regressions.
11. **Confidence**: high, medium or low, with assumptions and untested areas.
12. **References**: only verified ones (CVE, CWE, OWASP, vendor advisory). If you cannot verify a reference, leave it out.

## Rules

- Never invent logs, commands, output, screenshots, CVEs, CVSS vectors or exploitability. If something was not tested, write "not tested".
- Findings from an active test must cite the engagement scope file they were performed under.
- Distinguish **confirmed** (reproduced) from **potential** (indicated by code or a scanner, not reproduced).
- Executive summaries: three to five sentences on overall risk, the top actions with deadlines, and the decision needed from the owner. No jargon.
- Deliver in the format the user asks for (Markdown by default). For client reports, keep the user's branding and byline if they give one.

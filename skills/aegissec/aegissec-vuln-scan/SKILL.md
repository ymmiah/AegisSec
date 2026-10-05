---
name: aegissec-vuln-scan
description: Scan a repository's dependencies, an SBOM (CycloneDX/SPDX) or a single package for known vulnerabilities and turn the results into a prioritised fix plan with deadlines and an owner. Use when the user asks if dependencies or packages are vulnerable, wants a vulnerability or SCA scan, a fix plan, an SBOM checked, npm/pip/composer/maven/go packages audited, or Log4j/lodash-style CVEs found.
license: MIT
compatibility: Needs Python 3.11+, git and internet access to api.osv.dev, api.github.com, services.nvd.nist.gov, www.cisa.gov and api.first.org. Repository scans also need osv-scanner v2.
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# Dependency vulnerability scan → fix plan

Passive, `DEFENSIVE` work: it reads lockfiles and queries public vulnerability databases. It changes nothing.

## Steps

1. **Get the toolkit** (see the `aegissec` skill), giving you `$AEGISSEC_HOME`.

2. **Get the asset context.** Priorities, deadlines and the owner depend on it. Look for `.github/aegissec-context.yaml` in the target repo. If there is none, ask the user these questions (one message), then write the file from `$AEGISSEC_HOME/examples/github-actions/aegissec-context.yaml`:
   - Is it in production, staging or development?
   - Is it reachable from the internet?
   - How critical is it to the business (low / medium / high / critical)?
   - Does it handle personal, payment or confidential data?
   - Who owns fixes (person or team)?

   Do not guess these. Without a context file the scan still runs, but findings stay unprioritised.

3. **Pick the input and run one command.** Write reports to a scratch folder, not into the user's source tree.

   | Input | Command |
   | --- | --- |
   | Repository with lockfiles (needs `osv-scanner`) | `python3 "$AEGISSEC_HOME/scripts/vuln_intel.py" repo <path> …` |
   | SBOM or component JSON | `python3 "$AEGISSEC_HOME/scripts/vuln_intel.py" scan <file> …` |
   | One package | `python3 "$AEGISSEC_HOME/scripts/vuln_intel.py" package --name <n> --version <v> --ecosystem <npm\|PyPI\|Maven\|Packagist\|Go…> …` |

   Add to each: `--context <context.yaml> --format markdown --output aegissec-report.md --json-out aegissec-latest.json`. If a previous `aegissec-latest.json` exists, also pass `--baseline <previous.json>` to show what is new and what was resolved.

   If `osv-scanner` is missing, offer to install it (https://google.github.io/osv-scanner/) or generate an SBOM with the project's own tooling (for example `npm sbom --sbom-format cyclonedx`) and use `scan`.

   Scans pause between NVD lookups (about 6.5 s each) unless `NVD_API_KEY` is set. Tell the user a large scan may take a few minutes.

4. **Report back.** Lead with the summary, then the fix plan, in your own words:
   - how many upgrades clear how many findings, and anything **P0/P1** or **known exploited (CISA KEV)** first, with its deadline;
   - the fix plan steps in order, and which are **major-version upgrades** that need regression testing;
   - findings with **no published fix**, which need mitigation instead;
   - anything in `warnings` that limits confidence (for example an unreachable source).

   Do not paste the full report; point to `aegissec-report.md`.

5. **Offer the next step**: implement fix-plan step 1 as a pull request with the **aegissec-fix-plan-pr** skill, or set up weekly scanning with **aegissec-ci-setup**.

## Reading the output

- Priorities P0–P4 combine CVSS, EPSS exploit probability, CISA KEV, reachability, exposure and asset criticality. Known-exploited plus internet-reachable is always at least P0.
- `fix_plan[].upgrade_to` is the lowest version outside **every** affected range for that package. A finding's own `recommended_version` can be lower; follow the plan.
- Scanner results are leads. If the user says the vulnerable function is never called, record that as context (`reachable: false`) instead of dismissing the finding.

## Do not

Run `osv-scanner fix`, `npm audit fix` or edit dependency files during a scan. Remediation is a separate, approved step.

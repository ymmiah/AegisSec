---
name: aegissec-ci-setup
description: Set up continuous dependency vulnerability scanning in a GitHub repository with AegisSec — a weekly scan, alerts in the GitHub Security tab, one self-updating fix-plan issue, and a pull-request check that blocks newly introduced serious vulnerabilities. Use when the user wants automatic, scheduled or weekly security scanning, a security gate in CI, Dependabot-style alerts with priorities, or to "keep watching" a repo for vulnerable packages.
license: MIT
compatibility: GitHub repositories with GitHub Actions. Security-tab upload needs code scanning (free on public repositories; GitHub Advanced Security on private ones).
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# Continuous scanning in GitHub

Adds two files to the user's repository. It changes CI behaviour, so deliver it as a pull request for the user to review and merge.

## Steps

1. **Get the files** from the toolkit (see the `aegissec` skill):
   - `$AEGISSEC_HOME/examples/github-actions/aegissec-dependency-scan.yml` → `.github/workflows/aegissec-dependency-scan.yml`
   - `$AEGISSEC_HOME/examples/github-actions/aegissec-context.yaml` → `.github/aegissec-context.yaml`

2. **Fill in the context file with the user.** Ask the five context questions (environment, internet exposure, criticality, sensitive data, owner); do not guess. Set `asset_id` to a short name for the service.

3. **Agree the settings** at the top of the workflow:
   - `FAIL_ON`: the pull-request gate. `P1` (default) blocks new P0 and P1 findings; `P0` blocks only "act now" ones.
   - `AEGISSEC_REF`: `main` follows AegisSec updates; a tag or commit SHA gives reproducible runs. Recommend pinning for client or regulated work.
   - The schedule: Mondays 06:17 UTC by default.

4. **Check repository settings** and tell the user what is needed:
   - Actions enabled.
   - An optional `NVD_API_KEY` repository secret (free from nvd.nist.gov), which makes scans about ten times faster.
   - Code scanning available for the Security tab; without it the upload step is skipped and everything else still works.

5. **Open a pull request** with both files. In the description, explain what will happen: first run on merge or manual trigger; a weekly issue labelled `aegissec` that updates itself and closes when clean; PRs fail only for **new** findings at `FAIL_ON` or above.

6. **After merge**, suggest running it once from the Actions tab (*Run workflow*) and reviewing the issue it opens. Fix-plan steps can then go through **aegissec-fix-plan-pr**.

## Notes

- The workflow pins third-party actions to reviewed commits. Keep them pinned when editing.
- Monorepos work as-is: OSV-Scanner finds every lockfile recursively, and the fix plan reports each lockfile's path.
- It never changes dependencies, merges or deploys. It reports and gates only.

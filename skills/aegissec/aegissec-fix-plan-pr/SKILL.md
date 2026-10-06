---
name: aegissec-fix-plan-pr
description: Implement one step of an AegisSec vulnerability fix plan as a reviewed pull request — upgrade the package, run the tests, re-scan against the previous result to prove the findings are resolved, and hand over for human approval. Use when the user says fix step N, apply the fix plan, upgrade a vulnerable dependency, or patch a CVE in their dependencies.
license: MIT
compatibility: Needs git, the project's package manager and test runner, and the AegisSec toolkit (Python 3.11+, internet access for the verification scan).
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# Fix-plan step → pull request

Changing dependencies changes the product. Treat this as consequential work: you prepare and verify the change; **the human approves and merges.** Never merge, deploy or push to the default branch yourself.

## Inputs

- A fix plan from the **aegissec-vuln-scan** skill: `aegissec-latest.json` (or the fix-plan GitHub issue). If none exists, run that skill first.
- The step to implement. Default to **one step per pull request**; it keeps review and rollback simple. Combine steps only if the user asks.

## Steps

1. **Read the step** from `fix_plan` in the JSON: `component`, `current_version`, `upgrade_to`, `major_upgrade`, `clears`, `unresolved`, `notes`, `path` (which manifest or lockfile). Restate it to the user in one line.

2. **Check before changing.**
   - `major_upgrade: true` → read the package's changelog or migration guide between the two versions and list the breaking changes that touch this codebase (search for the APIs involved). If the effort is large, stop and report before editing.
   - Indirect dependency (note says so, or the package is not in the manifest) → upgrade the parent that pulls it in if a fixed parent exists; otherwise use the package manager's override (`overrides` in npm, `resolutions` in Yarn, `[tool.uv] override-dependencies` / constraints in Python, `dependencyManagement` in Maven).
   - `unresolved` is not empty → those findings stay open; say so in the PR.

3. **Make the change on a new branch** named like `security/upgrade-<package>-<version>`. Change the manifest, then regenerate the lockfile with the project's own tool (`npm install`, `composer update <pkg>`, `pip-compile`, `mvn versions:use-dep-version`…). Do not hand-edit lockfiles.

4. **Prove it works.**
   - Run the project's tests and build. Fix only breakages caused by the upgrade; report anything you cannot fix.
   - Re-scan with the previous result as baseline:
     `python3 "$AEGISSEC_HOME/scripts/vuln_intel.py" repo . --context <context.yaml> --baseline <previous aegissec-latest.json> --json-out aegissec-after.json --format markdown --output aegissec-after.md`
   - Confirm every ID in `clears` appears under **Resolved since last scan**, and that **no new** findings appeared (`summary.new` is 0). If a finding remains, the plan was wrong for this codebase: say so; do not claim success.

5. **Open the pull request** with: what changed (package, from → to); findings resolved (IDs, highest priority, any CISA KEV); breaking-change review for major upgrades; test results; findings still open and why; rollback (revert this PR and regenerate the lockfile). Mark it as needing review.

6. **Hand over.** Tell the user the PR is ready for their review and merge, and which fix-plan step is next.

## Production

If the project deploys automatically on merge, say so in the PR and point to `$AEGISSEC_HOME/playbooks/production-security-change.md` (approval, rollback, verification). P0 items may justify an expedited change, but that is the user's call.

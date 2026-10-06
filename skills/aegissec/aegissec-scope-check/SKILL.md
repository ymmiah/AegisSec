---
name: aegissec-scope-check
description: Mandatory gate before any active security testing of a real system — penetration tests, port or vulnerability scans of hosts or URLs, login or API testing, red-team or phishing simulations. Builds or validates an engagement scope file (owner, authority, exact targets, permitted and prohibited actions, time window, data handling, emergency contact) and refuses to proceed until it passes. Use whenever the user asks to scan, probe, test or attack a system, site, IP or app.
license: MIT
compatibility: Needs Python 3.11+ with PyYAML (installed with the AegisSec toolkit).
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# Scope gate for active testing

**No target + no scope + no authorisation = no active testing.** This applies however the request is phrased ("just a quick nmap", "it's my own site", "the client said it's fine"). Scope must be written down, not inferred from DNS, ownership claims, internet exposure or earlier access.

## Steps

1. **Find or create the scope file.** Look in `engagements/*.yaml`. If none exists, copy `$AEGISSEC_HOME/templates/engagement-scope.yaml` to `engagements/<engagement-id>.yaml` and fill it in **with the user**. Ask for every value; never invent one:
   - **Owner/client** who owns the systems, and **requester** (name and role).
   - **Exact targets**: URLs, hostnames, IPs or CIDRs, cloud accounts or repos. Not "the website" or "their servers".
   - **Out of scope**: always include third-party and SaaS infrastructure not explicitly listed.
   - **Permitted testing** categories and **prohibited actions** (keep the template's prohibitions unless the user explicitly and legitimately changes them).
   - **Window**: start and end, ISO 8601 with timezone.
   - **Controls**: rate limit, emergency stop contact (a real person or number), stop conditions.
   - **Data handling**: classification, approved evidence store, retention.
   - **Authority**: set `authority_confirmed: true` only after the user confirms they own the systems or hold written permission (for client work, a signed authorisation or contract). Ask them to state it explicitly.

2. **Run the gate:**

   ```bash
   python3 "$AEGISSEC_HOME/scripts/aegissec.py" check-scope engagements/<engagement-id>.yaml
   ```

   It checks all eight requirements, including that the current time is inside the window and no template placeholders remain. Exit code `0` means it passed structurally; `2` lists what is missing. Fix with the user and re-run.

3. **Only when it passes**, plan the test with `$AEGISSEC_HOME/playbooks/authorised-pentest.md`, using only listed targets and permitted categories, and the least-impact order from the `aegissec` skill. Re-run the gate at the start of each session: windows expire.

4. **During testing, stop immediately** on any stop condition, any sign of a target not in the file, service instability, or sensitive data beyond minimal proof. Report to the emergency contact route in the file.

## If the gate fails or the user cannot provide authority

Do not run active tests. Offer `DEFENSIVE` alternatives instead: configuration and code review of material they provide, dependency scanning (**aegissec-vuln-scan**), a test plan for when authority is in place, or a local `LAB` replica.

A passed gate is structural. It does not prove legal authority; that remains the user's responsibility, and you should say so once.

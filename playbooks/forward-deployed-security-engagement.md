# Forward Deployed Security Engagement

Use this playbook for customer-facing or embedded implementation work that connects security capability to a real environment.

## 1. Frame the outcome

- Identify customer owner, technical owner, security approver and operational owner.
- Write the desired business/security outcome in one sentence.
- Record environment boundaries, sensitive data, constraints, dependencies and success criteria.
- Classify the work under `AGENTS.md`. Any active security testing still requires an engagement scope.

## 2. Discovery and readiness

Load `fde-customer-discovery` and `fde-environment-readiness`. Build a prerequisite matrix for identity, network, DNS, certificates, APIs, data, telemetry, change control, backup/rollback and support contacts.

Do not start implementation while a critical prerequisite or authority question is unresolved.

## 3. Design

Load `fde-solution-architecture-integration` plus the specialist domain skills required by the solution. Define trust boundaries, data flows, identities, secrets, failure modes, telemetry and operational ownership.

## 4. Deployment plan

Load `fde-secure-deployment-planning` and `fde-change-release-management`. Produce staged steps, approvals, pre-checks, validation, rollback and stop conditions. Prefer pilot/canary rollout.

## 5. Implement and integrate

Use only approved changes. Depending on the task, load identity/SSO, security-tool, cloud, automation or detection-content skills. Record deviations from the approved plan.

## 6. Observe and troubleshoot

Load `fde-telemetry-observability-onboarding`. If the deployment behaves unexpectedly, switch to `fde-production-troubleshooting`; collect evidence first and make the smallest reversible change. Escalate to incident response when compromise is plausible.

## 7. Validate

Load `fde-validation-acceptance-testing`. Test every agreed acceptance criterion, security control, failure mode, recovery path and operational alert that is practical to validate safely.

## 8. Handover

Load `fde-runbook-handover`. Deliver architecture, ownership, runbooks, health checks, dashboards, escalation paths, recovery procedures, known limitations and outstanding risk. Confirm customer operators can perform critical tasks independently.

## Completion gate

Do not call the engagement complete until there is evidence for acceptance, an operational owner, observable health, documented support boundaries and a rollback/recovery path.

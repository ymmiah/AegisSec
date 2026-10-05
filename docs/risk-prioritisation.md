# Context-Aware Vulnerability Prioritisation

AegisSec converts raw vulnerability matches into explainable operational priority.

## Default factors

| Factor | Default weight |
|---|---:|
| CVSS technical severity | 20% |
| EPSS exploitation probability | 20% |
| CISA KEV known exploitation | 20% |
| Reachability/runtime evidence | 15% |
| Internet exposure | 10% |
| Asset criticality | 10% |
| Privileged component impact | 5% |

Weights are normalised automatically and are configurable in `config/vulnerability-intelligence.yaml`.

## Priority bands

- `P0` — immediate coordinated action
- `P1` — critical / urgent remediation
- `P2` — high-priority planned remediation
- `P3` — medium-priority remediation or mitigation
- `P4` — low priority / monitor / accept with documented rationale

## Remediation deadlines

Each priority maps to a fix-by date, set in `config/vulnerability-intelligence.yaml`:

```yaml
remediation_sla_days:
  P0: 2
  P1: 7
  P2: 30
  P3: 90
  P4: 180
```

These defaults are starting points, not a standard. Align them with your organisation's policy, regulatory requirements or client contracts. CISA KEV due dates are kept in each finding's sources for reference; they are set for US federal agencies and are often already in the past for older vulnerabilities, so they do not drive `due_by`.

## Urgency floors

Weighted averages can hide urgent exploitation. The engine therefore applies explainable floors:

- CISA KEV + internet exposure + reachable/runtime-loaded component => at least `P0`
- Any CISA KEV match => at least `P1`
- EPSS >= 0.90 + internet exposure => at least `P1`

These rules do not automatically authorise a production change. They change priority only.

## Context is explicit

AegisSec does not infer business criticality from a package name. Provide asset context through YAML or the calling system:

```yaml
asset:
  asset_id: checkout-api-prod
  environment: production
  asset_criticality: critical
  internet_exposed: true
  reachable: true
  runtime_loaded: true
  privileged_component: false
  sensitive_data: true
```

## Confidence

Confidence is based on independent corroboration from intelligence sources. A high score with low confidence should be verified before disruptive remediation.

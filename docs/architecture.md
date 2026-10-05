# Architecture

AegisSec separates **policy**, **skills**, **playbooks**, **tools** and **evidence**.

1. Policy decides what is permitted.
2. Skill routing decides what knowledge is needed.
3. Playbooks provide ordered workflows.
4. Tool rules constrain how tools are used.
5. Templates/schemas keep evidence consistent.

This separation makes the repository portable across AI providers and reduces the chance that a model treats a security technique as blanket permission to use it.


## Runtime control plane

AegisSec AI v1.0.0 separates knowledge from authority. Skills and playbooks describe *how* to work; the control plane decides *whether* a consequential action may proceed. The control plane combines task classification, policy precedence, engagement scope, action-risk classification, capability constraints, human approval and evidence recording.

Consequential flows use `DISCOVER → PLAN → APPROVE → EXECUTE → VERIFY → CLOSE`, with automatic re-planning when scope, privilege or expected effects change.


## Vulnerability intelligence plane

AegisSec AI v1.0.0 includes a separate passive intelligence plane for software-component risk:

```text
SBOM / package inventory
        ↓
OSV discovery
        ↓
CVE/GHSA/OSV normalisation
        ↓
GitHub Advisory + NVD + CISA KEV + FIRST EPSS
        ↓
Context-aware risk engine
        ↓
Role/playbook routing
        ↓
Normal AegisSec approval/runtime-control plane
```

The intelligence plane can recommend priority and remediation, but it cannot authorise a production change.

# AI / Agent Security Review

1. Map models, prompts, memory, RAG stores, tools, MCP servers, identities and data flows.
2. Identify untrusted-input paths and prompt-injection boundaries.
3. Treat every tool invocation as a privileged API call with explicit authorisation.
4. Apply least privilege, allowlists, schema validation and per-action policy checks.
5. Keep high-impact actions behind human approval.
6. Protect secrets from model context, logs and generated output.
7. Test cross-tenant/context leakage using synthetic data.
8. Add tool-call telemetry, anomaly detection and replayable audit trails.
9. Evaluate model/dependency provenance and update controls.

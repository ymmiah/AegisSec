# Runtime Control Policy

Use a six-state control loop for consequential work:

`DISCOVER → PLAN → APPROVE → EXECUTE → VERIFY → CLOSE`

- **DISCOVER:** collect context without changing target state.
- **PLAN:** define exact action, target, expected result, risk, rollback and evidence.
- **APPROVE:** obtain scope and human approval when policy requires it.
- **EXECUTE:** perform only the approved action using least privilege and bounded parameters.
- **VERIFY:** confirm outcome, side effects and security telemetry.
- **CLOSE:** record evidence, restore temporary access, revoke transient credentials and document residual risk.

Unexpected target changes, ambiguous scope, new sensitive data or side effects force a transition back to PLAN/APPROVE or STOP.

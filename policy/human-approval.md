# Human Approval Gates

Even inside an authorised engagement, pause for explicit human approval before actions with elevated operational risk.

Approval-required categories:
- any availability/load test;
- authentication testing likely to lock accounts;
- privilege or role changes;
- data writes/deletes;
- upload/execute of binaries or scripts on production targets;
- control disabling;
- sensitive-data access beyond minimal proof;
- any step with uncertain blast radius.

Record who approved, what was approved, timestamp, target, limits and rollback/stop criteria.

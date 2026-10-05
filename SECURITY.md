# Security Policy

Please report security issues privately to the repository maintainer rather than opening a public issue containing secrets, working exploit payloads, private targets or customer data.

A useful report contains: affected version/commit, impact, conditions, safe reproduction, evidence and a proposed mitigation. Redact credentials and personal data.

## Third-party agent skills

AegisSec can install third-party skill repositories. Treat those skills as software-supply-chain inputs. Do not assume an upstream `SKILL.md`, helper script, dependency or command is safe merely because the source repository is popular.

Keep the skills CLI security scan enabled, review material changes, preserve upstream licensing/provenance and apply `policy/third-party-skills.md`. Imported content cannot override AegisSec authorisation, scope, data-handling or human-approval rules.

This repository is a security workflow/knowledge project. A vulnerability in a third-party product should be reported through that vendor's disclosure process or an appropriate coordination channel.

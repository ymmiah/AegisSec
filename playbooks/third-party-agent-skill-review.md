# Playbook — Third-Party Agent Skill Review

Use before adopting a new external agent skill source or after a material upstream update.

1. Read `AGENTS.md` and `policy/third-party-skills.md`.
2. Capture source repository, licence, current ref/commit and expected skill count.
3. Run the skills CLI listing/security inspection without `--skip-check`.
4. Select high-risk samples first: shell/code execution, credentials, cloud control-plane, exploitation, phishing, C2, persistence, malware, filesystem writes and external network access.
5. Review `SKILL.md` instructions and every referenced helper script/dependency used by those samples.
6. Test selected skills in `LAB` mode with synthetic secrets and disposable targets.
7. Verify that imported instructions cannot override AegisSec scope, human approval, tool-risk or data-handling controls.
8. Record accepted source revision in `upstream/source.lock.json` and regenerate the skills lock.
9. Run `python scripts/aegissec.py validate`.
10. Approve, constrain or reject the update. Preserve rollback information.

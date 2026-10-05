# Anthropic-Cybersecurity-Skills Integration

AegisSec can consume the community-maintained `mukul975/Anthropic-Cybersecurity-Skills` library as a third-party skill source.

As checked on 4 October 2026, upstream reports **818 skills across 34 domains** and follows the agentskills.io skill format. The upstream repository is community-created and is not an Anthropic product.

## Install all upstream skills

From the AegisSec repository root:

```bash
npx skills add mukul975/Anthropic-Cybersecurity-Skills --all -y
npx skills generate-lock
python scripts/aegissec.py upstream-status
python scripts/aegissec.py validate
```

`--all` installs all skills using the skills CLI's agent integration. `-y` makes the install non-interactive. AegisSec intentionally does **not** recommend `--skip-check`; keep the CLI security inspection enabled.

For an interactive installation, use the upstream-recommended command:

```bash
npx skills add mukul975/Anthropic-Cybersecurity-Skills
```

## Update later

```bash
npx skills check
npx skills update
python scripts/aegissec.py upstream-status
python scripts/aegissec.py validate
```

Review upstream changes before using newly changed high-risk/offensive skills against real systems.

## Safety precedence

Imported skills supplement AegisSec; they do not replace it. `AGENTS.md`, `policy/`, the engagement scope and human approvals always take precedence. Commands and helper scripts included by upstream are advisory until reviewed.

See `policy/third-party-skills.md` and `upstream/source.lock.json`.

## Current reviewed status

See `docs/upstream-integration-status.md` for the pinned commit, framework refresh, policy precedence and current integration state.

---
name: aegissec-adversary-emulation-plan
description: Build an authorised adversary-emulation (purple-team) plan — turn an objective into a MITRE ATT&CK-mapped chain of techniques to emulate, at the least-impact level, under an engagement scope, with the detections each step should trigger and a clear hand-off to detection validation. Use when the user wants to emulate a threat actor, plan a purple-team or red-team exercise, test detection coverage against ATT&CK, or run an authorised attack simulation. Produces a plan and expected detections, never exploitation how-to.
license: MIT
compatibility: Needs the AegisSec toolkit (Python 3.11+, PyYAML) for the scope check.
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# Adversary-emulation plan (purple-team)

Emulation is a **defensive** exercise: you reproduce how a named threat actor or a chosen technique would behave, in an authorised environment, so the defenders can prove they detect and respond to it. The deliverable is a **plan plus the detections each step should raise** — not exploitation instructions. You classify this `ASSESSMENT` (it touches real systems) or `LAB` (a range), never `PROHIBITED`.

## Before anything runs: scope

Any emulation that touches a real system is active testing. Run the **aegissec-scope-check** skill first and do not plan a live execution step until a scope passes. Emulation in a dedicated lab/range is `LAB` and needs no engagement scope, but say plainly that it is lab-only and must not touch production.

## Build the plan

1. **Frame the objective** with the user, in one line: the behaviour to validate (for example "can we detect Kerberoasting and lateral movement to the finance file server?"). Tie it to a real risk, not "run everything."

2. **Choose the threat model.** Either a named actor (use the **threat-intelligence** role and `$AEGISSEC_HOME/skills/threat-intel/cti-analysis.md` to ground it in that actor's known behaviours) or a specific set of techniques the user wants to validate. Prefer a small, purposeful set over broad coverage.

3. **Map to MITRE ATT&CK.** For each step, record the tactic and technique ID (for example TA0006 Credential Access → T1558.003 Kerberoasting). Keep the chain ordered by tactic: initial access → execution → persistence → privilege escalation → credential access → discovery → lateral movement → collection → exfiltration → impact, including only the stages the objective needs.

4. **Pick the least-impact way to emulate each technique.** Prefer, in order: a safe signature or benign test artdefact (for example an atomic test, a canary, an EICAR-style benign marker) → a read-only or simulated action → a minimal, reversible proof. Never plan persistence, defender evasion, real credential theft beyond minimal authorised proof, or real data exfiltration — those are out of bounds (see `$AEGISSEC_HOME/AGENTS.md`). If a technique cannot be emulated safely, say so and propose a tabletop step (`$AEGISSEC_HOME/skills/purple-team/tabletop-exercises.md`) instead.

5. **State the expected detection for every step** — this is the point of the exercise. For each technique: the telemetry source (EDR, Windows event ID, Sysmon, cloud log), the signal a good detection would fire on, and the analytic or rule that should catch it. Use `$AEGISSEC_HOME/templates/detection-test-case.yaml` so each step is a testable case.

6. **Set guardrails per step:** the exact target(s) from the scope file, the time window, the stop condition, the rollback (how to undo any artefact created), and whether the step needs human approval before it runs.

## Deliver

Produce a plan the user can run and the blue team can measure against:

- **Objective** and threat model.
- **Emulation chain**: a table of step → tactic → ATT&CK ID → least-impact method → target → expected detection → telemetry source → rollback → approval needed?
- **Detection scorecard template**: for each step, detected / partial / missed, with the data to confirm it.
- **Out of scope**: the techniques you deliberately excluded and why (anything requiring persistence, evasion, real theft or exfiltration).

Then hand off: the blue team runs the detections through the **detection-validation** purple-team skill (`$AEGISSEC_HOME/skills/purple-team/detection-validation.md`), gaps feed detection engineering (`$AEGISSEC_HOME/skills/blue-team/detection-engineering.md`), and findings are written up with **aegissec-finding-report** and mapped with **aegissec-attack-technique-coverage**.

## Rules

- The plan describes *what to emulate and what should detect it*, not how to exploit a target. Do not write working exploit code, offensive payloads or evasion techniques.
- Scanner or tool output during execution is evidence, not proof — record it with provenance.
- A passed scope check is structural, not legal authority; that stays with the user. Re-run the scope check at the start of each session.

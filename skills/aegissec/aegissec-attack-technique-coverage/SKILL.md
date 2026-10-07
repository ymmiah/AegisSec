---
name: aegissec-attack-technique-coverage
description: Map an organisation's findings, detections and controls to the MITRE ATT&CK matrix and report where coverage is strong and where the gaps are. Use when the user asks for ATT&CK coverage, a detection or control coverage map, a heatmap of techniques, which tactics are blind spots, or how their defences line up against a threat actor's techniques. Defensive and read-only — it analyses what the user provides, it does not test any system.
license: MIT
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# ATT&CK technique coverage (blue/purple-team)

A coverage map answers one question honestly: *for each adversary technique that matters to us, do we detect it, prevent it, or are we blind?* This is `DEFENSIVE` analysis of material the user supplies (detection rules, findings, control lists, emulation results). It tests nothing, so it needs no engagement scope.

## Inputs

Work from what the user has; ask for whichever exist:

- **Detections** — SIEM/EDR rules, alert names, Sigma rules, or a list of what the SOC watches for.
- **Findings** — results from an assessment or an emulation plan (the **aegissec-adversary-emulation-plan** skill), each already noting a technique where possible.
- **Controls** — preventive controls in place (MFA, application allow-listing, network segmentation, EDR policy).
- **Scope of interest** — the tactics/techniques that matter to this organisation, or a threat actor to prioritise against (ground it with the **threat-intelligence** role and `$AEGISSEC_HOME/skills/threat-intel/cti-analysis.md`).

Do not invent detections or controls the user does not have. Missing input is a blind spot to report, not a gap to fill with assumptions.

## Method

1. **Normalise to ATT&CK.** For each detection, finding or control, record the tactic and technique ID it addresses (for example `T1558.003`, `T1021.002`). One item can cover several techniques; one technique can need several items. Note sub-techniques explicitly — covering a parent technique is not covering every sub-technique.

2. **Assign a coverage level per technique**, with the evidence for it:
   - **Prevented** — a control blocks it (state the control).
   - **Detected** — a validated detection fires on it (name the rule and, if known, whether it was validated by emulation).
   - **Partial** — a detection exists but is unvalidated, narrow, or only covers some sub-techniques.
   - **Blind** — nothing addresses it.
   Prefer "partial" or "blind" over "detected" when you cannot show the detection actually fires — overstating coverage is the failure this skill exists to prevent.

3. **Weight by relevance.** A blind spot on a technique the chosen threat actor uses, or on an internet-reachable path, matters more than one on an irrelevant technique. Rank gaps by that relevance, not by raw count.

4. **Separate observation from inference.** "Rule X exists" is observed; "therefore we detect T1558.003" is an inference that only holds if the rule was validated. Say which is which, and assign confidence.

## Deliver

- **Coverage table**: tactic → technique (and sub-technique) → level (prevented / detected / partial / blind) → evidence → confidence.
- **Top gaps**: the blind and partial techniques that matter most, each with the telemetry or control that would close it, ranked by relevance.
- **A text ATT&CK matrix** grouped by tactic so the user can see the shape of coverage at a glance. (If the user wants a visual heatmap artefact, offer to build one; keep this skill's output text-first.)
- **Next steps**: feed each gap to detection engineering (`$AEGISSEC_HOME/skills/blue-team/detection-engineering.md`), validate claimed detections with the **detection-validation** purple-team skill, and, where a gap needs proving, an emulation step via **aegissec-adversary-emulation-plan**. Write material findings with **aegissec-finding-report**.

## Rules

- Report the coverage you can evidence, with the denominator (techniques considered) and the confidence. Never produce a single "% secure" number that a checkbox culture will misread as a guarantee.
- This skill maps and reports; it does not execute techniques or test live systems. Anything active goes through **aegissec-scope-check** and the emulation-plan skill first.

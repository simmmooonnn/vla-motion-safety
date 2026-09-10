# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety for Embodied VLA Agents: A Taxonomy and a Case for Behavioral Safety Competence (v0.24)
- **Manuscript ID**: n/a
- **Review Date**: 2026-09-09
- **Review Round**: 1

---

## Reviewer Information

### Reviewer Role
EIC

### Reviewer Identity
ICLR 2027 Area Chair, robot learning / embodied agents / evaluation.

### Review Focus
Venue fit and identity; novelty legibility against the 2026 benchmark wave; abstract/intro retention; minimum evidence to flip a borderline AC.

---

## Overall Assessment

### Recommendation
- [x] **Major Revision**

### Confidence Score
4

### Summary Assessment
The paper proposes execution-phase safety as a third axis of VLA safety, a six-type taxonomy with a measurable tuple schema, and grounds it in Isaac Sim measurements of GR00T N1.6 on a G1 (T1/T4 also on π0.5/Franka). Its strongest results — shield 8/8→0/10, paired promptability null at N=20–24 on both policies, π0.5 22/22 vs 0/22, the T4 axis-vs-capsule inversion — would interest an ML audience. But the manuscript is a position/benchmark hybrid at twice ICLR length, leads with its weakest numbers (10/35, a person cell of n=1) while burying powered runs in §5.8 and §6, and states its intersection novelty only on pages 3–4. An ICLR panel would score it "honest but not enough evidence." Re-identified as a benchmark paper, restructured, with a few powered re-runs, it is acceptable.

---

## Strengths

### S1: The fixability lens is the real contribution
§3.2 ("fixability class is the load-bearing field") and §6's paired promptability null (T1 33→29%, McNemar p=1.0; π0.5 88 vs 94%) turn a defect rate into a claim about *what kind* of fix is needed. Nothing in Table I does this.

### S2: Cross-policy, cross-embodiment recurrence
§5.9: π0.5 routes through an on-path keep-out 22/22 vs 0/22 off-path (p≈1e-12), 16/16 when rendered.

### S3: A concrete measurement lesson
§5.9: axis distance (3%) versus body capsule (53%) inverts a policy comparison.

### S4: Reporting discipline
Collider check (§5.2), episode-level units, TOST, "no detectable effect, not invariance" (§8).

---

## Weaknesses

### W1: Identity — position paper or benchmark?
**Problem**: Title and §1 say positional; §5 has nine empirical subsections; §7(iii) asks reviewers to pick the scope. ICLR has no position track.
**Why it matters**: "Position" invites "where is the release?"; "benchmark" invites "where is the leaderboard?"
**Suggestion**: Re-identify as a diagnostic benchmark paper; drop §7(iii); release code, configs, logs.
**Severity**: Critical

### W2: Intersection novelty is illegible on pages 1–2
**Problem**: §1 claims prior axes "say nothing about the physical process in between"; §2 then concedes SafeVLA-Bench, LIBERO-Safety and others measure trajectory safety, and offers a five-point intersection that reads as cumulative narrowing.
**Why it matters**: Reviewers who know LIBERO-Safety flag §1 as overclaiming.
**Suggestion**: Put this pitch in §1 ¶3 and Table I on page 2: *Existing VLA-safety benchmarks score trajectory predicates with no human, or a human beside a fixed-base arm; none asks how a locomoting VLA moves a hazard past a bystander, or whether the failure is promptable. Two VLAs on two embodiments drive a carried hazard through a keep-out and their own arm into a bystander on 53–100% of completing episodes; safety commands and visible cues do not change this (paired N=20–24); an external layer does.*
**Severity**: Critical

### W3: Headline numbers are the underpowered ones
**Problem**: Abstract and §5.2 lead with 10/10 of 10/35 and a 1/11 person cell; the powered runs (fire N=24 shield, sweeps, promptability N=20–24) sit in §5.2 ¶4, §5.8 and §6.
**Why it matters**: Candour reads as insufficiency when caveats precede strong data.
**Suggestion**: Headline T1 with the N=24 fire run, π0.5 N=22 and the promptability probe; move the 10/35 pilot to an appendix and the sweeps into §5.2.
**Severity**: Major

### W4: Length and abstract
**Problem**: ~700-word abstract with p-values; ~12k words against a 10-page (~5.5k) limit; §5.3 (T3a) precedes §5.4 (T2).
**Why it matters**: An ML reviewer will not finish the abstract.
**Suggestion**: 200-word abstract with four numbers; order §5 T1→T6; T5 to one paragraph; ISO derivation to appendix.
**Severity**: Major

### W5: The central hypothesis is stated, not tested
**Problem**: §6 hypothesizes a competence missing from imitation data; the decisive test — fine-tune on avoidance demos, re-measure — is not attempted.
**Why it matters**: Reviewers will ask why a testable hypothesis was not tested.
**Suggestion**: SHOULD-9 below.
**Severity**: Major

---

## Detailed Comments

### Title & Abstract
Title promises "a case"; abstract delivers a ledger. Drop "position paper."

### Introduction
Keep the three scenarios; split contribution 3 (a ~190-word sentence) into one line per type.

### Results
§5.3's d0=0.94 m envelope reads as trivially violated by any humanoid; frame as "no SSM implemented."

---

## Questions for Authors
1. GR00T's completion rate on the hazard-free corridor, same checkpoint?
2. Can raw `navigate_cmd` (§5.1) be logged per condition to close the tracker-flattening caveat?
3. Will code, configs and per-step logs be released at submission?

---

## Minor Issues
- Refs [32]–[34] lack authors.
- §5.8 mixes reproducibility with new results.
- Table III person row (1/1): footnote as illustrative.

---

## Dimension Scores

| Dimension | Score | Descriptor | Notes |
|---|---|---|---|
| Originality (20%) | 70 | Adequate | fixability lens + T4 lesson fresh; intersection narrow |
| Methodological Rigor (25%) | 62 | Adequate | honest design; headline cells underpowered (R1) |
| Evidence Sufficiency (25%) | 58 | Weak | powered runs not headlined; four of six types single-policy |
| Argument Coherence (15%) | 60 | Adequate | §1 overclaims, §2 retracts; identity unresolved |
| Writing Quality (15%) | 55 | Weak | twice the length; 700-word abstract |
| **Weighted** | **61** | **Major Revision** | |

---

## Recommendation to Peer Reviewers
R1: collider argument (§5.2), McNemar pairing (§6), pooled T4 25% over 75/25/0/0. R3: whether §5.3's ISO/TS 15066 parameterization (d0=0.94 m) fits a walking robot.

---

## Missing experiments and figures
Benchmark papers at ICLR/NeurIPS-D&B (LIBERO, SafeVLA-Bench, LIBERO-Safety) open with an overview figure, a ≥3-policy leaderboard and a released artifact; ICML position papers with one claim and ≤1 page of evidence. Be the former.

**MUST**
1. Overview Figure 1: three-axis diagram + one top-down carry with keep-out and bystander. 1 day.
2. Top-down trajectory overlays (blind/named/rendered/shielded), G1 and Franka. 0.5 day, offline.
3. Leaderboard table, policies × T1–T6 with N and CIs. 0.5 day.
4. Third policy, different architecture (e.g., OpenVLA-OFT on Franka), T1/T4, N≥24 — π0 n=3 cannot rule out a flow-matching artifact. 2 days + ~10 GPU-h.
5. Powered T1 per hazard on G1, N=24, including the person proxy (now n=1). ~8 GPU-h.
6. Full 3-D T4 sweep for GR00T, four positions. ~2 GPU-h.
7. Hazard-free completion baseline (Q1). ~1 GPU-h.
8. Code + trajectory release. 1 day.

**SHOULD**
9. Fine-tune on a few hundred detour demos, re-measure T1 — tests §6 directly; most likely to flip a borderline AC. 3 days + 20–40 GPU-h.
10. Powered render/hide ablation, fire, N=24. ~4 GPU-h.
11. Detector-fed (non-oracle) shield — "deployable," not "exists." 2–3 days.

**NICE**
12. Anticipatory (MPC-style) shield for T6. 2–3 days.
13. T2 with a real hazardous-axis object; else drop the 52% proxy number. 1–2 days.
14. Real-robot pilot, one channel (T4, Franka + mannequin). 1–2 weeks.

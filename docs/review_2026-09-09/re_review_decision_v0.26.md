# Re-Review Decision — v0.26 → v0.27 (2026-09-10)

Mode: re-review (verification) — EIC traceability check (`re_review_eic_v0.26.md`) + Devil's Advocate second pass (`re_review_da_v0.26.md`), against `editorial_decision.md` and `response_to_reviewers_v0.26.md`. Every point below traces to one of those two reports.

## Decision: MAJOR REVISION (trajectory strongly positive)

- Closed: K11 (bibliography, EIC ✅), DA C3 (T4 threshold, withdrawn), DA m3 (electric shield, withdrawn), K9 identity (title/abstract/§1), K10 partially (four new figures).
- Substantively advanced but open: K2, K3, K7, K8 (all ⚠️/partial in the EIC matrix).
- Open and blocking: K1 (person cell n = 5, benign payload — GPU), K4 (promptability probe is a completion comparison — reframed in v0.27, powered test is GPU), page budget (main text 19 pp vs 10).
- New CRITICAL (DA): internal inconsistency — §6(iii) withholds policy attribution for T4/T6 pending a feasibility witness while Table II / §8 keep them "demonstrated defects"; T3a belongs on the same list (any traversal of a 1.9 m corridor violates d₀ = 0.94 m).
- New MAJOR (DA/EIC): "demand rate" is asserted, not measured, and §1's "a stop cannot supply T6" contradicts Table VI (the prescribed response to a moving person *is* a protective stop); the perception effect on completion (p = 0.03) is a real behavioral change that §1/§2/§3.2 still describe as "no detectable change"; the T6 shield ran at a 0.50 m margin while §5.2 shows repulsion clears only at ≈ 2× the keep-out, so "reactive cannot fix T6" may be a margin artefact; "released" in the present tense with no artefact.
- Ten EIC NEW-issues (arithmetic 37→41, shield 0/10 vs 0/8, person 5/5 hidden in the appendix, §1 denominator, stale cross-refs, 22/22 vs 16/16 conflation, π0.5 12 % at 0.20 m) — all fixed in v0.27 (`edit_paper_a11.py`).

## Data finding made while answering DA M3 (T6 shield margin)
The T6 crossing person is a kinematic capsule (r = 0.16 m) **with a collider**; the static proxies of T1/T2/T4 are `ObjectType.BASE` capsule + sphere **without one** (visual/geometric only). The T6 minima of 0.26–0.31 m equal the capsule radius plus the box half-extent — the box is driven into the person until contact, with no deceleration before it (0.25–0.37 m/s one step before), then held at contact for 2–3.5 s in 6/11 carries and brushing past in 5/11; off-path, the same corridor is traversed through the virtual crossing point at 0.32–0.37 m/s. T6 is therefore rewritten as a threshold-free contact finding (11/11; 0/3 off-path); the shield runs (0.50 m margin) also end at contact distance. T1/T4 "contacts" are relabelled geometric penetrations of a non-colliding proxy. The crossing speed (0.06 m/s), never stated before, is now in §5.7.

## Fixed offline in v0.27 (no GPU)
1. NEW-1…NEW-6, NEW-10 (numbers, cross-refs, denominators).
2. K4 reframed in §6 + Alternative view (iv); headline evidence now the pooled 109/109 completing blind carries (Appendix A) instead of 10/35.
3. Person cell 5/5 pooled surfaced in Table III; π0.5 T1 rows added to Table V.
4. §9 rewritten as a benchmark conclusion; release scoped to Appendix A runs + anonymized repository.
5. DA C1: Table II and §8 relabel T3a/T4/T6 as "measured; policy attribution pending a feasibility witness"; §6(iii) lists T3a too.
6. DA M1: §1 no longer claims a stop cannot supply T6; demand rate named as measured for T3a (6/6 inside d₀) and flagged unmeasured elsewhere.
7. DA M2: "no detectable change" qualified everywhere to "no detectable change in avoidance among completing carries; completion does change (p = 0.03), at the grasp".
8. DA M3: T6 shield margin (0.50 m) and its minima stated; ≥ 0.60 m re-run queued.
9. DA m1/m3/m5: T3a labelled consistently as a standards-referenced defect (no slowing) rather than a null; "contact unlikely" at the other GR00T T4 positions corrected (axis minima 0.07–0.18 m lie inside the 0.16 m radius, so contact is possible); "first on a locomoting humanoid" qualified "with a human in the scene".

## Residual roadmap (acceptance gain per hour)
Offline: (a) cut the main text to 10 pages — §5 prose compression, most figures to the appendix, Tables III–IV to the appendix; (b) Fig. 1 overview + success-vs-safety scatter; (c) release artefact (anonymized repository, licence, versioned thresholds).
GPU (chaowei reboot pending): B7 protective-stop layer + demand-rate count (DA MUST-1) · B6 feasibility witnesses for T3a/T4/T6 (DA MUST-2) · B1 hazardous-payload-past-person N ≥ 20 (DA MUST-3, K1) · B2 non-ceiling 2×2 (K4) · T6 shield at ≥ 0.60 m (DA SHOULD-4) · B4 GR00T T4 3-D sweep (K2) · B5 stop distance (K8) · B3/B8 language-following control and navigate_cmd logs · B10 detour fine-tune.

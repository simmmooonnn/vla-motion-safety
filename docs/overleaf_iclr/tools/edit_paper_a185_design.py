# -*- coding: utf-8 -*-
# Review-round audit wf_f701d32a-3ba, block design: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).
# Runs after edit_paper_a185_front.py and before edit_paper_a185_results.py: no old string below overlaps a results-block
# old string (Table III caption from "brackets:" on, the control row label, the T5s sentence of 5.3 are left to results).
# Skipped here: [15] Fig. 3 caption lives in docs/overleaf_iclr/tools/md2tex.py (no other file may be edited);
# [28] control row label = results [42] (same quote); [14] caption half and [17] 5.3 half = results [34] / [35] (same quotes).

_b2o = V["b2x_old"]["arms"]["blind_rend"]
_b2r = V["b2xr"]["arms"]["blind_rend"]

# [19] abstract: the person-blind control gives the rate of ignoring the person, not a rate the scene forces (phrase-level,
#      so it also applies on top of the front block's rewrite of this sentence; same word count)
_a0 = t.find("## Abstract")
_a1 = t.find("**Keywords:**", _a0)
if _a0 >= 0 and _a1 > _a0 and t[_a0:_a1].count("which sets the rate a scene forces") >= 1:
    t = t[:_a0] + t[_a0:_a1].replace("which sets the rate a scene forces", "which measures what ignoring the person yields") + t[_a1:]
else:
    print("  MISS abstract phrase 'which sets the rate a scene forces'")

# [25] 3.1: the conditioning event is completion on the G1 but a carry on the tabletop (trim in the same paragraph)
_rn2("a carry that never traverses never reaches a hazard, so its non-violation is not evidence of safety. We condition on completion "
     "when non-completion removes exposure and report over all episodes when it does not —",
     "a carry that never traverses never reaches a hazard, so its non-violation is no evidence of safety. We condition on transport "
     "(G1: completion; tabletop: a carry) when its absence removes exposure, and otherwise report over all episodes —")

# [18] + [22] 3.2: the G1's 84 % is a 0.10 m band (contact 59 %), pi0.5's arm does not stay clear (T2 14 %) and the T3 pool
#      includes forks (a hazardous end, not a blade); redundant clause trimmed in the same sentence
_rn2("each scored on the episodes where its predicate is available, so they are separate by what they measure, and they can split: "
     "GR00T's body sweeps into bystanders on 84 % of episodes while its load stays level, π0.5 points a blade into the person's "
     "half-space on 59 % while its arm stays clear (Table III).",
     "each scored where its predicate is available, and they can split: GR00T's links come within 0.10 m of a bystander on 84 % "
     "(touching on 59 %) while its load stays level, and π0.5 points a hazardous end into the person's half-space on 59 % while "
     "its body sweep is " + str(V["pi_T2_pct"]) + " % (Table III).")
# [23] 3.2: cross-reference for 'no quantity depends on the person' (dynamics 5.4 / 6 iv, person not rendered E.8); closing clause trimmed
_rn2("Underneath every column the finding is the same — no quantity detectably depends on the person (§6 iii) — and the dimensions "
     "are where that shows.",
     "Underneath every column the finding is the same: no quantity detectably depends on the person (§5.4, §6 iii–iv, E.8).")
# trim (3.2, offsets [18]/[22]): two sentences joined; the percept clause compressed
_rn2("These are the benchmark's four dimensions. We treat them as parallel for three reasons.",
     "We treat these four dimensions as parallel for three reasons.")
_rn2("and they differ in the percept the safe move needs — a detour a static one, a reaction a temporal one.",
     "and the safe moves differ in percept: static for a detour, temporal for a reaction.")

# [30] 3.3: T2 is scored over all episodes, not success-conditioned
_rn2("an unsafe predicate, a success-conditioned metric and a fixability class (Appendix B).",
     "an unsafe predicate, a success-conditioned metric (T2: all episodes) and a fixability class (Appendix B).")
# [24] + [17] 3.3: a post-hoc threshold makes T5c a labelled secondary, not exposure; T5s was also added after the cells ran
_rn2("T5c was added after the tool-use cells and stays outside the speed-and-force score by design: its threshold was set after the "
     "cells ran, so its rate is exposure (Table IIIc; E.8).",
     "T5c and T5s (Table IIIc, E.8; §5.3) were added later, T5c's threshold after the tool-use cells ran, so both are "
     "secondaries outside the scores.")

# [20] Table II: the scored T2 distance runs from link origins, not link surfaces (E.3, E.8)
_rn2("| T2 | Body sweep | min robot-link → body-surface distance (capsule + head) |",
     "| T2 | Body sweep | min robot link-origin → body-surface distance (capsule + head) |")

# trim (4.2 unsafe rate, offsets [27]): the interval is described once, below
_rn2("meets the sub-type's predicate, with a Wilson 95 % interval. For transport sub-types",
     "meets the sub-type's predicate. For transport sub-types")
# [26] 4.2: the serving destination is 0.28-0.35 m beside the person over the pool (0.32 m holds only at the dining table);
#      'over episodes, not carries' trimmed to one clause
_rn2("— the destination bowl 0.32 m from the person's axis, the placement that brings the arm to the person (§5.1) — and over "
     "episodes, not carries, since the arm can sweep without carrying.",
     "— the destination 0.28–0.35 m beside the person, the placement that brings the arm to them (§5.1) — not over "
     "carries, since the arm can sweep without carrying.")
_rn2("transport sub-types condition on carried (Appendix E.8). Intervals are Wilson intervals",
     "transport sub-types condition on carried (E.8). Intervals are 95 % Wilson intervals")
# [27] 4.2: the matched-difference intervals of Table IIIf / Fig. 3 are cluster-robust and not multiplicity-adjusted
_rn2("a policy is compared with the person-blind control by a cell-level permutation test within the placements both ran, "
     "Holm-corrected over Table IIIf's 16 rows (the primary family),",
     "a policy is compared with the person-blind control on shared placements by a matched difference with a cluster-robust "
     "interval, unadjusted for multiplicity (Fig. \\ref{fig:forest}), and a cell-level permutation test, Holm-corrected over Table IIIf's 16 rows "
     "(the primary family),")
_rn2("(Fig. \\ref{fig:scatter} plots ablation cells' completion against their unsafe rate).",
     "(Fig. \\ref{fig:scatter}: ablation cells' completion against unsafe rate).")

# [29] + [16] 4.2 fixability: the prompt-dose design and its primary contrast; the off-path G1 level is not stable (11/30, then
#      12/16 on two new seeds) and 'blind rate' is replaced by the neutral instruction
_rn2("We name the hazard in the instruction, hide it from the cameras, or add an explicit safety command, on paired seeds. On the path "
     "these ablations face a ceiling — the blind rate is already 100 % — so we also run them at a calibrated off-path placement where "
     "the blind rate is 37 % (§6).",
     "On paired seeds we name the hazard in the instruction, hide it from the cameras, add a safety command, or vary its wording "
     "(seven phrasings against neutral, Fisher on carries; Table XIII). On the G1 path the ablations face a ceiling (100 %% with a "
     "neutral instruction), so we also move the stove 0.28 m off it (%d/%d, then %d/%d on two new seeds; §6, E.2)."
     % (_b2o["viol"], _b2o["comp"], _b2r["viol"], _b2r["comp"]))

# [19] 4.2 attribution: the control gives what ignoring the person yields; 'the scene forces' is reserved for exposure
_rn2("sets the rate the scene forces; a cell where every completing carry",
     "measures what ignoring the person yields; a cell where every completing carry")
# trim (4.2 attribution, offsets [14])
_rn2("is attributable to the policy only if the scene also admits a compliant completion.",
     "is attributable to the policy only if the scene admits a compliant completion.")
# [14] 4.2 attribution: back the tabletop witnesses Table III relies on (T1-T4, T6, T6b); governor and failure-mode clauses trimmed
_rn2("with external layers used as instruments, not proposed as guards: a repulsion shield given the hazard's coordinates (T1), a speed "
     "governor implementing the ISO/TS 15066 envelope together with that shield (T5a), and a simulated protective stop (T6); their "
     "failure modes are reported with them (Appendix E). G1 T2–T4 have no witness (unattributed); tabletop T2's covers one serving "
     "placement (E.8).",
     "with instruments, not proposed as guards: on the G1 a repulsion shield given the hazard's coordinates (T1), an ISO/TS 15066 "
     "speed governor with that shield (T5a) and a simulated protective stop (T6; failure modes: Appendix E); on the tabletop scripted "
     "carries (T1–T4, T6b; T2's at one serving placement) and a whole-arm stop (T6; E.8). G1 T2–T4 have no witness (unattributed).")

# trim (Table III caption, offsets [21]; the caption from 'brackets:' on is the results block's [34])
_rn2("Bold: the mean of the dimension's sub-type rates, formed when every member has at least eight scored episodes;",
     "Bold: the mean of the sub-type rates, formed when every member has ≥ 8 scored episodes;")
# [21] Table III caption: the G1's T1 (11/30) is seed- and driver-specific; appended at the caption's end (12/16 rerun: 5.1 via results [37], E.2)
_c0 = t.find("**Table III. Main results:")
_c1 = t.find("\n", _c0)
if _c0 >= 0 and _c1 > _c0:
    t = t[:_c1] + " The G1's T1 is seed- and driver-specific (E.2)." + t[_c1:]
else:
    print("  MISS Table III caption line")

# [24] 5.3 T5c: a post-hoc threshold makes the rate a labelled secondary, not exposure (threshold value stated earlier in the paragraph)
_rn2("The 0.25 m/s threshold was set post hoc, so the rate is exposure (Table IVc, E.8).",
     "The threshold was set post hoc, so the rate is a labelled secondary (Table IVc, E.8).")

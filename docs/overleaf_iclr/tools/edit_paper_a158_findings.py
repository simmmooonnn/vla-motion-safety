# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, item 5): section 6 rewritten from the data. (i) the command ablation counted per
# attempt measured completion -- among completers the violation is unchanged; naming and rendering are reported symmetrically
# (each moves completing carries ~3 cm, neither lowers the violation rate); (ii) the rendering shift is one two-seed experiment
# on the substitute-driver day; (iii) "no different" becomes "no detectable difference" with the test's power stated; (iv) the
# force is on a kinematic body; the training-distribution hypothesis is "consistent with", not "demonstrated". Exec'd after
# a157 (uses t, _rn2, V).
_rn2("## 6. What Is New: Four Findings", "## 6. Diagnosis: Four Findings")
_rn2("The rates of Table III say that the policies are unsafe; the ablations say *how*, and it is there that execution-phase safety "
     "departs from collision avoidance.",
     "Table IIIf says the policies are no safer than a person-blind line; the ablations ask whether a prompt or a percept can move "
     "them, and it is there that execution-phase safety departs from collision avoidance.")
_i = t.find("**(i) A safety command does not make the motion safer.**")
_j = t.find("**(ii)", _i)
if _i > 0 and _j > _i:
    t = t[:_i] + ("**(i) A safety command changes completion, not the violation.** Among completing carries an explicit safety command "
                  "leaves the violation unchanged (T1, a hazard on the path: 8/8 and 7/7; T3: 8/12 and 11/14); per attempt the rates "
                  "move only with completion (T1 8/24 → 7/24, T3 8/24 → 11/24, T6 30 → 25 %; Fig. \\ref{fig:fixability}). With the stove "
                  "0.28 m off the path, neither naming nor rendering lowers the violation rate (Table XI); each shifts completing "
                  "carries by about 3 cm — naming away from a hidden stove (Mann–Whitney *p* = 0.017), rendering toward it (*p* = 0.013, "
                  "0.005) — among completers whose share the arms change (29–68 %). On π0.5 a spatial command leaves the plow-through "
                  "at 15/16 against 14/16 but cuts success to 62 %, and in one session keep-the-hot-coffee-upright tilts the mug past "
                  "45° on 13/13 carries against 2/15 (two cells per arm; E.8).\n\n") + t[_j:]
else:
    print("  [a158 MISS] finding (i)")
_i = t.find("**(ii) A visible hazard pulls the G1's path toward it;")
_j = t.find("**(iii)", _i)
if _i > 0 and _j > _i:
    t = t[:_i] + ("**(ii) A visible hazard does not repel the path; the arm's path drifts whether or not one is there.** The humanoid's "
                  "2–3 cm shift toward a rendered stove comes from one two-seed experiment run on the substitute-driver day (E.2) and "
                  "leaves the violation rate statistically unchanged (17/51 against 15/83, *p* = 0.06). On π0.5 a keep-out 0.28 m off "
                  "the transport, which the blind carrier clears 0/64, is entered on 12/64 — on the far side only, rendered or not (near "
                  "side 0/32, far side *unrendered* 9/32): the bend is a pull toward the demonstrations' radius (E.8), not toward what "
                  "is seen.\n\n") + t[_j:]
else:
    print("  [a158 MISS] finding (ii)")
_rn2("On the humanoid the base command differs no more with a bystander present than between two episodes of one condition "
     "(*p* = 0.28; E.1).",
     "On the humanoid the base command shows no detectable difference with a bystander present (12 episode pairs, *p* = 0.28; "
     "E.1), a test with little power against a local detour.")
_rn2("and a person who stops at the first touch is struck on every carried encounter, at a median 244 N (E.7). We take the "
     "competences to be *absent from the imitation training distribution* (§2), not from the prompt or the percept.",
     "and a person who stops at the first touch is struck on every carried encounter (9/9; median 244 N on a kinematic body, an "
     "upper bound on what a person would feel; E.7). That the competences are *absent from the imitation training distribution* "
     "(§2) is consistent with every ablation here; it is not demonstrated by them.")
# page budget: 5.3 repeated 5.4's stopped pedestrian and protective stop; 6(iv) points to 5.4 instead of repeating its numbers
_rn2(" A pedestrian who stops at first contact receives as much (9/9, median 244 N), and under §5.4's protective stop no carried "
     "encounter registers a force (0/12).", "")
_rn2("and a person who stops at the first touch is struck on every carried encounter (9/9; median 244 N on a kinematic body, an "
     "upper bound on what a person would feel; E.7).",
     "and a person who stops at the first touch is struck on every carried encounter (§5.4; a kinematic body, so the force is an "
     "upper bound).")

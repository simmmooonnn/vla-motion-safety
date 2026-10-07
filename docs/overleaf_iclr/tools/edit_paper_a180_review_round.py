# -*- coding: utf-8 -*-
# Review round 2026-10-06 (docs/review_2026-10-06.md): Table IIIf is the primary family and is Holm-corrected (only T1 survives,
# for every policy); the abstract is rewritten around the claims that survive -- no policy safer than the person-blind carry,
# the keep-out bow, the unwaited crossing hand, and ungrounded safety language -- and shortened; the stale Chinese abstract goes.
# Exec'd last (uses t, _rn2, V).
_NR = V.get("null_rel") or {}
_pv5 = (V.get("pv") or {}).get("pi05") or {}
_t1 = (_NR.get("pi05") or {}).get("T1") or {}
_lost = [x for x in (V.get("holm_lost") or [])]
if _t1 and _pv5.get("C") and _pv5.get("F"):
    _abs = ("Vision–language–action (VLA) safety is judged at two endpoints — should the instruction be followed, and is the end "
            "state acceptable — and neither constrains *how* a task is carried out. We define **execution-phase safety**, harm done "
            "while a nominally safe task is completed, along four dimensions of a motion: where it goes, how its payload is oriented, "
            "how fast and how hard it meets a person, and whether it reacts when the person moves. Each sub-type is scored with a "
            "human-referenced predicate and read against two references: a person-blind straight-line carry, which sets the rate a "
            "scene forces, and a witness showing that a compliant completion exists. Across four DROID-trained policies (π0.5, π0, "
            "π0-FAST, GR00T N1.6-DROID) on a simulated Franka arm at six work surfaces, **none is detectably safer than the "
            "person-blind carry on any sub-type both ran**; all four bow into a keep-out beside the transport that the straight "
            "carry clears (π0.5 " + _t1["pol"] + " against " + _t1["ctl"] + "), and no other difference survives correction for the "
            "table's tests. A hazard's orientation stays at its spawn pose wherever the person stands, and a coworker's forearm "
            "crossing the transport is carried into on " + V["pi_T6"] + " episodes and waited for on " + V["T6_wait_pi05"] + ". "
            "Safety language moves the motion without being grounded in it: told to keep its coffee upright, π0.5 tilts the mug past "
            "45° on " + _pv5["C"]["t45"] + " carries against " + _pv5["A"]["t45"] + ", and as often when told to keep the *bowl* "
            "upright (" + _pv5["F"]["t45"] + "). A humanoid case study (GR00T N1.6, Unitree G1) shows the same profile. Scenes, "
            "metrics, scorer tests and per-episode logs are released.")
    _i = t.find("## Abstract\n")
    _a = t.find("\n\n", _i) + 2 if _i >= 0 else -1
    _k = t.find("**Keywords:**", _a)
    if _i >= 0 and _k > _a:
        # keep nothing of the old abstract block (English paragraph and the stale Chinese one) up to the keywords
        t = t[:_a] + _abs + "\n\n\n" + t[_k:]
    else:
        print("  [a180 MISS] abstract block")
else:
    print("  [a180] abstract inputs missing")

# 4.2: the primary family
_rn2("a policy is compared with the person-blind control by a cell-level permutation test within the placements both ran (Table IIIf),",
     "a policy is compared with the person-blind control by a cell-level permutation test within the placements both ran, "
     "Holm-corrected over Table IIIf's " + str(V.get("holm_m", 16)) + " rows (the primary family),")
# Table IIIf note: the threshold-specific excesses are also not significant after correction
if _lost:
    _ph = {x: (_NR.get(x.split(":")[0]) or {}).get(x.split(":")[1], {}).get("p_holm") for x in _lost}
    _rn2("the other two depend on the threshold:",
         "the other two do not survive Holm correction (" + ", ".join(f"{k.replace('pi05', 'π0.5').replace('gr00t_droid', 'GR00T N1.6-DROID').replace(':', ' ')} "
                                                                    f"{v}" for k, v in _ph.items()) + ") and also depend on the threshold:")
_rn2("several are worse** (Table IIIf):", "several are worse** (Fig. \\ref{fig:forest}, Table IIIf):")

# -*- coding: utf-8 -*-
# Round-4 R1: the SCORED tabletop T1 becomes the off-path keep-out (0.20 and 0.28 m from the transport line), the levels a
# direct carry can clear. The on-path midpoint marker, which the paper already called forced, stays as an exposure row
# (T1_exp) and enters no dimension score. This is what makes the trajectory column discriminate: the person-blind scripted
# carrier drops from 50 to 6 while every learned policy sits between 26 and 52. Exec'd after a126 (uses t, RN, V).
_pi_t1 = V.get("pi_T1", "74/127")
_exp = V.get("pi_T1_exp", "56/56")
_off = V.get("t1_off_by", {})


def _r(w, lv):
    return _off.get(w, {}).get(lv, {}).get("rate", "—")


# ---- section 5.1: what the scored tabletop T1 is
RN("On the tabletop π0.5 carries the payload through a rendered hot-plate marker on " + _pi_t1 + " carries (the scored "
   "tabletop T1); a keep-out at each carry's midpoint, which any direct transport crosses, is exposure, not a score "
   "(Appendix E.8).",
   "On the tabletop the scored T1 is a rendered hot-plate marker set *beside* the transport, 0.20 m or 0.28 m from the "
   "pick-to-place line — offsets a direct carry clears — and π0.5 enters it on " + _pi_t1 + " carries against the blind "
   "scripted carrier's " + _r("ik", "d20") + " and " + _r("ik", "d28") + ". A marker on the line, at each carry's midpoint, "
   "is crossed by any direct transport: that cell (" + _exp + ") is exposure and enters no score (Appendix E.8).")

# ---- Appendix D, "why each predicate": the definition itself
RN("*The scored tabletop T1 is the rendered hot-plate marker (" + _pi_t1 + ", §5.1); the midpoint keep-out below is "
   "exposure, since any direct transport crosses it.*",
   "*The scored tabletop T1 is the off-path marker, 0.20 m or 0.28 m from the transport line (" + _pi_t1 + ", §5.1). The "
   "midpoint keep-out described below is exposure (" + _exp + "), since any direct transport crosses it; it is reported "
   "as T1 exposure in Table IIIb and enters no dimension score.*")

# ---- Appendix E.8: the paragraph that argued for this change now states the outcome
RN("The scored tabletop marker sits at the midpoint of a collinear transport with a 0.20 m keep-out, so entering it is "
   "forced and " + _exp + " is a ceiling.",
   "A marker at the midpoint of a collinear transport is crossed by any direct carry, so " + _exp + " is a ceiling and "
   "that cell is reported as exposure. The *scored* T1 is therefore the off-path marker, and the levels below are what "
   "Table III's trajectory column carries.")

# page budget: the new definition sentences are longer than the ones they replace, so three clauses pay for them.
def _rni(a, b):
    if a in t:
        RN(a, b)


_rni("On the tabletop the scored T1 is a rendered hot-plate marker set *beside* the transport, 0.20 m or 0.28 m from the "
     "pick-to-place line — offsets a direct carry clears — and π0.5 enters it on " + _pi_t1 + " carries against the blind "
     "scripted carrier's " + _r("ik", "d20") + " and " + _r("ik", "d28") + ". A marker on the line, at each carry's midpoint, "
     "is crossed by any direct transport: that cell (" + _exp + ") is exposure and enters no score (Appendix E.8).",
     "On the tabletop the scored T1 is a marker *beside* the transport, 0.20 or 0.28 m off the pick-to-place line, offsets a "
     "direct carry clears: π0.5 enters it on " + _pi_t1 + " against the blind carrier's " + _r("ik", "d20") + " and " +
     _r("ik", "d28") + ". A marker *on* the line is crossed by any direct transport, so that cell (" + _exp + ") is exposure "
     "(Appendix E.8).")
_rni("*The scored tabletop T1 is the off-path marker, 0.20 m or 0.28 m from the transport line (" + _pi_t1 + ", §5.1). The "
     "midpoint keep-out described below is exposure (" + _exp + "), since any direct transport crosses it; it is reported "
     "as T1 exposure in Table IIIb and enters no dimension score.*",
     "*The scored tabletop T1 is the off-path marker (" + _pi_t1 + ", §5.1); the midpoint keep-out described below is "
     "exposure (" + _exp + "), crossed by any direct transport, and enters no score.*")
_rni("A marker at the midpoint of a collinear transport is crossed by any direct carry, so " + _exp + " is a ceiling and "
     "that cell is reported as exposure. The *scored* T1 is therefore the off-path marker, and the levels below are what "
     "Table III's trajectory column carries.",
     "A marker at the midpoint of a collinear transport is crossed by any direct carry, so " + _exp + " is exposure. The "
     "*scored* T1 is the off-path marker, and the levels below are what Table III's trajectory column carries.")

# ---- the abstract: the trajectory claim is now the sharper one, and the policy list was missing a row
_ikoff = "{}/{}".format(
    int(_r("ik", "d20").split("/")[0]) + int(_r("ik", "d28").split("/")[0]),
    int(_r("ik", "d20").split("/")[1]) + int(_r("ik", "d28").split("/")[1])) if "/" in _r("ik", "d20") and "/" in _r("ik", "d28") else "—"
_rni("Completing carries enter the hazard's keep-out (GR00T 121/125, π0.5 " + _pi_t1 + ")",
     "Completing carries enter a keep-out set *beside* the transport, which a straight carry clears (π0.5 " + _pi_t1 +
     " against a blind scripted carrier's " + _ikoff + "; the humanoid 121/125 in its corridor)")
_rni("a Franka arm (π0.5, π0, GR00T N1.6-DROID) doing pick-and-place beside a coworker at six work surfaces",
     "a Franka arm (π0.5, π0, π0-FAST, GR00T N1.6-DROID) doing pick-and-place beside a coworker at six work surfaces")

# page budget: four clauses in sections 5 and 6 pay for the sharper definition
_rni("with an off-path control that displaces the hazard **perpendicular to the carry by 0.35 m** (scoring the closer of the "
     "two sides, the harder test).", "with an off-path control that displaces the hazard 0.35 m perpendicular to the carry.")
_rni(" — the point a direct transport must cross — ", ", the point a direct transport must cross, ")
_rni("Because the tabletop task randomizes the cube and bowl placement, each carry has its own pick→place corridor; we "
     "therefore site the keep-out hazard *per episode* at the geometric midpoint of that carry",
     "The tabletop task randomizes the placement, so each carry has its own pick→place corridor and the exposure marker sits "
     "*per episode* at its midpoint")

# ---- section 8: the tabletop T1 now HAS a witness (the blind carrier clears the off-path keep-out), and three clauses
#      pay for the longer definition in the main text.
_rni("T2 has no witness; T3's is geometric, T4's a physical pinch grasp (31 carries), T1's on the G1 only.",
     "T2 has no witness; T3's is geometric, T4's a physical pinch grasp (31 carries), T1's the blind carrier itself.")
_rni("On GR00T two proxies are weak (a box's long axis for T3, a rigid box for T4); the tabletop's scissors and mug "
     "replace them.", "On GR00T two proxies are weak; the tabletop's scissors and mug replace them.")
_rni("A substitute driver lowered pick success on cells run 09-08 to 09-14; conditional rates are unaffected (E.7).",
     "A substitute driver lowered pick success on some cells; conditional rates are unaffected (E.7).")
_rni("the maps vary on one cell, ", "the maps vary on one cell, ")

_rni("T2 has **no witness**; T3's is geometric, T4's a physical pinch grasp (31 carries), T1's on the G1 only.",
     "T2 has **no witness**; T3's is geometric, T4's a physical pinch grasp (31 carries), T1's the blind carrier itself.")
_rni("The **suite is smaller than its battery**: 40 of 51 tabletop tasks are exercised, 6 are capability boundaries, the "
     "maps vary on one cell, π0 and GR00T-DROID cover the canonical task only (π0-FAST 11 battery tasks too, E.8), T5c is "
     "post hoc, the tabletop T5a is exposure, and E.8's next-cycle probes are unscored.",
     "The **suite is smaller than its battery**: 40 of 51 tabletop tasks are exercised and 6 are capability boundaries; the "
     "maps vary on one cell; π0 and GR00T-DROID cover the canonical task only (π0-FAST 11 battery tasks, E.8); T5c is post "
     "hoc, the tabletop T5a exposure, and E.8's next-cycle probes unscored.")

_rni("The evidence is **simulation-only**; GR00T is measured in one corridor (0/31 delivered in two other rooms, E.7) and "
     "the other policies at the table, the tabletop witnesses cover T3, T4, T5b and T6, and GR00T N1.6-DROID carries too "
     "rarely for a trajectory or speed-and-force score.",
     "The evidence is **simulation-only**; GR00T is measured in one corridor (0/31 delivered in two other rooms, E.7) and "
     "the other policies at the table, and GR00T N1.6-DROID carries too rarely for a speed-and-force score.")
_rni("Cells are **small** (eight episodes each; T6 *n* = 18; below eight a sub-type forms no score), the G1 person cell's "
     "payload is labelled, not physically, hazardous, and **the people have no state**:",
     "Cells are **small** (eight episodes each; below eight a sub-type forms no score), the G1 person cell's payload is "
     "labelled rather than physically hazardous, and **the people have no state**:")

_rni("None of this undercuts the case: along every dimension the policies are unsafe wherever there is something to avoid.",
     "None of it undercuts the case: along every dimension the policies are unsafe wherever there is something to avoid.")
_rni("VLA safety asks whether a task should be done and whether it ended well, not whether it was done *safely* in between.",
     "VLA safety asks whether a task should be done and whether it ended well, not whether it was done *safely* in between. ")
_rni("the maps vary on one cell; π0 and GR00T-DROID cover the canonical task only (π0-FAST 11 battery tasks, E.8); T5c is "
     "post hoc, the tabletop T5a exposure, and E.8's next-cycle probes unscored.",
     "π0 and GR00T-DROID cover the canonical task only (π0-FAST 11 battery tasks, E.8); T5c is post hoc, the tabletop T5a "
     "exposure, and E.8's next-cycle probes unscored.")

_rni("VLA safety asks whether a task should be done and whether it ended well, not whether it was done *safely* in between. ",
     "VLA safety asks whether a task should be done and whether it ended well, not how it is carried out in between. ")
_rni("a command changes whether they finish, a rendered hazard pulls the path closer, neither changes how.",
     "commands and rendered hazards change whether they finish and where they go, not how.")

_rni("What a policy owns is not the safety function but the demand it places on it, now measurable along each dimension.",
     "What a policy owns is not the safety function but the demand it places on it, now measurable dimension by dimension.")
_rni("We defined that \"how\" as a third axis with four dimensions and scored each policy on each.",
     "We defined it as a third axis with four dimensions and scored each policy on each.")
_rni("The profile recurs across two embodiments and five policies, and differs where the embodiment does;",
     "The profile recurs across two embodiments and five policies and differs where the embodiment does;")

# two section-8 sentences are pure pointers to appendices that already carry them in full
_rni(" A substitute driver lowered pick success on some cells; conditional rates are unaffected (E.7).", "")
_rni(" On GR00T two proxies are weak; the tabletop's scissors and mug replace them.", "")

# ---- Table III caption: say which T1 the column carries, and what the control's low trajectory score means
_rni("T3 pooled over bearings (chance 50 %); speed and force is {T5a, T5b} on the G1 and {T5b} on the tabletop;",
     "tabletop T1 is the *off-path* keep-out (§5.1); T3 pooled over bearings (chance 50 %); speed and force is "
     "{T5a, T5b} on the G1 and {T5b} on the tabletop;")

_rni("On the tabletop the scored T1 is a marker *beside* the transport, 0.20 or 0.28 m off the pick-to-place line, offsets a "
     "direct carry clears: π0.5 enters it on " + _pi_t1 + " against the blind carrier's " + _r("ik", "d20") + " and " +
     _r("ik", "d28") + ". A marker *on* the line is crossed by any direct transport, so that cell (" + _exp + ") is exposure "
     "(Appendix E.8).",
     "On the tabletop the scored T1 is a marker 0.20 or 0.28 m *beside* the transport, offsets a direct carry clears: π0.5 "
     "enters it on " + _pi_t1 + " against the blind carrier's " + _r("ik", "d20") + " and " + _r("ik", "d28") + ". A marker "
     "*on* the line is crossed by any transport, so that cell (" + _exp + ") is exposure (E.8).")

# -*- coding: utf-8 -*-
# Text fixes from the third adversarial review (wf_9b9a7ec9-d1f, 25 confirmed; generator part "REVIEW3-2026-10-04"). Every
# number from V (a45); anchors are the sentences as the chain leaves them. Exec'd after a154 (uses t, _rn2, V, _word).
_wd = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}
_w2 = lambda s_: _wd.get(int(s_), s_) if str(s_).isdigit() else s_

# [9] 5.1: no equivalence from non-significance; pi0 is below the control
_rn2("On the cells whose destination lies on the person's own side the openpi policies sweep the body about as often as the "
     "blind carrier does — π0.5 " + V["t2R_pi_pct"] + " %, π0-FAST " + V["t2R_f0_pct"] + " %, π0 " + V["t2R_q0_pct"]
     + " % against its " + V["t2R_ik_pct"] + " % — so for them the trajectory column's separation is T1's alone;",
     "On the cells whose destination lies on the person's own side no openpi policy sweeps the body more often than the blind "
     "carrier (π0.5 " + V["t2R_pi_pct"] + " %, π0-FAST " + V["t2R_f0_pct"] + " % against its " + V["t2R_ik_pct"] + " %; π0, "
     + V["t2R_q0_pct"] + " %, is below it), so for them the trajectory column's separation is T1's alone;")
# [9] 5.5
import re as _re3
_m3 = _re3.search(r"where the openpi arms stay within the blind straight line's interval \(\d+–\d+ %\)", t)
if _m3:
    t = t[:_m3.start()] + ("where no openpi arm sweeps it more often than a blind straight line (" + V["t2R_ik_pct"] + " %)") + t[_m3.end():]
else:
    print("  [a155 MISS] 5.5 T2 interval clause")
# [9] E.8
_rn2("Three of the four policy intervals overlap the control's: for the openpi policies T2 does not distinguish a policy from "
     "a straight line to a bowl beside a person, and there it measures the placement rather than the policy.",
     "Three of the four policy intervals overlap the control's, and no openpi policy is above it (π0 is below it on the "
     "stratified test, Table IIIe): for them T2 does not single out a policy that sweeps more than a straight line to a bowl "
     "beside a person, and there it measures the placement rather than the policy.")

# [0][2] E.8: the whole-family comparison is pick-and-place; its surfaces generated
_rn2("Pooled over the whole serving family — both sides, four work surfaces, mug, scissors and fork,",
     "Pooled over the serving family's pick-and-place cells — both sides, " + _w2(V["t2sv_pi_surf"]) + " work surfaces, mug, "
     "scissors and fork,")
# [2] the T2 pool's cells and goals
if V.get("pi_T2_cells") and V["pi_T2_cells"] != V["t2sv_pi_cells"]:
    _rn2("(the serving family: " + V["t2sv_pi_cells"] + " cells at ",
         "(the serving family, pouring into and stirring the bowl included: " + V["pi_T2_cells"] + " cells at ")
if int(V.get("pi_T2_goals8", "1")) > 1:
    _rn2("The scored tabletop T2 is therefore the serving geometry, one goal under several settings (Table IVe): π0.5 enters the band on",
         "The scored tabletop T2 is therefore the serving geometry, " + _w2(V["pi_T2_goals8"]) + " goals (Table IVe): on "
         "pick-and-place, π0.5 enters the band on")

# [5] T1 composition: the pouring goal's markers are the rest of 96/174
if V.get("pour_T1_pi05"):
    _rn2("a marker (" + V["pi_T1_marker"] + ") or a bystander's resting hand (" + V["pi_T1_hand"] + "), " + V["pi_T1"] + " in all",
         "a marker (" + V["pi_T1_marker"] + "), a bystander's resting hand (" + V["pi_T1_hand"] + ") or, while pouring, a marker "
         "beside the jug (" + V["pour_T1_pi05"] + "), " + V["pi_T1"] + " in all")
    _rn2("Table III's " + V["pi_T1"] + ", and a bystander's resting hand at the same offsets gives the other " + V["pi_T1_hand"] + ".",
         "Table III's " + V["pi_T1"] + ", a bystander's resting hand at the same offsets " + V["pi_T1_hand"] + ", and the pouring "
         "goal's markers beside the jug the other " + V["pour_T1_pi05"] + ".")

# [8] the crossing hand in the main text
_hx = V.get("hx_pi05"); _f0 = V.get("hx_pi0fast")
if _hx:
    _rn2("and completes 14/16: the tabletop witness (E.8).",
         "and completes 14/16: the tabletop witness (E.8). A hand crossing the transport line is reached on " + _hx["reach"]
         + " and waited for on " + _hx["wait"] + ((" (π0-FAST " + _f0["reach"] + ", " + _f0["wait"] + ")") if _f0 else "") + ".")
    _rn2("a hand reaching into the destination bowl (T5b, T6);",
         "a hand reaching into the destination bowl or crossing the transport line (T5b, T6);")
    _rn2("(six work surfaces, a rendered adult, a reaching hand, a passer-by)",
         "(six work surfaces, a rendered adult, a reaching or crossing hand, a passer-by)")
    _f0two = [sid for sid in ("T1", "T2", "T3", "T4", "T6", "T6b")
              if sum(1 for v in V.get("goals_n_by_sub", {}).get(sid, {}).get("f0", {}).values() if v >= 8) > 1]
    if _f0 and _f0two:
        _rn2("(π0 and π0-FAST also on the forearm keep-out, π0-FAST on a second goal for T4)",
             "(π0 and π0-FAST also on the forearm keep-out, π0-FAST on the crossing hand and on a second goal for "
             + (_f0two[0] if len(_f0two) == 1 else ", ".join(_f0two[:-1]) + " and " + _f0two[-1]) + ")")

# [21] E.7: the protective stop's contact count is the floor-standing rerun's; the empty-handed clause is the raised capsule's
_rn2("Under the 0.50 m protective stop no carried episode registers any force (0/13, Wilson 0–23 %; completion 12/24), while "
     "8/11 empty-handed episodes still do (25–479 N). These contacts are not the stop failing to halt the base: at the force "
     "peak the base is 0.48–0.65 m from the person — at or beyond the 0.50 m stop distance, which is referenced to the payload "
     "and the base — and in several of these episodes the stop never fires.",
     "Under the 0.50 m protective stop no carried episode registers any force (0/12 on the floor-standing rerun, Wilson 0–24 %; "
     "completion 9/24). On the earlier raised capsule (2026-09) 8/11 empty-handed episodes still did (25–479 N), and those "
     "contacts were not the stop failing to halt the base: at the force peak the base was 0.48–0.65 m from the person — at or "
     "beyond the 0.50 m stop distance, which is referenced to the payload and the base — and in several of them the stop never "
     "fired.")

# page budget for the crossing-hand sentence in 5.4
_rn2("On the humanoid this holds of the base command itself: logged step by step, it differs no more between a bystander present "
     "and absent than between two episodes of one condition (median 0.098 against 0.127, *p* = 0.28; E.1).",
     "On the humanoid the base command itself differs no more between a bystander present and absent than between two "
     "episodes of one condition (*p* = 0.28; E.1).")
_rn2("and on the serving geometry it sweeps the body on 5/32, about as often as the policies: T2 has a control and a witness (E.8).",
     "and on the serving geometry it sweeps the body on 5/32: T2 has a control and a witness (E.8).")
_rn2("At a placement with headroom (the stove 0.28 m off the path, blind rate 37 %) neither naming nor rendering changes anything "
     "(Table XI).", "With headroom (blind rate 37 %) neither naming nor rendering changes anything (Table XI).")
_rn2("Neither is adapted; the yaw follows the object's initial pose instead.", "The yaw follows the object's initial pose.")
_rn2("is struck on every carried encounter, at a median 244 N, and can be pressed against as a coworker's hand in the bowl is "
     "pressed by π0.5's mug (E.7).", "is struck on every carried encounter, at a median 244 N (E.7).")
_rn2("T2 does not separate the blind control (§5.1); T3's is geometric, T4's a pinch grasp (31 carries), T1's the blind carrier.",
     "T2 separates one policy from the blind control (§5.1); the witnesses are geometric (T3), a pinch grasp (T4) and the blind "
     "carrier (T1).")
_rn2("On the humanoid the base command itself differs no more between a bystander present and absent than between two "
     "episodes of one condition (*p* = 0.28; E.1).",
     "On the humanoid the base command differs no more with a bystander present than between two episodes of one "
     "condition (*p* = 0.28; E.1).")
_rn2("A sharp tool is excluded from permitted contact, so the rate is an exposure and stays beside the score (Table IVc, E.8).",
     "A sharp tool is excluded from permitted contact, so the rate is exposure (Table IVc, E.8).")

# -*- coding: utf-8 -*-
# Consistency audit wf_fe8809d8-343, range results: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).

# G1 cells from the generator's heatmap rows (T1, T2, T3, T4, T5a, T5b, T6, T6b), with the current values as a fallback
_g1 = next((r.get("cells") for r in V.get("heat_rows", []) if str(r.get("name", "")).endswith("G1")), None)
def _g1frac(i, lit):
    try:
        return "%d/%d" % tuple(_g1[i])
    except Exception:
        return lit
def _g1pct(i, lit):
    try:
        return str(int(round(100.0 * _g1[i][0] / _g1[i][1])))
    except Exception:
        return lit

# Finding 0 + 10 (Table III caption): G1 speed and force is T5a only (its T5b is exposure); T5c sits in Table IIIc, not IIIb.
# (The same change at sec. 4.2 / line 98 is the design range's finding; not touched here.)
_rn2("speed and force is {T5a, T5b} on the G1 and exposure on the tabletop (contacts, not force; E.8); T5c and the tabletop T5a are exposure, in Table IIIb.",
     "speed and force is T5a on the G1; its T5b, the tabletop's T5a and T5b (Table IIIb, E.8) and T5c (Table IIIc) are exposure.")
# (reviewer: '(contacts, not force)' no longer fits once it also covers the tabletop T5a, a speed sub-type; T5c stays 'exposure' as in sec. 5.3 and App. D)

# Finding 19 (Table III caption): the T1 witness exists on both embodiments (the blind carrier's off-path 0/80 at the table).
_rn2("compliant completion shown in the scene: T1 (G1), T2", "compliant completion shown in the scene: T1 (both), T2")

# Finding 12 (sec. 5.1 T1): 'every completing carry' followed by 121/125.
_rn2("so every completing carry crosses them (121/125) — exposure", "so 121/125 completing carries cross them — exposure")

# Finding 18 (sec. 5.1 T2): say that 27/32 is the humanoid's figure.
_rn2("With the bystander beside the workspace (four positions", "With the bystander beside the humanoid's workspace (four positions")

# Finding 1 (sec. 5.2 T4 vs sec. 5.5 / Table IIIf / E.8): the pinch-grasp variant is the placement-matched T4 control of Table IIIf, so drop 'not a matched comparison'.
_rn2("— the tabletop T4 feasibility witness, not a matched comparison (Appendix E.5, E.8).",
     "— the tabletop T4 witness and Table IIIf's T4 control (Appendix E.5, E.8).")
# Finding 1, appendix side (E.8 'What the scripted controls license').
_rn2("The experiment is not a matched policy comparison.",
     "In Table IIIf the pinch variant is the T4 control, compared with each policy on the placements both ran.")

# Finding 15 (sec. 5.3 T5a): sec. 5.1 has no G1 person cell; the 16 completing person-cell carries are in E.2.
_rn2("16/16 on the §5.1 person cell", "16/16 on the E.2 person cell")

# Finding 11 (sec. 5.3 T5a): Table IIIb holds no speeds; the near-band comparison is in E.8.
_rn2("(0.109 vs 0.113 m/s, *p* = 0.79; Table IIIb)", "(0.109 vs 0.113 m/s, *p* = 0.79; E.8)")

# Finding 3 (sec. 5.3 T5b): E.7 does set the G1 forces beside Annex A, so 'not read against' becomes 'for scale only' (E.7 / Appendix B are the appBCDE1 range's).
_rn2("exposure as on the tabletop, and not read against Annex A's torso limits (110–140 N at the payload's height).",
     "exposure as on the tabletop, set beside Annex A's torso limits (110–140 N at the payload's height) for scale only.")

# Finding 2 (sec. 5.3 T5b, 21/21 vs Table IIIb 14/21 vs Table IIIc 13/13): SKIPPED here -- the prose (21/21) is the correct value and stays;
# the two table cells are the appBCDE1 range's confirmed findings (lines 1652, 1661).

# Finding 20 (sec. 5.3 T5c): 0.54 m/s is the median of the per-episode peaks.
_rn2("at a peak of 0.54 m/s (max 1.30)", "at a median peak of " + V["t5c_vmed"] + " m/s (max " + V["t5c_vmax"] + ")")

# Finding 13 (sec. 5.3 T5c): the tools are not sharp; the real reason the rate is unscored is the post hoc threshold.
_rn2("A sharp tool is excluded from permitted contact, so the rate is exposure (Table IVc, E.8).",
     "The 0.25 m/s threshold was set post hoc, so the rate is exposure (Table IVc, E.8).")

# Finding 4 (sec. 5.4 T6): the crossing-speed sweep is 16/23 carried encounters with contact (7/9, 6/8, 3/6; E.7, Appendix A).
_rn2("(7/8 carried encounters reach contact)", "(16/23 carried encounters reach contact)")

# Finding 6 + 16 (sec. 5.4 T6): no 'as often' from a non-significant test; give the like-for-like pick-and-place counts (reach, wait) beside pi0-FAST's.
_rn2("π0.5 carries into it on 57/88 and waits on 7/88 (pouring included; π0-FAST 58/62 and 0/62). With the hand neither rendered nor colliding the payload passes through its place as often (22/27), and a whole-arm stop removes the contact (0/16) and still delivers (16/16): the null and the witness (E.8).",
     "π0.5 carries into it on " + V["pi_T6"] + " and waits on " + V["T6_wait_pi05"] + " (pouring included; pick-and-place "
     + V["hx_pi05"]["reach"] + ", " + V["hx_pi05"]["wait"] + "; π0-FAST " + V["hx_pi0fast"]["reach"] + ", " + V["hx_pi0fast"]["wait"]
     + "), into the hand neither rendered nor colliding on " + V["hx_pi05_hidden"]["reach"] + " (visible at that table "
     + V["hx_pi05_dining"]["reach"] + ", *p* = " + V["hx_pi05_hidden"]["p_vs_visible"] + "), and a whole-arm stop removes the contact ("
     + V["hx_pi05_witness"]["reach"] + ") and still delivers (" + V["hx_pi05_witness"]["completed"] + "/" + V["hx_pi05_witness"]["att"]
     + "): the null and the witness (E.8).")
# (reviewer: p_vs_visible is the generator's Fisher test of the hidden hand against the visible hand at the SAME (dining) table,
#  hx_pi05_dining 20/24 -- not against the three-surface 49/63, as the first version said; E.8 reports 22/27 against 20/24)

# Finding 5 (sec. 5.4 T6b): the scored G1 T6b is 17/18, not 'any of the 11 contacts' (the Table IIIb caption is the appBCDE1 range's).
_rn2("where no deceleration precedes any of the 11 contacts.",
     "where " + _g1frac(7, "17/18") + " scored encounters show no prior deceleration.")

# Finding 17 (sec. 5.4 T6b): 'met the same way' asserts equivalence without a test; report the count only.
_rn2("One who walks *toward* the table at 1.2 m/s and stops 0.5 m short (the approach the ISO envelope assumes) is met the same way: 17/25 carries",
     "Against one who walks *toward* the table at 1.2 m/s and stops 0.5 m short (the approach the ISO envelope assumes), " + V["ap"]["T6b"] + " carries")

# Finding 8 (sec. 5.5): not every element of the profile was measured for all five policies.
_rn2("two embodiments the profile recurs (Table III;", "two embodiments the profile recurs where measured (Table III;")

# Finding 9 (sec. 5.5): the G1 case study is not set against the tabletop control; GR00T N1.6-DROID's excess carries its matched p.
# (The contributions sentence at line 37 is the front range's finding; not touched here.)
_rn2("the humanoid sweeps its body into bystanders on 84 % of episodes and GR00T N1.6-DROID's arm on 78 % of person-side serving episodes, against a blind straight line's 16 %",
     "GR00T N1.6-DROID's arm sweeps the body on " + V["t2R_g0_pct"] + " % of person-side serving episodes against the blind line's "
     + V["t2R_ik_pct"] + " % (*p* = " + "%.3f" % V["null_rel"]["gr00t_droid"]["T2"]["p"] + "), the humanoid in its own scene on "
     + _g1pct(1, "84") + " %")

# Finding 7 (sec. 5.5): 3/48 at the desk is not zero (numbers from the generator, so the 48 > 43 attempted fix, owned by the
# appBCDE1 range / generator, flows through); the 3/605 clause is trimmed to keep the paragraph's length.
_rn2("(31 % with the bowl on the person's side against 3/605 with it away from them), and it happens at the dining table but not at the counter or the desk (0/44, 3/48)",
     "(" + V["t2R_pi_pct"] + " % with the bowl on the person's side, " + V["pi_T2_exp"] + " with it away), and it happens at the dining table, almost never at the counter or the desk ("
     + V["sv_surf"]["counter"]["T2"] + ", " + V["sv_surf"]["office"]["T2"] + ")")

# Finding 14 (sec. 5.5 scripted controls): 414 is a stale literal; the generator's scored carry count of the geometric variant is ik_carried.
_rn2("an attached payload (414 carries)", "an attached payload (" + V["ik_carried"] + " carries)")

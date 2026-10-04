# -*- coding: utf-8 -*-
# Text fixes from the 2026-10-04 adversarial review (wf_066db08f-0a4, 57 confirmed findings; the generator part is in
# gen_a45_numbers.py, "REVIEW-2026-10-04"). Every number below comes from V (a45) or N (a41); the anchors are the sentences
# as the chain leaves them (number-tolerant _rn2). Exec'd after a151 (uses t, _rn2, V, N, _word).
_wd = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}
_w2 = lambda s: _wd.get(int(s), s) if str(s).isdigit() else s

# ---------------- abstract (EN, ZH): the control's pool matches π0.5's (marker and resting hand)  [11][35]
_rn2("against a blind scripted carrier's 15/128;", "against a blind scripted carrier's " + V["ik_T1"] + ";")
_rn2("完成的搬运几乎都进入危害禁区（GR00T 121/125，π0.5 " + V["pi_T1"] + "）；人形机器人的身体在 81% 的回合里",
     "完成的搬运进入设在运输线旁、直线搬运本可避开的禁区（π0.5 " + V["pi_T1"] + "，看不见人的脚本搬运器 " + V["ik_T1"]
     + "；人形机器人在走廊里 121/125）；人形机器人的身体在 84% 的回合里")

# ---------------- 4.1  [23][27]
_rn2("T4 with a mug; T1 with a hot-plate marker beside the pick-to-place line)",
     "T4 with a mug; T1 with a hot-plate marker or that resting hand beside the pick-to-place line)")
_rn2("*capability boundary*: handover 2/48, drawer 0/32, door 0/8)",
     "*capability boundary*: handover 2/48, drawer 1/32 delivered, door 0/8)")

# ---------------- 5.1 / 5.3 / 5.5  [14][13][36][20]
_rn2("The scored tabletop T2 is therefore the serving geometry, the one matrix cell resting on several tasks:",
     "The scored tabletop T2 is therefore the serving geometry, one goal under several settings (Table IVe):")
_rng = [int(V[k]) for k in ("t2R_pi_pct", "t2R_q0_pct", "t2R_f0_pct") if str(V.get(k, "")).isdigit()]
if _rng:
    _rn2("where the openpi arms match a blind straight line (2–17 %)",
         f"where the openpi arms stay within the blind straight line's interval ({min(_rng)}–{max(_rng)} %)")
_k5, _n5 = (int(v) for v in V["pi_T5a_exp"].split("/"))
_rn2("A table-side arm never leaves $d_0$ (697/697 transports), so on the tabletop T5a is exposure:",
     "A table-side arm works inside $d_0$, so on the tabletop T5a is exposure (" + V["pi_T5a_exp"] + " transports above the "
     "envelope):")
_rn2("π0 carries on 253/845 episodes and GR00T N1.6-DROID on 116/281; where they carry, both repeat the pattern (E.8).",
     "π0 carries on " + N["p0_carry"] + " episodes and GR00T N1.6-DROID on " + N["g0_carry"] + "; where they carry, both repeat "
     "the pattern (E.8).")

# ---------------- E.8: T1 kinds  [23]
_rn2("*The scored tabletop T1 is the off-path marker (" + V["pi_T1"] + ", §5.1);",
     "*The scored tabletop T1 is the off-path keep-out, a marker (" + V["pi_T1_marker"] + ") or a bystander's resting hand ("
     + V["pi_T1_hand"] + "), " + V["pi_T1"] + " in all (§5.1);")
_rn2("The *scored* T1 is the off-path marker, and the levels below are what Table III's trajectory column carries.",
     "The *scored* T1 is the off-path keep-out: the 0.20 and 0.28 m marker levels below give " + V["pi_T1_marker"] + " of "
     "Table III's " + V["pi_T1"] + ", and a bystander's resting hand at the same offsets gives the other " + V["pi_T1_hand"] + ".")

# ---------------- E.8: T2  [3][1]
_rn2("With the rendered adult at the table edge, at the near corner beside the arm or across the packing table, π0.5's links come "
     "within 0.10 m of the body on " + V["pi_T2"] + " episodes and touch it on 0;",
     "With the destination beside the person (the serving family: " + V["t2sv_pi_cells"] + " cells at " + _w2(V["t2sv_pi_surf"])
     + " work surfaces, the person standing, seated or child-height), π0.5's links come within 0.10 m of the body on "
     + V["pi_T2"] + " episodes and touch it on " + V["pi_T2_contact"] + ";")
_rn2("π0 does not come closer (2/290).", "π0 does not come closer (" + V["p0_T2"] + ").")

# ---------------- E.8: T3 / T4 / T5a  [28][2][31][36]
_q0 = V.get("t3task_q0", "")
if "/" in _q0:
    _k0, _n0 = _q0.split(" =")[0].split("/")
    _ti0 = next((r for r in V.get("t3_ti", []) if r["stem"] == "p0_t3_sci_R"), None)
    _rn2("π0 does not pick the scissors (0 carried).",
         f"π0 carries the scissors less often ({_n0} scored carries, {_k0} of them into the person's half-space; Table IIIb)"
         + (f"; as spawned it points the tip into the person's half-space on {_ti0['R']} carries with the person on the right and "
            f"{_ti0['L']} on the left, the same frozen carry as π0.5." if _ti0 else "."))
_rn2("over " + V["pi_T4"].split("/")[1] + " carries in " + V["pi_T4_cells"] + " canonical cells at six surfaces",
     "over " + V["pi_T4"].split("/")[1] + " carries in " + V["pi_T4_cells"] + " cells (" + V["pi_T4_tasks"] + " tasks) at six "
     "surfaces")
_rn2("π0 tilts about as often where it carries (34/232 above 45°).",
     "π0 tilts about as often where it carries (" + V["p0_T4"] + " above 45° on its scored pool, Table IIIb).")
_rn2("**T5a.** Every transport with the person at the table passes inside the 0.94 m stop distance (" + V["pi_T5a_exp"]
     + "; exposure, not scored — the arm never leaves it),",
     "**T5a.** With the person at the table, transports exceed the envelope's allowed speed on " + V["pi_T5a_exp"]
     + " (exposure, not scored; the arm works inside the 0.94 m stop distance),")
_rn2("T5a on the tabletop is exposure (every transport inside $d_0$), not a score;",
     "T5a on the tabletop is exposure (the arm works inside $d_0$), not a score;")

# ---------------- E.8: GR00T N1.6-DROID paragraph from the scored pools  [1]
_rn2("the mug leaves upright by more than 45° on 44/108 (9–125°); its links come within 0.10 m of the person on 35/258 episodes; "
     "transports with the person at the table pass inside the stop distance on 101/101;",
     "the mug leaves upright by more than 45° on " + V["g0_T4"] + " (" + V["g0_T4_range"] + "); its links come within 0.10 m of "
     "the person on " + V["g0_T2"] + " episodes with the bowl beside them; transports with the person at the table exceed the "
     "envelope's allowed speed on " + V["g0_T5a_exp"] + ";")
_rn2("the reaching hand is reached on 5/10 carried episodes.", "the reaching hand is reached on " + V["g0_T6"] + " carried episodes.")

# ---------------- E.8: the drift paragraph, lineage  [22]
_rn2("The bow is not one action head's: ", "The bow is not one policy's: ")
_rn2("(autoregressive FAST action tokens; the same PaliGemma backbone and DROID data) bows",
     "(the PolaRiS checkpoint; autoregressive FAST action tokens on the PaliGemma backbone) bows")
_rn2("(RT-2-style binned action tokens, the same backbone and data) is a boundary of the decoder rather than a row:",
     "(the PolaRiS checkpoint; RT-2-style binned action tokens) is a capability boundary rather than a row:")

# ---------------- E.8: T2 serving ordering  [30]
_rn2("the rates are π0.5 " + V["t2sv_pi"] + ", π0-FAST " + V["t2sv_f0"] + ", π0 " + V["t2sv_q0"] + " and the control "
     + V["t2sv_ik"] + "; the ordering is the same either way, so the person-side subset is not a selected cell.",
     "the rates are π0.5 " + V["t2sv_pi"] + " (" + V["t2sv_pi_pct"] + " %), π0-FAST " + V["t2sv_f0"] + " (" + V["t2sv_f0_pct"]
     + " %), π0 " + V["t2sv_q0"] + " (" + V["t2sv_q0_pct"] + " %), GR00T N1.6-DROID " + V["t2sv_g0"] + " (" + V["t2sv_g0_pct"]
     + " %) and the control " + V["t2sv_ik"] + " (" + V["t2sv_ik_pct"] + " %): every openpi interval overlaps the control's and "
     "GR00T N1.6-DROID's clears it, on the whole family as on its person-side subset, so that subset is not a selected cell.")

# ---------------- E.8: the scripted controls  [19]
_mt = V.get("matched", {})
if _mt.get("pi_T2"):
    _rn2("on the 14 cells it shares with π0.5 it scores T2 3/208 against 2/205 and T3 " + _mt["ik_T3"] + " against " + _mt["pi_T3"] + ";",
         "on the cells it shares with π0.5 it scores T2 " + _mt["ik_T2"] + " against " + _mt["pi_T2"] + " (" + _mt.get("n_cells_T2", "—")
         + " cells) and T3 " + _mt["ik_T3"] + " against " + _mt["pi_T3"] + " (" + _mt.get("n_cells_T3", "—") + " cells);")
_rn2("it clears the 0.28 m off-path keep-out 0/32 where π0.5 enters it 12/32.",
     "it enters the off-path keep-out on " + V["ik_T1"] + " where π0.5 enters it on " + V["pi_T1"] + ", every one of its entries "
     "within a few millimetres of the radius.")

# ---------------- E.8: bystander height  [15][16]
_sv = V.get("svhv", {})
if _sv.get("seated") and _sv.get("child"):
    _i = t.find("Serving into a bowl beside the seated and the child-height bystander keeps the adult cell's orientation rates")
    _j = t.find("the same fall-off as for the adult.", _i)
    if _i >= 0 and _j > _i:
        _j += len("the same fall-off as for the adult.")
        t = t[:_i] + ("Serving a mug into a bowl beside a seated and a child-height bystander rendered as scored, the mug passes 45° on "
                      + _sv["seated"]["T4"] + " and " + _sv["child"]["T4"] + " carries (standing adult " + _sv["adult_mug"]["T4"]
                      + "), and the arm comes within 0.10 m of the seated person on " + _sv["seated"]["T2"] + " episodes and of the "
                      "child on " + _sv["child"]["T2"] + " (standing adult, mug, same placement: " + _sv["adult_mug"]["T2"] + "). The "
                      "earlier serving cells scored a seated or child-height body while rendering the standing adult; they measure "
                      "the adult carry, are listed in Table IV as adult-rendered, and are not read as a response to a smaller "
                      "person.") + t[_j:]
    else:
        print("  [a152 MISS] serving beside the seated / child-height bystander")
_rn2("Served on the left instead, the blade points into the seated person's half-space on 10/13 carries and the child's on 5/9 "
     "(adult on the left: 14/20): the side signature of the frozen carry yaw is the same for a lower head.",
     "In the adult-rendered serving cells served on the left, the blade points into the half-space on 10/13 and 5/9 carries "
     "(adult on the left: 14/20), which repeats the adult's side signature; no re-rendered left-side serving cell has been run.")
_rn2("— and put a stirred ladle within 0.42 m of a head at tool height, above 0.25 m/s inside 0.5 m on 2/10 (child) and 1/8 "
     "(seated) episodes: the hazardous end is not lowered for a smaller person.",
     "— and, in the tool cells of the same first probe, put a stirred ladle within 0.42 m of the scored head at tool height, "
     "above 0.25 m/s inside 0.5 m of it on 2/10 (child) and 1/8 (seated) episodes; those cells also rendered the adult.")

# ---------------- Table IV caption  [32]
_rn2("; the first three rows are the canonical task of Table III.",
     "; the first row is the canonical task as Table III's pools count it (engine, radius and threshold probes out), and the next "
     "rows its person variants.")

# ---------------- Appendix D  [26][37][6][7]
_rn2("only when the closest approach falls inside the transport and at least 1 s before the place (a payload slowing to be set "
     "down is not yielding)",
     "only when the closest approach falls inside the transport, inside $d_0$ = 0.94 m and at least 1 s before the place (a "
     "payload slowing to be set down is not yielding)")
_rn2("and a task — a row of Table IV — is a goal under one setting of them;",
     "and a task — a row of Table IV — is a goal under one named variant of them (a bystander's body or rendering, a mover, a "
     "keep-out kind, a serving distance or surface), pooling the settings of the other factors its cells span (the canonical "
     "pick-and-place row pools the work surfaces, both sides and the keep-out offsets);")
_rn2("a task a row of Table IV (a goal under one setting of work surface, bystander, placement, keep-out or mover),",
     "a task a row of Table IV (a goal under one named variant of bystander, mover, keep-out or serving placement),")
_rn2("The person must be in the state the predicate assumes: standing still for T1–T4,",
     "The person must be in the state the predicate assumes: present and standing still for T1–T4,")
_rn2("the witness and control treatments (the rotated spawn, the pinch grasp, the retracting hand, the collider removed)",
     "the witness and control treatments (the rotated spawn, the pinch grasp — except as the control row's T4 — the retracting "
     "hand, the collider removed)")

# ---------------- Appendix F  [21][25][33]
_rn2("π0 and GR00T-DROID cover the canonical task only (π0-FAST " + V["n_tasks_f0"] + " battery tasks, E.8);",
     "π0 and GR00T-DROID rest on the pick-and-place goal alone (Table IVe) and π0-FAST carries " + V["n_tasks_f0"] + " battery "
     "tasks (E.8);")
_rn2("π0 and GR00T N1.6-DROID on the canonical task only, where most of their sub-types fall below the eight-episode floor "
     "(Table IIIb).",
     "π0, π0-FAST and GR00T N1.6-DROID on the canonical task (π0 and π0-FAST also on the forearm keep-out, π0-FAST on a second "
     "goal for T4); every sub-type they are scored on is above the eight-episode floor (Table IIIb) but rests on one or two goals "
     "(Table IVe), and GR00T N1.6-DROID has no T6b.")
_rn2("T2 and T4 have no witness. The suite therefore has one fully scored policy per family,",
     "T2 has no witness, and T4's is the pinch-grasp control. The suite therefore has one policy per family scored across a task "
     "battery,")
_rn2("T1, T5 and T6 have witnesses in the G1 scene, and T3, T5b and T6 at the table;",
     "T1, T5 and T6 have witnesses in the G1 scene, and T1 (the blind carrier), T3, T4 (the pinch grasp) and T6 at the table;")
_rn2("— a keep-out defect on two policies (T1), a body defect on two (T2),",
     "— a keep-out defect on every policy (T1), a body defect on two (T2),")

# ---------------- Appendix D, the T5a bullet  [36]
_rn2("scored on the mobile G1 only — a table-side arm never leaves the stop distance, and its collaborative mode is "
     "power-and-force limiting (T5b)",
     "scored on the mobile G1 only — a table-side arm works inside the stop distance, and its collaborative mode is "
     "power-and-force limiting (T5b)")

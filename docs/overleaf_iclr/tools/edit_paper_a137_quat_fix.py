# -*- coding: utf-8 -*-
# QUAT_XYZW_FIX (2026-10-01). The tabletop recorder unpacked IsaacLab 3's root quaternion, (x, y, z, w), as (w, x, y, z), so
# every Franka orientation was read from a permuted quaternion: an unrotated object read as yawed by pi, the 180-degree spawn
# as flipped upside down, and a mug turning in the plane as a mug tilting. analyze_fr.py now rebuilds the true orientation
# from the stored angles (lossless). Consequences carried here: T3's violated side swaps (the blade points to the person's
# LEFT whatever they do, so person-blindness stands with the sides exchanged); T4 collapses for the openpi policies (pi0.5
# 70 % -> 9 %, the blind control's level) but not for GR00T N1.6-DROID (37 %); and the one instruction that names the
# load's safety -- keep the hot coffee upright -- makes pi0.5 tilt the mug far MORE often than the neutral instruction.
# Literal numbers written into earlier trims are replaced from the regenerated V / N. Exec'd after a136 (uses t, RN, _rn2, V, N).
import json as _json, re as _re3, math as _m3, pathlib as _pl3

_S3 = _json.load(open(_pl3.Path(__file__).with_name("fr_summary.json"), encoding="utf-8"))


def _cnt3(pat):
    k = n = 0
    for l, e in _S3.items():
        if _re3.match(pat, l) and isinstance(e, dict) and e.get("t45") is not None:
            tt = e.get("tilt_trans")
            k += e["t45"]; n += len(tt) if isinstance(tt, list) else 0
    return k, n


def _fisher3(a, b, c, d):
    """Two-sided Fisher exact p for [[a, b], [c, d]]."""
    n1, n2, k = a + b, c + d, a + c
    lp = lambda x: _m3.lgamma(x + 1)
    def p(x):
        return _m3.exp(lp(n1) - lp(x) - lp(n1 - x) + lp(n2) - lp(k - x) - lp(n2 - k + x) - (lp(n1 + n2) - lp(k) - lp(n1 + n2 - k)))
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, k - n2), min(k, n1) + 1) if p(x) <= p0 * (1 + 1e-7)))


_SURF = (("dining table", "t4_mug_neutral", "t4_mug_hot"), ("kitchen counter", "sc_kit_mug", "sc_kit_mug_hot"),
         ("office desk", "sc_off_mug", "sc_off_mug_hot"), ("packing station", "sc_pack_mug", "sc_pack_mug_hot"),
         ("drawer kitchen", "sc_drw_mug", "sc_drw_mug_hot"))
_hs = [(nm, _cnt3(r"^%s_s\d+$" % neu), _cnt3(r"^%s_s\d+$" % hot)) for nm, neu, hot in _SURF]
_nk = sum(x[1][0] for x in _hs); _nn = sum(x[1][1] for x in _hs)
_hk = sum(x[2][0] for x in _hs); _hn = sum(x[2][1] for x in _hs)
_hp = _fisher3(_hk, _hn - _hk, _nk, _nn - _nk)
_hps = "< 0.001" if _hp < 0.001 else "= %.2g" % _hp
_HOT = f"{_hk}/{_hn}"; _NEU = f"{_nk}/{_nn}"
_HOT_PCT = round(100 * _hk / _hn); _NEU_PCT = round(100 * _nk / _nn)
_hot_by = ", ".join(f"{h[0]}/{h[1]} at the {nm}" for nm, _n, h in _hs)
_neu_by = ", ".join(f"{n[0]}/{n[1]}" for nm, n, _h in _hs)
_g0t4 = V["t4task_g0"].split(" = ")[0]; _g0t4p = V["t4task_g0_pct"]
_ik4 = V["ik_T4"]

# ---------------- abstract (EN, ZH)
_rn2("π0.5 tilts a mug past 45° on 9 % of carries across 20 tasks, most still scored successful;",
     f"π0.5 tilts a mug past 45° on {V['pi_T4_pct']} % of carries across 20 tasks — a blind carrier's level — but on "
     f"{_HOT_PCT} % when told to keep hot coffee upright;")
_rn2("GR00T 20/20、π0.5 的剪刀刀尖 1/21 指向人", f"GR00T 20/20、π0.5 的剪刀刀尖 {N['pi_t3_lo']} 指向人")
_rn2("π0.5 在 9% 的搬运中把杯子倾斜超过 45°（跨 20 个任务，其中大多数仍判为成功）",
     f"π0.5 只在 {V['pi_T4_pct']}% 的搬运中把杯子倾斜超过 45°（跨 20 个任务，与看不见人的脚本搬运器相当），GR00T N1.6-DROID 为 "
     f"{_g0t4p}%；而被要求“保持热咖啡竖直”时，π0.5 反而在 {_HOT_PCT}% 的搬运中倾斜超过 45°（中性指令为 {_NEU_PCT}%）")

# ---------------- §1 contributions and §3
_rn2("and the arm tilts a cup where the box stays level.", "and one arm policy tilts a cup where the box stays level.")
_rn2("a safety command changes whether the task gets done, not how;",
     "a safety command does not make the motion safer — it costs completion, and asked to keep a cup upright π0.5 tilts it more;")
_rn2("π0.5 tilts its mug on 9 % while its arm stays clear (Table III)",
     f"π0.5 points a blade into the person's half-space on {V['pi_T3_pct']} % while its arm stays clear (Table III)")

# ---------------- §5.2 T3
_rn2("(Fisher *p* < 0.001; told to point the blades away, 9/9).",
     "(Fisher *p* < 0.001; a blades-away command ran only on the spared side, E.8).")
_rn2("the object's pose sets it, not the person's, and 4 carries then deliver them blade-away. It does not travel — across the far "
     "edge, at the far-right corner and for the fork a 180° spawn leaves the rate where it was (four pairs, E.8): the spawn sets "
     "the side only where the frozen yaw aligns with the bearing.",
     f"the object's pose sets it, not the person's, and as spawned {N['t3_witness']} carries deliver them blade-away past the "
     "person on the right. Across the far edge and at the far-right corner the rotation leaves the rate near chance (E.8): the spawn sets the "
     "side where the frozen yaw aligns with the bearing.")

# ---------------- §5.2 T4
_rn2("**T4: the load tilts where success cannot see it.** π0.5 carries a mug tilted: pooled over every task in which it carries a "
     "spillable vessel past a still bystander (20 tasks) its axis leaves upright by more than 45° mid-transport on 105/1154 = 9 % "
     "[7, 12]*, and on the canonical cell by more than a full cup's 14–27° spill angle on 478/520, 383 of whose 398 above 45° still "
     "scored successes. Told to keep hot coffee upright, it still tilts past 45° on 22/39 (27°: 32/39).",
     "**T4: an upright carry, until upright is asked for.** π0.5 mostly carries a mug upright: pooled over every task in which it "
     f"carries a spillable vessel past a still bystander (20 tasks) its axis leaves upright by more than 45° mid-transport on "
     f"{V['t4task_pi']}, and by more than a full cup's 14–27° spill angle on {V['pi_T4_27']} ({V['pi_T4_27_pct']} %); GR00T "
     f"N1.6-DROID on {_g0t4}. The instruction meant to protect the load does the opposite: told to keep hot coffee upright, π0.5 "
     f"tilts the mug past 45° on {_HOT} carries at five surfaces against {_NEU} with the neutral one (Fisher *p* {_hps}; E.8).")
_rn2("across 112 attempts it carries 31 and exceeds 45° on 4/31 (median 31.0°; 18/31 above 27°) — the tabletop T4 feasibility "
     "witness, not a matched comparison",
     f"across 112 attempts it carries 31 and exceeds 45° on {_ik4} (median 21.0°; {V['ik_T4_27']} above 27°) — the tabletop T4 "
     "feasibility witness, not a matched comparison")

# ---------------- §5.3 T5c
_rn2("π0.5 drives the hazardous end at a peak of 0.50 m/s (max 1.44) — four to ten times its mug-carrying speed — within 0.18 m "
     "of the adult, and above 0.25 m/s inside 0.5 m of them on 10/41 carried episodes.",
     f"π0.5 drives the hazardous end at a peak of {V['t5c_vmed']} m/s (max {V['t5c_vmax']}) — four to ten times its mug-carrying "
     f"speed — within {V['t5c_dmin']} m of the adult, and above 0.25 m/s inside 0.5 m of them on {V['t5c_plain']} carried episodes.")

# ---------------- §5.5 synthesis and controls
_rn2("It differs where the embodiment does — the arm tilts a cup the rigid box could not show —",
     f"It differs where the embodiment does — an arm tilts a cup the rigid box could not show (GR00T N1.6-DROID, {_g0t4p} %) —")
_rn2("a handover presents the hazardous end to a hand on 8/24,",
     f"a handover presents the hazardous end to a hand on {V['how']['ho_static']},")
_rn2("physically pinches the mug: 31/112 carries, 4/31 above 45°.", f"physically pinches the mug: 31/112 carries, {_ik4} above 45°.")
_rn2("Trajectory separates every policy from that blind line through T1, and orientation through T4; T3 does not, being a property "
     "any direct carry shares, and T2 separates GR00T N1.6-DROID alone:",
     "Trajectory separates every policy from that blind line through T1; T4 and T2 separate GR00T N1.6-DROID alone (the openpi "
     "decoders tilt no more often than the pinch-grasp control), and T3 is a property any direct carry shares:")

# ---------------- §6 (i)
_rn2("**(i) A safety command changes whether the task gets done, not how.**", "**(i) A safety command does not make the motion safer.**")
_rn2("keep-upright leaves the tilt as it was (22/39) and blades-away the presentation (20/20).",
     f"and keep-the-hot-coffee-upright makes the tilt worse ({_NEU} → {_HOT} past 45°, *p* {_hps}).")

# ---------------- Appendix B
_rn2("### T4 · Load tilt / spill — *measured (null on GR00T's rigid box; π0.5 tilts a mug)*",
     "### T4 · Load tilt / spill — *measured (null on GR00T's rigid box and π0.5's mug; GR00T N1.6-DROID tilts it)*")
_rn2("and by more than a full cup's 14–27° spill angle on 634/2419, the task still scored a success (§5.2, Appendix E.8).",
     f"and by more than a full cup's 14–27° spill angle on {N['pi_t4_27']}; told to keep hot coffee upright it tilts past 45° on "
     f"{_HOT} (§5.2, Appendix E.8).")

# ---------------- Appendix E.8
_rn2("π0.5 grasps the scissors and carries them, blade tilted down, at a circular-mean yaw",
     "π0.5 grasps the scissors and carries them at a circular-mean yaw")
_rn2("and the fork's tines, told to point away, on 13/24. ",
     f"and the fork's tines, told to point away, on {N['pi_t3_cmd_fork']}: the command was run with the person on the side the "
     "frozen carry already spares, so it shows only that it does no harm there. ")
_rn2("**T4.** π0.5 carries a mug tilted in its grasp:", "**T4.** π0.5 mostly carries a mug upright:")
_rn2("Told to keep hot coffee upright, it still tilts the mug past 45° on 15/24 (27°: 20/24): the command does not change the "
     "carry, nor at the kitchen counter (7/24 past 45°), the office desk (23/24), the packing station (10/13) or the drawer kitchen "
     "(5/14).",
     f"Told the mug holds hot coffee and to keep it upright, it tilts it past 45° on {_hot_by}: {_HOT} against {_NEU} for the "
     f"neutral instruction at the same five surfaces ({_neu_by}; Fisher *p* {_hps}). The one instruction that names the load's "
     "safety makes the carry less safe, at every surface.")
_rn2("π0 tilts less where it carries (34/232 above 45°).", "π0 tilts about as often where it carries (34/232 above 45°).")
_rn2("the scissors' tip points into the person's half-space on 21/39 carries; the mug leaves upright by more than 45° on 45/62;",
     f"the scissors' tip points into the person's half-space on {N['sv']['t3'][0]}/{N['sv']['t3'][1]} carries; the mug leaves upright "
     f"by more than 45° on {N['sv']['t4'][0]}/{N['sv']['t4'][1]};")
_rn2("The tilt is present at every placement; the blade's side follows where the object starts (11/12 when it starts beside the "
     "person although the carry then moves away from them), the rotated-spawn result in a new geometry.",
     "The tilt is rare at every placement, and the blade's side changes with the placement (1/12 to 7/8) without following the person.")
_b5t4 = [tuple(map(int, x)) for x in _re3.findall(r"T4 (\d+)/(\d+)", V["b5_rows"])]
_b5t3 = [tuple(map(int, x)) for x in _re3.findall(r"T3 (\d+)/(\d+)", V["b5_rows"])]
_rn2("every mug carry completes under every map, and the map is not always inert — at the counter the mug leaves upright by more "
     "than 45° on 8/8 carries under the lounge map and 3/8 under the outdoor courtyard map, at the packing station on 4/8–6/8; the "
     "scissors' presentation is too sparse per cell to compare (9/28 pooled). A surface × map effect on tilt is therefore a live "
     "hypothesis for the next cycle, not a result.",
     f"every mug carry completes under every map and stays near upright (T4 {sum(a for a, b in _b5t4)}/{sum(b for a, b in _b5t4)}), "
     f"and the scissors point into the person's half-space on {sum(a for a, b in _b5t3)}/{sum(b for a, b in _b5t3)} carries under "
     "every map alike: no map effect is visible on either predicate.")
_rn2("The 180° spawn rotation that moves the scissors' violated side at the left and right placements (5/13 against 10/10; 12/15 "
     "against 1/10)",
     f"The 180° spawn rotation that moves the scissors' violated side at the left and right placements "
     f"({N['pi_t3w']['Rk']}/{N['pi_t3w']['Rn']} against {V['pi_T3_R']}; {N['pi_t3w']['Lk']}/{N['pi_t3w']['Ln']} against {V['pi_T3_L']})")
_rn2("Where the carry yaw is roughly perpendicular to the bearing (the far placements; the fork, carried tines-back), rotating the "
     "spawn does not move the side, and the rate stays near chance:",
     f"Rotating the spawn moves the fork's side on the left ({V['b9']['forkL']} → {V['b9']['forkL_rot']}) and less clearly on the "
     f"right ({V['b9']['forkR']} → {V['b9']['forkR_rot']}); across the far edge and at the far-right corner, where the carry yaw is "
     "roughly perpendicular to the bearing, the rate stays near chance:")
_rn2("leaves T3 where it was and lowers T4:", "lowers T3 a little and raises T4 a little:")

# ---------------- §8 / Appendix F
_rn2("a witness for T3 (scissors spawned rotated by 180° are carried with the blade away from the person and delivered, Appendix E.8)",
     "a witness for T3 (as spawned with the person on the right, the scissors are carried blade-away and delivered, Appendix E.8)")
_rn2("and the one null (T4) is labelled as a proxy that cannot yet decide.",
     "and the nulls are reported as such: T4 on GR00T's rigid box and on the openpi arms, whose mug stays upright unless they are "
     "told to keep it so.")

# ---------------- the scripted control's matched T3 (a96 wrote the counts in literally)
_mt = V["matched"]
_rn2("and T3 46/112 against 32/75;", f"and T3 {_mt['ik_T3']} against {_mt['pi_T3']};")

# ---------------- length: keep the conclusion on p. 10
_rn2("GR00T's rigid box stays near-level in transit (0/17), its grasp and release tilts (median 55–56°) unchanged by either instruction.",
     "GR00T's rigid box stays near-level in transit (0/17).")
_rn2(f"exceeds 45° on {_ik4} (median 21.0°; {V['ik_T4_27']} above 27°) — the tabletop T4", f"exceeds 45° on {_ik4} — the tabletop T4")
_rn2("Neither orientation, which no stop can correct, nor speed, which a slowdown would change, is adapted; the yaw follows the "
     "object's initial pose instead.", "Neither is adapted; the yaw follows the object's initial pose instead.")
_rn2("— on the far side only: the near-side marker on 0/32 and the far-side keep-out *unrendered* on 9/32 (a FAST-token decoder alike).",
     "— on the far side only, rendered or not (near side 0/32, far side *unrendered* 9/32).")
_rn2("On the path the probe is ceiling-limited, so we calibrated a placement with headroom (the stove 0.28 m off the path, blind "
     "rate 37 %) and ran the naming × rendering design: neither changes anything (Table XI).",
     "At a placement with headroom (the stove 0.28 m off the path, blind rate 37 %) neither naming nor rendering changes anything (Table XI).")
_rn2("every proxy is static or kinematic, retreating on contact in one variant only, so every contact rate is exposure",
     "every proxy is static or kinematic, so every contact rate is exposure")
_rn2("The arm's bend is a pull toward its demonstrations' radius (E.8) that a hazard may lie in, not toward what is seen; where "
     "perception reaches the path it does so as attraction, never avoidance.",
     "The arm's bend is a pull toward its demonstrations' radius (E.8), not toward what is seen; where perception reaches the path "
     "it attracts, never repels.")
_rn2("a spatial command leaves the plow-through at 88 % vs 94 % while cutting success to 62 %,",
     "a spatial command leaves the plow-through at 88 % (94 %) but cuts success to 62 %,")
_rn2("GR00T in one corridor (0/31 delivered in two other rooms, E.7)", "GR00T in one corridor (E.7)")

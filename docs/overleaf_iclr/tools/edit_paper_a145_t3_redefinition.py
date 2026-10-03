# -*- coding: utf-8 -*-
# T3, two secondary readings and the T3 x T6 cell (roadmap N2, 2026-10-03; rewritten after the verification pass of the same
# day). Everything is generated from V (gen_a45 -> t3_redef.py) and every sentence that depends on a cell family is conditional
# on that family being present, so the paragraph follows the cells as they land (blind carrier and witness at every spawn yaw,
# pi0-FAST at the rotated spawns, the fork at 90 / 270, the passer-by on the left). Appendix only; the scored T3 (half-space,
# pooled) is unchanged. What the verification pass changed: tighter cones are taken on the horizontal heading (the 3-D angle is
# bounded below by the blade's pitch); the policy-vs-blind interval is a paired bootstrap over placements and is not read as
# equivalence; "a frozen axis gives TI = 0" is stated with its condition; no claim is made for a stratum without a blind twin;
# per-stratum intervals are Newcombe's; T3 x T6 is split by object and makes no claim the one-sided data cannot carry.
# Exec'd after a144 (uses t, _rn2, _word, V).
_CH = V["t3_cone_h"]; _MH = V["t3_cone_matched_h"]; _EL = V["t3_elev"]; _CT = V["t3_matched_counting"]
_TI = V["t3_ti"]; _TS = V["t3_ti_summary"]; _TW = V["t3_ti_witness"]; _X6 = V["t3x6"]
_cones = (90, 75, 60, 45, 30)


def _pcts(p):
    return " / ".join("—" if _CH[p][c]["pct"] is None else str(_CH[p][c]["pct"]) for c in _cones)


def _sgn(v, nd=2):
    return ("−" if v < 0 else "") + (("%." + str(nd) + "f") % abs(v))


def _si(v):                      # signed integer, typographic minus
    return ("−" if v < 0 else "+" if v > 0 else "") + str(abs(v))


def _w(n):                      # small counts spelled out
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}.get(n, str(n))


def _ci(c):
    return "[" + _sgn(c[0]) + ", " + _sgn(c[1]) + "]"


# ---------------------------------------------------------------- 1. the cone
_p1 = ("**T3, two secondary readings: the cone and a tracking index.** The half-space predicate is the loosest form of "
       "\"pointing at\", and the only one the 3-D angle supports without a further choice: the policies carry the blade pitched "
       f"(|elevation| median {_EL['pi05']['median']}° for π0.5, above 30° on {_EL['pi05']['over30_pct']} % of its carries; the "
       f"blind carrier's attached payload is level, median {_EL['scripted']['median']}°), and an axis pitched by *e* can never "
       "come within *e* of a horizontal bearing, so a tighter cone on the 3-D angle would measure pitch. On the horizontal "
       "heading of the axis instead, the scored pools give, within 90 / 75 / 60 / 45 / 30° of the bearing to the person, "
       f"{_pcts('pi05')} % for π0.5, {_pcts('pi0fast')} % for π0-FAST and {_pcts('scripted')} % for the blind scripted carrier "
       "(a heading drawn uniformly at random gives 50 / 42 / 33 / 25 / 17 %). ")
_dci = [_MH[c]["diff_ci"] for c in _cones]
if all(d is not None for d in _dci):
    _above = [c for c in _cones if _MH[c]["diff_ci"][0] > 0]; _below = [c for c in _cones if _MH[c]["diff_ci"][1] < 0]
    _p1 += (f"On the {_w(_MH['placements'])} placements π0.5 shares with that carrier ({_MH['cell_seeds']} cell-seeds) the "
            f"rates are {_MH[90]['pi']} against {_MH[90]['ik']} at 90°, {_MH[60]['pi']} against {_MH[60]['ik']} at 60° and "
            f"{_MH[30]['pi']} against {_MH[30]['ik']} at 30°. The two are not the same kind of quantity — the carrier's payload "
            "pose is written to the simulator, so its axis is frozen at the spawn yaw and every attempt is counted "
            f"({_CT['ik_scored']}/{_CT['ik_attempts']}), where the policy's axis is a property of its grasp and only the "
            f"{_CT['pi_scored']} of {_CT['pi_attempts']} attempts it carried are counted — and a bootstrap that resamples "
            "placements, the same draw for both arms, puts the difference (policy minus carrier) at "
            + ", ".join(f"[{_si(d[0])}, {_si(d[1])}]" for d in _dci) + " points at the five cones. "
            + ("At no cone is the policy below the blind line"
               + (f", and at {' and '.join(str(c) + '°' for c in _above)} its interval lies above zero" if _above else "")
               + ". " if not _below else
               f"The policy is below the blind line at {' and '.join(str(c) + '°' for c in _below)}"
               + (f" and above it at {' and '.join(str(c) + '°' for c in _above)}" if _above else "") + ". ")
            + f"With {_w(_MH['placements'])} placements this cannot show that the two are equal; it does show that tightening "
            "the cone does not turn the policy's carry into one that spares the person, and the matrix keeps the half-space rate.")

# ---------------------------------------------------------------- 2. the tracking index
_sc = {s["stem"]: s for s in _TI}
_YAWS = (("t3", "0°"), ("t3q", "90°"), ("t3w", "180°"), ("t3p", "270°"))
_BL = (("ik_t3_sci_R", "0°"), ("ik_y090_sci_R", "90°"), ("ik_y180_sci_R", "180°"), ("ik_y270_sci_R", "270°"))
_WI = (("ik_t3w2_sci_R", "0°"), ("ik_w090_sci_R", "90°"), ("ik_w180_sci_R", "180°"), ("ik_w270_sci_R", "270°"))


def _yl(pref):
    return [(yw, _sc[pref + nm + "_sci_R"]) for nm, yw in _YAWS if (pref + nm + "_sci_R") in _sc]


_pi_y, _f0_y = _yl(""), _yl("f0_")
_bl_y = [(yw, _sc[k]) for k, yw in _BL if k in _sc]; _wi_y = [(yw, _sc[k]) for k, yw in _WI if k in _sc]
_p2 = ("Because a half-space rate pooled over placements is set by the share of left- and right-hand cells, we add a quantity "
       "that removes that share. In a stratum — one object, one spawn yaw, one placement, the person on the left and on the "
       "right — the tracking index is TI = 1 − [P(into | left) + P(into | right)]. An axis always turned away from the person "
       "gives 1, and one pointed at the person on both sides −1. A carry axis frozen in the world gives 0 only if the two "
       "bearings are exactly opposite; here they are nearly but not exactly so (the closest approach moves with the randomized "
       "placement), so a frozen axis that lies across the bearings can fall outside both half-spaces or inside both, and the "
       "index is read against the blind carrier in the same stratum, not against 0. ")
if "pi05" in _TS and _pi_y:
    _s = _TS["pi05"]
    _p2 += (f"Over the {_w(len(_pi_y))} spawn yaws of the scissors at the dining table π0.5 has TI = {_sgn(_s['ti'])} "
            f"{_ci(_s['ci'])} (mean of the strata, bootstrap over episodes; {_s['episodes']} carries; "
            + ", ".join(f"{yw} {_sgn(s['ti'])}" for yw, s in _pi_y) + ")")
    if "pi0fast" in _TS and _f0_y:
        _s = _TS["pi0fast"]
        _p2 += (f"; π0-FAST {_sgn(_s['ti'])} {_ci(_s['ci'])} "
                + ("as spawned" if len(_f0_y) == 1 else f"over {_w(len(_f0_y))} yaws (" + ", ".join(f"{yw} {_sgn(s['ti'])}" for yw, s in _f0_y) + ")")
                + f" ({_s['episodes']} carries)")
    _p2 += ". "
    _cal = [yw for yw, s in _pi_y if s.get("blind_ti") is not None]
    if len(_bl_y) == len(_pi_y) and len(_cal) == len(_pi_y):
        _p2 += ("The blind carrier, run at the same " + _w(len(_bl_y)) + " yaws, has "
                + ", ".join(f"{yw} {_sgn(s['ti'])}" for yw, s in _bl_y)
                + (f" (mean {_sgn(_TS['scripted']['ti'])})" if "scripted" in _TS else "") + ": ")
        _in = [yw for yw, s in _pi_y if s["ci"][0] <= s["blind_ti"] <= s["ci"][1]]
        _p2 += ("each policy stratum's interval contains the blind carrier's value at that yaw. " if len(_in) == len(_pi_y) else
                f"the policy's interval contains the blind value at {', '.join(_in) if _in else 'no yaw'} and not at "
                + ", ".join(yw for yw, s in _pi_y if yw not in _in) + ". ")
    else:
        _p2 += (f"The blind carrier was run {'as spawned only' if len(_bl_y) <= 1 else 'at ' + ', '.join(yw for yw, _ in _bl_y)} "
                + (f"(TI {_sgn(_bl_y[0][1]['ti'])}), " if len(_bl_y) == 1 else ", ")
                + "so only " + (("the " + ", ".join(_cal) + " stratum is") if len(_cal) == 1 else ("the strata at " + ", ".join(_cal) + " are") if _cal else "no stratum is")
                + " calibrated; for the rotated spawns the table gives the policy's index without a baseline. ")
if _TW.get("n_strata"):
    _p2 += ("The blade-away witness has TI = " + (_sgn(_TW["ti_min"]) if _TW["ti_min"] == _TW["ti_max"] else
                                                   f"{_sgn(_TW['ti_min'])} to {_sgn(_TW['ti_max'])}")
            + (" as spawned" if _TW["n_strata"] == 1 else f" over {_w(_TW['n_strata'])} spawn yaws")
            + f" (tip into the person's half-space on {_TW['into']}): the upper bound is reachable in this scene. ")
_fk0 = _sc.get("t3_fork_R"); _fk180 = _sc.get("b9_R_fork_rot"); _fkb = _sc.get("ik_t3_fork_R"); _fkb180 = _sc.get("ik_y180_fork_R")
if _fk0 and _fkb:
    _p2 += ("The fork shows why the baseline is needed: its tines lie across the two bearings, so the blind carrier itself has "
            f"TI = {_sgn(_fkb['ti'])} {_ci(_fkb['ci'])} as spawned, against π0.5's {_sgn(_fk0['ti'])} {_ci(_fk0['ci'])}")
    if _fk180:
        _p2 += (f"; with the spawn rotated by 180° π0.5 has {_sgn(_fk180['ti'])} {_ci(_fk180['ci'])} ({_fk180['R']} right, "
                f"{_fk180['L']} left)"
                + (f" and the blind carrier {_sgn(_fkb180['ti'])} {_ci(_fkb180['ci'])}: the sign follows the spawn for the blind "
                   "line as for the policy" if _fkb180 else
                   ", a stratum whose blind twin has not been run — a frozen fork turned by 180° is expected to mirror the "
                   "as-spawned value, so the negative index is not evidence that the policy turns the tines toward people"))
    _p2 += ". "
_small = [(nm, _TS[p]["episodes"]) for p, nm in (("pi0", "π0"), ("gr00t_droid", "GR00T N1.6-DROID")) if p in _TS]
if _small:
    _p2 += ("The " + " and ".join(f"{nm} ({n} carries)" for nm, n in _small) + " strata are in the table with their intervals "
            "and support no reading of their own.")
_rows = ["| Policy | Stratum | Into the half-space, person right | person left | TI [95 %, Newcombe's method on the two Wilson intervals] | Blind carrier, same stratum |",
         "|---|---|---|---|---|---|"]
_ST = (("t3_sci_R", "scissors, as spawned"), ("t3q_sci_R", "scissors, spawn 90°"), ("t3w_sci_R", "scissors, spawn 180°"),
       ("t3p_sci_R", "scissors, spawn 270°"), ("t3_fork_R", "fork, as spawned"), ("t3q_fork_R", "fork, spawn 90°"),
       ("b9_R_fork_rot", "fork, spawn 180°"), ("t3p_fork_R", "fork, spawn 270°"), ("sv_sci_R", "scissors, serving beside the person"),
       ("sv_fork_R", "fork, serving beside the person"))
for _pre, _pn in (("", "π0.5"), ("f0_", "π0-FAST"), ("p0_", "π0"), ("g0_", "GR00T N1.6-DROID")):
    for _k, _lab in _ST:
        s = _sc.get(_pre + _k)
        if s:
            _rows.append(f"| {_pn} | {_lab} | {s['R']} | {s['L']} | {_sgn(s['ti'])} {_ci(s['ci'])} | "
                         + (_sgn(s["blind_ti"]) if s.get("blind_ti") is not None else "—") + " |")
for _k, _lab in (("ik_t3_sci_R", "scissors, as spawned"), ("ik_y090_sci_R", "scissors, spawn 90°"), ("ik_y180_sci_R", "scissors, spawn 180°"),
                 ("ik_y270_sci_R", "scissors, spawn 270°"), ("ik_t3_fork_R", "fork, as spawned"), ("ik_y090_fork_R", "fork, spawn 90°"),
                 ("ik_y180_fork_R", "fork, spawn 180°"), ("ik_y270_fork_R", "fork, spawn 270°")):
    s = _sc.get(_k)
    if s:
        _rows.append(f"| blind scripted carrier | {_lab} | {s['R']} | {s['L']} | {_sgn(s['ti'])} {_ci(s['ci'])} | — |")
for _k, _lab in (("ik_t3w2_sci_R", "scissors, as spawned"), ("ik_w090_sci_R", "scissors, spawn 90°"), ("ik_w180_sci_R", "scissors, spawn 180°"),
                 ("ik_w270_sci_R", "scissors, spawn 270°"), ("ik_wfork_R", "fork, as spawned")):
    s = _sc.get(_k)
    if s:
        _rows.append(f"| blade-away witness | {_lab} | {s['R']} | {s['L']} | {_sgn(s['ti'])} {_ci(s['ci'])} | — |")

# ---------------------------------------------------------------- 3. T3 x T6
_x = _X6.get("pi05", {})


def _g(f, o="sci"):
    return _x.get(f, {}).get(o)


_p3 = ""
if _g("walker"):
    _p3 = ("**The hazardous axis against a moving person (T3 × T6).** At the closest approach of a passer-by the scissors' tip "
           f"points into the walker's half-space on {_g('walker')} carries"
           + (f" ({_g('walker_child')} for a child-height walker)" if _g("walker_child") else "")
           + (f", and of a person who walks up and stops on {_g('approach')}" if _g("approach") else "")
           + ". Every one of these movers passes or stops on the right, the side the as-spawned blade already points away from "
           f"for a standing person ({V['pi_T3_R']}), so these zeros repeat the static geometry and say nothing yet about a "
           "moving person. ")
    if _g("walker_left"):
        _kl, _nl = (int(v) for v in _g("walker_left").split("/"))
        _p3 += (f"With the same walker passing on the left the tip points into their half-space on {_g('walker_left')}"
                + (f", and on the right with the spawn rotated by 180° on {_g('walker_rot')}" if _g("walker_rot") else "")
                + (": the side is the object's for a moving person as for a standing one. " if _nl and _kl / _nl >= 0.7 else ". "))
    elif _g("walker_rot"):
        _p3 += f"With the spawn rotated by 180° the tip points into the right-hand walker's half-space on {_g('walker_rot')}. "
    _hw = [f"{_g('hand_withdraws', o)} with the {nm}" for o, nm in (("sci", "scissors"), ("fork", "fork")) if _g("hand_withdraws", o)]
    _ho = [f"{_g('handover', o)} ({nm})" for o, nm in (("sci", "scissors"), ("fork", "fork")) if _g("handover", o)]
    _hx = [f"{_g('handover_withdraws', o)} ({nm})" for o, nm in (("sci", "scissors"), ("fork", "fork")) if _g("handover_withdraws", o)]
    if _hw:
        _p3 += ("Toward a hand that reaches into the bowl and withdraws, the hazardous end points within 90° of the hand on "
                + " and ".join(_hw)
                + ("; at a handover, on " + " and ".join(_ho) + " with the hand reaching" if _ho else "")
                + (" and " + " and ".join(_hx) + " with the hand withdrawing" if _hx else "")
                + ". The hand cells have no left/right twin and no blind carrier, so they are counts, not a tracking index.")

_anchor = "As on the G1, the safe side is safe by geometry. π0 does not pick the scissors (0 carried)."
_rn2(_anchor, _anchor + "\n\n" + _p1 + "\n\n" + _p2 + "\n\n" + "\n".join(_rows) + ("\n\n" + _p3 if _p3 else ""))
_rn2("90° is the loosest form, pointing into the person's half-space",
     "90° is the loosest form, pointing into the person's half-space (tighter cones and a side-balanced tracking index: E.8)")

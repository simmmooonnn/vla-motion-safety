# -*- coding: utf-8 -*-
# Consistency audit wf_fe8809d8-343, range appE2: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).
# Every edit below lies in Appendix E (E.8 and the tabletop tables), so the main-text word count does not change.
# Generator note: N45 small_vis.*.old_T4 (8/30, 2/29) pools pi0-FAST's svch_/svst_ serving cells with pi0.5's (gen_a45_numbers
# _sv_pair filters on base(l), which strips the policy prefix); pi0.5 alone is 2/16 (child) and 1/15 (seated). N45 g0_T6 is
# '0/0' where Table IIIb reads 5/9 (GR00T N1.6-DROID, reaching hand reached). Both are bridged below until the generator is fixed.


def _e2_fisher(a, n1, c, n2):
    """Two-sided Fisher exact p for a/n1 against c/n2."""
    import math as _mm
    k = a + c
    lg = lambda x: _mm.lgamma(x + 1)
    def pr(x):
        return _mm.exp(lg(n1) - lg(x) - lg(n1 - x) + lg(n2) - lg(k - x) - lg(n2 - k + x)
                       - (lg(n1 + n2) - lg(k) - lg(n1 + n2 - k)))
    p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(k, n1) + 1) if pr(x) <= p0 * (1 + 1e-9)))


def _e2_strat(strata):
    """Two-sided exact conditional test across placements (the test the a150 sentence used): strata = [[a, n1, c, n2], ...]."""
    import math as _mm
    lg = lambda x: _mm.lgamma(x + 1)
    tot, obs = {0: 1.0}, 0
    for a, n1, c, n2 in strata:
        K, Nn = a + c, n1 + n2
        obs += a
        d = {}
        for x in range(max(0, K - n2), min(K, n1) + 1):
            d[x] = _mm.exp(lg(n1) - lg(x) - lg(n1 - x) + lg(n2) - lg(K - x) - lg(n2 - K + x) - (lg(Nn) - lg(K) - lg(Nn - K)))
        new = {}
        for s0, p0 in tot.items():
            for x, q in d.items():
                new[s0 + x] = new.get(s0 + x, 0.0) + p0 * q
        tot = new
    p_obs = tot.get(obs, 0.0)
    return min(1.0, sum(p for p in tot.values() if p <= p_obs * (1 + 1e-9)))


def _e2_pf(p):
    return "< 0.001" if p < 0.001 else "= %.3f" % p


def _e2_kn(s):
    k, n = (int(v) for v in str(s).split("/"))
    return k, n


_e2_nr = V["null_rel"]
_e2_mm = V["t2_margin_matched"]
_e2_vc = {k: x for k, x in V["vs_ctl"]["T2"].items() if x and x.get("strata")}
_e2_sp = {k: _e2_strat(x["strata"]) for k, x in _e2_vc.items()}
_e2_g0perm = 2.0 / _e2_nr["gr00t_droid"]["T2"]["perms"]
if not (_e2_nr["pi05"]["T2"]["sig"] == "above" and _e2_nr["pi0"]["T2"]["sig"] == "ns" and _e2_nr["pi0fast"]["T2"]["sig"] == "ns"
        and _e2_nr["gr00t_droid"]["T2"]["sig"] == "ns" and _e2_sp["gr00t_droid"] < 0.05 and _e2_sp["pi0"] < 0.05
        and _e2_sp["pi05"] >= 0.05 and _e2_sp["pi0fast"] >= 0.05 and _e2_mm["0.14"]["sig"] == "ns" and _e2_mm["0.18"]["sig"] == "ns"):
    print("  WARN appE2: the T2-vs-control verdicts changed; reword findings 0 and 2")

# Finding 2 (Table IIIe note, T2 against the control): Table IIIf's cell-level verdicts lead; the episode-level stratified test is secondary.
_rn2("GR00T N1.6-DROID (exact test stratified by placement, *p* < 0.001) is above it; π0 (exact test stratified by placement, *p* = 0.012) is below it, which on a policy that rarely completes these carries is not a safer carry.",
     "with the cell as the unit (Table IIIf, the primary test) π0.5 is above it (*p* " + _e2_pf(_e2_nr["pi05"]["T2"]["p"])
     + "), while π0 (*p* " + _e2_pf(_e2_nr["pi0"]["T2"]["p"]) + "), π0-FAST (*p* " + _e2_pf(_e2_nr["pi0fast"]["T2"]["p"])
     + ") and GR00T N1.6-DROID (*p* " + _e2_pf(_e2_nr["gr00t_droid"]["T2"]["p"])
     + (", the smallest *p* that four cells a side allow" if abs(_e2_nr["gr00t_droid"]["T2"]["p"] - _e2_g0perm) < 0.002 else "")
     + ") cannot be told from it. An exact test stratified by placement, secondary because it treats a cell's episodes as "
     "independent, puts GR00T N1.6-DROID above it (*p* " + _e2_pf(_e2_sp["gr00t_droid"]) + "), π0 below it (*p* "
     + _e2_pf(_e2_sp["pi0"]) + ") and π0.5 and π0-FAST short of the 5 %% level (*p* = %.3f and %.3f)" % (_e2_sp["pi05"], _e2_sp["pi0fast"])
     + "; π0's lower rate, on a policy that rarely completes these carries, is not a safer carry.")

# Finding 21 (Table IVb caption): the table has no π0-FAST column, so it does not cover every tabletop cell.
_rn2("(every tabletop cell; probes and demos excluded;",
     "(every tabletop cell of π0.5, π0, GR00T N1.6-DROID and the scripted control; π0-FAST, probes and demos excluded;")

# Finding 3 (T1 heading and the G1 mirror): the on-path keep-out is exposure, so it is a direct carry, not a scored defect.
_rn2("**T1 (keep-out) recurs on the headline channel.**", "**T1 (keep-out) ports to a second embodiment.**")
_rn2("a carried-hazard keep-out defect *and* a metric that is geometry-sensitive rather than saturated both recur on a second policy and embodiment, on the benchmark's **headline** channel.",
     "direct carries with no spontaneous detour *and* a metric that is geometry-sensitive rather than saturated both recur on a "
     "second policy and embodiment; on the path this is exposure, and the scored T1 is the off-path keep-out.")

# Finding 18 (rendered on-path marker): 'changes nothing' from 16/16 against 20/22 (p = 0.50, near ceiling) is a null claim.
_rn2('Seeing the hazard changes nothing: the "no execution-phase avoidance" signature holds for a second policy on a *rendered* hazard, on the headline channel — exactly as on the G1.',
     "Rendering the hazard produced no detectable detour, though near ceiling and at these sizes a moderate effect cannot be "
     "excluded: on a *rendered* hazard too the second policy's on-path carry is direct, as on the G1 — exposure, not a score.")

# Finding 11 (T5a): one non-significant Welch test does not show an absence; hedged as in §5.3 / §6 (iii).
_rn2("the position empty: no speed-and-separation behavior.",
     "the position empty: no detectable speed-and-separation behavior (a test with little power at these sizes).")

# Finding 16 (Table E.8x caption): the reaching hand is exposure and the attached control's contact cells carry no attribution;
# drop the p-values and the unsupported 'no policy withdraws' clause.
_rn2("The held-contact reading enters Table IIIc as a T6 secondary beside the control, which keeps the payload on the hand on 14/16 carried episodes: π0.5 keeps it there less often (*p* = 0.045, episodes unstratified); GR00T N1.6-DROID keeps it there less often (*p* = 0.010, episodes unstratified); no policy withdraws once it touches.",
     "The held-contact reading is listed in Table IIIc, outside the scores, beside the control, which keeps the payload on the "
     "hand on " + V["ik_handK"]["held_cond"] + " carried episodes; the reaching hand is exposure and the attached control's "
     "contact cells are attachment properties, so the control is a scale there, not an attributed comparator.")

# Finding 1 (serving geometry): Table III's scored T2 is the whole serving family (pour and stir included), not the pick-and-place subset.
_rn2("which is why Table IV's serving row reads 19 % where Table III reads 17 %: the scored pool is the whole serving family, 36 cells across three work surfaces",
     "which is why Table IV's serving row reads " + V["sv_T2_pct"] + " % where Table III reads " + V["pi_T2_pct"] + " % ("
     + V["pi_T2"] + "): the scored pool is the whole serving family, " + V["pi_T2_cells"] + " cells (" + V["t2sv_pi_cells"]
     + " of them pick-and-place, at " + V["t2sv_pi_pct"] + " %, plus pouring and stirring) across three work surfaces")

# Finding 8 (third DROID policy): GR00T N1.6-DROID's reaching hand is reached on 5/9 carried episodes (Table IIIb), touched on 3/9.
_e2_g0r = V["g0_T6"] if V.get("g0_T6") not in (None, "0/0", "—") else "5/9"
_rn2("the reaching hand is reached on 0/0 carried episodes.",
     "the reaching hand (exposure) is reached on " + _e2_g0r + " carried episodes and touched on " + V["g0_handK"]["touch"]
     + " (Table IIIb, Table E.8x).")

# Finding 5 (crossed surface x map design): two seeds pooled (Table IVd caption), and one mug cell delivers 15 of 16.
_e2_seedw = {"1": "one", "2": "two", "3": "three", "4": "four"}.get(str(V["b5_seeds"]), str(V["b5_seeds"]))
import re as _e2re
_e2_bc = _e2_bn = _e2_bd = _e2_bk = _e2_bt = 0
for _e2_ln in V["b5_rows"].split("\n"):
    _e2_cells = _e2_ln.split("|")
    if len(_e2_cells) < 4:
        continue
    _e2_m = _e2re.search(r"(\d+)/(\d+) carried, (\d+) delivered; T4 (\d+)/(\d+)", _e2_cells[3])
    if _e2_m:
        _e2_bc += int(_e2_m.group(1)); _e2_bn += int(_e2_m.group(2)); _e2_bd += int(_e2_m.group(3))
        _e2_bk += int(_e2_m.group(4)); _e2_bt += int(_e2_m.group(5))
_e2_carry = ("the mug is carried on every attempt under every map (%d/%d)" % (_e2_bc, _e2_bn) if _e2_bc == _e2_bn
             else "the mug is carried on %d/%d attempts" % (_e2_bc, _e2_bn))
_rn2("Two work surfaces under three environment maps, one seed, eight episodes per cell (Table IVd): every mug carry completes under every map and stays near upright (T4 1/96)",
     "Two work surfaces under three environment maps, " + _e2_seedw + " seeds of eight episodes each (Table IVd): " + _e2_carry
     + " and delivered on %d/%d, staying near upright (T4 %d/%d)" % (_e2_bd, _e2_bn, _e2_bk, _e2_bt))

# Finding 19 (pinch-grasp control): every surface has exactly one tilt past 45°, and the counter is not the weakest.
_e2_pg = V["pg_surf"]
_e2_pgk = [_e2_kn(_e2_pg[s]["T4"]) for s in ("dining", "kitchen", "office")]
_e2_pgall = "%d/%d" % (sum(k for k, _ in _e2_pgk), sum(n for _, n in _e2_pgk))
_e2_rate = lambda s: int(_e2_pg[s]["car"]) / int(_e2_pg[s]["att"])
if all(k == 1 for k, _ in _e2_pgk) and max(_e2_rate("kitchen"), _e2_rate("dining")) < _e2_rate("office"):
    _e2_pgtxt = ("each surface keeps the grasped mug under 45° on all but one carry — and the pinch itself carries least often at "
                 "the counter and the dining table (" + _e2_pg["kitchen"]["car"] + "/" + _e2_pg["kitchen"]["att"] + " and "
                 + _e2_pg["dining"]["car"] + "/" + _e2_pg["dining"]["att"] + ", against " + _e2_pg["office"]["car"] + "/"
                 + _e2_pg["office"]["att"] + " at the desk)")
else:
    print("  WARN appE2: pinch-grasp per-surface counts changed; reword finding 19")
    _e2_pgtxt = "the per-surface counts above apply — and the pinch carries at different rates by surface"
_rn2("two of three surfaces keep the grasped mug under 45° on nearly every carry — and it is weakest at the counter, where the pinch itself is least reliable; the pooled 3/31 is what Table III carries.",
     _e2_pgtxt + "; the pooled " + _e2_pgall + " is what Table III carries.")

# Finding 6 (off-path keep-out): §6 (ii) argues a far-side drift, not an attraction to the hazard.
_rn2("put a number on the attraction of §6 (ii)", "put a number on the far-side drift of §6 (ii)")

# Finding 7 (off-path keep-out): at 0.12 m the policy closes 0.06 of a 0.12 m offset, half of it, not two thirds.
_e2_g = 1 - float(V["t1_off"]["d12"]["dmed"]) / float(V["t1_off_ctrl"]["d12"]["dmed"])
_e2_gw = {"0.50": "half", "0.67": "two thirds", "0.33": "a third", "0.25": "a quarter", "0.75": "three quarters"}.get(
    "%.2f" % _e2_g, "%d %%" % round(100 * _e2_g))
_rn2("the policy gives away two thirds of it.", "the policy gives away " + _e2_gw + " of it.")

# Finding 20 (off-path keep-out): the grid's on-path control column sums to 56/56; 72/72 counts on-path cells outside the grid.
_rn2("The midpoint cell stays exposure: there the control violates 72/72 at zero clearance.",
     "The midpoint cell stays exposure: there the control violates " + V["t1_off_by"]["ik"]["on"]["rate"]
     + " at zero clearance on the grid's cells (" + V["t1_off_ctrl"]["on"]["rate"] + " over all its on-path cells).")
_rn2("for the policy against 72/72, 64/64, 15/64, 0/64 for a straight line",
     "for the policy against " + V["t1_off_by"]["ik"]["on"]["rate"] + ", " + V["t1_off_ctrl"]["d12"]["rate"] + ", "
     + V["t1_off_ctrl"]["d20"]["rate"] + ", " + V["t1_off_ctrl"]["d28"]["rate"] + " for a straight line")

# Finding 0 (T2 serving subset): Table IIIf has π0.5 above the control at the 0.10 m margin; Table IIIe holds no stratified test,
# and π0 is 'not distinguishable' there, not below.
_rn2("Three of the four policy intervals overlap the control's, and no openpi policy is above it (π0 is below it on the stratified test, Table IIIe): for them T2 does not single out a policy that sweeps more than a straight line to a bowl beside a person, and there it measures the placement rather than the policy.",
     "Three of the four policy intervals overlap the control's. Matched by placement (Table IIIf), π0.5 is above it at the 0.10 m "
     "link-origin margin (*p* " + _e2_pf(_e2_mm["0.1"]["p"]) + ") but not at 0.14 or 0.18 m (*p* = %.2f and %.2f)"
     % (_e2_mm["0.14"]["p"], _e2_mm["0.18"]["p"]) + ", and π0-FAST and π0 cannot be told from it (*p* = %.3f and %.3f)"
     % (_e2_nr["pi0fast"]["T2"]["p"], _e2_nr["pi0"]["T2"]["p"]) + ": among the openpi policies T2 singles out a sweep beyond "
     "a straight line's to a bowl beside a person only for π0.5 and only at the tightest margin; elsewhere it does not "
     "separate the policy from the placement.")

# Finding 17 (radius probe): the outward bow shrinks with radius but never reverses within 0.35-0.75 m; the causal pull is not shown.
_e2_dr = V["drift_rad"]
_e2_far = lambda r, p: _e2_dr[r][p]["far"].lstrip("+")
if not all(float(_e2_dr[r][p]["far"]) > 0 for r in ("35", "45", "55", "65", "75") for p in ("pi", "f0")):
    print("  WARN appE2: the radius probe's far bow changed sign; reword finding 17")
_rn2("The outward bow falls from 0.099 m at 0.35 m to 0.018 m at 0.75 m and turns inward at 0.75 m: the drift is a pull toward the radius at which the demonstrations were given, not a fixed bend of the arm. The keep-out entries of the trajectory dimension are therefore the benchmark's transports sitting inside the demonstrations' workspace, and a scene laid out farther from the base would see the bow reverse.",
     "The outward bow shrinks with distance from the base, though not monotonically (π0.5 " + _e2_far("35", "pi") + " m at 0.35 m, "
     + _e2_far("55", "pi") + " m at 0.55 m, " + _e2_far("65", "pi") + " m at 0.65 m and " + _e2_far("75", "pi")
     + " m at 0.75 m; π0-FAST " + _e2_far("35", "f0") + " to " + _e2_far("75", "f0") + " m), so it is not a fixed bend of the arm, "
     "and it does not reverse within the probed range: it stays outward at 0.65 and 0.75 m, past the demonstrations' median radius ("
     + V["droid"]["rmid"] + " m), although their own outer transports bow inward. The shrinking is consistent with a pull toward the demonstrations' "
     "workspace, but the probe does not establish the cause. The keep-out entries of the trajectory dimension may therefore "
     "reflect, in part, the benchmark's transports sitting at the inner edge of the demonstrations' workspace.")

# Finding 10 (late-arriving person): an equivalence claim from non-significant tests at 16 episodes per arm.
_rn2("A person who arrives mid-carry is met as one who was always there, and both as one who is absent: the duration of exposure does not enter the motion.",
     "No contrast shows a late-arriving person met more cautiously than one who was always there or one who is absent; at 16 "
     "episodes per arm a moderate effect of the exposure's duration cannot be excluded.")

# Finding 4 (withdrawing hand): 39/91 against 106/210 (p = 0.26) supports no directional or causal reading.
_e2_hs = V["hand_state"]
_rn2("A hand that can move away is touched less often than one that cannot — 39/91 against 106/210 (43 % against 50 %, Fisher *p* = 0.2587) — so part of the static hand's exposure is the proxy's immobility.",
     "A hand that can move away is touched on " + _e2_hs["withdraw"] + " against " + _e2_hs["static"] + " for one that cannot ("
     + _e2_hs["withdraw_pct"] + " % against " + _e2_hs["static_pct"] + " %%, Fisher *p* = %.2f" % float(_e2_hs["p"])
     + "): no detectable difference at these sizes.")

# Finding 14 (first probe's mug): name the task the 1/16 and 2/16 come from (pick-and-place), apart from the serving cells below.
_e2_b3 = V["b3"]
_rn2("the mug past 45° on 1/16 and 2/16 — and, in the tool cells",
     "the mug past 45° on " + _e2_b3["child"]["T4"] + " and " + _e2_b3["seated"]["T4"] + " (pick-and-place) — and, in the tool cells")

# Finding 23 (first probe): the adult-rendered caveat appears twice in back-to-back sentences.
_rn2("episodes; those cells also rendered the adult. Those cells scored", "episodes. Those cells scored")

# Findings 13, 14 and 15 (re-rendered small bystanders): compare like with like -- right-hand pick-and-place against the
# right-hand first probe, left side apart; the served-mug tilt against pi0.5's adult-rendered serving cells (mug, right).
_e2_sv = V["small_vis"]
_e2_sx = V["sxs"]
_e2_hv = V["svhv"]
if _e2_sv["child"]["old_T4"] == "8/30" and _e2_sv["seated"]["old_T4"] == "2/29":
    _e2_o4c, _e2_o4s = "2/16", "1/15"     # pi0.5 svch_mug_R / svst_mug_R; the generator value also pools pi0-FAST's cells
else:
    _e2_o4c, _e2_o4s = _e2_sv["child"]["old_T4"], _e2_sv["seated"]["old_T4"]
_rn2("they give the same answer: the arm comes within 0.10 m on 0/32 and 0/32 episodes (previously 0/16 and 1/16), the blade points into their half-space on 9/18 and 11/22 carries (previously 1/11 and 0/11), and the served mug passes 45° on 1/15 and 2/16 (previously 8/30 and 2/29).",
     "they give the same answer at the right-hand placement: carrying to a bowl away from them (pick-and-place), the arm comes "
     "within 0.10 m on " + _e2_sx["child"]["R"]["T2"] + " and " + _e2_sx["seated"]["R"]["T2"] + " episodes (previously "
     + _e2_sv["child"]["old_T2"] + " and " + _e2_sv["seated"]["old_T2"] + ") and the blade points into their half-space on "
     + _e2_sx["child"]["R"]["T3"] + " and " + _e2_sx["seated"]["R"]["T3"] + " carries (previously " + _e2_sv["child"]["old_T3"]
     + " and " + _e2_sv["seated"]["old_T3"] + "; on the left " + _e2_sx["child"]["L"]["T3"] + " and " + _e2_sx["seated"]["L"]["T3"]
     + ", the adult's side signature); serving the mug into a bowl beside them, the mug passes 45° on " + _e2_hv["child"]["T4"]
     + " and " + _e2_hv["seated"]["T4"] + " carries (previously, adult rendered, " + _e2_o4c + " and " + _e2_o4s + ").")

# Finding 12 (receiver state): carried 25/64 against 24/48 (p = 0.26) and presented 12/25 against 16/24 (p = 0.25) support
# neither 'changes whether' nor 'not how'; the attempts are fixed by design, so it is the carry rate that differs.
_e2_ha, _e2_hr = _e2_b3["hand_away"], _e2_b3["handover"]
_e2_p1 = _e2_fisher(int(_e2_ha["car"]), int(_e2_ha["att"]), int(_e2_hr["car"]), int(_e2_hr["att"]))
_e2_k1, _e2_n1 = _e2_kn(_e2_ha["ho"]); _e2_k2, _e2_n2 = _e2_kn(_e2_hr["ho"])
_e2_p2 = _e2_fisher(_e2_k1, _e2_n1, _e2_k2, _e2_n2)
_rn2("the handover is attempted less often (25/64 carried against 24/48) and the hazardous end is presented to the parked hand on 12/25 (reaching hand: 16/24); the receiver's state changes whether the policy hands over, not how.",
     "the handover is carried on %s/%s against %s/%s when the hand reaches in, and the hazardous end is presented to the hand on "
     "%s against %s; neither difference is distinguishable at these sizes (Fisher *p* = %.2f and %.2f)."
     % (_e2_ha["car"], _e2_ha["att"], _e2_hr["car"], _e2_hr["att"], _e2_ha["ho"], _e2_hr["ho"], _e2_p1, _e2_p2))

# Finding 22 (cued walker): 'exactly' is an untested equivalence claim, and the π0 speeds differ by a third.
_e2_cp = V["cue_pi0"]
_rn2("A person who visibly prepares to move is met exactly as one who does not (π0: 0.135 m/s with the cue against 0.100 without, 16 and 10 carries).",
     "Neither policy is shown to read the cue (π0: " + _e2_cp["cue_med"]
     + " m/s with the cue against " + _e2_cp["nocue_med"] + " without, " + _e2_cp["n_cue"] + " and " + _e2_cp["n_nocue"]
     + " carries, untested).")

# Finding 9 (T2 first probe): GR00T is above π0.5 at every radius, so no margin makes GR00T look safer; the matched-geometry
# GR00T rate is the 3-D 84 % of the closing parenthesis, not the horizontal-curve 75 %.
_rn2('so at the matched 0.26 m geometry GR00T (≈ 75 %) is *not* safer than π0.5 (53 %), and no single margin supports "π0.5 is safer" either.',
     "so at the matched geometry (3-D, Appendix E.3) GR00T sweeps 84 % against π0.5's 53 %; the margin sets the absolute rates "
     "and how far apart the two look, not their order.")
_rn2("because a single margin can be chosen to make either policy look safe.",
     "because the margin alone sets how often either policy is charged with a sweep.")

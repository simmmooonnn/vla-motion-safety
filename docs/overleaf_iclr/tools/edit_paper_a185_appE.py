# -*- coding: utf-8 -*-
# Review-round audit wf_f701d32a-3ba, block appE: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).

_PD = V["pdose"]["arms"]
_pi, _fa = _PD["pi05"], _PD["pi0fast"]
_n2 = V["null_rel"]["pi05"].get("T2")      # MISRUN 2026-10-08: absent once the mis-run control cells are removed
_g2 = V["null_rel"]["gr00t_droid"].get("T2")
_g4 = V["null_rel"]["gr00t_droid"]["T4"]
_g4_27 = V["t4_thr_matched"]["gr00t_droid"]["27"]
_bo = V["b2x_old"]["arms"]
_br = V["b2xr"]["arms"]
_pcp = V["pcp"]


def _ci(c):
    return "[%s, %s]" % tuple(("+%d" % x) if x > 0 else ("−%d" % -x) if x < 0 else "0" for x in c)


# E.8 T4 (F9): the hot-coffee instruction also carries the spill clause; say so where it is first described
_rn2("Told the mug holds hot coffee and to keep it upright, it tilts it past 45° on 8/14 carries at the dining table",
     "Told the mug holds hot coffee and to keep it upright so the coffee does not spill, it tilts it past 45° on 8/14 carries at the dining table")
# E.8 T4 (F9): X1 list, the "keep-upright sentence alone" arm is the full sentence with the spill clause
_rn2("the keep-upright sentence alone 27/32 (against neutral",
     """the sentence alone ("Keep the mug upright so the coffee does not spill.") 27/32 (against neutral""")
# E.8 T4 (F1): the bowl arm kept the spill clause, so it cannot show the words are ungrounded
_rn2("""("keep the bowl upright") 26/32 (against the mug sentence, *p* = 1.00); delivered on 32/32 (neutral), 16/32 (sentence), 31/32 (irrelevant), 19/32 (bowl). The sentence, not its length, raises the tilt, and not through what it says: aimed at the bowl it tilts the mug as often, so the words change the carry without being grounded in the object they name.""",
     """("Keep the bowl upright so the coffee does not spill.") 26/32 (against the mug sentence, *p* = 1.00); delivered on 32/32 (neutral), 16/32 (sentence), 31/32 (irrelevant), 19/32 (bowl). The sentence, not its length, raises the tilt. The swapped sentence still carries the clause about the coffee, which the dose experiment below finds to be an active part (Table XIII), so this arm does not show that the words act without being grounded in the object they name.""")
# E.8 T4 (F7): reconcile the pi0-FAST X1 null with the dose result at the same table (seeds and noun both differ)
_rn2("π0-FAST at the dining table: neutral 4/16, noun and sentence 3/14, irrelevant sentence 0/16.",
     "π0-FAST at the dining table (seeds 7 and 11): neutral 4/16, noun and sentence 3/14, irrelevant sentence 0/16, with no detectable rise; in the dose experiment below (seeds 13 and 17), by contrast, the sentence without the noun tilts its mug on 8/14 carries at the same table against 0/16 neutral (Fisher *p* < 0.001; pooled with the office desk in Table XIII). The two runs differ in seeds and in the noun, and which difference accounts for the contrast is not separated.")
# E.8 T4 (F7, follow-on): the dose experiment is now referred to ahead ("below"), so its introduction takes the definite article
_rn2("A dose experiment (seeds 13 and 17, dining table and office desk, both policies)",
     "The dose experiment (seeds 13 and 17, dining table and office desk, both policies)")
# E.8 T4 (F6 + F8): add the "as little as possible" arm; the upright clause alone is not detectably active (not "does nothing"), and placed first it lowers pi0-FAST's deliveries
_rn2("""the clause about spilling raises the tilt on its own (π0.5 Fisher *p* < 0.001, π0-FAST *p* < 0.001 against neutral), "keep the mug upright" or "level" or "carefully" does not, and the upright clause alone does nothing, before the task or after it.""",
     """the clause about spilling raises the tilt on its own (π0.5 %s, π0-FAST %s; Fisher *p* < 0.001 each against neutral), and so does "tilt the mug as little as possible" (%s and %s, *p* < 0.001 each); "keep the mug level" or "carefully" does not detectably raise it, nor does the upright clause alone, after the task or before it (π0.5 %s and %s, π0-FAST %s and %s, against %s and %s), though placed first it lowers π0-FAST's deliveries (%s against %s, *p* < 0.001).""" % (
         _pi[3]["t45"], _fa[3]["t45"], _pi[6]["t45"], _fa[6]["t45"],
         _pi[1]["t45"], _pi[7]["t45"], _fa[1]["t45"], _fa[7]["t45"], _pi[0]["t45"], _fa[0]["t45"],
         _fa[7]["delivered"], _fa[0]["delivered"]))
# E.8 T4 (F19): blank line after Table XIII's last row, so the paragraph is not absorbed into the table
_rn2("|\n The instruction changes the carry, not the grasp:", "|\n\nThe instruction changes the carry, not the grasp:")
# E.8 T4 (F9): hot-lift sentence, "under the keep-upright sentence" -> the sentence alone (X1 arm)
_rn2("3 of the 27 under the keep-upright sentence)", "3 of the 27 under the sentence alone)")
# E.8 T4 pools (F2): pi0.5 T2 is not above the control once Holm-corrected (Table IIIf, primary)
_n2 and _g2 and _rn2("with the cell as the unit (Table IIIf, the primary test) π0.5 is above it (*p* = 0.013), while π0 (*p* = 0.067), π0-FAST (*p* = 0.167) and GR00T N1.6-DROID (*p* = 0.056, the smallest *p* that four cells a side allow) cannot be told from it.",
     "with the cell as the unit (Table IIIf, the primary test) none of the four can be told from it once the 16 tests are Holm-corrected: π0.5 *p* = %.3f uncorrected (Holm %.3f; +%d points %s), π0 *p* = 0.067, π0-FAST *p* = 0.167 and GR00T N1.6-DROID *p* = 0.056, the smallest *p* that four cells a side allow." % (
         _n2["p"], _n2["p_holm"], _n2["rd"], _ci(_n2["ci"])))
# E.8 T4 pools (F3): GR00T-DROID T4 is an uncorrected, threshold-specific excess, not "above" on the primary test
_rn2("GR00T N1.6-DROID (exact test stratified by placement, *p* = 0.033) is above it.",
     "GR00T N1.6-DROID is higher (+%d points %s; cell permutation *p* = %.3f, an exact test stratified by placement *p* = 0.033), but the excess does not survive Holm correction (%.3f) and is not seen past 27° (%s against %s, *p* = 0.45; Table IIIf)." % (
         _g4["rd"], _ci(_g4["ci"]), _g4["p"], _g4["p_holm"], _g4_27["pol"], _g4_27["ctl"]))
# Table IIIf note (F14): "holds" -> uncorrected excess appears; precise cross-reference
_rn2("π0.5's T2 holds at the 0.10 m link-origin margin but not at the 0.14–0.18 m a link's surface implies (23/64 against 10/32 at 0.14 m, *p* = 0.70; E), and GR00T N1.6-DROID's T4 holds past 45° but not past 27°",
     "π0.5's uncorrected T2 excess appears at the 0.10 m link-origin margin but not at the 0.14–0.18 m a link's surface implies (23/64 against 10/32 at 0.14 m, *p* = 0.70; E.8, T2), and GR00T N1.6-DROID's uncorrected T4 excess appears past 45° but not past 27°")
# Table IIIf caption (F15): define the "min", Holm and interval notation as printed
_rn2("with the smallest attainable p in brackets when it is above 0.01).",
     """with the smallest attainable p added as "min" when it is above 0.01); the final parenthesis holds the Holm-adjusted p over the table's 16 rows, and the brackets a 95 % interval for the difference (cluster-robust by cell, *t* with the smaller arm's cell count minus one degrees of freedom).""")
# Table IIIf T1 rows (F15): Holm printed "(0.0)"; with 4000 permutations and none as extreme, 16 x 1/4001 = 0.004, so "< 0.005" (not "< 0.001")
if t.count("< 0.001 (0.0) |") == 2:
    t = t.replace("< 0.001 (0.0) |", "< 0.001 (< 0.005) |")
else:
    print("  MISS x%d Table IIIf T1 Holm (0.0)" % t.count("< 0.001 (0.0) |"))
# E.8 T2 (F5): the 0.10 m excess is not distinguishable once Holm-corrected; report CI and Holm
_n2 and _g2 and _rn2("π0.5's excess of +16 points at 0.10 m (20/64 against 5/32, *p* = 0.013) is +5 at 0.14 m (23/64 against 10/32, *p* = 0.70) and −5 at 0.18 m (33/64 against 18/32, *p* = 0.73): where the margin is drawn decides whether π0.5's arm sweeps the body more than the straight line does.",
     "π0.5's excess of +%d points at 0.10 m (20/64 against 5/32; 95 %% CI %s, *p* = %.3f, Holm %.3f) shrinks to +5 at 0.14 m (23/64 against 10/32, *p* = 0.70) and −5 at 0.18 m (33/64 against 18/32, *p* = 0.73): at no margin is π0.5's sweep distinguishable from the straight line's after correction, and the uncorrected 0.10 m excess depends on where the margin is drawn." % (
         _n2["rd"], _ci(_n2["ci"]), _n2["p"], _n2["p_holm"]))
# E.8 T2 serving family (F4): T2 singles out no openpi policy at any margin once Holm-corrected; drop the redundant tail
_n2 and _g2 and _rn2("π0.5 is above it at the 0.10 m link-origin margin (*p* = 0.013) but not at 0.14 or 0.18 m (*p* = 0.70 and 0.73), and π0-FAST and π0 cannot be told from it (*p* = 0.167 and 0.067): among the openpi policies T2 singles out a sweep beyond a straight line's to a bowl beside a person only for π0.5 and only at the tightest margin; elsewhere it does not separate the policy from the placement.",
     "π0.5's excess at the 0.10 m link-origin margin (*p* = %.3f) does not survive Holm correction (%.3f) and is not seen at 0.14 or 0.18 m (*p* = 0.70 and 0.73), and π0-FAST and π0 cannot be told from the control (*p* = 0.167 and 0.067): once Holm-corrected, T2 does not separate any openpi policy's sweep from a straight line's." % (
         _n2["p"], _n2["p_holm"]))
# E.8 T2 serving family (F13): GR00T-DROID's divergence is suggested by the pooled intervals, not established by the matched test
_n2 and _g2 and _rn2("GR00T N1.6-DROID is the exception and its interval clears the control's by a wide margin, so on this predicate the policies diverge where §5.5 finds them recurring — the same body-sweep geometry that the humanoid's walking base produces is produced at the table by this policy's arm and by no other.",
     "GR00T N1.6-DROID's pooled interval clears the control's and its matched difference is +%d points %s, but with four cells a side the permutation test cannot go below *p* = %.3f (Holm %.2f; Table IIIf): a divergence from the recurrence §5.5 finds is suggested, not established, and the body-sweep geometry the humanoid's walking base produces may be produced at the table by this policy's arm and by no other." % (
         _g2["rd"], _ci(_g2["ci"]), _g2["p"], _g2["p_holm"]))
# E.8 T1 grid (F12): move the T1-twin paragraph and Table XIV after "the on-path cell is exposure.", so the surface grid follows its colon
_a = t.find("**Is the keep-out avoided or only bowed into?**")
_c = t.find("**Table XIV.", _a) if _a >= 0 else -1
_h = t.find("| Policy | far, rendered", _c) if _c >= 0 else -1
_b = t.find("\n\n", _h) if _h >= 0 else -1
_anc = "the on-path cell is exposure. **The body sweep needs a destination beside the person.**"
if min(_a, _c, _h, _b) >= 0 and t.count(_anc) == 1 and t.find(_anc) > _b and t[_b + 2:].startswith("| Surface |"):
    _blk = t[_a:_b]
    t = t[:_a] + t[_b + 2:]
    t = t.replace(_anc, "the on-path cell is exposure.\n\n" + _blk + "\n\n**The body sweep needs a destination beside the person.**", 1)
else:
    print("  MISS move T1-twin paragraph and Table XIV")
# E.2 replication (F11): the naming effect is one uncorrected test, leaves the clearance unmoved and reverses the earlier direction
_rn2("naming the stove raises the violation with it rendered (Fisher *p* = 0.031 rendered, = 0.44 hidden).",
     "with the stove rendered the named arm violates more often (%d/%d against %d/%d blind, Fisher *p* = 0.031, one of four uncorrected tests; *p* = 0.44 hidden) without moving the median clearance (%.3f against %.3f m, *p* = 0.99), opposite in direction to the substitute-driver day (37 %% to 29 %%), so no naming effect on the rate is established." % (
         _br["named_rend"]["viol"], _br["named_rend"]["comp"], _br["blind_rend"]["viol"], _br["blind_rend"]["comp"],
         _br["named_rend"]["clr_med"], _br["blind_rend"]["clr_med"]))
# E.2 replication (F10): the completion interaction does not replicate (naming the hidden stove now lowers completion)
_rn2("The direction of the rendering effect replicates; the scored G1 T1 rate is specific to its seeds and driver and is read as a case-study figure, not an estimate.",
     "The direction of the rendering effect replicates; the completion interaction does not: naming the hidden stove now lowers completion (%d/%d against %d/%d, Fisher *p* = 0.031, where before it raised it from 47 %% to 68 %%), and the named-plus-visible arm (%d/%d) is no longer the lowest. The scored G1 T1 rate and these completion effects are specific to their seeds and driver and are read as case-study figures, not estimates." % (
         _br["named_hid"]["comp"], _br["named_hid"]["att"], _br["blind_hid"]["comp"], _br["blind_hid"]["att"],
         _br["named_rend"]["comp"], _br["named_rend"]["att"]))
# E.2 Table XI (F16): medians from the full-precision recompute (b2x_old) and Wilson [22, 54] for 11/30
_rn2("| blind, rendered | 30 / 49 (61 %) | 11 / 30 = 37 % [22, 55] | 0.310 |",
     "| blind, rendered | 30 / 49 (61 %%) | 11 / 30 = 37 %% [22, 54] | %.3f |" % _bo["blind_rend"]["clr_med"])
_rn2("| named, rendered | 21 / 72 (29 %) | 6 / 21 = 29 % [14, 50] | 0.315 |",
     "| named, rendered | 21 / 72 (29 %%) | 6 / 21 = 29 %% [14, 50] | %.3f |" % _bo["named_rend"]["clr_med"])
_rn2("| blind, hidden | 34 / 72 (47 %) | 7 / 34 = 21 % [10, 37] | 0.333 |",
     "| blind, hidden | 34 / 72 (47 %%) | 7 / 34 = 21 %% [10, 37] | %.3f |" % _bo["blind_hid"]["clr_med"])
_rn2("| named, hidden | 49 / 72 (68 %) | 8 / 49 = 16 % [9, 29] | 0.363 |",
     "| named, hidden | 49 / 72 (68 %%) | 8 / 49 = 16 %% [9, 29] | %.3f |" % _bo["named_hid"]["clr_med"])
# E.2 text (F16): the same medians in the rendering sentence (p values kept: full-precision analysis)
_rn2("(0.333 → 0.310 m blind, 0.363 → 0.315 m named;",
     "(%.3f → %.3f m blind, %.3f → %.3f m named;" % (_bo["blind_hid"]["clr_med"], _bo["blind_rend"]["clr_med"], _bo["named_hid"]["clr_med"], _bo["named_rend"]["clr_med"]))
# E.2 text (F16): naming moves the rendered-stove path 1 cm (0.308 -> 0.321), not "not at all"
_rn2("and the rendered one not at all (*p* = 0.30)", "and the rendered one 1 cm, not detectably (*p* = 0.30)")
# E.8 locate-the-person probe (F17): 16 counts episodes, not carries (15 and 14 carried)
_rn2("on 0/16 carries with the person rendered (median distance 0.72 m) and on 0/16 with the same words and the person hidden (0.77 m;",
     "on 0/16 episodes with the person rendered (%d carried; median distance 0.72 m) and on 0/16 with the same words and the person hidden (%d carried; 0.77 m;" % (
         _pcp["B"]["carried"], _pcp["C"]["carried"]))
# E.8 crossing hand (F18): pi0's scored crossing pool comes from two surfaces, not three
_rn2("π0 reaches it on 7/8 across the three surfaces and waits on 0/8",
     "π0 reaches it on 7/8 at two surfaces (its office-desk cells score no crossing) and waits on 0/8")

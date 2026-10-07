# -*- coding: utf-8 -*-
# Review-round audit wf_f701d32a-3ba, block back: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).
# Main-text edits (Sec. 6-8, Reproducibility Statement) trim inside the same paragraph so the main text does not grow;
# Appendix C edits are free. Nothing here touches the running rp_ replication or the p0_pd_/g0_pd_ prompt dose.
import math as _m185


def _a185_fisher(a, n1, c, n2):
    """Two-sided Fisher exact p for a/n1 against c/n2."""
    k = a + c
    lg = lambda x: _m185.lgamma(x + 1)
    def pr(x):
        return _m185.exp(lg(n1) - lg(x) - lg(n1 - x) + lg(n2) - lg(k - x) - lg(n2 - k + x)
                         - (lg(n1 + n2) - lg(k) - lg(n1 + n2 - k)))
    p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(k, n1) + 1) if pr(x) <= p0 * (1 + 1e-9)))


def _a185_kn(s):
    a, b = str(s).split("/")
    return int(a), int(b)


def _a185_get(path, default):
    try:
        v = V
        for k in path:
            v = v[k]
        return v
    except Exception:
        return default


# numbers from the generator (fallbacks are the values the audit verified)
_a185_tilt5 = _a185_get(["pdose", "arms", "pi05", "6", "t45"], "18/32")       # "tilt the mug as little as possible"
_a185_tiltf = _a185_get(["pdose", "arms", "pi0fast", "6", "t45"], "21/28")
_a185_bowl = _a185_get(["pv", "pi05", "F", "t45"], "26/32")                         # keep the bowl upright so ... spill
_a185_mug = _a185_get(["pv", "pi05", "C", "t45"], "27/32")                          # keep the mug upright so ... spill
_a185_namep = _a185_get(["b2xr", "contrasts", "naming_hidden", "clr_p"], 0.492)   # naming shift, two new seeds
_a185_v = _a185_get(["b2xr", "contrasts", "rendering_pooled", "viol"], "32/36")
_a185_vh = _a185_get(["b2xr", "contrasts", "rendering_pooled", "viol_hid"], "22/33")
_a185_vp = _a185_fisher(*_a185_kn(_a185_v), *_a185_kn(_a185_vh))
_a185_shifts = [abs(_a185_get([r, "contrasts", c, "clr_shift"], d)) for r, c, d in
           [("b2x_old", "rendering_blind", -0.024), ("b2x_old", "rendering_named", -0.045),
            ("b2xr", "rendering_blind", -0.033), ("b2xr", "rendering_named", -0.047)]]
_a185_srng = "%d–%d" % (int(round(100 * min(_a185_shifts))), int(round(100 * max(_a185_shifts))))


def _a185_g1t6b():
    for _r in str(_a185_get(["tab3b_rows"], "")).split("\n"):
        if _r.startswith("| GR00T N1.6 · G1 |"):
            _c = [c.strip() for c in _r.strip().strip("|").split("|")][1:]
            _d = dict(zip(["T1", "T2", "T3", "T4", "T5a", "T5b", "T6", "T6b"], _c))
            return _d.get("T6b", "17/18").split(" = ")[0]
    return "17/18"


_a185_t6b = _a185_g1t6b()

# ---------------------------------------------------------------- Sec. 6 (i)
# F54 + trim: "leaves the violation unchanged" overclaims a non-significant test -> "does not detectably lower"; to pay for the
# words, the per-attempt T1/T3 rates (shown in Fig. fixability) leave the sentence and "explicit" goes (Sec. 4.2 defines it).
_rn2("Among completing carries an explicit safety command leaves the violation unchanged (T1, a hazard on the path: 8/8 and 7/7; "
     "T3: 8/12 and 11/14); per attempt the rates move only with completion (T1 8/24 → 7/24, T3 8/24 → 11/24, T6 30 → 25 %; "
     "Fig. \\ref{fig:fixability}).",
     "Among completing carries a safety command does not detectably lower the violation (T1, a hazard on the path: 8/8 and "
     "7/7; T3: 8/12 and 11/14); per attempt the rates move only with completion (T6 30 → 25 %; Fig. \\ref{fig:fixability}).")
# F49: the naming shift is from the substitute-driver seeds only and does not recur on the two new seeds (b2xr naming_hidden);
# the test name goes (Sec. 4.2 gives Mann-Whitney for ablation clearance), and "rate" goes from the previous clause to pay
_rn2("With the stove 0.28 m off the path, neither naming nor rendering lowers the violation rate (Table XI)",
     "With the stove 0.28 m off the path, neither naming nor rendering lowers the violation (Table XI)")
_rn2("naming away from a hidden stove (Mann–Whitney *p* = 0.017), rendering toward it (*p* = 0.013, 0.005)",
     "naming away from a hidden stove (*p* = 0.017; %.2f on two new seeds), rendering toward it (*p* = 0.013, 0.005)" % _a185_namep)
# F47 + F51: the spill clause is not the only wording that tilts the mug ("tilt the mug as little as possible" does too), and
# the bowl sentence is compared with its matched mug sentence on the prompt control's seeds, not with the dose's 30/32
_rn2("The clause about spilling is what moves the carry: \"do not spill the coffee\" tilts the mug past 45° on 30/32 carries "
     "(π0-FAST 14/27) against 3/32 (0/32) neutral and \"keep the mug upright\" alone on 5/32 (1/31), and "
     "keep-the-*bowl*-upright-so-it-does-not-spill does it as often (26/32): the words act on the carry without being grounded "
     "in their object (E.8).",
     "\"Do not spill the coffee\" tilts the mug past 45° on 30/32 carries (π0-FAST 14/27) and \"tilt the mug as little as "
     "possible\" on %s (%s), against 3/32 (0/32) neutral and \"keep the mug upright\" alone on 5/32 (1/31); "
     "keep-the-*bowl*-upright-so-it-does-not-spill does it as often as its *mug* version (%s, %s): the words act on the carry, "
     "ungrounded in their object (E.8)." % (_a185_tilt5, _a185_tiltf, _a185_bowl, _a185_mug))

# ---------------------------------------------------------------- Sec. 6 (ii)
# F50 + F48: the rendered-stove shift is 2-5 cm across both runs (E.2), and on the two new seeds the higher violation rate is
# significant (32/36 against 22/33); the parenthetical and the twin's last clause are tightened to pay for it
_rn2("The humanoid's 2–3 cm shift toward a rendered stove (two seeds on the substitute driver, replicated on two new seeds; E.2) "
     "comes with a non-significantly higher violation rate (17/51 against 15/83, *p* = 0.06).",
     "The humanoid's %s cm shift toward a rendered stove (two substitute-driver seeds, replicated on two new ones; E.2) comes "
     "with a higher violation rate (17/51 against 15/83, *p* = 0.06; new seeds %s against %s, *p* = %.2f)."
     % (_a185_srng, _a185_v, _a185_vh, _a185_vp))
# trims (pay for F48 and for naming which run each pair comes from): same meaning, fewer words
_rn2("the bend toward the far side is there whether or not anything is",
     "the far-side bend is there whether or not anything is")
_rn2("and 22/24 with it absent on the far side,", "and 22/24 without it on the far side,")

# ---------------------------------------------------------------- Sec. 6 (iv)
# F61: "at any crossing speed" is false at 0.06 m/s (one of 18 scored encounters decelerates); scope it to the sweep (T6) and
# give the G1 T6b count; the next clause is tightened to pay for it
_rn2("No deceleration precedes contact at any crossing speed (T6), and a person who stops at the first touch is struck on every "
     "carried encounter (§5.4).",
     "No deceleration precedes contact at 0.3–1.2 m/s (T6) or on %s scored encounters (T6b), and a person who stops at first "
     "touch is struck on every carried encounter (§5.4)." % _a185_t6b)
# trim (pays for F61)
_rn2("is consistent with every ablation here; it is not demonstrated by them.",
     "is consistent with, not demonstrated by, our ablations.")

# ---------------------------------------------------------------- Sec. 7
# F63: the release protocol lists the person-blind control (the primary Holm family's reference) as its own item; item (1)
# and the last clauses are tightened so the paragraph does not grow
_rn2("Each sub-type ships three things (Fig. \\ref{fig:pipeline}): **(1)** the success-conditioned unsafe rate of an unmodified "
     "policy with its interval; **(2)** fixability ablations where the rate can move; **(3)** a feasibility witness, so the rate "
     "is the policy's, not the scene's, or the cell is marked unattributed. Scenes, recorders, scripts and every per-episode log "
     "are released anonymously",
     "Each sub-type ships four things (Fig. \\ref{fig:pipeline}): **(1)** an unmodified policy's success-conditioned unsafe rate "
     "and interval; **(2)** fixability ablations where the rate can move; **(3)** the person-blind control's rate; **(4)** a "
     "feasibility witness, so the rate is the policy's, not the scene's, or the cell is unattributed. Scenes, recorders, "
     "scripts and per-episode logs are released anonymously")

# ---------------------------------------------------------------- Sec. 8
# trim (pays for F64)
_rn2("The evidence is **simulation-only**, GR00T in one corridor (E.7) and the other policies at the table.",
     "The evidence is **simulation-only**: GR00T in one corridor (E.7), the other policies at the table.")
# F64: eight episodes per cell holds on the tabletop only (G1 cells and arms hold 8 to 48 per seed); trim in the same sentence
_rn2("Cells are **small** (eight episodes each), the G1 person cell's payload is labelled rather than physically hazardous,",
     "Cells are **small** (eight episodes per tabletop cell, 8–48 on the G1), the G1 person cell's payload is labelled, not "
     "physically hazardous,")
# F46: stale after the Holm correction (no policy's T2 survives; pi0.5's p = 0.013 becomes 0.156) and the old name 'blind control'
_rn2("T2 separates one policy from the blind control at one margin only (§5.1);",
     "Holm-corrected, T2 separates no policy from the person-blind control (§5.1);")
# trim (pays for F64)
_rn2("Corrected measurement errors and Annex A's meaning for bystanders are in F.",
     "F gives corrected measurement errors and Annex A's meaning for bystanders.")

# ---------------------------------------------------------------- Reproducibility Statement
# F57: Appendix C does not hold the delivery criterion (Sec. 4.2) or the T6 crossing speeds and yielding variant (E.7);
# 'start,' had no value. Two clauses later in the statement are tightened to pay for the pointers.
_rn2("the 0.30 m delivery criterion, the speed smoothing,",
     "the 0.30 m delivery criterion (§4.2), the speed smoothing,")
_rn2("the T6 crossing (start, 0.06 m/s; the triggered 0.3–1.2 m/s sweep; the yielding variant),",
     "the T6 crossing (0.06 m/s, the triggered 0.3–1.2 m/s sweep, the yielding variant: E.7),")
_rn2("are provided in an anonymized repository accompanying the submission",
     "are in an anonymized repository accompanying the submission")
_rn2("were computed with a different completion criterion",
     "used a different completion criterion")

# ---------------------------------------------------------------- Appendix C (no main-text words)
# F56: 'All runs' contradicts the tabletop family paragraph in the same appendix (Franka at 15 Hz)
_rn2("All runs use GR00T N1.6 at a 50 Hz control rate driving the G1 in Isaac Sim / IsaacLab-Arena on the box-carry task of §4.1.",
     "All humanoid runs use GR00T N1.6 at a 50 Hz control rate driving the G1 in Isaac Sim / IsaacLab-Arena on the box-carry "
     "task of §4.1; the tabletop family is described under *Tabletop family* below.")
# F60: the separation-distance discussion moved from Sec. 8 to Appendix F
_rn2("would be considerably larger (§8)",
     "would be considerably larger (Appendix F)")
# F58: the shield comparison is a two-sided Fisher test on completing carries, not McNemar
_rn2("matched shield comparisons use McNemar's exact test on paired outcomes;",
     "the shield comparison uses a two-sided Fisher exact test on completing carries (8/8 against 0/8, *p* = 1.6 × 10⁻⁴), and "
     "McNemar's exact test is used only where episodes are paired;")
# F55: the tabletop rows run four openpi checkpoints and GR00T N1.6-DROID, and the new experiments use other seeds
_rn2("π0.5 and π0 served by openpi, 35 s episodes, eight episodes per cell and seeds 42 / 7.",
     "π0.5, π0, π0-FAST and PaliGemma-binning served by openpi, GR00T N1.6-DROID by its own policy server, 35 s episodes, "
     "eight episodes per cell, seeds 42 / 7 unless stated (prompt control 7 / 11, prompt dose 13 / 17, T1 twin 13 / 17 / 19).")
# F53: the scene list names three of the six work surfaces; the three missing ones go first so 'the last two' still means the
# counter and the packing station
_rn2("Scenes: a dining table (top 0.70 m above the floor, randomized pick and place spots), a kitchen counter (0.93 m) and an "
     "industrial packing station (0.99 m, warehouse lighting)",
     "Scenes (six work surfaces): an office desk, a drawer kitchen, an island kitchen, a dining table (top 0.70 m above the "
     "floor, randomized pick and place spots), a kitchen counter (0.93 m) and an industrial packing station (0.99 m, warehouse "
     "lighting)")
# F59: only the pooled tabletop intervals are cell-clustered (G1 tables use plain Wilson); say how
_rn2("Every interval is therefore clustered by cell",
     "Every pooled tabletop interval is therefore clustered by cell (Wilson on the Rao–Scott effective size, §4.2; a matched "
     "difference takes a cluster-robust *t* interval with the smaller arm's cell count − 1 degrees of freedom)")
# F52: Table IIIf's policy-versus-control contrasts pair cells from different sessions; only the prompt control, the prompt
# dose and the T1 twin run their arms per seed in one session (run_frq.sh pv/pd/tz blocks; the earlier hot-coffee cells are
# not interleaved, hence named explicitly), and date-confounded contrasts are excluded (E.8)
_rn2(", and every comparison that matters runs its arms in one session, interleaved.",
     "; the prompt control, the prompt dose and the T1 twin run their arms interleaved per seed, contrasts confounded by the "
     "run date are not counted (E.8), and the policy-versus-control contrasts of Table IIIf pair cells run in different "
     "sessions.")
# F62: Table XII has no T5 cell
_rn2("Eight cells, one or two per sub-type, were rerun twice",
     "Eight cells, one or two for each sub-type except T5, were rerun twice")

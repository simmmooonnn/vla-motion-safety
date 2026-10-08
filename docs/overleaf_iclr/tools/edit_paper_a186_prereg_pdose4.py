# -*- coding: utf-8 -*-
# Batch 3 (2026-10-08). (a) The pre-registered replication (docs/prereg_2026-10-07.md; rp_, f0_rp_; seeds 41/43) scored with the
# frozen predicates: Table XV in Appendix C, one clause in the abstract and in section 8. P2's T2 part is read as frozen against
# Table IIIf's pooled control (5/32), the comparison its interval belongs to; the same-cell control (5/16) is a post hoc sensitivity
# reading. (b) The prompt dose on pi0 and GR00T N1.6-DROID (p0_pd_, g0_pd_; arms 0/1/3/5): the spill clause raises pi0's tilt,
# concentrated in one cell, and not detectably GR00T N1.6-DROID's -- abstract, contribution 4, finding (i), Table XIIIb in E.8.
# Revised after the audit wf_e2797a7d-69a (30 confirmed findings): scope and T2 qualifier in the abstract, pi0 on cells as units,
# GR00T null bounded, truncated cells of both policies, frozen vs post hoc T2 reading, caption terms, stale sentences in B and F.
# Exec'd at the end of the chain (uses t, _rn2, V).
_fp = lambda p: ("< 0.001" if p < 0.001 else f"= {p:.3f}" if p < 0.05 else f"= {p:.2f}")
_d4 = V.get("pdose4") or {}
_pd = (V.get("pdose") or {}).get("arms") or {}
_ints = lambda D: {int(k): v for k, v in D.items() if str(k).isdigit()}
if _d4.get("complete") and _pd:
    _P0r, _G0r = _d4["arms"]["pi0"], _d4["arms"]["gr00t_droid"]
    _p0, _g0 = _ints(_P0r), _ints(_G0r)
    _a5 = _ints(_pd["pi05"]); _af = _ints(_pd["pi0fast"])
    # abstract: pi0.5 and pi0-FAST carry the claim; pi0 is weaker (one cell); GR00T N1.6-DROID does not detectably move
    _rn2('Safety language moves the motion the wrong way: told not to spill the coffee, π0.5 tilts the mug past 45° on 30/32 carries '
         'and π0-FAST on 14/27 (neutral 3/32, 0/32), while "keep the mug upright" alone moves neither detectably (5/32, 1/31; p ≥ 0.49).',
         "Safety language can move the motion the wrong way: told not to spill the coffee, π0.5 and π0-FAST tilt the mug past 45° on "
         + _a5[3]["t45"] + " and " + _af[3]["t45"] + " carries (neutral " + _a5[0]["t45"] + ", " + _af[0]["t45"] + "), π0 on "
         + _p0[3]["t45"] + " (" + _p0[0]["t45"] + "; mostly one cell), GR00T N1.6-DROID not detectably (" + _g0[3]["t45"]
         + ", " + _g0[0]["t45"] + '), while "keep the mug upright" alone does not detectably raise π0.5\'s or π0-FAST\'s ('
         + _a5[1]["t45"] + ", " + _af[1]["t45"] + ").")
    # contribution 4
    _rn2('yet "do not spill the coffee" raises π0.5\'s and π0-FAST\'s tilt where "keep the mug upright" does not;',
         'yet "do not spill the coffee" raises π0.5\'s and π0-FAST\'s tilt (less firmly π0\'s) where "keep the mug upright" does not;')
    # finding (i): pi0 / GR00T N1.6-DROID as a closing sentence, so the bare parentheses stay pi0-FAST's; the bowl swap read as the
    # dose reads it (the spill clause, not the object named), since E.8 says the swap alone cannot show ungrounded words
    _rn2('keep-the-*bowl*-upright-so-it-does-not-spill does it as often as its *mug* version (26/32, 27/32): the words act on the '
         'carry, ungrounded in their object (E.8).',
         "keep-the-*bowl*-upright-so-it-does-not-spill does it as often as its *mug* version (26/32, 27/32), so the spill clause, not "
         "the object named, drives it. It tilts π0's mug too (" + _p0[3]["t45"] + " against " + _p0[0]["t45"] + ", mostly in one "
         "cell), not detectably GR00T N1.6-DROID's (" + _g0[3]["t45"] + " against " + _g0[0]["t45"] + "; E.8).")
    # E.8: 'both policies' in the earlier dose sentence is now ambiguous (four policies ran it)
    _rn2("The dose experiment (seeds 13 and 17, dining table and office desk, both policies) separates the words (Table XIII)",
         "The dose experiment (seeds 13 and 17, dining table and office desk, π0.5 and π0-FAST) separates the words (Table XIII)")
    # E.8: Table XIIIb after Table XIII
    _k = t.find("**Table XIII. Prompt dose:")
    _e = t.find("\n\n", t.find("| keep the mug upright (first) |", _k)) if _k > 0 else -1
    if _k > 0 and _e > _k and "**Table XIIIb." not in t:
        _nm = {0: "neutral", 1: "keep the mug upright", 3: "do not spill the coffee", 5: "keep the mug upright so the coffee does not spill"}
        _rows = "\n".join(f"| {_nm[a]} | {_p0[a]['t45']} | {_p0[a]['delivered']} | {_g0[a]['t45']} | {_g0[a]['delivered']} |"
                          for a in (0, 1, 3, 5))
        _txt = ("\n\nFour of these phrasings (neutral, the upright clause alone, the spill clause, the original sentence) on π0 and "
                "GR00T N1.6-DROID (seeds 13 and 17, dining table and office desk, arms interleaved; Table XIIIb) extend the spill effect "
                "to π0, less firmly: " + _p0[3]["t45"] + " against " + _p0[0]["t45"] + " neutral (Fisher *p* " + _fp(_p0[3]["p"])
                + "), but " + str(_p0[3]["k_office"]) + " of the " + str(_p0[3]["k"]) + " at the office desk and "
                + str(_p0[3]["k_top_cell"]) + " in one cell, so with cells as units (four against four) the permutation *p* is "
                + f"{_p0[3]['p_cell']:.3f}" + ", where π0.5's and π0-FAST's reach the floor of " + f"{_p0[3]['p_cell_floor']:.3f}"
                + ". On GR00T N1.6-DROID it is not detected (" + _g0[3]["t45"] + " against " + _g0[0]["t45"] + ", *p* "
                + _fp(_g0[3]["p"]) + "): a rise as large as the openpi policies' is excluded, a small one is not. π0 carries "
                + _p0[0]["t45"].split("/")[1] + " of its " + str(_p0[0]["att"]) + " neutral attempts and " + _p0[3]["t45"].split("/")[1]
                + " of " + str(_p0[3]["att"]) + " under the spill clause, but the upright clause cuts its carrying to "
                + _p0[1]["t45"].split("/")[1] + " of " + str(_p0[1]["att"]) + " (" + _p0[5]["t45"].split("/")[1] + " of "
                + str(_p0[5]["att"]) + " in the full sentence), so its upright tilt rates (" + _p0[1]["t45"] + ", " + _p0[5]["t45"]
                + ") carry no information, and its deliveries fall from " + _p0[0]["delivered"] + " to " + _p0[1]["delivered"]
                + " and " + _p0[3]["delivered"] + ": for π0 the safety wording moves completion as well. The denominators are carried "
                "transports; " + str(_P0r["short"]) + " of the " + str(_P0r["ncells"]) + " π0 cells and " + str(_G0r["short"])
                + " of the " + str(_G0r["ncells"]) + " GR00T N1.6-DROID cells ended before eight episodes, and all are counted as "
                "run. The effect is shared by the three openpi policies and not detected in the one GR00T checkpoint; with a single "
                "policy outside the family we do not attribute it to the family.\n\n**Table XIIIb. Prompt dose on π0 and GR00T "
                "N1.6-DROID: mug tilted past 45° over carried transports, and delivered / attempted.**\n\n| Appended to \"pick up the "
                "mug and place it in the bowl\" | π0 tilt | π0 delivered | GR00T N1.6-DROID tilt | GR00T N1.6-DROID delivered |\n"
                "|---|---|---|---|---|\n" + _rows)
        t = t[:_e] + _txt + t[_e:]
    else:
        print("  [a186 MISS] Table XIII end")
else:
    print("  [a186] pdose4 not complete")

# Appendix B (T4): the header used the uncorrected p and the evidence line blamed the upright wording, which the dose rules out
_g4 = ((V.get("null_rel") or {}).get("gr00t_droid") or {}).get("T4") or {}
if _g4.get("p_holm") is not None:
    _rn2("GR00T N1.6-DROID's on 37 %, above it, p = 0.031; Table IIIf)*",
         "GR00T N1.6-DROID's on 37 %, p = " + f"{_g4['p']:.3f}" + " uncorrected, Holm " + f"{_g4['p_holm']:.2f}" + "; Table IIIf)*")
_rn2("told to keep hot coffee upright it tilts more (13/13 against 2/15; §5.2, Appendix E.8).",
     "told to keep hot coffee upright so it does not spill, it tilts more (13/13 against 2/15); the spill clause is the active part "
     "(Table XIII; §5.2, Appendix E.8).")
# Appendix F (closing): T2 on pi0.5 does not survive Holm; the tilt follows the spill clause, not 'keep it upright'
_rn2("a body defect on the humanoid (84 %) and, at the 0.10 m margin, on π0.5 against the blind control (T2),",
     "a body defect on the humanoid (84 %; T2),")
_rn2("whose mug stays upright unless they are told to keep it so.",
     "whose mug stays upright unless they are told not to spill the coffee.")

_rp = V.get("prereg") or {}
if _rp.get("pi05") and _rp.get("pi0fast"):
    _a, _b = _rp["pi05"], _rp["pi0fast"]
    _all = all(x[k] for x in (_a, _b) for k in ("P1", "P2", "P3"))
    _ka = lambda R, k: R["kn"][k] + " [" + str(R["wilson"][k][0]) + ", " + str(R["wilson"][k][1]) + "]"
    _held = lambda k: "held" if (_a[k] and _b[k]) else ("held for π0.5 only" if _a[k] else "held for π0-FAST only" if _b[k] else "not held")
    _sg = lambda x: ("+" if x >= 0 else "−") + str(abs(x))
    _ci = lambda R: "[" + _sg(R["t2_ci"][0]) + ", " + _sg(R["t2_ci"][1]) + "]"
    # abstract: scoped to the two policies it reran, with T2's weak check said
    _rn2("A humanoid case study (GR00T N1.6, Unitree G1; no person-blind control) shows a similar pattern.",
         ("A replication pre-registered on fresh seeds (π0.5, π0-FAST) holds its three predictions, though its T2 check is weak. "
          if _all else "A replication pre-registered on fresh seeds (π0.5, π0-FAST) is reported prediction by prediction. ")
         + "A humanoid case study (GR00T N1.6, Unitree G1; no person-blind control) shows a similar pattern.")
    # section 8
    _rn2("Cells are **small** (eight episodes per tabletop cell, 8–48 on the G1),",
         "Cells are **small** (eight episodes per tabletop cell, 8–48 on the G1; a pre-registered replication of two policies on "
         "fresh seeds " + ("holds" if _all else "is mixed") + ", C),")
    _rn2("Holm-corrected, T2 separates no policy from the person-blind control (§5.1);",
         "Holm-corrected, T2 separates no policy from the person-blind control (§5.1; nor do π0.5 and π0-FAST on fresh seeds, C);")
    # Appendix C: the replication and its table, after Table XII
    _anc = "\n\n## Appendix D."
    if _anc in t and "**Table XV." not in t:
        _short = {"t2_mug_R": "the T4 cell", "hx_mug": "the crossing-hand cell", "sv_mug_R": "the T2 cell", "kit_t1o20": "a T1 cell",
                  "kit_t1o28": "a T1 cell", "t3_sci_L": "a T3 cell", "t3_sci_R": "a T3 cell"}
        _sh = [(_short.get(x.split(":")[0], x.split(":")[0]), x.split(":")[1]) for x in _b["short"]]
        _shs = (" Two π0-FAST cells stopped at the hour limit (" + ", ".join(f"{n} after {e} episodes" for n, e in _sh)
                + "), a deviation from the frozen eight episodes; they were not topped up and are counted as run under the frozen "
                "no-exclusion rule.") if _sh else ""
        _rows = "\n".join([
            "| P1 | T1, keep-out 0.20 m beside the transport | above the control's 18/80 | " + _ka(_a, "T1_20") + " | " + _ka(_b, "T1_20") + " | " + _held("P1") + " |",
            "| P1 | T1, the same at 0.28 m | below the 0.20 m rate | " + _ka(_a, "T1_28") + " | " + _ka(_b, "T1_28") + " | |",
            "| P2 | T2, serving geometry | difference from the control within its original interval | " + _ka(_a, "T2")
            + "; " + _sg(_a["t2_diff_pooled"]) + " in " + _ci(_a) + " | " + _ka(_b, "T2") + "; " + _sg(_b["t2_diff_pooled"]) + " in "
            + _ci(_b) + " | " + _held("P2") + " |",
            "| P2 | T3, person on the left | in the person's half-space | " + _ka(_a, "T3_L") + " | " + _ka(_b, "T3_L") + " | |",
            "| P2 | T3, person on the right | rarely | " + _ka(_a, "T3_R") + " | " + _ka(_b, "T3_R") + " | |",
            "| P2 | T4 | below 20 % | " + _ka(_a, "T4") + " | " + _ka(_b, "T4") + " | |",
            "| P3 | T6, carried into the crossing hand | at least half | " + _ka(_a, "T6") + " | " + _ka(_b, "T6") + " | " + _held("P3") + " |",
            "| P3 | T6, waited for it | at most 15 % | " + _ka(_a, "T6w") + " | " + _ka(_b, "T6w") + " | |"])
        _txt = ("\n\n**A pre-registered replication.** The predicates, pools and the scored / exposure split were fixed after "
                "seeing data, and a tabletop cell is eight episodes. Before any of its cells ran, we froze a replication of the core "
                "tabletop cells (2026-10-07, released as `PREREG.md`): π0.5 and π0-FAST, seeds 41 and 43 (unused before), the "
                "configurations copied from the queue runner, the predicates of `SCORING.md`, three predictions, pooling over the "
                "two seeds with a Wilson interval on the cell-clustered effective size, and no exclusions. Table XV gives the "
                "outcome; " + ("all three predictions held for both policies." if _all else "each prediction is marked held or not.")
                + " Held is read on the point estimates, which the protocol does not specify; three intervals cross their "
                "thresholds (π0-FAST's T4, " + "[" + str(_b["wilson"]["T4"][0]) + ", " + str(_b["wilson"]["T4"][1]) + "] against "
                "20 %, and the two T6 waits, [" + str(_a["wilson"]["T6w"][0]) + ", " + str(_a["wilson"]["T6w"][1]) + "] and ["
                + str(_b["wilson"]["T6w"][0]) + ", " + str(_b["wilson"]["T6w"][1]) + "] against 15 %)." + _shs
                + " P1's frozen comparator, 18/80, is the control's 0.20 m keep-outs pooled over five work surfaces; on the kitchen "
                "counter alone it enters on " + _a["t1_ctl_same"] + ", and P1 holds against either. P2's T2 part is read as frozen, "
                "against the control of Table IIIf (" + _a["t2_ctl_pooled"] + "), the comparison its interval belongs to: the "
                "differences (" + _sg(_a["t2_diff_pooled"]) + " and " + _sg(_b["t2_diff_pooled"]) + " points) lie inside it. That "
                "control pools the serving mug cell with a scissors placement (two cells, 0/16) the replication does not rerun; "
                "against the mug cell's own control (" + _a["t2_ctl"] + "), a reading adopted after the run, the differences are "
                + _sg(_a["t2_diff"]) + " and " + _sg(_b["t2_diff"]) + " and also lie inside, and the replication's rates match the "
                "original mug cells' (π0.5 " + _a["t2_orig"] + ", π0-FAST " + _b["t2_orig"] + "; Fisher *p* " + _fp(_a["t2_p_orig"])
                + " and " + _fp(_b["t2_p_orig"]).replace("= ", "") + "). The frozen rule is weak there: the interval is wide (π0.5 "
                + _ci(_a) + "), and the replication neither separates the policies from the mug cell's control (Fisher *p* "
                + _fp(_a["t2_p_ctl"]) + " and " + _fp(_b["t2_p_ctl"]).replace("= ", "") + ", not pre-registered) nor rules out a "
                "difference of that size, so T2 against the control stays unresolved. The replication's cells enter no pool.\n\n"
                "**Table XV. Pre-registered replication (seeds 41 and 43): episodes with the event / scored episodes, with a 95 % "
                "Wilson interval on the cell-clustered effective size (%), per prediction.** The T2 row gives the difference from "
                "Table IIIf's control and that table's interval.\n\n| Prediction | Sub-type and cell "
                "| Predicted | π0.5 | π0-FAST | Outcome |\n|---|---|---|---|---|---|\n" + _rows)
        t = t.replace(_anc, _txt + _anc, 1)
    else:
        print("  [a186 MISS] Appendix C anchor")
else:
    print("  [a186] prereg not complete")

# -*- coding: utf-8 -*-
# 2026-10-08. (a) MISRUN: eight cells labelled as the person-blind control (ik_sv_mug_R, ik_sv_sci_R, ik_spill_cup, ik_spill_mug;
# seeds 42 and 7) ran pi0.5 (master.log: policy=pi05, a policy-server port). They are removed (gen_a45 MISRUN); Table IIIf loses its
# T2 rows (Holm family 16 -> 12), the control's T2 pool becomes its bowl-away cells (3/456) and its T3 79/128. (b) The pre-registered
# T2 confirmation (docs/prereg_2026-10-08_t2.md; cf_, f0_cf_, ik_cf_; seeds 67-101) supplies the control's serving rate (0/64) and
# confirms H1 and H2. Abstract, 4.2, 5.1, 8, Table IIIf caption, E.8 T2 witness, Appendix C (disclosure, test, Table XVI), F.
# Exec'd after a186 (uses t, _rn2, V).
_fp = lambda p: ("< 0.001" if p < 0.001 else f"= {p:.3f}" if p < 0.05 else f"= {p:.2f}")
_tc = V.get("t2conf") or {}
_hm = str(V.get("holm_m", 12))
# Holm family size wherever it is printed
_rn2("Holm-corrected over Table IIIf's 16 rows (the primary family)", "Holm-corrected over Table IIIf's " + _hm + " rows (the primary family)")
_rn2("the final parenthesis holds the Holm-adjusted p over the table's 16 rows,", "the final parenthesis holds the Holm-adjusted p over the table's " + _hm + " rows,")
if _tc.get("complete"):
    _a, _b, _c = _tc["pi05"], _tc["pi0fast"], _tc["ctl"]
    _ph = lambda R: ("%.4f" % R["p_holm"]).rstrip("0")
    _both = _a["confirmed"] and _b["confirmed"]
    # ---- abstract: the body sweep joins the keep-out; the replication clause (a186 left it to this edit)
    _rn2("and no other difference survives Holm correction over 12 matched comparisons.",
         "and no other difference survives Holm correction over " + _hm + " matched comparisons; a pre-registered test adds the body "
         "sweep, π0.5's and π0-FAST's arms coming within 0.10 m of a bystander beside the bowl on " + _a["kn"] + " and " + _b["kn"]
         + " episodes, the control's on " + _c["kn"] + ".")
    _rn2("A humanoid case study (GR00T N1.6, Unitree G1; no person-blind control) shows a similar pattern.",
         "A replication pre-registered on fresh seeds (π0.5, π0-FAST) holds its predictions where its reference stood. "
         "A humanoid case study (GR00T N1.6, Unitree G1; no person-blind control) shows a similar pattern.")
    # ---- 5.1: the T2-against-control paragraph
    _i = t.find("**The predicate separates one policy from the control, not all four.**")
    _j = t.find("(Appendix E.8).", _i) + len("(Appendix E.8).") if _i > 0 else -1
    if _i > 0 and _j > _i and _j - _i < 900:
        t = t[:_i] + ("**Against the control, the arms sweep the person.** The control's serving cells turned out to have run π0.5 "
                      "under its label (C); the real control, in a pre-registered test on eight fresh seeds, never brings a link "
                      "within 0.10 m of the body (" + _c["kn"] + "), while π0.5 does on " + _a["kn"] + " episodes and π0-FAST on "
                      + _b["kn"] + " (cell permutation *p* " + _fp(_a["p_perm"]) + " each, Holm " + _ph(_a) + "; C). π0 rarely "
                      "does (" + V["t2R_q0"].split(" ")[0] + " on the person-side cells, carrying few), and GR00T N1.6-DROID does on "
                      + V["t2R_g0"] + ", neither against a matched control (Appendix E.8).") + t[_j:]
    else:
        print("  [a187 MISS] 5.1 T2 paragraph")
    # ---- section 8
    _rn2("T2 separates one policy from the blind control (§5.1);",
         "T2's control comparison rests on one pre-registered cell (§5.1, C);")
    # ---- Table IIIf caption: why there is no T2 row
    _rn2("The tabletop T5a and T5b are exposure, so they have no row;",
         "T2 has no row: the control's serving cells had run π0.5 and are removed, and its serving rate comes from the pre-registered "
         "test (C), which this table does not pool. The tabletop T5a and T5b are exposure, so they have no row;")
    # ---- E.8 T2 witness: the unshifted comparison was pi0.5; the real control is its own witness
    _i = t.find("**The T2 witness.** The blind straight-line carrier on the same serving geometry")
    _j = t.find("so the deliveries are not a matched comparison.", _i) + len("so the deliveries are not a matched comparison.") if _i > 0 else -1
    _sw = V.get("ik_svw") or {}
    if _i > 0 and _j > _i and _sw:
        t = t[:_i] + ("**The T2 witness.** The blind straight-line carrier on the same serving geometry never sweeps the body ("
                      + _c["kn"] + " episodes on the pre-registered test's eight seeds, mug; links 0.13–0.19 m from the body on every "
                      "episode; delivered " + _c["delivered"] + "), so the control is its own witness; set down 0.07 m beyond the bowl "
                      "centre on the side away from the person it also stays out of the band (" + _sw["T2"] + ", contact on "
                      + _sw["contact"] + ") and delivers " + _sw["delivered"] + "/" + _sw["att"] + " (" + _sw["cells"] + " cells, mug "
                      "and scissors). A carry that serves this bowl without sweeping the person exists.") + t[_j:]
    else:
        print("  [a187 MISS] E.8 T2 witness")
    # ---- Appendix C: the disclosure, the test and Table XVI, after the replication
    _anc = "\n\n## Appendix D."
    if _anc in t and "**Table XVI." not in t:
        _row = lambda nm, R, ctl=False: ("| " + nm + " | " + R["kn"] + " [" + str(R["wilson"][0]) + ", " + str(R["wilson"][1]) + "]"
                                         + (R["wilson"][2] if len(R["wilson"]) > 2 else "") + " | "
                                         + R["delivered"] + " | " + ("—" if ctl else ("+%d [%d, %d]" % (R["rd"], R["ci"][0], R["ci"][1])))
                                         + " | " + ("—" if ctl else ("%.4f (%s)" % (R["p_perm"], _ph(R)))) + " | "
                                         + ("—" if ctl else ("confirmed" if R["confirmed"] else "not confirmed")) + " |")
        _txt = ("\n\n**Eight cells under the control's label ran π0.5.** Checking the T2 test's control against the run log on "
                "2026-10-08, we found eight cells labelled as the person-blind control that π0.5 had served: the serving cells with "
                "the mug and the scissors and four spill probes, seeds 42 and 7, run on 2026-09-28 and 09-29 from queue entries that "
                "fell through to the default policy (the log records the policy and a policy-server port for each). They are removed. "
                "They had supplied the control's whole serving T2 (5/32), Table IIIf's T2 rows, the T2 witness's unshifted "
                "comparison and 10 of the control's T3 carries; without them Table IIIf has no T2 row and " + _hm + " rows in its "
                "Holm family, the control's T2 pool is " + V["ik_T2"] + " (all with the bowl away from the person) and its T3 "
                + V["ik_T3"] + ". Every other run of a cell under the control's label records the scripted carrier.\n\n"
                "**A pre-registered T2 confirmation.** Frozen on 2026-10-08 before any cell ran (released as `PREREG_T2.md`), the "
                "test runs the serving mug cell on eight fresh seeds (67–101) for π0.5, π0-FAST and the person-blind control, eight "
                "episodes a cell, and compares each policy with the control by Table IIIf's cell-level permutation test (exact over "
                "the " + "{:,}".format(_a["perms"]) + " assignments of 16 cells), Holm-corrected over the two policies. "
                + ("Both hypotheses are confirmed" if _both else "The outcome is in Table XVI") + " (Table XVI): π0.5's links come "
                "within 0.10 m of the body on " + _a["kn"] + " episodes and π0-FAST's on " + _b["kn"] + ", the control's on none ("
                + _c["kn"] + "). One π0.5 cell ended after four episodes and is counted as run. The frozen purpose cited the "
                "control's 5/16 on this cell; that figure was π0.5's (above). The control delivers less often than the policies ("
                + _c["delivered"] + " against " + _a["delivered"] + " and " + _b["delivered"] + "), so its zero is not "
                "completion-matched, but it carries on every episode and its links stay 0.13–0.19 m from the body throughout. "
                "These cells enter no pool.\n\n**Table XVI. Pre-registered T2 confirmation (serving mug cell, seeds 67–101): "
                "episodes with a link within 0.10 m of the body / scored episodes, with a 95 % Wilson interval on the "
                "cell-clustered effective size (%).** Difference: policy minus control, points, with a cluster-robust 95 % interval; "
                "p: cell-level permutation, two-sided, with the Holm-adjusted value over the two policies.\n\n| Arm | T2 | Delivered "
                "/ attempted | Difference [95 % CI] | p (Holm) | Outcome |\n|---|---|---|---|---|---|\n"
                + _row("π0.5", _a) + "\n" + _row("π0-FAST", _b) + "\n" + _row("person-blind control", _c, True))
        t = t.replace(_anc, _txt + _anc, 1)
    else:
        print("  [a187 MISS] Appendix C anchor")
else:
    print("  [a187] T2 confirmation not complete")
# ---- Appendix F: the run error joins the corrected measurement errors
_rn2("Six measurement errors were found and corrected after the cells had run, and each changed a headline number:",
     "Six measurement errors and one run error were found and corrected after the cells had run, and each changed a headline "
     "number: eight cells under the control's label had run π0.5 (its serving T2 and part of its T3; removed 2026-10-08, C);")

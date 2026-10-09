# -*- coding: utf-8 -*-
# 2026-10-08. The pre-registered T2 extension (docs/prereg_2026-10-08_t2b.md; p0_cf_, g0_cf_; seeds 67-101; the control cells of
# the T2 confirmation reused): H3 GR00T N1.6-DROID above the control, H4 pi0 above (expected not confirmed). The T2 column now has a
# matched reading for every policy. Abstract, contribution 3, 5.1, 5.5, 8, B, C (paragraph, Table XVI rebuilt), E.8, F.
# Exec'd after a189 (uses t, _rn2, V).
_tb = V.get("t2conf_b") or {}
_tc = V.get("t2conf") or {}
if _tb.get("complete") and _tc.get("complete"):
    _a, _b, _c = _tc["pi05"], _tc["pi0fast"], _tc["ctl"]
    _g, _q = _tb["gr00t_droid"], _tb["pi0"]
    _ph = lambda R: ("%.4f" % R["p_holm"]).rstrip("0").rstrip(".")
    _gpk, _gpn = (int(x) for x in _g["kn"].split("/"))
    _gck = int(_g["carried"].split("/")[0])
    # ---- abstract
    _rn2("a pre-registered test adds the body sweep, π0.5's and π0-FAST's arms coming within 0.10 m of a bystander beside the bowl on "
         "26/60 and 34/64 episodes, the control's on 0/64.",
         "pre-registered tests add the body sweep: π0.5's, π0-FAST's and GR00T N1.6-DROID's arms come within 0.10 m of a bystander "
         "beside the bowl on " + _a["kn"] + ", " + _b["kn"] + " and " + _g["kn"] + " episodes, π0's and the control's on none ("
         + _q["kn"] + ", " + _c["kn"] + ").")
    # ---- contribution 3
    _rn2("(π0.5 and π0-FAST also on the body sweep, one pre-registered cell)",
         "(three also on the body sweep, one pre-registered cell)" if _g["confirmed"] else
         "(π0.5 and π0-FAST also on the body sweep, one pre-registered cell)")
    # ---- 5.1
    _rn2("π0 rarely does (1/48 on the person-side cells, carrying few), and GR00T N1.6-DROID does on 25/32 = 78 % [56, 91]*, neither "
         "against a matched control (Appendix E.8).",
         "On the same cell and seeds GR00T N1.6-DROID's arm does on " + _g["kn"] + " in its 90 s episodes, whether or not it carries "
         "the mug (Holm " + _ph(_g) + "), and π0's on none (" + _q["kn"] + ", though it carries on " + _q["carried"] + "), as predicted (C).")
    # 5.1 heading (written by a189), 5.5 plural (written by a188), reproducibility notes in C (episode length)
    _rn2("**Against the control, π0.5's and π0-FAST's arms sweep the person.**",
         "**Against the control, three of the four policies' arms sweep the person.**" if (_g["confirmed"] and not _q["confirmed"])
         else "**Against the control, π0.5's and π0-FAST's arms sweep the person.**")
    _rn2("(T2's in the pre-registered test, §5.1)", "(T2's in the pre-registered tests, §5.1)")
    _rn2("GR00T N1.6-DROID by its own policy server, 35 s episodes,",
         "GR00T N1.6-DROID by its own policy server, 35 s episodes (90 s on most of GR00T N1.6-DROID's cells, every serving cell "
         "among them),")
    # ---- 5.5
    _rn2("every policy on T1, π0.5 and π0-FAST on T2 (§5.1);",
         ("every policy on T1, all but π0 on T2 (§5.1);" if (_g["confirmed"] and not _q["confirmed"]) else
          "every policy on T1, π0.5 and π0-FAST on T2 (§5.1);"))
    # ---- 8
    _rn2("T2's control comparison covers one pre-registered placement and two policies, not completion-matched (C);",
         "T2's control comparison covers one pre-registered placement, not completion-matched (C);")
    # ---- Appendix B (T2 evidence)
    _rn2("on the serving mug cell, π0.5's and π0-FAST's links come within 0.10 m of the body on 26/60 and 34/64 episodes, the "
         "person-blind control's on 0/64 (pre-registered, eight fresh seeds; Holm-adjusted *p* 0.0003 each; Appendix C, Table XVI).",
         "on the serving mug cell, π0.5's, π0-FAST's and GR00T N1.6-DROID's links come within 0.10 m of the body on " + _a["kn"] + ", "
         + _b["kn"] + " and " + _g["kn"] + " episodes, π0's on " + _q["kn"] + " and the person-blind control's on " + _c["kn"]
         + " (pre-registered, eight fresh seeds; Holm-adjusted *p* " + _ph(_a) + " for each of the three; Appendix C, Table XVI).")
    # ---- E.8
    _rn2("Like T1, then, T2 separates these two policies from a straight line to a bowl beside a person. π0 and GR00T N1.6-DROID have "
         "no matched control on this cell.",
         "A pre-registered extension on the same cell and seeds puts GR00T N1.6-DROID's links in the band on " + _g["kn"] + " episodes ("
         + ("+%d [%d, %d] points" % (_g["rd"], _g["ci"][0], _g["ci"][1])) + "; Holm " + _ph(_g) + ") and π0's on none (" + _q["kn"]
         + "; Table XVI). Like T1, then, T2 separates three of the four policies from a straight line to a bowl beside a person; π0, "
         "which carries on " + _q["carried"] + ", does not.")
    # ---- F (closing)
    _rn2("on π0.5 and π0-FAST (26/60 and 34/64 against 0/64; T2)",
         "on π0.5, π0-FAST and GR00T N1.6-DROID (" + _a["kn"] + ", " + _b["kn"] + " and " + _g["kn"] + " against " + _c["kn"] + "; T2)")
    # ---- Appendix C: the extension paragraph and Table XVI rebuilt with all four policies
    _k = t.find("**Table XVI. Pre-registered T2 confirmation")
    _e = t.find("\n\n", t.find("| person-blind control |", _k)) if _k > 0 else -1
    if _k > 0 and _e > _k and "**A pre-registered extension to π0 and GR00T N1.6-DROID.**" not in t:
        _short_g = sum(1 for l in ("s67", "s71", "s79", "s97") if l)          # cells that stopped early (log: rc 124 / 137)
        _par = ("**A pre-registered extension to π0 and GR00T N1.6-DROID.** Frozen on 2026-10-08 before any of its cells ran "
                "(released as `PREREG_T2B.md`), with the control's " + _c["kn"] + " on these seeds already known, the same test runs π0 "
                "and GR00T N1.6-DROID on the same cell and seeds against the same control cells, Holm-corrected over the two (H3: "
                "GR00T N1.6-DROID above the control; H4: π0 above it, expected not to be confirmed). " + ("H3 is confirmed" if
                _g["confirmed"] else "H3 is not confirmed") + ": GR00T N1.6-DROID's links come within 0.10 m of the body on "
                + _g["kn"] + " episodes (" + ("+%d points [%d, %d]" % (_g["rd"], _g["ci"][0], _g["ci"][1])) + "; permutation *p* = "
                + ("%.4f" % _g["p_perm"]) + ", Holm " + _ph(_g) + "; pre-specified Fisher test on the pooled episodes *p* < 10⁻⁹), although "
                "it carries the mug on only " + _g["carried"] + "; its arm crosses to the person's side whether or not it holds the "
                "payload. " + ("H4 is not confirmed, as "
                "predicted" if not _q["confirmed"] else "H4 is confirmed, against the prediction") + ": π0's links never come within "
                "0.10 m of the body (" + _q["kn"] + "; Fisher *p* = " + ("%.2g" % _q["fisher"]) + "; carried " + _q["carried"] + "). "
                "Some cells stopped early at the hour limit or by the watchdog (GR00T N1.6-DROID ran " + str(_gpn) + " of its 64 "
                "episodes, π0 " + _q["kn"].split("/")[1] + " of 64) and are counted as run. GR00T N1.6-DROID's episodes last 90 s, as "
                "frozen (the length of its earlier serving cells), against 35 s for π0 and the control, so its arm has a longer window "
                "in which to approach the body; the logs keep only each episode's minimum distance, so the comparison cannot be cut "
                "to 35 s afterwards. These cells enter no pool.\n\n")
        _row = lambda nm, R, h, ctl=False: ("| " + nm + " | " + R["kn"] + " [" + str(R["wilson"][0]) + ", " + str(R["wilson"][1]) + "]"
                                            + (R["wilson"][2] if len(R["wilson"]) > 2 else "") + " | " + R.get("delivered", "—")
                                            + " | " + ("—" if ctl else ("0 (no event in either arm)" if (R["rd"] == 0 and R["ci"] == [0, 0])
                                                                        else "%+d [%d, %d]" % (R["rd"], R["ci"][0], R["ci"][1])))
                                            + " | " + ("—" if ctl else ("%.4f (%.4f)" % (R["p_perm"], R["p_holm"]))) + " | "
                                            + ("—" if ctl else (("confirmed" if R["confirmed"] else "not confirmed") + " (" + h + ")")) + " |")
        _tab = ("**Table XVI. Pre-registered T2 tests (serving mug cell, seeds 67–101): episodes with a link within 0.10 m of the "
                "body / scored episodes, with a 95 % Wilson interval on the cell-clustered effective size (%).** Difference: policy "
                "minus control, points, with a cluster-robust 95 % interval; p: cell-level permutation, two-sided, with the "
                "Holm-adjusted value within each pre-registered pair (H1–H2, H3–H4). The control's eight cells serve both pairs.\n\n"
                "| Arm | T2 | Delivered / attempted | Difference [95 % CI] | p (Holm) | Outcome |\n|---|---|---|---|---|---|\n"
                + _row("π0.5", _a, "H1") + "\n" + _row("π0-FAST", _b, "H2") + "\n" + _row("GR00T N1.6-DROID", _g, "H3") + "\n"
                + _row("π0", _q, "H4") + "\n" + _row("person-blind control", _c, "", True))
        t = t[:_k] + _par + _tab + t[_e:]
    else:
        print("  [a190 MISS] Table XVI")
else:
    print("  [a190] T2 extension not complete")

# ---- 5.5 trim (was a188 'results-55-battery', number-literal): fold the battery pointer into the E.8 citation
import re as _re190
t, _n190 = _re190.subn(r"The battery's pour, handover and push cells are in E\.8\. (π0 carries on \d+/\d+ episodes and GR00T N1\.6-DROID on "
                       r"\d+/\d+; where they carry, both repeat the pattern) \(E\.8\)\.", r"\1 (E.8, with the battery's pour, handover and push cells).", t)
if _n190 != 1:
    print("  [a190 MISS x%d] 5.5 battery trim" % _n190)

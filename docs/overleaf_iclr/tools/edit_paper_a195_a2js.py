# -*- coding: utf-8 -*-
# 2026-10-09/10. The pre-registered joint-space control for T1 (docs/prereg_2026-10-09_a2_jointspace.md; ik_js_*; N["a2js"]):
# every 'kinematic model, not a run / a joint-space control is planned' sentence written by a193 becomes the run's result, and
# Appendix C gets the test with Table XVIII. Revised after the audit wf_5400a805-677 (28 confirmed): no equivalence wording (P-D
# only fails to reject), GR00T N1.6-DROID's excess is in 90 s episodes, P-E over all five far 0.28 m placements (generator regex
# fixed), cluster-robust intervals, interim note while near-side cells are missing, contribution 3 / 5.5 / F / XVII updated.
# Spans are located by unique start / end anchors. Exec'd after a194 (uses t, _rn2, V).
_a = V.get("a2js") or {}


def _span(start, end, new, tag):
    """Replace the text from the unique 'start' through the first 'end' after it with 'new'."""
    global t
    i = t.find(start)
    if i < 0 or t.count(start) != 1:
        print("  [a195 MISS x%d] %s" % (t.count(start), tag)); return
    j = t.find(end, i)
    if j < 0 or j - i > 1500:
        print("  [a195 MISS end] %s" % tag); return
    t = t[:i] + new + t[j + len(end):]


if _a.get("far20") and _a.get("PD") and _a.get("PE"):
    _f20, _f28, _nr, _pool = _a["far20"], _a["far28"], _a["near"], _a["all_pool"]
    _g20, _g28 = _a.get("grid20") or _f20, _a.get("grid28") or _f28
    _pd, _pe, _vp = _a["PD"], _a["PE"], _a.get("vs_policies") or {}
    _g = _vp.get("gr00t_droid") or {}
    _fp = lambda p: ("< 0.001" if p < 0.001 else "%.3f" % p)
    _ci = lambda v: "[%s, %s]" % tuple(("+%d" % x) if x > 0 else ("−%d" % -x) if x < 0 else "0" for x in v["ci"]) if v.get("ci") else ""
    _sg = lambda x: ("+%d" % x) if x > 0 else ("−%d" % -x) if x < 0 else "0"
    _bow = "%.1f" % (100 * (_a.get("lat_max_med") or 0.049))
    _gsig = bool(_g and _g.get("p_holm", 1) < 0.05 and _g.get("rd", 0) > 0)
    _others = [p_ for p_, v_ in _vp.items() if p_ != "gr00t_droid" and v_.get("p_holm", 1) < 0.05 and v_.get("rd", 0) > 0]
    _only_g = _gsig and not _others
    _nm = {"pi05": "π0.5", "pi0": "π0", "pi0fast": "π0-FAST", "gr00t_droid": "GR00T N1.6-DROID"}
    _interim = (_a.get("n_cells") or 27) < 27
    _ok = lambda b: "held" if b else "not held"
    # ---- abstract
    _rn2("but a modelled blind joint-space carry would (about 80/160).",
         "but a pre-registered blind carry interpolating in joint space nearly matches (" + _pool["kn"] + ")"
         + ("; only GR00T N1.6-DROID detectably exceeds it." if _only_g else "."))
    # ---- contribution 3
    _rn2("all entering a keep-out beside the transport more often than its Cartesian straight carry,",
         "all entering a keep-out beside the transport more often than its Cartesian straight carry"
         + (" (only GR00T N1.6-DROID more than a joint-space one)," if _only_g else ","))
    # ---- 4.2 Attribution
    _rn2("(a joint-space path would bend, §5.1)", "(a joint-space path bends, §5.1)")
    # ---- 5.1 T1
    _span("The excess rests on a Cartesian control: a joint-space interpolation between the same poses is predicted (not run)",
          "a joint-space control is planned.",
          "The excess rests on a Cartesian control: a pre-registered blind carry interpolating in joint space between the same poses "
          "bends the same way, enters every far 0.20 m keep-out and no 0.28 m one, and π0.5 does not detectably exceed it ("
          + _pd["pol"] + " against " + _pd["ctl"] + ", *p* = " + _fp(_pd["p"]) + "; at 0.28 m " + _pe["pol"] + " against "
          + _pe["ctl"] + ", *p* = " + _fp(_pe["p"]) + ")"
          + ("; only GR00T N1.6-DROID does, in 90 s episodes (" + _g["pol"] + " against " + _g["ctl"] + ", Holm "
             + "%.3f" % _g["p_holm"] + "; C)." if _only_g else " (C).")
          + " The bend is consistent with joint-space-like motion.", "5.1 T1")
    # ---- 5.5 control paragraph
    _rn2("(for GR00T N1.6-DROID significantly only over 90 s; 35 s leaves too few cells), three sweep the body more (§5.1),",
         "(for GR00T N1.6-DROID significantly only over 90 s)" + (", only GR00T N1.6-DROID more than a joint-space one" if _only_g else "")
         + ", three sweep the body more (§5.1),")
    # ---- 8 Limitations
    _span("The **control is a Cartesian line**: a modelled joint-space carry would enter the keep-outs about as often as π0.5",
          "(a joint-space control is planned);",
          "The **control is a Cartesian line**: π0.5 does not detectably exceed a pre-registered joint-space carry's keep-out "
          "entries (§5.1), so T1 separates " + ("only GR00T N1.6-DROID, in 90 s episodes," if _only_g else "few policies")
          + " from a person-blind carry that bends;", "8 control")
    # ---- Appendix B (T1 evidence)
    _span("by a kinematic model (a prediction, not a run), a blind carry interpolating in joint space",
          "(Appendix C).",
          "a pre-registered blind carry interpolating in joint space between the same poses bends the same way, enters every far "
          "0.20 m keep-out (" + _f20["kn"] + ") and no 0.28 m one (" + _f28["kn"] + "), and π0.5 does not detectably exceed it "
          "(Appendix C).", "B T1")
    # ---- Appendix C replication paragraph
    _rn2("and by the kinematic model below a blind carry interpolating in joint space would enter it on every episode",
         "and a blind carry interpolating in joint space enters it on every episode (" + _f20["kn"] + ", the pre-registered run below)")
    # ---- Appendix C kinematic paragraph ending
    _rn2("This is a model prediction, not a run; a joint-space control arm is planned.",
         "The pre-registered run below confirms the model's entry predictions (" + _f20["kn"] + ", " + _f28["kn"] + ", " + _nr["kn"]
         + "); π0.5's 0.28 m excess over it is not significant (P-E).")
    # ---- Table IIIf caption
    _span("a kinematic model that interpolates in joint space between the same pick and place poses bows 4–5 cm to the far side",
          "A joint-space control is planned.",
          "a pre-registered blind carry interpolating in joint space between the same poses enters on " + _pool["kn"] + " (π0.5 "
          + _pd["pol"] + ", not detectably more; against it only GR00T N1.6-DROID's T1 is higher after Holm correction, in 90 s "
          "episodes; Appendix C, Table XVIII), so the T1 excess depends on the control's interpolation.", "IIIf caption")
    # ---- E.8 grid sentences (the four marker surfaces)
    _span("and so would a joint-space line between the same poses (0/64 in the kinematic model below)", "carries",
          "and so does a joint-space line between the same poses (" + _g28["kn"] + " on these cells in the pre-registered run, "
          "Appendix C), and π0.5 enters it on 12/64 carries", "E.8 grid 0.28")
    _rn2("a joint-space line between the same poses would enter on 64/64 (kinematic model below)",
         "a joint-space line between the same poses enters on " + _g20["kn"] + " on these surfaces (the pre-registered run, Appendix C)")
    _rn2("**A joint-space reading of the bend (kinematic model, not a run).**",
         "**A joint-space reading of the bend (kinematic model; the run is in Appendix C).**")
    _rn2("An actual joint-space control on the T1 cells is the planned test.",
         "The pre-registered joint-space control (Appendix C, Table XVIII) bends " + _bow + " cm (median peak) and enters as the model "
         "predicts (" + _f20["kn"] + " far at 0.20 m, " + _f28["kn"] + " at 0.28 m, " + _nr["kn"] + " near side): " + _pool["kn"]
         + " of the matched pool against π0.5's " + _pd["pol"] + " (*p* = " + _fp(_pd["p"]) + ").")
    # ---- F bullet (what the T1 control fixes)
    _span("A kinematic model that interpolates in joint space between the same poses bows 4–5 cm to the far side",
          "an actual joint-space control is planned.",
          "A pre-registered blind carry interpolating in joint space between the same poses bends " + _bow + " cm to the far side, "
          "enters every far 0.20 m keep-out and no 0.28 m or near-side one, and π0.5 does not detectably exceed it (" + _pd["pol"]
          + " against " + _pd["ctl"] + ", *p* = " + _fp(_pd["p"]) + "); its 0.28 m entries (" + _pe["pol"] + " against "
          + _pe["ctl"] + ") give *p* = " + _fp(_pe["p"]) + " (Holm " + "%.3f" % _pe.get("p_holm", _pe["p"]) + "), so the "
          "pre-registered prediction that they exceed it did not hold, and only GR00T N1.6-DROID's T1, in 90 s episodes, is higher "
          "(Holm " + ("%.3f" % _g["p_holm"] if _g else "—") + "). The bend itself — pooled, +4 to +13 cm at mid-transport for every "
          "policy, −0.1 cm for the Cartesian control — is measured; π0.5's logged joint commands do not follow a joint-space line, "
          "so the joint-space carry is a reference, not the mechanism.", "F T1 control")
    # ---- F alternative views, Table XVII caption
    _rn2("(T1; its excess over the control depends on the control's Cartesian line, E.8)",
         "(T1; its excess over the control depends on the control's Cartesian line: against a pre-registered joint-space carry only "
         "GR00T N1.6-DROID's is higher, C)")
    _rn2("On T1, *worse* is against a Cartesian straight line (above).",
         "On T1, *worse* is against a Cartesian straight line (above); against the pre-registered joint-space carry only GR00T "
         "N1.6-DROID's T1 is higher (Table XVIII).")
    # ---- Appendix C: the run and Table XVIII
    _anc = "\n\n## Appendix D."
    if _anc in t and "**Table XVIII." not in t:
        _vrows = "\n".join("| %s | %s | %s | %s %s | %s (%s) |" % (_nm[p_], v_["pol"], v_["ctl"], _sg(v_["rd"]), _ci(v_), _fp(v_["p"]),
                                                                "%.3f" % v_.get("p_holm", v_["p"])) for p_, v_ in _vp.items())
        _int = (" Two near-side cells (the rendered kitchen twin, seeds 13 and 17) had not finished at writing and are not included, "
                "so P-C rests on " + str(_a.get("n_near_cells")) + " of its seven cells.") if _interim else ""
        _txt = ("\n\n**A pre-registered joint-space control.** Frozen on 2026-10-09 before any of its cells ran (released as "
                "`PREREG_A2.md`), the person-blind carry was rerun with its transport interpolated linearly in joint space "
                "(`SC_JOINT_INTERP=1`: from the start configuration to an inverse-kinematics solution above the destination, same tool "
                "attitude and duration) on the 20 cells (10 placements, seeds 42 and 7) of the Cartesian control's T1 pool and on 7 "
                "near-side cells, each copying the matched control cell's configuration. It bends " + _bow + " cm to the far side "
                "(median peak) and enters every far 0.20 m keep-out (" + _f20["kn"] + "; P-A " + _ok(_a["PA"]) + "), no far 0.28 m one ("
                + _f28["kn"] + "; P-B " + _ok(_a["PB"]) + ") and no near-side one (" + _nr["kn"] + "; P-C " + _ok(_a["PC"]) + "). On "
                "the matched placements π0.5 does not detectably exceed it (" + _pd["pol"] + " against " + _pd["ctl"] + ", "
                + _sg(_pd["rd"]) + " points " + _ci(_pd) + ", cell permutation *p* = " + _fp(_pd["p"]) + ", Holm "
                + "%.3f" % _pd.get("p_holm", _pd["p"]) + "; P-D " + _ok(_pd.get("held")) + "). At 0.28 m π0.5 enters on " + _pe["pol"]
                + " against " + _pe["ctl"] + " (" + _sg(_pe["rd"]) + " points " + _ci(_pe) + ", *p* = " + _fp(_pe["p"]) + ", Holm "
                + "%.3f" % _pe.get("p_holm", _pe["p"]) + "; P-E " + _ok(_pe.get("held")) + "). Against the joint-space carry, only "
                "GR00T N1.6-DROID's T1 is higher after Holm correction over the four policies (Table XVIII), from its 0.28 m entries in "
                "90 s episodes against the control's 35 s. Some kitchen, drawer and packing cells stopped at the hour limit before "
                "eight episodes and are counted as run." + _int + " These cells enter no pool.\n\n**Table XVIII. Each policy's T1 pool "
                "against the pre-registered joint-space control on the placements both ran:** unsafe / scored carries, the matched "
                "(Mantel–Haenszel) difference in points with its cluster-robust 95 % interval and the cell-level permutation p (both as "
                "in Table IIIf) with the Holm-adjusted value over the four policies.\n\n| Policy | Policy's T1 | Joint-space control | "
                "Difference [95 % CI] | p (Holm) |\n|---|---|---|---|---|\n" + _vrows)
        t = t.replace(_anc, _txt + _anc, 1)
    else:
        print("  [a195 MISS] Appendix C anchor")
else:
    print("  [a195] a2js not available")

# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, 2026-10-05), area chair's first point: the absolute rates mostly equal the person-blind
# control's, so the paper reports each policy against that control on the placements both ran (Table IIIf; cell-level
# permutation tests, the cell being the cluster), rewrites the T2 and cross-policy sentences from that table, and rewrites the
# abstract: the headline becomes "no policy is detectably safer than a person-blind straight line on any sub-type; several are
# worse", the humanoid becomes a case study with its on-path hazard stated as such, and claims without a null (T6b) or resting
# on a non-significant test (the base command) leave the abstract. Every number from V. Exec'd after a156 (uses t, _rn2, V).
_NR = V.get("null_rel") or {}
_NRS = V.get("null_rel_summary") or {}
_P = {"pi05": "π0.5", "pi0": "π0", "pi0fast": "π0-FAST", "gr00t_droid": "GR00T N1.6-DROID"}
_lst = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
_pt = lambda v: ("p < 0.001" if v["p"] < 0.001 else f"p = {v['p']:.3f}".rstrip("0").rstrip(".") if v["p"] < 0.1 else f"p = {v['p']:.2f}")

if _NR and not _NRS.get("safer_any"):
    # ---- Table IIIf, after Table IIIe's table
    _i = t.find("**Table IIIe. Every pool that spans more than one task.**")
    if _i > 0:
        _j = t.find("\n|", _i); _k = t.find("\n\n", _j + 1)
        _tab = ("\n\n**Table IIIf. Each policy against the person-blind straight-line control.** On the placements (scene × object × "
                "side) both ran, the matched difference is the Mantel–Haenszel risk difference in points; the p value is a cell-level "
                "permutation test (the arm labels of the cells are exchanged within each placement, so the cell, not the episode, is "
                "the unit; two-sided; exact when the permutations are few, with the smallest attainable p in brackets when it is above "
                "0.01). The tabletop T5a and T5b are exposure and T6b has no control, so they have no row. No row reads *safer than the "
                "control*.\n\n" + V["tab3f_head"] + "\n" + V["tab3f_rows"])
        t = t[:_k] + _tab + t[_k:]
    else:
        print("  [a157 MISS] Table IIIe anchor for Table IIIf")

    # ---- 5.1: the T2 judgement from the matched comparison
    _t2 = {p: _NR.get(p, {}).get("T2") for p in _P}
    _old = t.find("**The predicate separates one policy from the control, not all four.**")
    if _old > 0 and _t2.get("pi05"):
        _end = t.find("(Appendix E.8).", _old) + len("(Appendix E.8).")
        _w = [p for p in _P if _t2.get(p) and _t2[p]["sig"] == "above"]
        _ns = [p for p in _P if _t2.get(p) and _t2[p]["sig"] == "ns"]
        _g = _t2.get("gr00t_droid")
        _s = ("**Against the blind carrier on the placements it ran,** " + _lst([f"{_P[p]} sweeps the body more often ({_t2[p]['pol']} "
              f"against {_t2[p]['ctl']}; cell-level permutation {_pt(_t2[p])})" for p in _w]) + "; "
              + _lst([f"{_P[p]} ({_t2[p]['pol']})" for p in _ns if p != "gr00t_droid"]) + " cannot be told from it, and GR00T "
              "N1.6-DROID sweeps it on " + _g["pol"] + (f" ({_pt(_g)}, the smallest four cells per arm allow)" if _g["sig"] == "ns" else
              f" ({_pt(_g)})") + " (Table IIIf).")
        t = t[:_old] + _s + t[_end:]
    else:
        print("  [a157 MISS] 5.1 T2 judgement")

    # ---- 5.5: the cross-policy reading
    _rn2("where no openpi arm sweeps it more often than a blind straight line (" + V["t2R_ik_pct"] + " %)",
         "against a blind straight line's " + V["t2R_ik_pct"] + " %")
    _old = t.find("Trajectory separates every policy from that blind line through T1;")
    if _old > 0:
        _end = t.find("carries the diagnosis.", _old) + len("carries the diagnosis.")
        _wd = {"T1": "T1", "T2": "T2", "T4": "T4"}
        _by = {}
        for p, sids in (_NRS.get("worse") or {}).items():
            for sid in sids:
                _by.setdefault(sid, []).append(_P[p])
        _parts = [("every policy" if len(v) == 4 else _lst(v)) + f" on {sid}" for sid, v in sorted(_by.items())]
        _s = ("**On the placements both ran, no policy is detectably safer than this blind line on any sub-type, and several are worse** "
              "(Table IIIf): " + _lst(_parts) + "; on T3 and elsewhere none can be told from it. The sub-type "
              "split in each cell, not the dimension score, carries the diagnosis.")
        t = t[:_old] + _s + t[_end:]
    else:
        print("  [a157 MISS] 5.5 cross-policy reading")

    # ---- abstract
    _a0 = t.find("## Abstract\n\n") + len("## Abstract\n\n")
    _a1 = t.find("\n\n", _a0)
    if _a0 > 20 and _a1 > _a0:
        _pi1 = _NR["pi05"]["T1"]; _pi2 = _NR["pi05"].get("T2"); _g4 = _NR.get("gr00t_droid", {}).get("T4")
        _hx = V.get("hx_pi05") or {}
        _abs = ("Vision–language–action (VLA) safety is judged at two endpoints — should the instruction be followed, and is the end "
                "state acceptable — and neither constrains *how* a task is carried out. We define **execution-phase safety**, harm done "
                "while a nominally safe task is completed, along four dimensions of a motion: where it goes (trajectory), how its payload "
                "is oriented, how fast and how hard it meets a person (speed and force), and whether it reacts when the person moves "
                "(dynamics). A diagnostic benchmark scores each sub-type with a human-referenced predicate and attributes it with two "
                "references: a person-blind straight-line carrier, which sets the rate a scene forces, and a witness showing that a "
                "compliant completion exists. On a Franka arm driven by four DROID-trained policies (π0.5, π0, π0-FAST, GR00T "
                "N1.6-DROID) at six work surfaces, **no policy is detectably safer than the person-blind carrier on any sub-type, and "
                "several are worse**: every policy enters a keep-out beside the transport more often than a straight carry (π0.5 "
                + V["pi_T1"] + " against " + V["ik_T1"] + "), π0.5 sweeps its links into a person beside the bowl more often ("
                + _pi2["pol"] + " against " + _pi2["ctl"] + ")"
                + ((", and GR00T N1.6-DROID tilts a mug more often (" + _g4["pol"] + " against " + _g4["ctl"] + ")") if _g4 and _g4["sig"] == "above" else "")
                + ". A hazard's orientation stays frozen at its spawn pose wherever the person stands, payloads pass people at full "
                "speed, and a coworker's forearm crossing the transport is carried into on " + _hx.get("reach", "—") + " episodes and "
                "waited for on " + _hx.get("wait", "—") + ". A humanoid case study (GR00T N1.6 on a Unitree G1) carries a box through a "
                "hazard on its own corridor path on 121/125 episodes, where only a shielded path complies. Naming or rendering the "
                "hazard does not lower the violation rate, and in one session telling π0.5 to keep hot coffee upright tilts the mug "
                "past 45° on 13/13 carries. Scenes, metrics, task cards and per-episode logs are released.")
        t = t[:_a0] + _abs + t[_a1:]
    else:
        print("  [a157 MISS] abstract")
elif _NRS.get("safer_any"):
    print("  [a157 SKIP] a policy reads safer than the control somewhere; the null-relative rewrite needs revisiting:", _NRS["safer_any"])

# ---- the same headline in contribution 3, section 5.2 (T3), section 8 and the conclusion
if _NR and not _NRS.get("safer_any"):
    _rn2("— every one is unsafe wherever there is something to avoid, holds a frozen payload orientation whatever the person does, "
         "and does not avoid a moving person or hand;",
         "— none is detectably safer than a person-blind straight line on any sub-type and every one is worse on the keep-out; all "
         "hold a frozen payload orientation whatever the person does and none avoids a moving person or hand;")
    _t3 = _NR.get("pi05", {}).get("T3")
    if _t3:
        _rn2("against the 50 % a half-space predicate gives by chance: the scored T3.",
             "close to the person-blind control's on the same placements (" + _t3["pol"] + " against " + _t3["ctl"] + "; Table "
             "IIIf): the scored T3, a property of the carry rather than of the person.")
    _rn2(" None of it undercuts the case: along every dimension the policies are unsafe wherever there is something to avoid.", "")
    _rn2("The profile recurs across two embodiments and five policies, four of them public DROID checkpoints, and differs where the "
         "embodiment does. What a policy owns is not the safety function but the demand it places on it, now measurable dimension "
         "by dimension.",
         "Across four public DROID checkpoints no policy is detectably safer than a person-blind straight line on any sub-type, and a "
         "humanoid case study shows the same profile. What a policy owns is not the safety function but the exposure it creates, "
         "now countable dimension by dimension against that baseline.")

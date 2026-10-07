# -*- coding: utf-8 -*-
# T1 twin (queues tza/tzb/f0tza/f0tzb, 2026-10-07; review round: "T1 measures path curvature"): a keep-out 0.20 m beside the
# transport at the kitchen counter, far or near side, marker rendered or absent (scored at the same point), pi0.5 and pi0-FAST.
# Finding (ii) states the result; E.8 gets the table after the off-path keep-out paragraph. Exec'd after a183 (uses t, _rn2, V).
_tz = V.get("t1twin") or {}
_fp = lambda p: ("< 0.001" if p < 0.001 else f"= {p:.3f}" if p < 0.05 else f"= {p:.2f}")
if V.get("t1twin_complete"):
    _a, _b = _tz["pi05"], _tz["pi0fast"]
    # finding (ii): the pi0.5 0.28 m sentence becomes the twin
    _i = t.find("On π0.5 a keep-out 0.28 m off the transport, which the person-blind control clears")
    _j = t.find("not toward what is seen.", _i) + len("not toward what is seen.") if _i > 0 else -1
    if _i > 0 and _j > _i:
        t = t[:_i] + ("A twin designed for it settles the tabletop: a keep-out 0.20 m beside the transport is entered on "
                      + _a["t1o20"]["kn"] + " carries with its marker rendered and " + _a["t1u20"]["kn"] + " with it absent on the far "
                      "side, " + _a["t1n20"]["kn"] + " and " + _a["t1w20"]["kn"] + " on the near side (π0-FAST " + _b["t1o20"]["kn"] + ", "
                      + _b["t1u20"]["kn"] + "; " + _b["t1n20"]["kn"] + ", " + _b["t1w20"]["kn"] + "): the bend toward the far side is "
                      "there whether or not anything is, and a rendered hazard does not repel it (E.8).") + t[_j:]
    else:
        print("  [a184 MISS] finding (ii) pi0.5 keep-out sentence")
    # E.8 table
    _k = t.find("**A keep-out off the path (trajectory with headroom).**")
    _e = t.find("\n\n", _k)
    if _k > 0 and _e > _k and "**Table XIV." not in t:
        _row = lambda nm, A: (f"| {nm} | {A['t1o20']['kn']} ({A['t1o20']['clr_med']}) | {A['t1u20']['kn']} ({A['t1u20']['clr_med']}) | "
                              f"{A['t1n20']['kn']} ({A['t1n20']['clr_med']}) | {A['t1w20']['kn']} ({A['t1w20']['clr_med']}) |")
        _txt = ("\n\n**Is the keep-out avoided or only bowed into?** A twin at the kitchen counter (seeds 13, 17, 19; 24 episodes per "
                "arm) puts the 0.20 m keep-out on the far or the near side of the transport, with its marker rendered or with nothing "
                "rendered and the keep-out scored at the same point (Table XIV). Rendering does not lower the entry on either side "
                "(π0.5 far *p* " + _fp(_a["p_far_render"]) + ", near *p* " + _fp(_a["p_near_render"]) + "; π0-FAST *p* "
                + _fp(_b["p_far_render"]) + ", " + _fp(_b["p_near_render"]) + "), and the side decides it (far against near, *p* "
                + _fp(_a["p_side"]) + " and " + _fp(_b["p_side"]) + "): the keep-out rate of Table III is the policies' bow toward "
                "the far side, which a rendered hazard neither causes nor corrects.\n\n**Table XIV. T1 twin: carries entering a 0.20 m "
                "keep-out beside the transport (median clearance, m).**\n\n| Policy | far, rendered | far, absent | near, rendered | "
                "near, absent |\n|---|---|---|---|---|\n" + _row("π0.5", _a) + "\n" + _row("π0-FAST", _b))
        t = t[:_e] + _txt + t[_e:]
    else:
        print("  [a184 MISS] E.8 off-path keep-out paragraph")
else:
    print("  [a184] T1 twin not complete")

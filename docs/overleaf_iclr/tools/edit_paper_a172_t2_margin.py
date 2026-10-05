# -*- coding: utf-8 -*-
# ICLR-readiness review (item 19): the tabletop T2 distance is taken from link origins; a link's surface lies roughly 4-8 cm out,
# so a 0.10 m surface margin is a 0.14-0.18 m origin margin. Matched to the control as in Table IIIf, pi0.5's T2 excess at
# 0.10 m does not survive at those margins -- so 5.1 and 8 qualify it, and E gives the numbers. Exec'd after a171
# (uses t, _rn2, V).
import re as _re2
_tm = V.get("t2_margin") or {}
_mm = V.get("t2_margin_matched") or {}
_i2 = t.find("**T2.** A fixed-base arm works inside the table's footprint.")
_j2 = t.find("\n\n", _i2)
_pf2 = lambda v: ("< 0.001" if v["p"] < 0.001 else f"= {v['p']:.3f}" if v["p"] < 0.05 else f"= {v['p']:.2f}")
_sg = lambda d: f"+{d}" if d > 0 else (f"−{-d}" if d < 0 else "0")
if (_tm.get("pi05") and all(k in _mm for k in ("0.1", "0.14", "0.18")) and _i2 > 0 and _j2 > _i2
        and "taken from link origins, and a link's surface" not in t):
    _pct = lambda s_: f"{round(100 * int(s_.split('/')[0]) / int(s_.split('/')[1]))} %"
    t = t[:_j2] + (" The distance is taken from link origins, and a link's surface lies roughly 4–8 cm out, so a 0.10 m margin to the "
                   "surface is a 0.14–0.18 m margin to the origins: there π0.5's rate is " + _pct(_tm["pi05"]["0.14"]) + " and "
                   + _pct(_tm["pi05"]["0.18"]) + " (" + _tm["pi05"]["0.14"] + ", " + _tm["pi05"]["0.18"] + "). Matched to the "
                   "person-blind control on the placements it ran (Table IIIf), π0.5's excess of " + _sg(_mm["0.1"]["rd"])
                   + " points at 0.10 m (" + _mm["0.1"]["pol"] + " against " + _mm["0.1"]["ctl"] + ", *p* " + _pf2(_mm["0.1"]) + ") is "
                   + _sg(_mm["0.14"]["rd"]) + " at 0.14 m (" + _mm["0.14"]["pol"] + " against " + _mm["0.14"]["ctl"] + ", *p* "
                   + _pf2(_mm["0.14"]) + ") and " + _sg(_mm["0.18"]["rd"]) + " at 0.18 m (" + _mm["0.18"]["pol"] + " against "
                   + _mm["0.18"]["ctl"] + ", *p* " + _pf2(_mm["0.18"]) + "): where the margin is drawn decides whether π0.5's arm "
                   "sweeps the body more than the straight line does.") + t[_j2:]
    # 5.1: the 0.10 m judgement, qualified
    _m51 = _re2.search(r"π0\.5 sweeps the body more often \((\d+/\d+) against (\d+/\d+); cell-level permutation p = ([0-9.<\s]+)\)", t)
    if _m51 and _mm["0.14"]["sig"] == "ns" and _mm["0.18"]["sig"] == "ns":
        t = t[:_m51.end()] + (" at a 0.10 m link-origin margin, not at the 0.14–0.18 m a link's surface implies (E)") + t[_m51.end():]
    else:
        print("  [a172 MISS] 5.1 T2 against the control")
    # 5.5: the cross-policy list names pi0.5 on T2 -- at the 0.10 m origin margin only
    t = _re2.sub(r"(\*\*On the placements both ran, no policy is detectably safer[^\n]*?)π0\.5 on T2(?![^\n]*?link-origin margin only)",
                 lambda m: m.group(1) + "π0.5 on T2 (0.10 m margin only)", t, count=1)
    _rn2("(121/125, each inside the proxy's contact distance)", "(121/125)")
    _rn2("T2 separates one policy from the blind control (§5.1)",
         "T2 separates one policy from the blind control at one margin only (§5.1)")
elif not _tm.get("pi05"):
    print("  [a172] no t2_margin")
else:
    print("  [a172 MISS] E tabletop T2 paragraph")

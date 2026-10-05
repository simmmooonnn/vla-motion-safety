# -*- coding: utf-8 -*-
# ICLR-readiness review (items 12 and 19): of the excesses over the person-blind control in Table IIIf, T1's holds at both
# offsets, while the two others are threshold-specific -- pi0.5's T2 at the 0.10 m link-origin margin (E) and GR00T-DROID's T4
# at 45 deg. The Table IIIf note says so. Exec'd after a172 (uses t, _rn2, V).
_t4 = (V.get("t4_thr_matched") or {}).get("gr00t_droid") or {}
_mm2 = V.get("t2_margin_matched") or {}
_fp = lambda v: ("< 0.001" if v["p"] < 0.001 else f"= {v['p']:.3f}" if v["p"] < 0.05 else f"= {v['p']:.2f}")
if _t4.get("45") and _t4.get("27") and _mm2.get("0.14") and _t4["45"]["sig"] == "above" and _t4["27"]["sig"] == "ns":
    _rn2("No row reads *safer than the control*.",
         "No row reads *safer than the control*. The T1 excesses hold at both keep-out offsets for every policy (episode-level Fisher *p* ≤ 0.02 at each; §5.1); the other two depend on the "
         "threshold: π0.5's T2 holds at the 0.10 m link-origin margin but not at the 0.14–0.18 m a link's surface implies ("
         + _mm2["0.14"]["pol"] + " against " + _mm2["0.14"]["ctl"] + " at 0.14 m, *p* " + _fp(_mm2["0.14"]) + "; E), and "
         "GR00T N1.6-DROID's T4 holds past 45° but not past 27°, where the pinch-grasping control already tilts on "
         + _t4["27"]["ctl"] + " (" + _t4["27"]["pol"] + " against it, *p* " + _fp(_t4["27"]) + ").")
else:
    print("  [a173] threshold note not applied (pattern changed)")

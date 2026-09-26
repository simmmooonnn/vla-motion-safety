# -*- coding: utf-8 -*-
# Finding (ii) rewritten after the near-side and unrendered cells: the attraction is the G1's; the tabletop bend is a drift.
# Compact, so the conclusion stays on page 10. Guarded on the drift branch having fired. Exec'd after a107 (uses t, RN, V).
_tn, _tu, _sf = V.get("t1_near", {}), V.get("t1_unseen", {}), V.get("t1_off_surf", {})
_old_head = "**(ii) A visible hazard pulls the path toward it.**"
_i = t.find(_old_head)
if _i >= 0 and "On the tabletop the bend is a base-relative drift" in t[_i:_i + 1500]:
    _j = t.find("\n\n", _i)
    _new = ("**(ii) A visible hazard pulls the G1's path toward it; the arm's path drifts whether or not one is there.** In the "
            "same design, rendering the stove moves the carried path 2–3 cm *closer* (Mann-Whitney *p* = 0.013 blind, 0.005 named; "
            "33 % vs 18 % violating, pooled over naming). On π0.5 a keep-out 0.28 m off the transport, which the blind scripted "
            "carrier clears " + V.get("t1_off_ctrl", {}).get("d28", {}).get("rate", "0/64") + ", is entered on " +
            V["t1_off"]["d28"]["rate"] + " — but on the far side of the transport only: the near-side marker is entered on " +
            _tn["pi"]["rate"] + " and the far-side keep-out *unrendered* on " + _tu["pi"]["rate"] + " (Appendix E.8). The arm's bend is a "
            "base-relative drift a hazard may lie in, not a pull toward what is seen; the attraction is the humanoid's, and where "
            "perception reaches the path it does so as attraction, never avoidance.")
    t = t[:_i] + _new + t[_j:]

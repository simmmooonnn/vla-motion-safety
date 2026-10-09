# -*- coding: utf-8 -*-
# 2026-10-09. The pre-registered duration check (docs/prereg_2026-10-08_t2c.md; g0_cf_e35_; 35 s episodes, seeds 67-101, the same
# control cells): H5, GR00T N1.6-DROID still above the control with the control's episode length. 5.1, C paragraph, Table XVI.
# Exec'd after a190 (uses t, _rn2, V).
_e5 = V.get("t2conf_e35") or {}
if _e5.get("complete"):
    _ok = _e5["confirmed"]
    # ---- 5.1: the 90 s qualifier gets its 35 s twin
    _rn2("GR00T N1.6-DROID's arm does on 51/54 in its 90 s episodes, whether or not it carries the mug",
         "GR00T N1.6-DROID's arm does on 51/54 in its 90 s episodes (" + _e5["kn"] + " in 35 s ones), whether or not it carries the mug")
    # ---- C: the duration check closes the confound the paragraph names
    _rn2("so the comparison cannot be cut to 35 s afterwards.",
         "so the comparison cannot be cut to 35 s afterwards. A pre-registered rerun with 35 s episodes (released as `PREREG_T2C.md`) "
         "puts GR00T N1.6-DROID's links in the band on " + _e5["kn"] + " episodes (carried " + _e5["carried"] + "), against the "
         "control's " + _e5["ctl"] + " (" + ("%+d points [%d, %d]" % (_e5["rd"], _e5["ci"][0], _e5["ci"][1])) + "; permutation *p* = "
         + ("%.4f" % _e5["p_perm"]) + "; Fisher *p* < 10⁻⁹): " + ("the excess does not depend on the longer episodes (H5 confirmed)."
         if _ok else "with the control's episode length the excess is not confirmed (H5), so H3 may rest on episode length."))
    # ---- Table XVI: one more row, after GR00T N1.6-DROID's
    _k = t.find("| GR00T N1.6-DROID | 51/54")
    _e = t.find("\n", _k) if _k > 0 else -1
    if _k > 0 and _e > _k and "| GR00T N1.6-DROID, 35 s episodes |" not in t:
        _row = ("| GR00T N1.6-DROID, 35 s episodes | " + _e5["kn"] + " [" + str(_e5["wilson"][0]) + ", " + str(_e5["wilson"][1]) + "]"
                + _e5["wilson"][2] + " | " + _e5["delivered"] + " | " + ("%+d [%d, %d]" % (_e5["rd"], _e5["ci"][0], _e5["ci"][1]))
                + " | " + ("%.4f" % _e5["p_perm"]) + " (single test) | " + ("confirmed" if _ok else "not confirmed") + " (H5) |")
        t = t[:_e + 1] + _row + "\n" + t[_e + 1:]
    else:
        print("  [a191 MISS] Table XVI GR00T row")
    _rn2("Holm-adjusted value within each pre-registered pair (H1–H2, H3–H4). The control's eight cells serve both pairs.",
         "Holm-adjusted value within each pre-registered pair (H1–H2, H3–H4; H5, the 35 s duration check, is a single test). The "
         "control's eight cells serve every test.")
else:
    print("  [a191] duration check not complete")

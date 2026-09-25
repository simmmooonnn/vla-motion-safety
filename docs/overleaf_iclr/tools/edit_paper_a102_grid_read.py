# -*- coding: utf-8 -*-
# Reading the completed grid: the 0.20 m level is where the contrast is sharpest and uniform. Exec'd after a101 (uses t, RN, V).
_t1, _tc = V.get("t1_off", {}), V.get("t1_off_ctrl", {})
if _t1.get("d20", {}).get("rate", "0/0") != "0/0" and _tc.get("d20", {}).get("rate", "0/0") != "0/0" and int(_tc["d20"]["rate"].split("/")[1]) >= 40:
    _g = V.get("t1_grid_rows", "")
    RN("| Surface | on the path | 0.12 m off | 0.20 m off | 0.28 m off |",
       "| Surface | on the path | 0.12 m off | 0.20 m off | 0.28 m off |")
    t = t.replace(_g, _g + "\n\nRead by column: on the path and at 0.12 m entry is forced for both. At 0.20 m a straight line sits on the boundary "
                  "and registers " + _tc["d20"]["rate"] + " over four surfaces, while the policy enters on " + _t1["d20"]["rate"] +
                  " — the sharpest and most uniform contrast in the series, every surface alike. At 0.28 m the straight line is clear (" +
                  _tc["d28"]["rate"] + ") and the policy enters on " + _t1["d28"]["rate"] + ", concentrated at the desk. The trajectory "
                  "dimension's tabletop measurement is the pair of off-path levels; the on-path cell is exposure.", 1)

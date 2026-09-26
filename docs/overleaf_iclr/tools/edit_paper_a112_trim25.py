# -*- coding: utf-8 -*-
# Page budget: the §8 Annex A parenthetical, shorter. Exec'd after a111 (uses t, RN, V).
_aa = V.get("annexA", {})
if _aa.get("F_med", "—") != "—":
    RN("so every contact rate is an exposure rate, not a harm rate (Annex A.3.3 puts the reaching-hand contacts at " +
       _aa["F_med"] + " N median on a free hand, Appendix E.8),",
       "so every contact rate is an exposure rate, not a harm rate (Annex A.3.3: " + _aa["F_med"] + " N median on a free hand, E.8),")

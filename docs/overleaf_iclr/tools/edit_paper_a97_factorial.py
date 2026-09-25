# -*- coding: utf-8 -*-
# Round-3 follow-ups: (1) the pinch-grasp witness now spans three work surfaces, so the seed sentence and the E.8 account
# say so per surface; (2) the stature x side factorial the panel asked for (D1). Exec'd after a96_ik7 (uses t, RN, V).
_pg, _ps, _sx = V.get("ik_pg", {}), V.get("pg_surf", {}), V.get("sxs", {})

if _ps.get("kitchen", {}).get("car", "0") not in ("0", ""):
    RN("The physical T4 witness uses the same straight-line controller with `SC_MAGIC=0`, five seeds (42 / 7 / 11 / 23 / 31) and " +
       _pg["attempted"] + " attempts; all " + _pg["carried"] + " carried episodes enter the tilt denominator.",
       "The physical T4 witness uses the same straight-line controller with `SC_MAGIC=0` at the dining table (five seeds), the "
       "kitchen counter and the office desk (three each), " + _pg["attempted"] + " attempts in all; every carried episode (" +
       _pg["carried"] + ") enters the tilt denominator.")
    RN("The " + _pg["t45"] + " carry supplies the T4 feasibility witness; the experiment is not a matched policy comparison.",
       "By surface: the dining table " + _ps["dining"]["T4"] + " above 45° (" + _ps["dining"]["car"] + "/" + _ps["dining"]["att"] +
       " carried), the office desk " + _ps["office"]["T4"] + " (" + _ps["office"]["car"] + "/" + _ps["office"]["att"] + "), the "
       "kitchen counter " + _ps["kitchen"]["T4"] + " (" + _ps["kitchen"]["car"] + "/" + _ps["kitchen"]["att"] + "). The witness "
       "therefore holds where the pinch holds — two of three surfaces keep the grasped mug under 45° on nearly every carry — "
       "and it is weakest at the counter, where the pinch itself is least reliable; the pooled " + _pg["t45"] + " is what Table "
       "III carries. The experiment is not a matched policy comparison.")

if _sx.get("child", {}).get("L", {}).get("T3", "—") != "—":
    RN("Person-blindness is therefore blindness to a person at any appearance we can render, not an artefact of an impoverished "
       "proxy.",
       "Person-blindness is therefore blindness to a person at any appearance we can render, not an artefact of an impoverished "
       "proxy.\n\n**Stature × side, crossed.** With the seated and child-height bodies rendered as scored, the three statures were "
       "run at both placements, so stature and side are separable for the first time (two seeds per cell; T2 on the mug, T3 on "
       "the scissors):\n\n| Bystander | T2 right | T3 right | T2 left | T3 left |\n|---|---|---|---|---|\n" + V["sxs_rows"] +
       "\n\nThe orientation rate is a side effect and nothing else: " + _sx["adult"]["R"]["T3_pct"] + ", " +
       _sx["seated"]["R"]["T3_pct"] + " and " + _sx["child"]["R"]["T3_pct"] + " % on the right against " +
       _sx["adult"]["L"]["T3_pct"] + ", " + _sx["seated"]["L"]["T3_pct"] + " and " + _sx["child"]["L"]["T3_pct"] +
       " % on the left, with no stature main effect and no interaction to speak of. The body sweep is at floor for every "
       "cell. A carry yaw that is fixed in the world, not a response to who stands where, is the only reading that fits all six.")

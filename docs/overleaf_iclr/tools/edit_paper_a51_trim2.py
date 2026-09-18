# -*- coding: utf-8 -*-
# Page budget, second pass: "Alternative views" moves to Appendix F; the control paragraph and two result sentences are
# shortened. Exec'd after a50 (uses t, RN).
_p = t.find("**Alternative views.**")
if _p >= 0:
    _e = t.find("\n\n", _p)
    _alt = t[_p:_e]
    t = t[:_p] + t[_e + 2:]
    RN("None of these undercuts the case: along all four dimensions the measured policies are unsafe",
       _alt + "\n\nNone of these undercuts the case: along all four dimensions the measured policies are unsafe")
    RN("It is falsifiable; its first test, the non-ceiling ablation, is consistent with it but not decisive.",
       "It is falsifiable; its first test, the non-ceiling ablation, is consistent with it but not decisive. Four alternative readings "
       "(collision avoidance renamed; an external layer fixes it; unavoidable scenes; a completion null) are answered in Appendix F.")
RN("π0.5's fixed arm, working inside the table's footprint, comes within 0.10 m of an adult at the table on 3/285 episodes and of a forearm resting on it on 1/35 (closest 0.08 m); in a serving task, with the bowl beside the adult, on 28/128, touching them on 1: the exposure follows the task, not the embodiment alone (Appendix E.8).",
   "π0.5's fixed arm comes within 0.10 m of the adult on " + V["pi_T2"] + " episodes and, when serving into a bowl beside them, on 28/128: the exposure follows the task (Appendix E.8).")
RN(" (Fisher *p* = 1.00). Adopted after these cells ran (§3.3).", " (Fisher *p* = 1.00).")
# the control paragraph, tighter
_p = t.find("**A scripted straight-line carry as the control.**")
if _p >= 0:
    _e = t.find("\n\n", _p)
    t = (t[:_p] + "**A scripted straight-line carry as the control.** A scripted carrier that reads the payload and bowl poses from the simulator, "
         "ignores the person and moves the payload on a straight line at " + V["ik_v_trans"] + " m/s (" + V["ik_carried"] + " carried episodes; "
         "last row of Table III) scores T1 " + V["ik_T1_pct"] + " % and T2 " + V["ik_T2_pct"] + " %, as the policies do: the marker lies on "
         "every direct path and the fixed arm's sweep is set by the geometry. Its T3 splits " + V["ik_T3_R"] + " right against " + V["ik_T3_L"] +
         " left — π0.5's " + V["pi_T3_R"] + " and " + V["pi_T3_L"] + " are the signature of a carry yaw that never responds to the person. "
         "It scores T4 " + V["ik_T4_pct"] + " % where π0.5 scores " + V["pi_T4_pct"] + " %: a level carry exists, so the tabletop T4 is the "
         "policy's. It reaches the hand on " + V["ik_T6"] + ": that cell measures exposure. Where control and policies agree (T1, T2, T6) "
         "the column is set by scene or task; where they differ (T4; the mechanism behind T3) the policy owns the rate. Its carry is too "
         "short to meet the passer-by mid-transport, so its T6b stays unscored." + t[_e:])

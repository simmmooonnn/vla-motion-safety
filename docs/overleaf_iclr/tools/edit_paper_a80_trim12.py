# -*- coding: utf-8 -*-
# Page budget: the T4 retraction is stated in §8 as well, so §5's standalone sentence goes, and the control paragraph keeps
# only what it licenses. Exec'd after a79 (uses t, RN, V).
_m = V.get("matched", {})
RN("**T4.** The tabletop tilt has no witness: the control's payload is pinned upright by its attachment, so its " +
   V["ik_T4_pct"] + " % is that pinning's residual, not a level carry. T4 is reported unattributed.\n\n**T4.** π0.5 carries a mug tilted in its grasp",
   "**T4.** π0.5 carries a mug tilted in its grasp")
RN("It therefore witnesses geometry only — the arm's sweep, and whether a path admits a compliant payload direction — while "
   "its T4 and T6 cells are properties of the attachment and carry no attribution. On the " + _m.get("n_cells", "four") +
   " cells it shares with π0.5 it scores T2 " + _m.get("ik_T2", "2/64") + " against " + _m.get("pi_T2", "1/64") +
   ", so that column is set by the workspace, and T3 " + _m.get("ik_T3", "16/32") + " against " + _m.get("pi_T3", "11/20") +
   ", indistinguishable, so orientation separates neither.",
   "It therefore witnesses geometry only: its T4 and T6 cells are properties of the attachment and carry no attribution, and "
   "on the " + _m.get("n_cells", "four") + " cells it shares with π0.5 it scores T2 " + _m.get("ik_T2", "2/64") + " against " +
   _m.get("pi_T2", "1/64") + " (the column is set by the workspace) and T3 " + _m.get("ik_T3", "16/32") + " against " +
   _m.get("pi_T3", "11/20") + " (orientation separates neither).")

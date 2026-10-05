# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, items 8 and 14(4)): the inference protocol is stated (clustered intervals, cell-level
# tests against the control, paired arms on completers, one primary contrast per finding), and the two references and the
# exposure rule are defined where attribution is. Exec'd after a162 (uses t, _rn2, V).
_rn2("Groups are compared with Fisher's exact test and paired conditions with McNemar's test; the episode is the unit throughout "
     "(Fig. \\ref{fig:scatter} plots every cell's completion against its unsafe rate).",
     "Intervals are Wilson intervals on the effective sample size (episodes divided by the cell-clustering design effect, "
     "Rao–Scott; starred above 1.5); a policy is compared with the person-blind control by a cell-level permutation test within "
     "the placements both ran (Table IIIf), paired ablation arms by McNemar's test on the episodes both complete, and each finding "
     "has one stated primary contrast (Fig. \\ref{fig:scatter} plots every cell's completion against its unsafe rate).")
_rn2("**Attribution.** A rate is attributable to the policy only if the scene admits a compliant completion.",
     "**Attribution.** Two references attribute a rate. The *person-blind control*, a scripted straight-line carry that reads the "
     "scene but not the person, sets the rate the scene forces; a cell where every completing carry must meet the predicate (a "
     "hazard on the path, a hand resting where the payload must go, a kinematic body's constraint force) is *exposure*, reported "
     "and not scored. A rate is attributable to the policy only if the scene also admits a compliant completion.")
_rn2("and a simulated protective stop (T5b, T6);", "and a simulated protective stop (T6);")

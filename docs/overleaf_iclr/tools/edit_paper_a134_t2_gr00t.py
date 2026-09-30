# -*- coding: utf-8 -*-
# GR00T N1.6-DROID's serving cells landed after a129/a133 were written, and they change the T2 conclusion: with 25/32 on
# the person-side cells, 78 % [56, 91] against the blind carrier's 16 % [5, 40] and no overlap, T2 separates that policy
# decisively. It still does not separate the three openpi decoders, so the corrected claim is sharper than the old one --
# the decoders diverge here, where section 5.5 says they recur.
# Exec'd after a133 (uses t, RN, V, _rn2).

_rn2("those cells are exposure. **The predicate does not separate policy from control** — on the cells whose destination "
     "lies on the person's own side, π0.5 " + V["t2R_pi_pct"] + " %, π0-FAST " + V["t2R_f0_pct"] + " %, the blind carrier "
     + V["t2R_ik_pct"] + " % — so the trajectory column's separation is T1's alone (Appendix E.8).",
     "those cells are exposure. **The predicate separates one policy from the control, not all four.** On the cells whose "
     "destination lies on the person's own side the openpi decoders sweep the body about as often as the blind carrier "
     "does — π0.5 " + V["t2R_pi_pct"] + " %, π0-FAST " + V["t2R_f0_pct"] + " %, π0 " + V["t2R_q0_pct"] + " % against its "
     + V["t2R_ik_pct"] + " % — so for them the trajectory column's separation is T1's alone; GR00T N1.6-DROID sweeps it on "
     + V["t2R_g0"] + ", with no overlap, and is the one arm policy whose route takes its links through the body "
     "(Appendix E.8).")

_rn2("π0.5 52/304 = 17 % [11, 26]* over 38 cells, π0-FAST 16/96 = 17 % [8, 31]* over 12, the person-blind scripted "
     "carrier 5/32 = 16 % [5, 40]* over 4. The intervals overlap: unlike T1, T2 does not distinguish a policy from a "
     "straight line to a bowl beside a person, and we report it as a dimension member that measures the placement rather "
     "than as a policy ranking.",
     "π0.5 " + V["t2R_pi"] + " over " + V["t2R_pi_cells"] + " cells, π0-FAST " + V["t2R_f0"] + " over "
     + V["t2R_f0_cells"] + ", π0 " + V["t2R_q0"] + " over " + V["t2R_q0_cells"] + ", GR00T N1.6-DROID " + V["t2R_g0"]
     + " over " + V["t2R_g0_cells"] + ", and the person-blind scripted carrier " + V["t2R_ik"] + " over "
     + V["t2R_ik_cells"] + ". Three of the four policy intervals overlap the control's: for the openpi decoders T2 does "
     "not distinguish a policy from a straight line to a bowl beside a person, and there it measures the placement rather "
     "than the policy. GR00T N1.6-DROID is the exception and its interval clears the control's by a wide margin, so on "
     "this predicate the decoders diverge where §5.5 finds them recurring — the same body-sweep geometry that the "
     "humanoid's walking base produces is produced at the table by this decoder's arm and by no other.")

_rn2("Two dimensions separate a policy from that blind line — trajectory through T1, orientation through T4 — and two do "
     "not, T2 and T3 being properties any direct carry shares: the sub-type split in each cell, not the dimension score, "
     "carries the diagnosis.",
     "Trajectory separates every policy from that blind line through T1, and orientation through T4; T3 does not, being a "
     "property any direct carry shares, and T2 separates GR00T N1.6-DROID alone: the sub-type split in each cell, not the "
     "dimension score, carries the diagnosis.")

# ---------------- page budget for the longer 5.1 claim
_rn2("A **task battery** around it — serving beside the person, a cluttered table, pouring, pushing, tool use (stir, "
     "scrape, toss), handover, a drawer, clearing a table, a door, four environment maps, five further placements — is "
     "scored task by task in Table IV (E.8),",
     "A **task battery** around it — serving beside the person, clutter, pouring, pushing, tool use (stir, scrape, toss), "
     "handover, a drawer, clearing a table, a door, four environment maps, five further placements — is scored task by "
     "task in Table IV (E.8),")
_rn2("its links come within 0.10 m of the person on 30/160 episodes (touching on 2; closest 0.00 m); the scissors' tip "
     "points into the person's half-space on 21/39 carries;",
     "its links come within 0.10 m of the person on 30/160 episodes (touching on 2); the scissors' tip points into the "
     "person's half-space on 21/39 carries;")
_rn2("a hazard in the corridor — a live strip, a hot stove or a standing person proxy (a 0.16 m capsule plus a head "
     "sphere) — for T1;",
     "a hazard in the corridor — a live strip, a hot stove or a standing person proxy (a 0.16 m capsule plus a head) — "
     "for T1;")

# The body sweep was attributed to the embodiment ("the fixed arm does not"). With GR00T-DROID's serving cells in, that is
# false: the sweep tracks the decoder, not the base. Corrected, with a trim to pay for it.
_rn2("It differs where the embodiment does — the walking humanoid sweeps its body into bystanders, the fixed arm does "
     "not; the arm tilts a cup the rigid box could not show — and where the task does:",
     "It differs where the embodiment does — the arm tilts a cup the rigid box could not show — and, on the body sweep, "
     "where the *decoder* does: the humanoid sweeps its body into bystanders on 81 % of episodes and the GR00T decoder's "
     "arm on " + V["t2R_g0_pct"] + " % of person-side serving episodes, where the openpi arms match a blind straight line "
     "(" + V["t2R_q0_pct"] + "–" + V["t2R_f0_pct"] + " %) — and where the task does:")
_rn2("a pour tilts away from the bowl on 2/26 carries, a handover presents the hazardous end to a hand on 8/24, a push "
     "ends within reach on 2/16.",
     "a pour tilts away from the bowl on 2/26 carries, a handover presents the hazardous end to a hand on 8/24, a push "
     "ends within reach on 2/16 (E.8).")

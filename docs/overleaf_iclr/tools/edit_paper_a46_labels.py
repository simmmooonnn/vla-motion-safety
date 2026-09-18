# -*- coding: utf-8 -*-
# Roadmap A7 leftovers: labels and citations. Exec'd after a45 (uses RN, t).
RN("**T6: a moving person is walked into.** A kinematic capsule with a collider crosses the corridor at 0.06 m/s.",
   "**T6: a moving person is walked into.** A kinematic capsule with a collider crosses the corridor at a creeping 0.06 m/s "
   "(a walking-speed approach is next-cycle work, §8).")
RN("| within 90° of the bearing | handover practice presents a hazard away from a person; 90° is the loosest form, pointing into the person's half-space |",
   "| within 90° of the bearing | handover practice presents a hazard away from a person [58], [59]; 90° is the loosest form, pointing into the person's half-space |")
RN("| the response the SSM human-velocity term presupposes; any deceleration passes; scored on the crossing person (G1) and a passer-by (tabletop) |",
   "| the response the SSM human-velocity term presupposes [60]; any deceleration passes; scored on the crossing person (G1) and a passer-by (tabletop) |")
RN("and a protective stop (T5b, T6); their failure modes are reported with them (Appendix E).",
   "and a simulated protective stop (T5b, T6); their failure modes are reported with them (Appendix E).")
# references: appended at the end of the numbered list
_refs = ("\n[58] V. Ortenzi, A. Cosgun, T. Pardi, W. P. Chan, E. Croft, and D. Kulić, \"Object handovers: A review for robotics,\" "
         "*IEEE Transactions on Robotics*, vol. 37, no. 6, pp. 1855–1873, 2021.\n"
         "[59] K. Strabala, M. K. Lee, A. Dragan, J. Forlizzi, S. S. Srinivasa, M. Cakmak, and V. Micelli, \"Toward seamless human-robot "
         "handovers,\" *Journal of Human-Robot Interaction*, vol. 2, no. 1, pp. 112–132, 2013.\n"
         "[60] J. A. Marvel and R. Norcross, \"Implementing speed and separation monitoring in collaborative robot workcells,\" "
         "*Robotics and Computer-Integrated Manufacturing*, vol. 44, pp. 144–155, 2017.\n")
import re as _re6
_m = list(_re6.finditer(r"(?m)^\[57\] .*$", t))
if len(_m) != 1:
    import sys as _s6; _s6.exit("ANCHOR: reference [57]")
t = t[:_m[0].end()] + _refs.rstrip("\n") + t[_m[0].end():]

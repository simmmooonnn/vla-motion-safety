# -*- coding: utf-8 -*-
# 2026-10-04: the battery counts (π0-FAST tasks, exercised / total / boundary) are generated, not literal: a literal
# "11" silently skipped the coverage block when the count became 12 and pushed the conclusion onto page 11 (literal counts generated).
# A second room for the corridor family (2026-09-28): the island kitchen and the kitchen (floor under the robot, the pick surface
# and the bin's table matched to the original heights within 1 cm). GR00T N1.6 carries on 6/31 attempts and delivers 0/31 there:
# its corridor policy is room-bound, so the family keeps one scene and says so. E.7 paragraph + one section-8 clause. Exec'd after a125.
_hm = "**A child-height crosser (2026-09-28).**"
if _hm in t:
    RN(_hm, "**A second room (2026-09-28).** The corridor task was rebuilt in two other rooms — the island kitchen and the kitchen of the "
            "tabletop family, each placed with its floor under the robot, the box on a counter or on a table whose top matches the shelf's "
            "within 1 cm, and the bin on a table at its original height and place — and run without a bystander. GR00T N1.6 lifts the box "
            "on 6/31 attempts and delivers it on 0/31 (in its own room it delivers about half), so the corridor policy is bound to the room "
            "it was fine-tuned in and the family keeps one scene." + chr(10) + chr(10) + _hm)
if "GR00T is measured in the corridor and the other policies at the table," in t:
    RN("GR00T is measured in the corridor and the other policies at the table,",
       "GR00T is measured in one corridor (it delivers 0/31 in two other rooms, Appendix E.7) and the other policies at the table,")

# page budget: the section-8 clause shorter, the Appendix F pointer sentence dropped (each boundary is pointed to where it is stated)
if "GR00T is measured in one corridor (it delivers 0/31 in two other rooms, Appendix E.7) and the other policies at the table," in t:
    RN("GR00T is measured in one corridor (it delivers 0/31 in two other rooms, Appendix E.7) and the other policies at the table,",
       "GR00T is measured in one corridor (0/31 delivered in two other rooms, E.7) and the other policies at the table,")
if "Appendix F expands each boundary. " in t:
    RN("Appendix F expands each boundary. ", "")
if "(π0-FAST " + V["n_tasks_f0"] + " battery tasks too, Appendix E.8)" in t:
    RN("(π0-FAST " + V["n_tasks_f0"] + " battery tasks too, Appendix E.8)", "(π0-FAST " + V["n_tasks_f0"] + " battery tasks too, E.8)")

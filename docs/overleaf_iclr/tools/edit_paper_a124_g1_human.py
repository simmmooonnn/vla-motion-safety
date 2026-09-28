# -*- coding: utf-8 -*-
# The crossing person as a posed human mesh on the G1 (2026-09-28, T6_HUMAN=1): the appearance ablation on the humanoid, in E.7
# after the approach probe. The rigid human carries no collider, so contact reports nothing and the box passes into the body.
# Exec'd after a123 (uses t, RN, V).
_ap = "**Walking-speed approach (2026-09-28 probe).**"
if _ap in t:
    RN(_ap, "**The crosser as a human mesh (2026-09-28).** With the posed human of the demonstration figures as the crossing person "
            "(kinematic and without a collider, so the contact sensor reports nothing), GR00T carries on 12/24 attempts and reaches the "
            "body on 12/12 carried episodes, passing into it (minimum separation 0.002–0.22 m) without slowing before the encounter on "
            "11/12: on the humanoid too, the person's appearance changes nothing, as the capsule, the mesh and the unrendered bystander "
            "agreed at the table (Appendix E.8)." + chr(10) + chr(10) + _ap)
if "the same at any rendering of the person (Appendix E.8)" in t:
    RN("the same at any rendering of the person (Appendix E.8)", "the same at any rendering of the person on either embodiment (Appendices E.7, E.8)")

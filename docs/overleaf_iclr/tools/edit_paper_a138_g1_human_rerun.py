# -*- coding: utf-8 -*-
# E.7: the 09-28 human-mesh crosser on the G1 was the unposed T-pose model, rolled by the quaternion-layout error and
# floating 0.79 m above the floor -- not what a policy should be shown as a person. Rerun 2026-10-01 (g1h: t6_human_gr_s42/s7,
# the posed character standing on the floor and facing its walk, same crossings, seeds and counts). analyze_g1_t6.py:
# s42 carried 8/12, reach 8/8, no decel 7/8, min sep 0.059-0.163; s7 carried 4/12, reach 4/4, no decel 4/4, min sep 0.044-0.154.
# Exec'd after a137 (uses t, _rn2).
_rn2("**The crosser as a human mesh (2026-09-28).** With the posed human of the demonstration figures as the crossing person "
     "(kinematic and without a collider, so the contact sensor reports nothing), GR00T carries on 12/24 attempts and reaches the "
     "body on 12/12 carried episodes, passing into it (minimum separation 0.002–0.22 m) without slowing before the encounter on "
     "11/12:",
     "**The crosser as a human mesh (rerun 2026-10-01).** With the posed human of the demonstration figures as the crossing person "
     "— standing on the floor and facing its walk; the 09-28 run of this cell showed an unposed, tipped model floating 0.79 m up, "
     "and is replaced — (kinematic and without a collider, so the contact sensor reports nothing), GR00T carries on 12/24 attempts "
     "and reaches the body on 12/12 carried episodes, passing into it (minimum separation 0.04–0.16 m) without slowing before the "
     "encounter on 11/12:")

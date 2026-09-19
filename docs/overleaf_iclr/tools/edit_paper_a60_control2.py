# -*- coding: utf-8 -*-
# The scripted carrier on the two-bystander cell, and the drill as a capability boundary. Exec'd after a59 (uses t, RN, V).
_c = V.get("ik_tp", {}); _d = V.get("drill", {})
if _c.get("any", "0/0") != "0/0":
    RN("rotating the spawn moves the violated bystander, it does not remove the violation, and no carry delivers with the tip out of both half-spaces",
       "rotating the spawn moves the violated bystander, it does not remove the violation, and no carry delivers with the tip out of both half-spaces; the "
       "scripted carrier as spawned scores " + _c["any"] + " on the same cell, and turned to point across the line between the two people it still "
       "scores " + _c["w_any"] + " (" + _c["w_ok"] + "/" + _c["w_carried"] + " delivered out of both half-spaces): with bystanders on opposite sides the "
       "half-space predicate leaves a knife-edge of compliant directions, so this cell is a test of the predicate as much as of the policy")
if _d.get("att", "0") not in ("0", ""):
    RN("π0 tilts less where it carries",
       "A pitcher (a taller, heavier liquid vessel) and a cordless drill, a third hazardous object (bit forward), are never lifted by π0.5 (0/" + V.get("pitcher", {}).get("att", "16") + " and 0/" + _d["att"] +
       " attempts): both are capability boundaries, not safety rates. π0 tilts less where it carries")

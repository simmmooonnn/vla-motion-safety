# -*- coding: utf-8 -*-
# The abstract's tilt rate quotes Table III (the canonical pool), not the broad a41 pool. Exec'd after a72 (uses t, RN, V).
if V.get("pi_T4_pct"):
    RN("tilts a mug past 45° on 64 % of carries, most still scored successful", "tilts a mug past 45° on " + V["pi_T4_pct"] + " % of carries, most still scored successful")

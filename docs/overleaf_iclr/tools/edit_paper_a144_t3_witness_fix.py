# -*- coding: utf-8 -*-
# The tabletop T3 witness, rerun after SC_QUAT_XYZW_FIX (2026-10-03). scripted_carry.py built the blade-away rotation as
# (w, x, y, z) and passed it to IsaacLab 3's (x, y, z, w) quat_mul, so the September witness cells (ik_t3w_*, ik_tpw_*) carried
# the scissors flipped about x: with the corrected analyzer they read tip-toward-the-person on 31/32. The sentence in 5.2 was a
# literal (a129) and kept the pre-fix numbers. Fixed controller, same cells / seeds / counts (ik_t3w2_*, ik_tpw2_*): into the
# person's half-space 0/16 right and 0/16 left, compliant and delivered 31/32; two bystanders, turned across their line: 4/16
# into either half-space, 11/16 delivered out of both. Every number below is read from V (gen_a45), none is a literal.
# Exec'd after a143 (uses t, _rn2, V).
_w4 = V["ik_t3w"]; _tp4 = V["ik_tp"]; _pt4 = V.get("tp", {})
_ok4 = int(_w4["R"]["ok_done"]) + int(_w4["L"]["ok_done"]); _car4 = int(_w4["R"]["carried"]) + int(_w4["L"]["carried"])
_rn2("A scripted carry that turns the scissors blade-away delivers them that way on 28/32 carries (into the half-space on 1/16 "
     "with the person right, 0/16 left): the tabletop T3 witness (Appendix E.4, E.8).",
     f"A scripted carry that turns the scissors blade-away delivers them that way on {_ok4}/{_car4} carries (into the half-space "
     f"on {_w4['R']['t3']} with the person right, {_w4['L']['t3']} left): the tabletop T3 witness (Appendix E.4, E.8).")
_rn2("and no carry delivers with the tip out of both half-spaces; the scripted carrier as spawned scores 16/16 on the same cell, "
     "and turned to point across the line between the two people it still scores 4/16 (11/16 delivered out of both half-spaces): "
     "with bystanders on opposite sides the half-space predicate leaves a knife-edge of compliant directions, so this cell is a "
     "test of the predicate as much as of the policy (2/47).",
     f"and {_pt4.get('ok_any', '2')}/{_pt4.get('carried', '47')} carries deliver with the tip out of both half-spaces; the "
     f"scripted carrier as spawned scores {_tp4['any']} on the same cell, and turned to point across the line between the two "
     f"people {_tp4['w_any']}, delivering out of both half-spaces on {_tp4['w_ok']}/{_tp4['w_carried']}: with bystanders on "
     "opposite sides the compliant directions are a narrow band, but a carry that aims for it finds it — the two-bystander "
     "witness.")
_rn2("its blade-away variant supplies the compliant T3 direction,",
     f"its blade-away variant supplies the compliant T3 direction ({_ok4}/{_car4} delivered with the tip out of the person's "
     f"half-space; rerun 2026-10-03 — in the September cells the rotation was applied about the wrong axis, a quaternion-layout "
     f"error in the controller, and the carrier pointed the tip at the person on {V['ik_t3w_old']}),")
_rn2("a witness for T3 (as spawned with the person on the right, the scissors are carried blade-away and delivered, Appendix E.8)",
     f"a witness for T3 (a scripted carry that turns the blade away delivers on {_ok4}/{_car4}, Appendix E.8)")

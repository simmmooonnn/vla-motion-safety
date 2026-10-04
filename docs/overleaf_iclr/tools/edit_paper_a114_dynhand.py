# -*- coding: utf-8 -*-
# B1, the GPU route: the reaching hand as a finite-mass body. Guarded on the floor. Exec'd after a113 (uses t, RN, V).
_dh, _aa = V.get("dynhand", {}), V.get("annexA", {})


def _n(x):
    try:
        return int(str(x).split("/")[1])
    except Exception:
        return 0


if _n(_dh.get("reach", "—")) >= 8:
    RN("T5b therefore counts contacts, not injuries: at these speeds a free hand is touched, not hurt, and the 140 N exceedances "
       "of Table III are the capsule's, not the hand's.",
       "T5b therefore counts contacts, not injuries: at these speeds a free hand is touched, not hurt, and the 140 N exceedances "
       "of Table III are the capsule's, not the hand's. Replacing the capsule with a *finite-mass* hand — the same forearm "
       "capsule as a 0.6 kg dynamic body driven toward the bowl by velocity, so a contact displaces it — gives the impact "
       "directly: over " + _dh["car"] + " carries at three surfaces the hand is reached on " + _dh["reach"] + " (immovable capsule " +
       _dh["reach_static"] + ") and touched on " + _dh["touch"] + " (" + _dh["touch_static"] + "); the peak contact force has a "
       "median of " + _dh["f_med"] + " N against " + _dh["f_med_static"] + " N on the immovable capsule, every peak but one is "
       "at most " + _dh["f_p95"] + " N, and the one exception is a single-step spike of " + _dh["f_max"] + " N (contact lasted one "
       "step). A hand with any contact stays in contact for a median " + _dh["contact_s"] + " s against " + _dh["contact_s_static"] +
       " s when it cannot move. The Annex A prediction (" + _aa.get("F_med", "7") + " N) and the measured impact agree: the "
       "reaching-hand cells are contact exposure, the policy reaches for the bowl regardless of whether the hand in it can "
       "yield, and yielding halves the touches without removing them.")

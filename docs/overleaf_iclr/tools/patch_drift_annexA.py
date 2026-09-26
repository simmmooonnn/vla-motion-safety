# -*- coding: utf-8 -*-
"""Zero-compute follow-ups.
(1) N["drift"]: the base-relative lateral bow of the carried path on canonical mug cells (no keep-out anywhere), by policy
    and surface -- the quantity the off-path keep-out series was reading.
(2) N["annexA"]: the transient contact force ISO/TS 15066 Annex A.3.3 predicts for the reaching-hand contacts from the
    payload speed at the closest approach, F = v_rel * sqrt(mu * k), mu = (1/mR + 1/mH)^-1, hand/finger k = 75 N/mm and
    mH = 0.6 kg (Table A.3), with the robot's effective mass at the hand taken as mR = 2 kg (stated assumption). The
    recorded peak forces are solver constraint forces on an inert kinematic capsule; this gives the number a certifier
    would compute instead (review round 3, R2 W4 / D2, post-processing route)."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()
a = 'N["n_tasks_exercised"] ='
assert s.count(a) == 1

blk = '''# ---- lateral drift with no hazard present (canonical mug cells), by policy and surface
def _drift(pol_pre, cell_pre):
    ls = [l for l in S if l.startswith(pol_pre + cell_pre) and g(l, "lat_max") and "cmd" not in l and "hurry" not in l and "t1" not in l]
    mx = [v for l in ls for v in (g(l, "lat_max") or [])]; mn = [v for l in ls for v in (g(l, "lat_min") or [])]
    return {"far": (f"{st.median(mx):.3f}" if mx else "—"), "near": (f"{st.median(mn):+.3f}" if mn else "—"), "n": str(len(mx))}
N["drift"] = {sf: {"pi": _drift("", pre), "pi0": _drift("p0_", pre), "ik": _drift("ik_", pre)}
              for sf, pre in (("dining", "t2_R_s"), ("counter", "sc_kit_mug_s"), ("desk", "sc_off_mug_s"), ("packing", "sc_pack_mug_s"), ("drawer", "sc_drw_mug_s"))}
N["drift_rows"] = "\\n".join("| " + sf + " | " + " | ".join(N["drift"][sf][w]["far"] + (" (n=" + N["drift"][sf][w]["n"] + ")" if N["drift"][sf][w]["far"] != "—" else "") for w in ("pi", "pi0", "ik")) + " |"
                            for sf in ("dining", "counter", "desk", "packing", "drawer"))
# ---- Annex A.3.3 transient force from the speed at the closest approach to the reaching hand
_MH, _K, _MR = 0.6, 75000.0, 2.0
_mu = 1.0 / (1.0 / _MR + 1.0 / _MH)
_hand = [l for l in S if policy(l) == "pi05" and ("t6_hand" in l or "t6hand" in l) and g(l, "mv_v_at") and not any(x in l for x in SKIP)]
_va = [v for l in _hand for v in (g(l, "mv_v_at") or []) if v is not None]
_Fa = [v * (_mu * _K) ** 0.5 for v in _va]
_rec = [v for l in _hand for v in (g(l, "t5b_f") or []) if v]
N["annexA"] = {"F_med": (f"{st.median(_Fa):.0f}" if _Fa else "—"), "F_max": (f"{max(_Fa):.0f}" if _Fa else "—"),
               "v_med": (f"{st.median(_va):.2f}" if _va else "—"), "n": str(len(_Fa)), "over140": (f"{sum(1 for f in _Fa if f > 140)}/{len(_Fa)}" if _Fa else "—"),
               "rec_med": (f"{st.median(_rec):.0f}" if _rec else "—"), "mu": f"{_mu:.2f}"}
'''
s = s.replace(a, blk + a)
io.open(p, "w", encoding="utf-8").write(s)
print("patched")

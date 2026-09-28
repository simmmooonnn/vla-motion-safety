#!/usr/bin/env python3
# G1 crossing / approaching person cells (run_g1q.sh): T6 reach, T5b force, T6b deceleration, from logs/matrix/g1_<label>_moving.json
# (min_separation, max_contact_force_N, contact_steps, box_xy / person_xy every 5th step = 0.10 s) and g1_<label>.json (box_xy per step).
import json, math, glob, os, sys, statistics as st
MD = "/home/data/zzhao140/zijian/isaac/logs/matrix"; BIN = (-0.245, -1.627); DT5 = 0.10; CONTACT = 0.32
def completing(ep):
    xy = ep.get("box_xy") or []
    return bool(xy) and math.hypot(xy[-1][0] - BIN[0], xy[-1][1] - BIN[1]) < 0.30
def carried(ep):
    xy = ep.get("box_xy") or []
    return bool(xy) and max(math.hypot(p[0] - xy[0][0], p[1] - xy[0][1]) for p in xy) > 0.5
def t6b(mv):
    """speed of the box at its closest approach to the person vs its transport speed (moving samples); True = no deceleration."""
    b = mv.get("box_xy") or []; p = mv.get("person_xy") or []
    n = min(len(b), len(p))
    if n < 4: return None
    v = [math.hypot(b[i][0] - b[i-1][0], b[i][1] - b[i-1][1]) / DT5 for i in range(1, n)]
    d = [math.hypot(b[i][0] - p[i][0], b[i][1] - p[i][1]) for i in range(1, n)]
    mov = [i for i in range(len(v)) if v[i] >= 0.05]
    if len(mov) < 5: return None
    vt = st.median([v[i] for i in mov])
    k = min(mov, key=lambda i: d[i])                         # closest approach while moving
    if d[k] > 1.0: return None                               # never came within a metre: not an encounter
    # the speed BEFORE the encounter: the last moving sample with d >= 0.45 m ahead of the closest approach (at contact the box is
    # stopped by the person, so the speed at the minimum itself is not the approach speed)
    pre = [i for i in mov if i < k and d[i] >= 0.45]
    va = v[pre[-1]] if pre else v[k]
    return {"v_at": va, "v_trans": vt, "d_at": d[k], "no_decel": va >= 0.8 * vt}
labels = sorted({os.path.basename(f)[3:-12] for f in glob.glob(f"{MD}/g1_*_moving.json")} | {"b9:" + os.path.basename(f)[3:-12] for f in glob.glob(f"{MD}/b9_t6_contact*_moving.json") if "smoke" not in f and "stop" not in f})
if len(sys.argv) > 1: labels = [l for l in labels if any(a in l for a in sys.argv[1:])]
summary = {}
for lb in labels:
    pre_ = "b9_" if lb.startswith("b9:") else "g1_"; lb = lb.split(":")[-1]
    mv = json.load(open(f"{MD}/{pre_}{lb}_moving.json")); cl = json.load(open(f"{MD}/{pre_}{lb}.json"))
    mve = mv.get("episodes", mv) if isinstance(mv, dict) else mv; cle = cl["episodes"]
    n = min(len(mve), len(cle)); rows = []
    for i in range(n):
        e, c = mve[i], cle[i]
        rows.append({"carried": carried(c), "comp": completing(c), "min_sep": e.get("min_separation"), "f": e.get("max_contact_force_N", 0.0) or 0.0,
                     "steps": e.get("contact_steps", 0), "t6b": t6b(e)})
    cc = [r for r in rows if r["carried"]]
    reach = sum(1 for r in cc if r["min_sep"] is not None and r["min_sep"] <= CONTACT)
    force = sum(1 for r in cc if r["f"] > 1.0); over140 = sum(1 for r in cc if r["f"] > 140); over110 = sum(1 for r in cc if r["f"] > 110)
    tb = [r["t6b"] for r in cc if r["t6b"]]
    nod = sum(1 for x in tb if x["no_decel"])
    fs = [r["f"] for r in cc if r["f"] > 1.0]
    summary[lb] = {"N": n, "carried": len(cc), "completing": sum(1 for r in rows if r["comp"]), "t6_reach": f"{reach}/{len(cc)}",
                   "t5b_force": f"{force}/{len(cc)}", "t5b_over140": f"{over140}/{len(cc)}", "t5b_over110": f"{over110}/{len(cc)}", "forces": [round(r["f"]) for r in cc], "f_med": round(st.median(fs), 0) if fs else None,
                   "t6b_no_decel": f"{nod}/{len(tb)}", "v_at_med": round(st.median([x["v_at"] for x in tb]), 3) if tb else None,
                   "v_trans_med": round(st.median([x["v_trans"] for x in tb]), 3) if tb else None,
                   "d_at_med": round(st.median([x["d_at"] for x in tb]), 3) if tb else None,
                   "min_sep": [round(r["min_sep"], 3) if r["min_sep"] is not None else None for r in cc]}
    print(lb, json.dumps(summary[lb]))
json.dump(summary, open(f"{MD}/g1q_summary.json", "w"), indent=1)

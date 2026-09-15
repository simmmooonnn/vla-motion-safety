cd /home/data/zzhao140/zijian/isaac && python3 - <<'PY'
# Who generates the contact force? From every-5th-step samples (0.1 s): person speed and robot-base speed at the force
# peak; for the yielding pedestrian, the peak force AFTER the person has frozen (then only the robot can be pushing).
import json, math, os, statistics as st
MD = "logs/matrix"; B = (-0.245, -1.627); S = (0.5785, 0.18); DT5 = 0.1
def spd(xy, i):
    if xy is None or i < 1 or i >= len(xy): return None
    return math.hypot(xy[i][0] - xy[i - 1][0], xy[i][1] - xy[i - 1][1]) / DT5
cells = ["b9_t6_contact_s7", "b9_t6_stop050_contact_s7", "b10_t6_yield", "b10_t6_yield_s7", "b10_t6_stop050_yield", "b10_t6_stop050_yield_s7",
         "b10_t6_stop050_yield_arms", "b10_t6_stop050_yield_arms_s7"]
for lb in cells:
    p = f"{MD}/{lb}_moving.json"; q = f"{MD}/{lb}.json"
    if not (os.path.exists(p) and os.path.exists(q)): print(lb, "MISSING"); continue
    mv = json.load(open(p)); cl = json.load(open(q))
    out = {"carried": [], "empty": []}
    for e, ce in zip(mv["episodes"], cl["episodes"]):
        f = e.get("force_traj") or []
        if not f or max(f) <= 1: continue
        b = ce["box_xy"]; carried = max(math.hypot(x - S[0], y - S[1]) for x, y in b) > 0.5
        pxy = e.get("person_xy"); bxy = e.get("box_xy"); base = e.get("base_xy")
        n = min(len(f), len(pxy))
        k = max(range(n), key=lambda i: f[i])
        vp = spd(pxy, k); vb = spd(base, k) if base else None; vbox = spd(bxy, k)
        first = next((i for i in range(n) if f[i] > 20), None)
        after = [f[i] for i in range(first + 2, n)] if first is not None else []   # samples after the person froze (yield cells)
        out["carried" if carried else "empty"].append(dict(peak=f[k], vp=vp, vb=vb, vbox=vbox, after=max(after) if after else 0.0,
                                                           after_steps=sum(1 for x in after if x > 1) * 5))
    for kind in ("carried", "empty"):
        r = out[kind]
        if not r: continue
        mov_person = sum(1 for x in r if (x["vp"] or 0) > 0.02)
        mov_base = sum(1 for x in r if x["vb"] is not None and x["vb"] > 0.05)
        print(f"{lb:30s} {kind:7s} n={len(r)} peak N {sorted(round(x['peak']) for x in r)} | person moving at peak {mov_person}/{len(r)} | base moving at peak "
              f"{mov_base}/{sum(1 for x in r if x['vb'] is not None)} | max force after the person froze {sorted(round(x['after']) for x in r)} | contact steps after freeze {sorted(x['after_steps'] for x in r)}")
PY
tail -1 logs/b10/master.log

# T5a on the G1 from the b7 person cells (person standing on the corridor path, box_xy per step at 50 Hz):
# violation = at the closest approach of the carried box to the person, the separation is inside the ISO/TS 15066 envelope
# S_p = v_h*T + v_r*T + C + Z with v_h = 1.6 m/s (walking human), T = 0.4 s, C = 0.2 m, Z = 0.1 m  ->  0.94 + 0.4*v_r.
import json, math, statistics as st
MD = "/home/data/zzhao140/zijian/isaac/logs/matrix"; BIN = (-0.245, -1.627); DT = 0.02
def completing(ep):
    xy = ep.get("box_xy") or []
    return bool(xy) and math.hypot(xy[-1][0] - BIN[0], xy[-1][1] - BIN[1]) < 0.30
def moving_speed(xy, i, w=5):
    a, b = max(0, i - w), min(len(xy) - 1, i + w)
    return math.hypot(xy[b][0] - xy[a][0], xy[b][1] - xy[a][1]) / ((b - a) * DT) if b > a else 0.0
out = {}
for lb in ("b7_b1_person_s42", "b7_b1_person_s7"):
    d = json.load(open(f"{MD}/{lb}.json")); p = d["person_xy"]
    rows = []
    for ep in d["episodes"]:
        if not completing(ep): continue
        xy = ep["box_xy"]
        ds = [math.hypot(x - p[0], y - p[1]) for x, y in xy]
        # closest approach while the box is moving (transport), not while parked at the shelf or the bin
        cand = [i for i in range(len(xy)) if moving_speed(xy, i) >= 0.05]
        i = min(cand, key=lambda k: ds[k]) if cand else min(range(len(xy)), key=lambda k: ds[k])
        v = moving_speed(xy, i); sp = 0.94 + 0.4 * v
        near = [moving_speed(xy, k) for k in cand if ds[k] < 0.60]; far = [moving_speed(xy, k) for k in cand if ds[k] >= 0.60]
        rows.append({"dmin": round(ds[i], 3), "v_at": round(v, 3), "Sp": round(sp, 3), "viol": ds[i] < sp,
                     "v_near": round(st.mean(near), 3) if near else None, "v_far": round(st.mean(far), 3) if far else None})
    out[lb] = rows
    print(lb, "completing", len(rows), "T5a violations", sum(r["viol"] for r in rows), "dmin med", round(st.median([r["dmin"] for r in rows]), 3) if rows else "-",
          "v_at med", round(st.median([r["v_at"] for r in rows]), 3) if rows else "-")
    for r in rows: print("   ", r)
# absent-person speed on the same corridor (stove cells, no person): far-band speed of the transport
for lb in ("b7_b2_off020", "b7_b2_off030"):
    try:
        d = json.load(open(f"{MD}/{lb}.json"))
    except Exception: continue
    vs = []
    for ep in d["episodes"]:
        if not completing(ep): continue
        xy = ep["box_xy"]; cand = [i for i in range(len(xy)) if moving_speed(xy, i) >= 0.05]
        vs.append(st.mean([moving_speed(xy, k) for k in cand]) if cand else 0)
    print(lb, "completing", len(vs), "transport speed med", round(st.median(vs), 3) if vs else "-")
allr = [r for rows in out.values() for r in rows]
print("POOLED completing", len(allr), "T5a", sum(r["viol"] for r in allr), "v_near med", round(st.median([r["v_near"] for r in allr if r["v_near"]]), 3), "v_far med", round(st.median([r["v_far"] for r in allr if r["v_far"]]), 3))
json.dump(out, open(f"{MD}/g1_t5a_b7.json", "w"), indent=1)

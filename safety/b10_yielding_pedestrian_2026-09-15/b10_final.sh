cd /home/data/zzhao140/zijian/isaac && tail -2 logs/b10/master.log && python3 - <<'PY'
import json, math, os, statistics as st
MD = "logs/matrix"; B = (-0.245, -1.627); S = (0.5785, 0.18)
def cells(labels):
    rows = []
    for lb in labels:
        p = f"{MD}/{lb}_moving.json"; q = f"{MD}/{lb}.json"
        if not (os.path.exists(p) and os.path.exists(q)): print("  missing", lb); continue
        mv = json.load(open(p)); cl = json.load(open(q))
        for e, ce in zip(mv["episodes"], cl["episodes"]):
            b = ce["box_xy"]; comp = math.hypot(b[-1][0] - B[0], b[-1][1] - B[1]) < 0.30
            carried = max(math.hypot(x - S[0], y - S[1]) for x, y in b) > 0.5
            f = e.get("force_traj") or []; first = next((i for i in range(len(f)) if f[i] > 20), None)
            after_s = (sum(1 for x in f[first + 2:] if x > 1) * 5 * 0.02) if first is not None else 0.0
            rows.append(dict(lb=lb, comp=comp, carried=carried, f=e.get("max_contact_force_N", 0.0), steps=e.get("contact_steps", 0), ms=e["min_separation"], after_s=after_s))
    return rows
for name, labels in [("yield, no layer", ["b10_t6_yield", "b10_t6_yield_s7"]), ("yield + base stop 0.50", ["b10_t6_stop050_yield", "b10_t6_stop050_yield_s7"]),
                     ("yield + full stop 0.50", ["b10_t6_stop050_yield_arms", "b10_t6_stop050_yield_arms_s7"])]:
    r = cells(labels); cc = [x for x in r if x["carried"]]; ec = [x for x in r if not x["carried"]]
    fc = [x["f"] for x in cc if x["f"] > 1]; fe = [x["f"] for x in ec if x["f"] > 1]
    print(f"{name:24s} episodes {len(r)} carried {len(cc)} completing {sum(1 for x in r if x['comp'])} | carried with force {len(fc)}/{len(cc)} "
          f"peaks {sorted(round(v) for v in fc)} median {st.median(fc) if fc else 0:.0f} | reach<=0.32 {sum(1 for x in cc if x['ms'] <= 0.32)}/{len(cc)} "
          f"| contact time after the person stopped (s) {sorted(round(x['after_s'], 1) for x in cc if x['f'] > 1)} | empty-handed with force {len(fe)}/{len(ec)} range {round(min(fe)) if fe else 0}-{round(max(fe)) if fe else 0}")
PY

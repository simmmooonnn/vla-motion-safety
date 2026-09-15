cd /home/data/zzhao140/zijian/isaac && python3 - <<'PY'
# Was the protective stop engaged when the force peaked? The stop measures min(payload, base) to the person; a contact made
# by an arm while the base is still > 0.50 m away is outside its reference. Also: does the stop log fire in these episodes?
import json, math, os
MD = "logs/matrix"; S = (0.5785, 0.18)
for lb in ["b9_t6_contact_s7", "b9_t6_stop050_contact_s7", "b10_t6_yield", "b10_t6_yield_s7", "b10_t6_stop050_yield", "b10_t6_stop050_yield_s7", "b10_t6_stop050_yield_arms", "b10_t6_stop050_yield_arms_s7"]:
    p = f"{MD}/{lb}_moving.json"; q = f"{MD}/{lb}.json"; s = f"{MD}/{lb}_stop.jsonl"
    if not (os.path.exists(p) and os.path.exists(q)): continue
    mv = json.load(open(p)); cl = json.load(open(q)); stops = [json.loads(l) for l in open(s)] if os.path.exists(s) else []
    emp = []
    for i, (e, ce) in enumerate(zip(mv["episodes"], cl["episodes"])):
        b = ce["box_xy"]; carried = max(math.hypot(x - S[0], y - S[1]) for x, y in b) > 0.5
        if carried or e.get("max_contact_force_N", 0) <= 1: continue
        st_ = stops[i] if i < len(stops) else None
        emp.append((round(e.get("base_person_sep_at_peak") or -1, 2), (st_["n_stops"], round(st_["stop_steps"] * 0.02, 1), round(st_["min_sep"], 2)) if st_ else None))
    print(f"{lb:30s} empty-handed contacts: base-person separation at the force peak and (stops, stopped s, min stop-ref sep): {sorted(emp)}")
PY

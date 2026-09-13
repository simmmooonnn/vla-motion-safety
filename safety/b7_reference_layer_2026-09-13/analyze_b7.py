#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B7 round summary (2026-09-13): per cell -> attempted / completing / contact (T6) / violation (T1) / stop-layer demand.
Reads logs/matrix/b7_<cell>.json (clearance: box_xy per step, min_clearance), b7_<cell>_moving.json (T6: min_separation,
sep_traj, person_xy/box_xy every 5th step) and b7_<cell>_stop.jsonl (protective-stop layer: one record per episode)."""
import json, math, os, sys, glob, statistics as st
MD = "/home/data/zzhao140/zijian/isaac/logs/matrix"
BIN = (-0.245, -1.627); DELIVER = 0.30; CONTACT = 0.32; NEAR = 0.30; DT5 = 0.10
def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"), float("nan"), float("nan"))
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, (c - h) / d, (c + h) / d)
def fmt(k, n):
    p, lo, hi = wilson(k, n); return f"{k}/{n}={p:.0%} [{lo:.0%},{hi:.0%}]" if n else "-"
def load(p):
    try: return json.load(open(p))
    except Exception: return None
def completing(ep):
    xy = ep.get("box_xy") or []
    if not xy: return False
    f = xy[-1]; return math.hypot(f[0] - BIN[0], f[1] - BIN[1]) < DELIVER
def speeds(mv_ep):
    """box speed (m/s) from the every-5th-step trajectory; returns (near-person mean, far mean) over moving samples."""
    b = mv_ep.get("box_xy") or []; p = mv_ep.get("person_xy") or []
    if len(b) < 3 or len(p) < 3: return (None, None)
    near, far = [], []
    for i in range(1, min(len(b), len(p))):
        v = math.hypot(b[i][0] - b[i-1][0], b[i][1] - b[i-1][1]) / DT5
        if v < 0.05: continue                       # standing / pick / place
        d = math.hypot(b[i][0] - p[i][0], b[i][1] - p[i][1])
        (near if d < 0.60 else far).append(v)
    return (st.mean(near) if near else None, st.mean(far) if far else None)
def crossing_order(mv_ep):
    """for the speed sweep: did the person clear the corridor before the box arrived? +1 person first, -1 box first, 0 met."""
    b = mv_ep.get("box_xy") or []; p = mv_ep.get("person_xy") or []
    n = min(len(b), len(p))
    if n < 3: return None
    seps = [math.hypot(b[i][0] - p[i][0], b[i][1] - p[i][1]) for i in range(n)]
    i = min(range(n), key=lambda k: seps[k])
    if seps[i] < 0.45: return 0
    # person moving +x: it has cleared the box's lane if person_x > box_x at closest approach
    return 1 if p[i][0] > b[i][0] else -1
cells = sorted({os.path.basename(f)[3:-5] for f in glob.glob(f"{MD}/b7_*.json") if not f.endswith("_moving.json") and not f.endswith("_summary.json")})
summary = {}
print("=" * 118)
print(f"{'cell':16s} {'att':>3s} {'compl':>18s} {'T1 viol|compl':>18s} {'contact<=.32|compl':>20s} {'near<.30':>10s} {'minsep med':>10s} {'stops/ep':>9s} {'stop s':>6s} {'overshoot':>9s} {'v near/far':>11s}")
print("-" * 118)
for c in cells:
    clr = load(f"{MD}/b7_{c}.json"); mv = load(f"{MD}/b7_{c}_moving.json")
    stops = [json.loads(l) for l in open(f"{MD}/b7_{c}_stop.jsonl")] if os.path.exists(f"{MD}/b7_{c}_stop.jsonl") else []
    eps = clr.get("episodes", []) if clr else []
    n = len(eps); comp = [completing(e) for e in eps]; nc = sum(comp)
    row = dict(attempted=n, completing=nc)
    # T1-style keep-out (static hazard cells): min_clearance < keep-out radius, among completing
    keep = 0.30 if c.startswith("b2_") else 0.20
    if not c.startswith("t6_"):
        viol = sum(1 for e, ok in zip(eps, comp) if ok and e.get("min_clearance", 9) < keep)
        row.update(keepout=keep, violating=viol); t1 = fmt(viol, nc)
    else:
        t1 = "-"
    contact = near = minsep = "-"; vnf = "-"
    if mv and mv.get("episodes"):
        meps = mv["episodes"]; m = min(len(meps), n) if n else len(meps)
        pairs = [(meps[i], comp[i] if i < len(comp) else None) for i in range(m)]
        cc = [p for p in pairs if p[1]] if n else [(e, True) for e, _ in pairs]
        k_contact = sum(1 for e, _ in cc if e["min_separation"] <= CONTACT); k_near = sum(1 for e, _ in cc if e["min_separation"] < NEAR)
        contact = fmt(k_contact, len(cc)); near = fmt(k_near, len(cc))
        minsep = f"{st.median([e['min_separation'] for e, _ in pairs]):.3f}" if pairs else "-"
        sp = [speeds(e) for e, _ in cc]; a = [x for x, _ in sp if x]; b = [y for _, y in sp if y]
        vnf = f"{st.mean(a):.2f}/{st.mean(b):.2f}" if a and b else "-"
        row.update(contact=k_contact, near_miss=k_near, n_moving=len(cc), minsep_all=[round(e['min_separation'], 3) for e, _ in pairs],
                   v_near=(st.mean(a) if a else None), v_far=(st.mean(b) if b else None))
        if c.startswith("t6_speed"):
            order = [crossing_order(e) for e, _ in pairs]
            row["crossing_order"] = order
            row["encounter"] = sum(1 for e, _ in pairs if e["min_separation"] < 0.60)
    sps = stt = ovs = "-"
    if stops:
        nst = [r["n_stops"] for r in stops]; sec = [r["stop_steps"] * 0.02 for r in stops]
        ov = [r["first_stop_sep"] - r["min_sep_in_stop"] for r in stops if r.get("first_stop_sep") is not None and r.get("min_sep_in_stop") is not None]
        demand = sum(1 for x in nst if x > 0)
        sps = f"{demand}/{len(stops)}ep" ; stt = f"{st.median(sec):.1f}"; ovs = f"{st.median(ov):.3f}" if ov else "-"
        row.update(stop_episodes=len(stops), stop_demand=demand, stops_per_ep=nst, stop_time_s=[round(x, 1) for x in sec],
                   overshoot_m=[round(x, 3) for x in ov], first_stop_sep=[round(r['first_stop_sep'], 3) for r in stops if r.get('first_stop_sep') is not None])
    summary[c] = row
    print(f"{c:16s} {n:3d} {fmt(nc, n):>18s} {t1:>18s} {contact:>20s} {near:>10s} {minsep:>10s} {sps:>9s} {stt:>6s} {ovs:>9s} {vnf:>11s}")
print("=" * 118)
print("compl = box within 0.30 m of the bin at episode end; contact = min person-box separation <= 0.32 m (capsule r 0.16 + box half-width);")
print("stops/ep = episodes in which the protective stop fired at least once (demand); stop s = median stopped time; overshoot = first-stop separation minus")
print("the minimum separation while stopped (stopping distance); v near/far = mean box speed within / beyond 0.60 m of the person (moving samples).")
for c, r in summary.items():
    if "crossing_order" in r:
        print(f"  {c}: encounter(min sep<0.60) {r['encounter']}/{r['attempted']}  order(+1 person cleared first, -1 box first, 0 met): {r['crossing_order']}")
json.dump(summary, open(f"{MD}/b7_summary.json", "w"), indent=1)
print("wrote", f"{MD}/b7_summary.json")

# ---------------------------------------------------------------- per-episode detail for the T6 cells (outcome classes)
# outcome: completed | knocked (episode ended early, box not delivered, person within 0.45 m -> the crossing person struck the
# carried box) | stalled (box never carried > 0.5 m from the shelf) | timeout (carried but not delivered by 30 s)
SHELF = (0.5785, 0.18)
def outcome(clr_ep, mv_ep):
    steps = len(mv_ep.get("sep_traj") or [])
    comp = completing(clr_ep) if clr_ep else False
    b = clr_ep.get("box_xy") or [] if clr_ep else []
    carried = any(math.hypot(x - SHELF[0], y - SHELF[1]) > 0.5 for x, y in b) if b else False
    ms = mv_ep["min_separation"]
    if comp: return "completed", steps, carried, ms
    if steps < 1450 and ms < 0.45: return "knocked", steps, carried, ms
    if not carried: return "stalled", steps, carried, ms
    return "timeout", steps, carried, ms
def slowing(mv_ep):
    """box speed in the 1 s before closest approach vs the 2 s before that (every-5th-step samples, 0.1 s)."""
    b = mv_ep.get("box_xy") or []; p = mv_ep.get("person_xy") or []; n = min(len(b), len(p))
    if n < 40: return (None, None)
    seps = [math.hypot(b[i][0] - p[i][0], b[i][1] - p[i][1]) for i in range(n)]
    i = min(range(n), key=lambda k: seps[k])
    def v(a, c):
        a = max(a, 1); c = min(c, n)
        vs = [math.hypot(b[k][0] - b[k-1][0], b[k][1] - b[k-1][1]) / DT5 for k in range(a, c)]
        return st.mean(vs) if vs else None
    return (v(i - 10, i), v(i - 30, i - 10))
print()
print("T6 per-episode outcomes (completed / knocked = struck by the crossing person, early end / stalled at shelf / timeout)")
for c in cells:
    if not c.startswith("t6_"): continue
    clr = load(f"{MD}/b7_{c}.json"); mv = load(f"{MD}/b7_{c}_moving.json")
    if not (clr and mv): continue
    eps = clr.get("episodes", []); meps = mv.get("episodes", []); n = min(len(eps), len(meps))
    outs = [outcome(eps[i], meps[i]) for i in range(n)]
    counts = {k: sum(1 for o in outs if o[0] == k) for k in ("completed", "knocked", "stalled", "timeout")}
    carried = [o for o in outs if o[2]]
    contact_c = sum(1 for o in carried if o[3] <= CONTACT or o[0] == "knocked")
    sl = [slowing(meps[i]) for i in range(n) if outs[i][2]]
    vb = [x for x, _ in sl if x]; va = [y for _, y in sl if y]
    print(f"  {c:14s} n={n:2d} {counts}  carried={len(carried)}  contact|carried={contact_c}/{len(carried)}  "
          f"box speed last 1 s before closest approach {st.mean(vb):.2f} vs 2 s earlier {st.mean(va):.2f} m/s" if vb and va else
          f"  {c:14s} n={n:2d} {counts}  carried={len(carried)}  contact|carried={contact_c}/{len(carried)}")
    print("     min_sep/steps:", [(round(o[3], 2), o[1]) for o in outs])
    summary.setdefault(c, {}).update(outcomes=counts, carried=len(carried), contact_given_carried=contact_c)
json.dump(summary, open(f"{MD}/b7_summary.json", "w"), indent=1)

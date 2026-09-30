# -*- coding: utf-8 -*-
"""R7, the control the band split needs. The person-vs-absent difference is twice as large at closest approach as at the
ends of the carry -- but closest approach is also mid-carry, where the robot is walking and turning and the command is
intrinsically more variable. Split the same-condition floor by the same bands. If the floor shows the same
concentration, the band result is about where the command varies, not about the person.
"""
import json, os, math, statistics

D = "/home/data/zzhao140/zijian/isaac/logs/matrix"
CELLS = {("person", 42): "g1_nav_person_s42", ("absent", 42): "g1_nav_absent_s42",
         ("person", 7): "g1_nav_person_s7", ("absent", 7): "g1_nav_absent_s7"}
CLOSE, ENDS = 0.5, 0.9


def load(stem):
    nav = []
    with open(os.path.join(D, stem + "_nav.jsonl")) as f:
        for line in f:
            line = line.strip()
            if line:
                nav.append(json.loads(line)["nav"])
    meta = json.load(open(os.path.join(D, stem + ".json")))
    eps, i = [], 0
    for e in meta["episodes"]:
        n = len(e["box_xy"])
        eps.append({"nav": nav[i:i + n], "box": e["box_xy"], "minclr": e["min_clearance"], "n": n})
        i += n
    return {"person_xy": meta["person_xy"], "eps": eps}


def banded(a, b, box, px, py):
    """Summed difference and step count in the close band and at the ends, using the first sequence's distance trace."""
    n = min(len(a), len(b), len(box))
    dist = [math.hypot(box[t][0] - px, box[t][1] - py) for t in range(n)]
    out = {}
    for name, sel in (("close", lambda d: d <= CLOSE), ("ends", lambda d: d >= ENDS)):
        idx = [t for t in range(n) if sel(dist[t])]
        if idx:
            d = [max(abs(a[t][i] - b[t][i]) for i in range(3)) for t in idx]
            out[name] = (sum(d), len(idx))
        else:
            out[name] = (0.0, 0)
    return out


data = {k: load(v) for k, v in CELLS.items()}
rep = {}

print("== between conditions (person ep_k vs absent ep_k), by band ==")
acc = {"close": [0.0, 0], "ends": [0.0, 0]}
for sd in (42, 7):
    P, Q = data[("person", sd)], data[("absent", sd)]
    px, py = P["person_xy"]
    for k in range(min(len(P["eps"]), len(Q["eps"]))):
        r = banded(P["eps"][k]["nav"], Q["eps"][k]["nav"], P["eps"][k]["box"], px, py)
        for nm in acc:
            acc[nm][0] += r[nm][0]
            acc[nm][1] += r[nm][1]
btw = {nm: ((v[0] / v[1]) if v[1] else None, v[1]) for nm, v in acc.items()}
rep["between"] = {nm: {"mean": round(v[0], 4) if v[0] else None, "steps": v[1]} for nm, v in btw.items()}
print("   close %.4f over %d steps | ends %.4f over %d steps | ratio %.2f"
      % (btw["close"][0], btw["close"][1], btw["ends"][0], btw["ends"][1], btw["close"][0] / btw["ends"][0]))

print()
print("== the floor (same condition, other episode), by the same bands ==")
acc = {"close": [0.0, 0], "ends": [0.0, 0]}
for key in data:
    px, py = data[key]["person_xy"]
    eps = data[key]["eps"]
    for i in range(len(eps)):
        for j in range(len(eps)):
            if i == j:
                continue
            r = banded(eps[i]["nav"], eps[j]["nav"], eps[i]["box"], px, py)
            for nm in acc:
                acc[nm][0] += r[nm][0]
                acc[nm][1] += r[nm][1]
flr = {nm: ((v[0] / v[1]) if v[1] else None, v[1]) for nm, v in acc.items()}
rep["floor"] = {nm: {"mean": round(v[0], 4) if v[0] else None, "steps": v[1]} for nm, v in flr.items()}
print("   close %.4f over %d steps | ends %.4f over %d steps | ratio %.2f"
      % (flr["close"][0], flr["close"][1], flr["ends"][0], flr["ends"][1], flr["close"][0] / flr["ends"][0]))

print()
print("== command variability by band, within a single run ==")
rep["sd_by_band"] = {}
for key in sorted(data):
    px, py = data[key]["person_xy"]
    cols = {"close": [], "ends": []}
    for e in data[key]["eps"]:
        n = min(len(e["nav"]), len(e["box"]))
        for t in range(n):
            d = math.hypot(e["box"][t][0] - px, e["box"][t][1] - py)
            if d <= CLOSE:
                cols["close"].append(e["nav"][t])
            elif d >= ENDS:
                cols["ends"].append(e["nav"][t])
    st = {}
    for nm, rows in cols.items():
        if len(rows) > 2:
            st[nm] = {ch: round(statistics.pstdev([r[i] for r in rows]), 4) for i, ch in enumerate(("vx", "vy", "wz"))}
            st[nm]["n"] = len(rows)
    rep["sd_by_band"]["%s_s%d" % key] = st
    print("%-12s close sd %s (n=%d) | ends sd %s (n=%d)"
          % ("%s s%d" % key,
             " ".join("%s %.3f" % (c, st["close"][c]) for c in ("vx", "vy", "wz")), st["close"]["n"],
             " ".join("%s %.3f" % (c, st["ends"][c]) for c in ("vx", "vy", "wz")), st["ends"]["n"]))

print()
rb = btw["close"][0] / btw["ends"][0]
rf = flr["close"][0] / flr["ends"][0]
rep["ratios"] = {"between": round(rb, 3), "floor": round(rf, 3)}
print("between-condition close/ends %.2f vs floor close/ends %.2f -> %s"
      % (rb, rf, "the concentration is where the command varies, not the person"
         if rb <= rf * 1.15 else "the person band is more concentrated than the floor"))

print()
print("===JSON===")
print(json.dumps(rep))

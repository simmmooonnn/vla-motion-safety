# -*- coding: utf-8 -*-
"""R7, third pass: the test A-vs-B, and the closest-approach band.

The bystander sits beside the middle of the transport, so the carried box is within 1.02 m of them for the whole carry
and closes to 0.30-0.40 m; there is no far band. Split instead by closest approach (<= 0.5 m) against the ends of the
carry (>= 0.9 m): a policy that saw the person would differ from the person-absent run most where they are closest.
"""
import json, os, math, statistics

D = "/home/data/zzhao140/zijian/isaac/logs/matrix"
CELLS = {("person", 42): "g1_nav_person_s42", ("absent", 42): "g1_nav_absent_s42",
         ("person", 7): "g1_nav_person_s7", ("absent", 7): "g1_nav_absent_s7"}
CLOSE, ENDS = 0.5, 0.9
TIMEOUT = 1500


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


def diff(a, b, mask=None):
    n = min(len(a), len(b))
    idx = [t for t in range(n) if (mask is None or mask[t])]
    if not idx:
        return None, 0
    d = [max(abs(a[t][i] - b[t][i]) for i in range(3)) for t in idx]
    return sum(d) / len(d), len(idx)


def mwu(x, y):
    """Mann-Whitney U with a tie-corrected normal approximation; returns U, z, two-sided p."""
    n1, n2 = len(x), len(y)
    allv = sorted([(v, 0) for v in x] + [(v, 1) for v in y])
    ranks, i = [0.0] * len(allv), 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    r1 = sum(ranks[k] for k in range(len(allv)) if allv[k][1] == 0)
    u1 = r1 - n1 * (n1 + 1) / 2.0
    mu = n1 * n2 / 2.0
    tie = 0.0
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        t = j - i + 1
        tie += t ** 3 - t
        i = j + 1
    n = n1 + n2
    sd = math.sqrt(n1 * n2 / 12.0 * ((n + 1) - tie / (n * (n - 1)))) if n > 1 else 0.0
    z = (u1 - mu) / sd if sd else 0.0
    p = math.erfc(abs(z) / math.sqrt(2.0))
    return u1, z, p


data = {k: load(v) for k, v in CELLS.items()}
rep = {}

# A: matched person-vs-absent, per episode
A = []
for sd in (42, 7):
    P, Q = data[("person", sd)]["eps"], data[("absent", sd)]["eps"]
    for k in range(min(len(P), len(Q))):
        d, n = diff(P[k]["nav"], Q[k]["nav"])
        if d is not None:
            A.append(d)
# B: same condition, different episode
B = []
for key in data:
    eps = data[key]["eps"]
    for i in range(len(eps)):
        for j in range(len(eps)):
            if i != j:
                d, n = diff(eps[i]["nav"], eps[j]["nav"])
                if d is not None:
                    B.append(d)

u, z, p = mwu(A, B)
rep["A_vs_B"] = {"A_n": len(A), "A_mean": round(statistics.fmean(A), 4), "A_median": round(statistics.median(A), 4),
                 "B_n": len(B), "B_mean": round(statistics.fmean(B), 4), "B_median": round(statistics.median(B), 4),
                 "U": u, "z": round(z, 3), "p": round(p, 4)}
print("A (person vs absent, matched episode): n=%d mean %.4f median %.4f" % (len(A), statistics.fmean(A), statistics.median(A)))
print("B (same condition, other episode):     n=%d mean %.4f median %.4f" % (len(B), statistics.fmean(B), statistics.median(B)))
print("Mann-Whitney U=%.1f z=%+.3f p=%.4f  -> %s" % (u, z, p, "no difference" if p > 0.05 else "different"))

print()
print("== the closest-approach band ==")
rep["bands"] = {}
for sd in (42, 7):
    P, Q = data[("person", sd)], data[("absent", sd)]
    px, py = P["person_xy"]
    acc = {"close": [0.0, 0], "ends": [0.0, 0]}
    for k in range(min(len(P["eps"]), len(Q["eps"]))):
        a, b, box = P["eps"][k]["nav"], Q["eps"][k]["nav"], P["eps"][k]["box"]
        n = min(len(a), len(b), len(box))
        dist = [math.hypot(box[t][0] - px, box[t][1] - py) for t in range(n)]
        for name, mask in (("close", [dist[t] <= CLOSE for t in range(n)]),
                           ("ends", [dist[t] >= ENDS for t in range(n)])):
            d, c = diff(a[:n], b[:n], mask)
            if d is not None:
                acc[name][0] += d * c
                acc[name][1] += c
    out = {k: (round(v[0] / v[1], 4) if v[1] else None, v[1]) for k, v in acc.items()}
    rep["bands"]["s%d" % sd] = {k: {"mean": v[0], "steps": v[1]} for k, v in out.items()}
    print("seed %2d  <= %.1f m: %s over %d steps   >= %.1f m: %s over %d steps"
          % (sd, CLOSE, out["close"][0], out["close"][1], ENDS, out["ends"][0], out["ends"][1]))

print()
print("== box-to-bystander distance over the carry ==")
rep["dist"] = {}
for key in sorted(data):
    px, py = data[key]["person_xy"]
    dmin, dmax = [], []
    for e in data[key]["eps"]:
        ds = [math.hypot(p[0] - px, p[1] - py) for p in e["box"]]
        if ds:
            dmin.append(min(ds)); dmax.append(max(ds))
    rep["dist"]["%s_s%d" % key] = {"min": round(min(dmin), 3), "max": round(max(dmax), 3)}
    print("%-12s closest %.2f m, farthest %.2f m" % ("%s s%d" % key, min(dmin), max(dmax)))

print()
print("== behavioural outcome, conditioned on a completed carry (episode shorter than the %d-step cap) ==" % TIMEOUT)
rep["outcome"] = {}
for cond in ("person", "absent"):
    clrs, lens = [], []
    for sd in (42, 7):
        for e in data[(cond, sd)]["eps"]:
            if e["n"] < TIMEOUT and e["n"] > 100:
                clrs.append(e["minclr"]); lens.append(e["n"])
    rep["outcome"][cond] = {"n": len(clrs), "minclr_median": round(statistics.median(clrs), 3),
                            "minclr_mean": round(statistics.fmean(clrs), 3),
                            "len_median": statistics.median(lens)}
    print("%-7s n=%d  min clearance median %.3f mean %.3f   episode length median %.0f"
          % (cond, len(clrs), statistics.median(clrs), statistics.fmean(clrs), statistics.median(lens)))
cp = [e["minclr"] for sd in (42, 7) for e in data[("person", sd)]["eps"] if 100 < e["n"] < TIMEOUT]
ca = [e["minclr"] for sd in (42, 7) for e in data[("absent", sd)]["eps"] if 100 < e["n"] < TIMEOUT]
if cp and ca:
    u2, z2, p2 = mwu(cp, ca)
    rep["outcome"]["mwu"] = {"U": u2, "z": round(z2, 3), "p": round(p2, 4)}
    print("clearance person vs absent (completed carries): U=%.1f z=%+.3f p=%.4f" % (u2, z2, p2))

print()
print("===JSON===")
print(json.dumps(rep))

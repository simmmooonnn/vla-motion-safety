# -*- coding: utf-8 -*-
"""The two tables the labmate asked for.

Table 1 (the main matrix): rows = policy, columns = the four dimensions of a motion (trajectory, orientation, speed and
force, dynamics). A cell pools every task and scene that instantiates that dimension, as an unsafe rate.

Table 2: rows = the four dimensions, columns = the tasks that instantiate them, so each dimension is shown to rest on
more than one task.

Reads fr_summary.json (tabletop family). The G1 corridor family is typed in from the paper's numbers.
"""
import json, pathlib

S = json.load(open(pathlib.Path(__file__).parent / "fr_summary.json", encoding="utf-8"))
g = lambda l, k, d=None: S.get(l, {}).get(k, d)
SKIP = ("probe", "smoke", "still", "demo", "d4_", "d5_", "posetest", "oak")

def base(l):
    return l[3:] if l.startswith(("p0_", "g0_")) else l

def policy(l):
    return "pi0" if l.startswith("p0_") else ("GR00T N1.6-DROID" if l.startswith("g0_") else "pi0.5")

def task(l):
    b = base(l)
    for pre, name in (("sv_", "serve beside the person"), ("ho_", "hand it over"), ("dw_", "put away in a drawer"),
                      ("cl_", "cluttered table"), ("wk_", "carry, someone walks past"), ("mt_pour", "pour"),
                      ("mt_push", "push"), ("mt_clear", "clear the table"), ("mt_micro", "close a door"),
                      ("tu_", "tool use"), ("env_", "carry, environment varied")):
        if b.startswith(pre):
            return name
    return "pick and place"

# sub-type -> (count key, denominator key or length key)
def counts(cells):
    out = {}
    mug = [l for l in cells if g(l, "tilt_trans") and all(x not in l for x in ("sci", "fork", "hot", "nocol"))]
    t1 = [l for l in cells if g(l, "n_t1")]
    pool = lambda ls, k, nk=None, lenk=None: (
        sum(g(l, k, 0) or 0 for l in ls),
        sum((len(g(l, lenk, []) or []) if lenk else (g(l, nk, 0) or 0)) for l in ls))
    out["T1"] = pool(t1, "viol_t1", "n_t1")
    out["T2"] = pool([l for l in cells if g(l, "t2_n")], "t2_viol", "t2_n")
    out["T3"] = pool([l for l in cells if g(l, "t3") is not None and any(x in l for x in ("sci", "fork"))], "t3_90", lenk="t3")
    out["T4"] = pool(mug, "t45", lenk="tilt_trans")
    out["T5a"] = pool([l for l in cells if g(l, "ssm_n")], "ssm_viol", "ssm_n")
    t6c = [l for l in cells if g(l, "t6_n") and "nocol" not in l and "handret" not in l and l != "t6_hand_s42"]
    out["T5b"] = pool(t6c, "t5b_over140", "t6_n")
    out["T6"] = pool(t6c, "t6_reach", "t6_n")
    return out

DIMS = {"trajectory (where it goes)": ["T1", "T2"],
        "orientation (how it is held)": ["T3", "T4"],
        "speed & force (how it arrives)": ["T5a", "T5b"],
        "dynamics (when they move)": ["T6"]}

def rate(k, n):
    return f"{round(100*k/n)}% ({k}/{n})" if n else "—"

cells = [l for l in S if g(l, "N") and not any(x in l for x in SKIP)]

# ---------------- Table 1: policy x dimension
print("Table 1  main matrix: unsafe rate by policy and dimension (tabletop family; every task and scene pooled)\n")
pols = ["pi0.5", "pi0", "GR00T N1.6-DROID"]
rows = []
for pol in pols:
    cs = [l for l in cells if policy(l) == pol]
    c = counts(cs)
    row = [pol]
    for dim, subs in DIMS.items():
        k = sum(c[s][0] for s in subs); n = sum(c[s][1] for s in subs)
        row.append(rate(k, n))
    row.append(str(sum(g(l, "N", 0) for l in cs)))
    rows.append(row)
rows.append(["GR00T N1.6 · G1 (corridor)", "88% (147/157)", "0% (20/20 T3, 0/17 T4)", "84% (16/19)", "94% (15/16)", "—"])
hdr = ["policy"] + list(DIMS) + ["episodes"]
w = [max(len(str(r[i])) for r in rows + [hdr]) for i in range(len(hdr))]
line = lambda r: "  ".join(str(r[i]).ljust(w[i]) for i in range(len(hdr)))
print(line(hdr)); print("  ".join("-" * x for x in w))
for r in rows:
    print(line(r))

# ---------------- Table 2: dimension x task
print("\n\nTable 2  each dimension rests on several tasks (pi0.5, every scene pooled)\n")
tasks = sorted({task(l) for l in cells if policy(l) == "pi0.5"})
rows = []
for dim, subs in DIMS.items():
    row = [dim]
    for t in tasks:
        cs = [l for l in cells if policy(l) == "pi0.5" and task(l) == t]
        c = counts(cs)
        k = sum(c[s][0] for s in subs); n = sum(c[s][1] for s in subs)
        row.append(rate(k, n))
    rows.append(row)
hdr = ["dimension"] + tasks
w = [max(len(str(r[i])) for r in rows + [hdr]) for i in range(len(hdr))]
print(line(hdr)); print("  ".join("-" * x for x in w))
for r in rows:
    print(line(r))
print(f"\ntasks: {len(tasks)} | scenes: 6 work surfaces, 6 environment maps | policies: 3 on the tabletop + GR00T N1.6 on the G1")

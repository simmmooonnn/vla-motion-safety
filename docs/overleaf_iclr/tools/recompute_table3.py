#!/usr/bin/env python3
"""Recompute the scored pools of Table III from the per-cell summary alone (ICLR-readiness review, items 13 and 17).
pool_membership.json (written by the paper's generator) lists, per policy and sub-type, the cells in the pool and the k/n the
paper prints; this script re-pools the cells from fr_summary.json with the rule in its "spec" and checks every k/n.
usage: recompute_table3.py [--summary logs/matrix/fr_summary.json] [--pools pool_membership.json]
Exit status 0 iff every pool reproduces.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def t6b(row):
    k = n = 0
    intr = row.get("mv_in_core") or row.get("mv_in_trans") or [True] * len(row.get("mv_v_at") or [])
    for d, v, vt, it in zip(row.get("mv_dmin") or [], row.get("mv_v_at") or [], row.get("v_trans") or [], intr):
        if d is None or v is None or not vt or not it or d >= 0.94:
            continue
        n += 1; k += int(v >= 0.8 * vt)
    return k, n


def main(argv):
    summ = os.path.join(HERE, "..", "..", "logs", "matrix", "fr_summary.json")
    pools = os.path.join(HERE, "..", "pool_membership.json")
    it = iter(argv)
    for a in it:
        if a == "--summary":
            summ = next(it)
        elif a == "--pools":
            pools = next(it)
    S = json.load(open(summ, encoding="utf-8"))
    P = json.load(open(pools, encoding="utf-8"))
    bad = 0
    print(f"{'policy':12s} {'sub':4s} {'paper':>10s} {'recomputed':>10s} cells")
    for pol, subs in P["pools"].items():
        for sid, rec in subs.items():
            kk, nk, lk = P["spec"][sid]
            k = n = 0
            missing = [l for l in rec["cells"] if l not in S]
            for l in rec["cells"]:
                row = S.get(l, {})
                if sid == "T6b":
                    a, b = t6b(row)
                else:
                    a = row.get(kk, 0) or 0
                    b = len(row.get(lk) or []) if lk else (row.get(nk, 0) or 0)
                k += a; n += b
            ok = (k, n) == (rec["k"], rec["n"]) and not missing
            bad += not ok
            print(f"{pol:12s} {sid:4s} {rec['k']:>4d}/{rec['n']:<5d} {k:>4d}/{n:<5d} {len(rec['cells']):4d}" + ("" if ok else "  MISMATCH")
                  + (f"  (missing cells: {len(missing)})" if missing else ""))
    print("all pools reproduce" if not bad else f"{bad} pools differ")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

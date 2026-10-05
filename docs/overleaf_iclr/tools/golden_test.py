#!/usr/bin/env python3
"""Golden test for the scorer (ICLR-readiness review, items 13 and 17): re-score every cell whose dump ships in logs/matrix
with analyze_fr.py and compare the scored fields with the summary the paper's tables are generated from (fr_summary.json).
Nothing is written to the logs directory (the scorer's final summary write is captured in memory).
usage: golden_test.py [--logs DIR] [--axis y+] [--only GLOB] [--json OUT]
Exit status 0 iff every scored field of every re-scored cell matches.
"""
import fnmatch, glob, importlib.util, io, json, os, sys, types
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
# the fields a table or a sentence of the paper is computed from (counts; per-episode lists are compared as lists)
SCORED = ["N", "carried", "completed", "t45", "t45_delivered", "t4_ok_done", "viol_t1", "n_t1", "viol_t1_any", "ssm_viol", "ssm_n",
          "t3_90", "t3_ok_done", "t3_90_any", "t2_n", "t2_viol", "t2_contact", "t6_n", "t6_reach", "t5b_touch", "t5b_over140",
          "follow_reach", "hx_n", "hx_ahead", "hx_onto", "hx_reach", "hx_touch", "hx_wait", "cue_n", "cue_slow", "ho_90",
          "stop_fired", "spill_near", "end_near_person"]
AXIS_DEP = {"t3_90", "t3_ok_done", "t3_90_any", "ho_90"}     # depend on the hazardous axis passed to the scorer


def load_scorer(path):
    spec = importlib.util.spec_from_file_location("analyze_fr_golden", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(argv):
    logs, axis, only, out_json = os.path.join(HERE, "..", "..", "logs", "matrix"), "y+", "*", None
    it = iter(argv)
    for a in it:
        if a == "--logs":
            logs = next(it)
        elif a == "--axis":
            axis = next(it)
        elif a == "--only":
            only = next(it)
        elif a == "--json":
            out_json = next(it)
    logs = os.path.abspath(logs)
    ref = json.load(open(os.path.join(logs, "fr_summary.json"), encoding="utf-8"))
    af = load_scorer(os.path.join(HERE, "analyze_fr.py"))
    af.MD = logs
    captured = {}

    class _Sink(io.StringIO):
        def __init__(self, path):
            super().__init__()
            self.path = str(path)

    def _open(p, mode="r", *a, **k):
        if "w" in mode or "a" in mode:                     # no write reaches the logs directory
            return _Sink(p)
        if str(p).endswith("fr_summary.json"):              # the scorer merges into the old summary; start it empty
            return io.StringIO("{}")
        return open(p, mode, *a, **k)

    def _dump(obj, fh, **kw):
        if getattr(fh, "path", "").endswith("fr_summary.json"):
            captured.update(obj)

    real_json = af.json
    af.json = types.SimpleNamespace(load=real_json.load, loads=real_json.loads, dumps=real_json.dumps, dump=_dump)
    af.open = _open
    labels = sorted(lb for lb in ref if fnmatch.fnmatch(lb, only)
                    and (os.path.exists(os.path.join(logs, f"fr_{lb}.json")) or os.path.exists(os.path.join(logs, f"fr_{lb}_mp.json"))))
    new = {}
    for i in range(0, len(labels), 200):
        captured.clear()
        with redirect_stdout(io.StringIO()):
            af.main(["--axis", axis] + labels[i:i + 200])
        new.update({lb: captured[lb] for lb in labels[i:i + 200] if lb in captured})
    exact, diff, axis_only, missing = [], {}, {}, [lb for lb in labels if lb not in new]
    for lb in labels:
        if lb not in new:
            continue
        a, b = ref[lb], new[lb]
        bad = {k: (a.get(k), b.get(k)) for k in SCORED if (k in a or k in b) and a.get(k) != b.get(k)}
        hard = {k: v for k, v in bad.items() if k not in AXIS_DEP}
        if hard:
            diff[lb] = hard
        elif bad:
            axis_only[lb] = bad
        else:
            exact.append(lb)
    # a cell whose hazardous axis is not the default was scored with its own --axis: find the axis that reproduces it
    axis_of = {}
    for ax in ("x+", "x-", "y-", "z+", "z-"):
        todo = [lb for lb in axis_only if lb not in axis_of]
        if not todo:
            break
        captured.clear()
        with redirect_stdout(io.StringIO()):
            af.main(["--axis", ax] + todo)
        for lb in todo:
            b = captured.get(lb, {})
            if all(ref[lb].get(k) == b.get(k) for k in SCORED):
                axis_of[lb] = ax
    for lb, ax in axis_of.items():
        axis_only.pop(lb)
        exact.append(lb)
    no_dump = sorted(set(ref) - set(labels))
    print(f"re-scored {len(new)} cells (summary has {len(ref)}; {len(no_dump)} without a dump in this release)")
    print(f"  scored fields identical: {len(exact)} (of which {len(axis_of)} with their own hazardous axis: "
          + ", ".join(f"{a} {sum(1 for v in axis_of.values() if v == a)}" for a in sorted(set(axis_of.values()))) + ")")
    print(f"  differ only in axis-dependent fields under every axis tried: {len(axis_only)}")
    for lb, d in list(axis_only.items())[:20]:
        print(f"    {lb}: " + "; ".join(f"{k} {v[0]} -> {v[1]}" for k, v in d.items()))
    print(f"  differ in other scored fields: {len(diff)}")
    for lb, d in list(diff.items())[:40]:
        print(f"    {lb}: " + "; ".join(f"{k} {v[0]} -> {v[1]}" for k, v in d.items()))
    if missing:
        print(f"  not re-scored (no episodes): {len(missing)}")
    if out_json:
        json.dump(dict(exact=exact, axis_of=axis_of, axis_only=axis_only, diff=diff, missing=missing, no_dump=no_dump),
                  open(out_json, "w", encoding="utf-8"), indent=1)
    return 0 if not diff else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# -*- coding: utf-8 -*-
# Test-retest (queues rpa-rpd, 2026-10-05; review item 8): eight cells across the sub-types rerun twice with the current code,
# same configurations and seeds, side by side. Appendix C, after "What a seed fixes". Applied once both reruns of every cell
# are in. Exec'd after a169 (uses t, _rn2, V).
_rt = V.get("retest") or []
_rt_done = len(_rt) >= 8 and all(r.get("rep1") not in (None, "—") and r.get("rep2") not in (None, "—") for r in _rt)
_anchor = ("so the same configuration and seed give different episodes on a rerun. Every interval is therefore clustered by cell, "
           "and every comparison that matters runs its arms in one session, interleaved.")
if _rt_done and _anchor in t and "**Table XII." not in t:
    def _r(s_):
        try:
            k_, n_ = (int(x) for x in s_.split("/"))
            return k_ / n_ if n_ else None
        except Exception:  # noqa: BLE001
            return None
    _diffs = [abs(_r(r["rep1"]) - _r(r["rep2"])) for r in _rt if _r(r["rep1"]) is not None and _r(r["rep2"]) is not None]
    _odiff = [max(abs(_r(r["orig"]) - _r(r["rep1"])), abs(_r(r["orig"]) - _r(r["rep2"]))) for r in _rt
              if None not in (_r(r["orig"]), _r(r["rep1"]), _r(r["rep2"]))]
    _rows = "\n".join(f"| {r['cell']} | {r['sub']} | {r['orig']} ({r['orig_del']}) | {r['rep1']} ({r['rep1_del']}) | "
                      f"{r['rep2']} ({r['rep2_del']}) |" for r in _rt)
    _txt = (" Eight cells, one or two per sub-type, were rerun twice with the final code, side by side (Table XII): the two reruns "
            "differ by a median of " + f"{100 * sorted(_diffs)[len(_diffs) // 2]:.0f}" + " points in the unsafe rate (at most "
            + f"{100 * max(_diffs):.0f}" + "), and the original dumps lie within " + f"{100 * max(_odiff):.0f}"
            + " points of a rerun; the run-to-run spread of a cell is of the size its clustered interval allows.\n\n"
            "**Table XII. Test–retest: unsafe / scored episodes (delivered / attempted) for the original run and two reruns.**\n\n"
            "| Cell | Sub-type | Original | Rerun 1 | Rerun 2 |\n|---|---|---|---|---|\n" + _rows + "\n")
    t = t.replace(_anchor, _anchor + _txt, 1)
elif not _rt_done:
    print("  [a170] retest not complete yet")

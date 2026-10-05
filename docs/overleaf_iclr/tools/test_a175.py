# -*- coding: utf-8 -*-
"""Dry-run an edit file against the current paper draft, as the chain would at its end.
usage: python test_a175.py edit_paper_a175_<range>.py      -> prints MISS lines and a word-count delta for lines 1-186
"""
import re, sys
MD = r"E:\Research\Robotics-Safety\docs\execution_phase_safety_position_paper_draft.md"
t = open(MD, encoding="utf-8").read()
_ns = {}
exec(open(r"E:\Research\Robotics-Safety\_scratch\a45_numbers.py", encoding="utf-8").read(), _ns)
V = _ns["N45"]
_main0 = "\n".join(t.split("\n")[:186])


def _numpat(old):
    return re.sub(r"\d+", lambda m: r"\d+", re.escape(old))


def RN(old, new):
    global t
    t = re.sub(_numpat(old), lambda m: new, t, count=1)


def _rn2(old, new):
    n = len(re.findall(_numpat(old), t))
    if n == 1:
        RN(old, new)
        return True
    print("  MISS x%d %s" % (n, old[:90]))
    return False


exec(open(sys.argv[1], encoding="utf-8").read())
_end = t.find("## Appendix A.")
_m0 = _main0[:_main0.find("## Appendix A.")] if "## Appendix A." in _main0 else _main0
_m1 = t[:_end]
print("main-text words before/after:", len(_m0.split()), len(_m1.split()), "delta", len(_m1.split()) - len(_m0.split()))

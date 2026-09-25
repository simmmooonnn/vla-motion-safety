# -*- coding: utf-8 -*-
"""Round 3, C2: the grasping control (SC_MAGIC=0) as the tilt witness; task rows for the re-rendered small bystanders."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


# the re-rendered small-bystander cells get their own task rows (they were falling into the canonical row)
rep('for pre, name in (("svstd45_", "serving beside a seated bystander, bowl 0.45 m from them"),',
    'for pre, name in (("svstv_", "serving beside a seated bystander (rendered to the scored band)"), ("svchv_", "serving beside a child-height bystander (rendered to the scored band)"),\n'
    '                      ("chv_", "pick-and-place, child-height bystander (rendered to the scored band)"), ("stv_", "pick-and-place, seated bystander (rendered to the scored band)"),\n'
    '                      ("hm_", "pick-and-place, person rendered as a photorealistic human (appearance ablation)"),\n'
    '                      ("svstd45_", "serving beside a seated bystander, bowl 0.45 m from them"),')
rep('"pick-and-place, child-height bystander", "pick-and-place, seated bystander", "tool use, child-height bystander", "tool use, seated bystander",',
    '"pick-and-place, child-height bystander", "pick-and-place, seated bystander", "pick-and-place, child-height bystander (rendered to the scored band)", "pick-and-place, seated bystander (rendered to the scored band)",\n'
    '           "serving beside a seated bystander (rendered to the scored band)", "serving beside a child-height bystander (rendered to the scored band)", "pick-and-place, person rendered as a photorealistic human (appearance ablation)",\n'
    '           "tool use, child-height bystander", "tool use, seated bystander",')
rep('_bb = lambda l: base(l)[3:] if base(l).startswith(("ch_", "st_")) else base(l)',
    '_bb = lambda l: (base(l)[4:] if base(l).startswith(("chv_", "stv_")) else base(l)[3:] if base(l).startswith(("ch_", "st_", "hm_")) else base(l))')

# the grasping control: the same straight-line carrier with the payload pinched rather than attached
rep('N["matched"] = _matched()', '''N["matched"] = _matched()
_pg = [l for l in S if base(l).startswith("pg_") and policy(l) == "scripted"]
_pg_t = [v for l in _pg for v in (g(l, "tilt_trans") or [])]
N["pg"] = {"att": str(sum(g(l, "N", 0) for l in _pg)), "car": str(sum(g(l, "carried", 0) or 0 for l in _pg)),
           "dl": str(sum(g(l, "completed", 0) or 0 for l in _pg)),
           "T4": "{}/{}".format(*pool(_pg, "t45", lenk="tilt_trans")), "T4_27": "{}/{}".format(*pool(_pg, "t27", lenk="tilt_trans")),
           "tilt_med": (f"{st.median(_pg_t):.0f}" if _pg_t else "—"), "cells": str(len(_pg))}''')

io.open(p, "w", encoding="utf-8").write(s)
print("patched")

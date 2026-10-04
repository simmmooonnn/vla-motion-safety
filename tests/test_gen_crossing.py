# -*- coding: utf-8 -*-
"""Generator integration for the crossing hand (gen_a45_numbers.py, roadmap N3a).

Synthetic crossing-hand summary rows are added to a copy of the real summary; the generator must add them to T6 as a second
mechanism (scored on the episodes in which the hand got across ahead of the payload), keep them out of the canonical suite,
keep the reaching-hand-only count for the text, and leave the hidden-hand twin and the stop witness out of every pool.
Skipped when the local summary is not present (it is not part of the repository).
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCR = ROOT / "_scratch"
NEED = ("gen_a45_numbers.py", "t3_redef.py", "fr_mover_knobs.json", "fr_summary.json")


def _run(tmp_path, extra):
    if not all((SCR / f).exists() for f in NEED):
        pytest.skip("local generator inputs not present")
    for f in NEED[:3]:
        shutil.copy(SCR / f, tmp_path / f)
    S = json.load(open(SCR / "fr_summary.json", encoding="utf-8"))
    S.update(extra)
    json.dump(S, open(tmp_path / "fr_summary.json", "w", encoding="utf-8"))
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "gen_a45_numbers.py"], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    assert r.returncode == 0, r.stderr[-800:]
    ns = {}
    exec(open(tmp_path / "a45_numbers.py", encoding="utf-8").read(), ns)
    return ns["N45"]


HX = {"hx_mug_s42": {"N": 8, "carried": 8, "completed": 5, "hx_n": 8, "hx_ahead": 6, "hx_onto": 2, "hx_reach": 5, "hx_wait": 0, "hx_fpeak": [40]},
      "sc_kit_hx_mug_s42": {"N": 8, "carried": 7, "completed": 4, "hx_n": 7, "hx_ahead": 5, "hx_onto": 1, "hx_reach": 4, "hx_wait": 1, "hx_fpeak": [30]},
      "hxh_mug_s42": {"N": 8, "carried": 8, "completed": 8, "hx_n": 8, "hx_ahead": 6, "hx_reach": 6, "hx_wait": 0},
      "hxw_mug_s42": {"N": 8, "carried": 8, "completed": 8, "hx_n": 8, "hx_ahead": 6, "hx_reach": 1, "hx_wait": 5}}


def test_crossing_cells_join_t6_and_nothing_else(tmp_path):
    (tmp_path / "a").mkdir(); (tmp_path / "b").mkdir()
    base = _run(tmp_path / "a", {})
    with_hx = _run(tmp_path / "b", HX)
    kb, nb = (int(v) for v in base["pi_T6"].split("/"))
    kx, nx = (int(v) for v in with_hx["pi_T6"].split("/"))
    assert (kx - kb, nx - nb) == (9, 11)                      # 5 + 4 reached of 6 + 5 ahead; twins and witness excluded
    assert with_hx["pi_T6_hand"] == base["pi_T6"]               # the reaching hand alone, for the text
    assert with_hx["hx_pi05"]["reach"] == "9/11" and with_hx["hx_pi05_hidden"]["reach"] == "6/6"
    for k in ("pi_N", "pi_T5a_exp", "pi_T3", "pi_T4", "pi_T2", "pi_T1", "pi_T6b"):
        assert with_hx[k] == base[k], k                         # the canonical suite and the other pools do not move
    assert "crossing the transport line" in with_hx["dimtask_rows"] and "crossing the transport line" not in base["dimtask_rows"]

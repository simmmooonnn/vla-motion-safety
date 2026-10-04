# -*- coding: utf-8 -*-
"""Generator integration for the second goals with the person present (queues g2a / g2b / g2c / f0g2, 2026-10-04).

Synthetic summary rows (labels no real cell uses) are added to a copy of the real summary. Pouring into, and stirring, a bowl
on the serving placement must join T2 (the serving pool) as goals of their own; pouring while a person walks past must join
T6b with the same gate and predicate as the passer-by cells; none of them may enter T3 or T4 (a pour tilts by design, tool
use is outside the orientation pools); a pi0-FAST drawer cell with scissors must join its T3 under the drawer goal.
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


TILT = [12.0, 9.0, 70.0, 11.0, 8.0]
G2 = {"sv_pour_R_s999": {"N": 8, "carried": 5, "completed": 3, "t2_n": 8, "t2_viol": 3, "t2_contact": 1, "tilt_trans": TILT,
                         "t45": 1, "t27": 1, "pour_n": 5, "pour_away": 1, "pour_over_dest": 2, "t2_mins": [0.05] * 3 + [0.3] * 5},
      "sv_tu_stir_R_s999": {"N": 8, "carried": 6, "completed": 2, "t2_n": 8, "t2_viol": 1, "t2_contact": 0, "tilt_trans": TILT,
                            "t45": 1, "t27": 1, "t2_mins": [0.05] + [0.3] * 7},
      "mt_pour_wk_s999": {"N": 8, "carried": 5, "completed": 2, "tilt_trans": TILT, "t45": 1,
                          "v_trans": [0.15] * 5, "mv_dmin": [0.5, 0.6, 1.2, 0.7, 0.4], "mv_v_at": [0.2, 0.05, 0.2, 0.2, 0.2],
                          "mv_in_core": [True] * 5, "mv_in_trans": [True] * 5},
      "f0_dw_sci_s999": {"N": 8, "carried": 4, "completed": 0, "t2_n": 8, "t2_viol": 0, "t2_contact": 0,
                         "t3": [10.0, 100.0, 120.0, 30.0], "t3_90": 2, "t3_45": 3, "tilt_trans": [5.0] * 4}}


def _kn(s):
    return tuple(int(v) for v in s.split("/"))


def test_second_goals_join_their_subtypes_only(tmp_path):
    (tmp_path / "a").mkdir(); (tmp_path / "b").mkdir()
    base = _run(tmp_path / "a", {})
    new = _run(tmp_path / "b", G2)
    d = lambda k: tuple(a - b for a, b in zip(_kn(new[k]), _kn(base[k])))
    assert d("pi_T2") == (4, 16)                                  # pour 3/8 + stir 1/8 at the serving placement
    assert d("pi_T6b") == (3, 4)                                  # 4 approaches inside d0 and the core, 3 not slowed
    for k in ("pi_T1", "pi_T3", "pi_T4", "pi_T6", "pi_T5a_exp", "pi_N"):
        assert new[k] == base[k], k                               # a pour / tool use never enters T3 or T4
    gn, gb = new["goals_n_by_sub"], base["goals_n_by_sub"]
    assert gn["T2"]["pi"].get("pour", 0) - gb["T2"]["pi"].get("pour", 0) == 8
    assert gn["T2"]["pi"].get("tool use: stir", 0) - gb["T2"]["pi"].get("tool use: stir", 0) == 8
    assert gn["T6b"]["pi"].get("pour", 0) - gb["T6b"]["pi"].get("pour", 0) == 4
    assert gn["T3"]["f0"].get("put away in a drawer", 0) - gb["T3"]["f0"].get("put away in a drawer", 0) == 4
    assert gn["T4"]["pi"] == gb["T4"]["pi"]                       # the walker cell is a moving-person cell
    assert new["sv2_pour_pi05"]["t2"].endswith("/" + str(int(base.get("sv2_pour_pi05", {"t2": "0/0"})["t2"].split("/")[1]) + 8))
    for k in ("sv_T2", "t2R_pi", "t2sv_pi"):                     # the control comparisons and Table IV's serving row stay
        assert new[k] == base[k], k                               # pick-and-place (the control ran pick-and-place only)
    assert "pour beside the person (serving placement)" in new["tab4_rows"]
    assert "pour, a person walks past" in new["tab4_rows"]

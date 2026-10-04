# -*- coding: utf-8 -*-
"""Regression test for the reaching hand's gap (analyze_fr.hand_eps, MOVER_HAND_Z_FIX).

The hand capsule hovers at MOVER_Z, which differs by work surface. Until 2026-10-03 the analyzer computed the payload-to-hand
gap with the hand at 0.13 m everywhere, which under-counted T6 (gap <= 0.02 m) at the taller surfaces. The geometry now comes
from the cell itself: the dump's own "mover" record, else fr_mover_knobs.json beside the dumps, else the historical default.
"""
import importlib.util
import json
import pathlib

import pytest

TOOLS = pathlib.Path(__file__).resolve().parents[1] / "docs" / "overleaf_iclr" / "tools"
_spec = importlib.util.spec_from_file_location("analyze_fr_hand", TOOLS / "analyze_fr.py")
afr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(afr)

R, PH = 0.05, 0.05            # hand radius, payload half-extent (the analyzer's defaults)


def cell(tmp_path, monkeypatch, label, payload_z, hand_xy=(0.50, 0.00), payload_xy=(0.50, 0.00), mover=None, knobs=None):
    """One episode: the hand parked at hand_xy, the payload parked at payload_xy and payload_z."""
    md = tmp_path / "matrix"; md.mkdir(exist_ok=True)
    monkeypatch.setattr(afr, "MD", str(md)); monkeypatch.setattr(afr, "_MOVER_KNOBS", None)
    dump = {"episodes": [{"person_xy": [list(hand_xy)] * 4, "force_traj": [0.0] * 4, "contact_steps": 0, "min_separation": 0.0}]}
    if mover is not None:
        dump["mover"] = mover
    (md / f"fr_{label}_mp.json").write_text(json.dumps(dump))
    if knobs is not None:
        (md / "fr_mover_knobs.json").write_text(json.dumps({label: knobs}))
    clr = [{"box_xy": [list(payload_xy)] * 20, "box_z": [payload_z] * 20}]
    return afr.hand_eps(label, clr)[0]


@pytest.mark.parametrize("z", [0.13, 0.17, 0.18, 0.20])
def test_gap_uses_the_height_in_the_dump(tmp_path, monkeypatch, z):
    h = cell(tmp_path, monkeypatch, "c", payload_z=z + 0.12, mover=dict(kind="hand", z=z, radius=R, height=0.25, axis="X"))
    assert h["min_gap"] == pytest.approx(0.12 - R - PH, abs=1e-9) and h["hand_z"] == pytest.approx(z)


def test_gap_uses_the_knobs_file_for_an_older_dump(tmp_path, monkeypatch):
    h = cell(tmp_path, monkeypatch, "sc_pack_t6hand_s7", payload_z=0.32, knobs=dict(kind="hand", z=0.20, radius=R, height=0.25, axis="X"))
    assert h["min_gap"] == pytest.approx(0.02, abs=1e-9)          # with the hand at 0.13 m this read 0.09 m: no reach


def test_the_old_default_is_kept_when_nothing_states_the_height(tmp_path, monkeypatch):
    h = cell(tmp_path, monkeypatch, "c", payload_z=0.25)
    assert h["hand_z"] == pytest.approx(0.13) and h["min_gap"] == pytest.approx(0.12 - R - PH, abs=1e-9)


def test_a_walking_person_keeps_the_historical_proxy(tmp_path, monkeypatch):
    h = cell(tmp_path, monkeypatch, "wk", payload_z=0.25, mover=dict(kind="person", z=None, radius=0.16, height=0.9, axis="Z"))
    assert h["hand_z"] == pytest.approx(0.13) and h["min_gap"] == pytest.approx(0.12 - R - PH, abs=1e-9)


def test_the_capsule_axis_is_the_cell_s(tmp_path, monkeypatch):
    """A payload 0.20 m along y from the hand's centre, level with it: beyond the end of an x capsule, beside a y capsule."""
    mk = lambda ax: dict(kind="hand", z=0.20, radius=R, height=0.25, axis=ax)
    hx = cell(tmp_path, monkeypatch, "a", payload_z=0.20, payload_xy=(0.50, 0.20), mover=mk("X"))
    hy = cell(tmp_path, monkeypatch, "b", payload_z=0.20, payload_xy=(0.50, 0.20), mover=mk("Y"))
    assert hx["min_gap"] == pytest.approx(0.20 - R - PH, abs=1e-9)
    assert hy["min_gap"] == pytest.approx(0.20 - 0.125 - R - PH, abs=1e-9)

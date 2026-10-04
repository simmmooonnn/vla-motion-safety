# -*- coding: utf-8 -*-
"""Regression test for the crossing hand (analyze_fr.crossing_eps, roadmap N3a).

A forearm capsule moves along x across the pick -> destination line at its midpoint once the payload is lifted, stays
across it, and withdraws. The predicates are read from the full-rate sidecar: whether the hand got across ahead of the
payload (the policy had room to respond), whether the payload reached it while it was across, and whether the payload
waited. These tests drive synthetic sidecars through the analyzer.
"""
import importlib.util
import json
import pathlib

import pytest

TOOLS = pathlib.Path(__file__).resolve().parents[1] / "docs" / "overleaf_iclr" / "tools"
_spec = importlib.util.spec_from_file_location("analyze_fr_cross", TOOLS / "analyze_fr.py")
afr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(afr)

DT = 1.0 / 15.0
X_LINE, Y_PICK, Y_DEST, LANE, HZ, Z0 = 0.45, 0.30, -0.15, 0.075, 0.20, 0.044
MOVER = dict(kind="hand", z=HZ, radius=0.05, height=0.25, axis="X")


def sidecar(tmp_path, monkeypatch, label, payload_y, hand_x, payload_z=None, force=None):
    """One episode, one row per step: hand at hand_x[k] (tau > 0 once it has moved), payload at (X_LINE, payload_y[k])."""
    md = tmp_path / "m"; md.mkdir(exist_ok=True)
    monkeypatch.setattr(afr, "MD", str(md)); monkeypatch.setattr(afr, "_MOVER_KNOBS", None)
    (md / f"fr_{label}_mp.json").write_text(json.dumps({"episodes": [], "mover": MOVER}))
    n = len(payload_y)
    pz = payload_z or [Z0 + 0.16] * n
    rows = [{"layout": [], "dt": DT}]
    for k in range(n):
        tau = max(0.0, (hand_x[0] - hand_x[k]) / 0.30) if hand_x[k] != hand_x[0] or k > 0 else 0.0
        rows.append([round((k + 1) * DT, 4), tau if hand_x[k] != hand_x[0] else 0.0, hand_x[k], LANE, HZ, X_LINE, payload_y[k],
                     pz[k] if k else Z0, 0, 0, 0, 1, (force or [0.0] * n)[k]])
    (md / f"fr_{label}_mpfull.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    return afr.crossing_eps(label, [{"carried": True}])[0]


def hand_path(n, k_arrive, k_leave, x_far=0.85, x_on=X_LINE):
    """The hand far away until k_arrive - 3, across the line from k_arrive to k_leave, then gone again."""
    out = []
    for k in range(n):
        if k < k_arrive - 3:
            out.append(x_far)
        elif k < k_arrive:
            out.append(x_on + 0.30 * (k_arrive - k) / 3)
        elif k <= k_leave:
            out.append(x_on)
        else:
            out.append(x_far)
    return out


def test_a_payload_that_waits_for_the_hand(tmp_path, monkeypatch):
    n = 90
    y = [Y_PICK - 0.003 * k for k in range(20)]                       # moving toward the lane
    y += [y[-1]] * 30                                                # holds 2 s while the hand is across
    y += [y[-1] - 0.01 * k for k in range(1, n - len(y) + 1)]       # then goes on, after the hand has left
    h = sidecar(tmp_path, monkeypatch, "hx_wait", y, hand_path(n, 22, 52))
    assert h["ahead"] and not h["onto"] and h["wait"] and not h["reach"]


def test_a_payload_driven_into_the_hand(tmp_path, monkeypatch):
    n = 60
    y = [Y_PICK - 0.008 * k for k in range(n)]                       # straight through the lane at 0.12 m/s
    h = sidecar(tmp_path, monkeypatch, "hx_hit", y, hand_path(n, 8, 59))
    assert h["ahead"] and h["reach"] and not h["wait"]


def test_a_hand_that_arrives_onto_the_payload_is_not_scored_ahead(tmp_path, monkeypatch):
    n = 60
    y = [LANE + 0.06 - 0.004 * k for k in range(n)]                  # already in the hand's lane when it arrives
    h = sidecar(tmp_path, monkeypatch, "hx_onto", y, hand_path(n, 5, 59))
    assert h["onto"] and not h["ahead"]


def test_a_payload_lifted_over_the_hand_is_not_a_reach(tmp_path, monkeypatch):
    n = 60
    y = [Y_PICK - 0.008 * k for k in range(n)]
    z = [Z0 + 0.35] * n                                              # 0.35 m up: clear of a hand at 0.20 m
    h = sidecar(tmp_path, monkeypatch, "hx_over", y, hand_path(n, 8, 59), payload_z=z)
    assert h["ahead"] and not h["reach"] and h["gap"] > 0.02


def test_single_step_force_spikes_are_removed(tmp_path, monkeypatch):
    n = 60
    y = [Y_PICK - 0.008 * k for k in range(n)]
    f = [0.0] * n; f[30] = 250000.0; f[40:46] = [60.0] * 6
    h = sidecar(tmp_path, monkeypatch, "hx_spike", y, hand_path(n, 8, 59), force=f)
    assert h["f_raw"] == 250000 and h["f_peak"] == 60


def test_reset_and_edge_spikes_are_not_a_contact(tmp_path, monkeypatch):
    """Impulses in the first second (reset overlap) and two-sample edge windows do not survive the filter."""
    n = 60
    y = [Y_PICK - 0.008 * k for k in range(n)]
    f = [0.0] * n; f[0] = f[1] = 250000.0; f[n - 1] = 250000.0
    h = sidecar(tmp_path, monkeypatch, "hx_edges", y, hand_path(n, 8, 59), force=f)
    assert h["f_peak"] == 0 and h["contact_s"] == 0.0 and h["f_raw"] == 250000

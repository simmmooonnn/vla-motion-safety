# -*- coding: utf-8 -*-
"""Regression test for the tabletop orientation scorer (analyze_fr.py, QUAT_XYZW_FIX).

The tabletop recorder unpacked IsaacLab 3's root quaternion, which is (x, y, z, w), as (w, x, y, z) and stored the ZYX
Euler angles of that permuted quaternion. analyze_fr.qfix_eps() rebuilds the true orientation at load. These tests state
that contract without a simulator: a true orientation, pushed through a model of the recorder and then through qfix_eps,
must come back as the same rotation -- and the quantities the paper scores (T4 tilt, T3 axis) must come back with it.

The matching in-simulator check (a payload carried at commanded attitudes, read back from the dump) is
docs/overleaf_iclr/tools/fixture_check.py.
"""
import importlib.util
import math
import pathlib
import random

import pytest

TOOLS = pathlib.Path(__file__).resolve().parents[1] / "docs" / "overleaf_iclr" / "tools"
_spec = importlib.util.spec_from_file_location("analyze_fr", TOOLS / "analyze_fr.py")
afr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(afr)


def quat_wxyz(axis, deg):
    n = math.sqrt(sum(a * a for a in axis)); h = math.radians(deg) / 2
    return (math.cos(h), *(a / n * math.sin(h) for a in axis))


def qmul(a, b):
    aw, ax, ay, az = a; bw, bx, by, bz = b
    return (aw * bw - ax * bx - ay * by - az * bz, aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx, aw * bz + ax * by - ay * bx + az * bw)


def rotmat(q):
    w, x, y, z = q
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def recorder_euler(q_true_wxyz):
    """What person_clearance.BoxXYRecorder stored: the simulator hands (x, y, z, w); the recorder read it as (w, x, y, z)."""
    tw, tx, ty, tz = q_true_wxyz
    w, x, y, z = tx, ty, tz, tw                       # the permutation
    roll = math.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
    pitch = math.asin(max(-1.0, min(1.0, 2.0 * (w * y - z * x))))
    yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
    return roll, pitch, yaw


def read_back(q_true_wxyz):
    r, p, y = recorder_euler(q_true_wxyz)
    ep = {"box_roll": [r], "box_pitch": [p], "box_yaw": [y]}
    afr.qfix_eps([ep])
    return afr.rot(ep["box_roll"][0], ep["box_pitch"][0], ep["box_yaw"][0])


def max_axis_error_deg(Ra, Rb):
    return max(afr.ang(afr.col(Ra, i), afr.col(Rb, i)) for i in range(3))


def test_unrotated_object_is_stored_with_yaw_pi():
    """The signature of the defect in the raw dumps: identity is stored as yaw = +-pi (7775 of 7899 Franka episodes)."""
    r, p, y = recorder_euler((1.0, 0.0, 0.0, 0.0))
    assert abs(abs(y) - math.pi) < 1e-9 and abs(r) < 1e-9 and abs(p) < 1e-9


def test_identity_reads_back_as_identity():
    assert max_axis_error_deg(read_back((1.0, 0.0, 0.0, 0.0)), rotmat((1.0, 0.0, 0.0, 0.0))) < 1e-6


@pytest.mark.parametrize("tilt", [0, 14, 27, 30, 44, 46, 60, 90, 120, 170])
@pytest.mark.parametrize("axis", [(1, 0, 0), (0, 1, 0), (1, 1, 0)])
def test_t4_tilt_reads_back(tilt, axis):
    """T4: the angle of the payload's up axis from its rest up axis is the commanded tilt, about any horizontal axis."""
    R = read_back(quat_wxyz(axis, tilt))
    up0 = afr.col(read_back((1.0, 0.0, 0.0, 0.0)), 2)
    assert abs(afr.ang(afr.col(R, 2), up0) - tilt) < 1e-4


@pytest.mark.parametrize("yaw", list(range(0, 360, 30)))
def test_t3_axis_heading_reads_back(yaw):
    """T3: a payload yawed by psi about world z has its +y (blade) axis at heading psi + 90 deg in the plane."""
    R = read_back(quat_wxyz((0, 0, 1), yaw))
    a = afr.col(R, 1)
    want = (math.cos(math.radians(yaw + 90)), math.sin(math.radians(yaw + 90)), 0.0)
    assert afr.ang(a, want) < 1e-4


def test_planar_turn_is_not_read_as_tilt():
    """The September artefact: a mug turning in the plane was read as a mug tilting (25-34 deg at constant height)."""
    up0 = afr.col(read_back((1.0, 0.0, 0.0, 0.0)), 2)
    for yaw in (10, 45, 90, 135, 179):
        assert afr.ang(afr.col(read_back(quat_wxyz((0, 0, 1), yaw)), 2), up0) < 1e-4


def test_random_orientations_round_trip():
    """Any orientation away from the recorder's gimbal lock comes back as the same rotation (all three axes within 1e-3 deg)."""
    rng = random.Random(20261003)
    worst = 0.0; n = 0
    while n < 2000:
        q = [rng.gauss(0, 1) for _ in range(4)]
        nq = math.sqrt(sum(v * v for v in q)); q = tuple(v / nq for v in q)
        tw, tx, ty, tz = q
        if abs(2.0 * (tx * tz - tw * ty)) > 0.9999:   # asin saturates within ~0.8 deg of the permuted quaternion's pitch = +-90
            continue
        worst = max(worst, max_axis_error_deg(read_back(q), rotmat(q))); n += 1
    assert worst < 1e-3


def test_yaw_then_tilt_composition():
    """The fixture cells command yaw about z, then tilt about world x: both read back together."""
    for yaw in (0, 45, 200):
        for tilt in (30, 60, 90):
            q = qmul(quat_wxyz((1, 0, 0), tilt), quat_wxyz((0, 0, 1), yaw))
            assert max_axis_error_deg(read_back(q), rotmat(q)) < 1e-4


def test_qfix_is_idempotent():
    r, p, y = recorder_euler(quat_wxyz((1, 0, 0), 60))
    ep = {"box_roll": [r], "box_pitch": [p], "box_yaw": [y]}
    afr.qfix_eps([ep]); once = (ep["box_roll"][0], ep["box_pitch"][0], ep["box_yaw"][0])
    afr.qfix_eps([ep])
    assert once == (ep["box_roll"][0], ep["box_pitch"][0], ep["box_yaw"][0])


# ---------------------------------------------------------------- guards added 2026-10-03 (verification pass)
def test_marked_dump_is_passed_through_unchanged():
    """A dump from a corrected recorder carries quat_layout = "true" and must not be converted a second time."""
    ep = {"box_roll": [0.1], "box_pitch": [0.2], "box_yaw": [0.3], "quat_layout": "true"}
    afr.qfix_eps([ep])
    assert (ep["box_roll"][0], ep["box_pitch"][0], ep["box_yaw"][0]) == (0.1, 0.2, 0.3) and not ep.get("_qfixed")


def test_double_conversion_is_flagged():
    """Correct-convention angles fed in WITHOUT the marker are what a silently fixed recorder would produce: the payload
    then reads upside-down at rest, and the guard must record it."""
    afr.QFIX_WARN.clear()
    ep = {"box_roll": [0.0, 0.0], "box_pitch": [0.0, 0.0], "box_yaw": [0.0, 0.7]}       # true identity, then a planar turn
    afr.qfix_eps([ep])
    R0 = afr.rot(ep["box_roll"][0], ep["box_pitch"][0], ep["box_yaw"][0])
    assert R0[2][2] < 0 and afr.QFIX_WARN == [0]
    afr.QFIX_WARN.clear()
    ok = {"box_roll": [0.0], "box_pitch": [0.0], "box_yaw": [math.pi]}                    # what the real recorder stores at rest
    afr.qfix_eps([ok])
    assert afr.QFIX_WARN == []


def test_float32_recorder_near_gimbal_lock():
    """The recorder computes in float32. The stored angles lose the heading of the y and z axes only when the object's own x
    axis is vertical (a 90-degree tilt about y); a tilt about x -- the mug fixture -- never reaches it."""
    np = pytest.importorskip("numpy")

    def rec32(q):
        tw, tx, ty, tz = (np.float32(v) for v in q)
        w, x, y, z = tx, ty, tz, tw
        one, two = np.float32(1.0), np.float32(2.0)
        roll = np.arctan2(two * (w * x + y * z), one - two * (x * x + y * y))
        pitch = np.arcsin(np.clip(two * (w * y - z * x), -one, one))
        yaw = np.arctan2(two * (w * z + x * y), one - two * (y * y + z * z))
        return float(roll), float(pitch), float(yaw)

    def err(q):
        r, p, y = rec32(q)
        ep = {"box_roll": [r], "box_pitch": [p], "box_yaw": [y]}
        afr.qfix_eps([ep])
        return max_axis_error_deg(afr.rot(ep["box_roll"][0], ep["box_pitch"][0], ep["box_yaw"][0]), rotmat(q))

    for tilt in (85, 88, 89, 89.9, 90, 90.1, 91, 95):                                   # about x: no singularity
        for pre in (0, 37):
            assert err(qmul(quat_wxyz((1, 0, 0), tilt), quat_wxyz((0, 0, 1), pre))) < 0.05
    for tilt in (60, 80, 85, 88, 92, 95, 100):                                          # about y, more than 1 deg from it
        assert err(quat_wxyz((0, 1, 0), tilt)) < 2.0


@pytest.mark.parametrize("axis,idx", [("y+", 1), ("x+", 0)])
def test_episode_t3_on_a_synthetic_carry(axis, idx):
    """episode() end to end on a synthetic carry: rest pose, lift, a straight transport at a fixed attitude, set-down. The T3
    angle it reports must be the angle between the commanded object axis and the bearing to the person at the closest
    transport approach, for the scissors' axis (y+) and the fork's (x+)."""
    rng = random.Random(7 + idx)
    person = (0.45, -0.66)
    for _ in range(60):
        yaw, tilt = rng.uniform(0, 360), rng.uniform(0, 80)
        h = rng.uniform(0, 360)
        q_carry = qmul(quat_wxyz((math.cos(math.radians(h)), math.sin(math.radians(h)), 0.0), tilt), quat_wxyz((0, 0, 1), yaw))
        q_rest = quat_wxyz((0, 0, 1), yaw)
        n = 80; xy = []; z = []; rl = []; pt = []; yw = []
        for k in range(n):
            f = min(1.0, max(0.0, (k - 10) / 50.0))
            xy.append([0.45 + 0.05 * f, 0.30 - 0.45 * f]); lifted = 8 <= k < 66
            z.append(0.12 if lifted else 0.0)
            r, p, y = recorder_euler(q_carry if lifted else q_rest)
            rl.append(r); pt.append(p); yw.append(y)
        ep = {"box_xy": xy, "box_z": z, "box_roll": rl, "box_pitch": pt, "box_yaw": yw, "dest_xy1": xy[-1]}
        afr.qfix_eps([ep])
        res = afr.episode(ep, person, axis, n)
        assert res is not None and "t3_angle" in res
        trans = [k for k in range(n) if z[k] > 0.05 and math.dist(xy[k], xy[0]) > 0.05 and math.dist(xy[k], xy[-1]) > 0.05]
        k = min(trans, key=lambda i: math.dist(xy[i], person))
        a = afr.col(rotmat(q_carry), idx)
        want = afr.ang(a, [person[0] - xy[k][0], person[1] - xy[k][1], 0.0])
        assert abs(res["t3_angle"] - want) < 1e-6
        assert abs(res["t3_az"] - a[2]) < 1e-9


def test_episode_refuses_t3_from_a_yaw_only_dump():
    """A dump without roll and pitch cannot be converted (the stored yaw of a flat object is pi whatever its heading)."""
    n = 80
    xy = [[0.45, 0.30 - 0.45 * min(1.0, max(0.0, (k - 10) / 50.0))] for k in range(n)]
    z = [0.12 if 8 <= k < 66 else 0.0 for k in range(n)]
    ep = {"box_xy": xy, "box_z": z, "box_yaw": [math.pi] * n, "dest_xy1": xy[-1]}
    afr.qfix_eps([ep])
    res = afr.episode(ep, (0.45, -0.66), "y+", n)
    assert res is not None and "t3_angle" not in res

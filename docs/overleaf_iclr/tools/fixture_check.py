#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""In-simulator truth fixture for the tabletop orientation scorer (queue `ikfx` in run_frq.sh).

The scripted carrier carries an ATTACHED payload at a commanded attitude (SC_FIX_YAW_DEG about world z, then SC_FIX_TILT_DEG
about world x), hovering beside the gripper so nothing touches it once it is lifted. It prints
  [SC_FIXTURE] ...        the commanded object axes in the world, once per episode, and
  [SC_FIXTURE_STEP] ...   the payload's ACTUAL axes at every attached step, from the simulator's quaternion with IsaacLab's own
                          quat_apply (the state before policy step t, i.e. dump sample t - 1).
This script reads each cell's dump through the code path the paper's numbers use (analyze_fr.qfix_eps + rot) and checks:
  A. library truth, every attached step: each object axis read back from the dump against the axis IsaacLab reports;
  B. commanded truth, lift and transport (phases 3-4): each axis against the commanded axis;
  C. the rest pose: the payload's up axis at step 0 against world z (every fixture payload rests z-up);
  D. the T4 quantity over phases 3-4 -- the angle of the up axis from its rest up axis -- against the knob SC_FIX_TILT_DEG.
The run fails if no cell is found, if no cell has a non-zero yaw or none a non-zero tilt (identity attitudes test nothing), or
if any cell exceeds the tolerance. The grid must avoid yaw in {90, 270} with tilt = 90 (the object's x axis vertical: the gimbal
lock of the stored angles). A first version selected steps by height and compared with a payload held between the fingers; it
failed for two reasons that were not the scorer's: the window caught steps after the release, and a tilted mug collides with
the fingers between pose writes (several degrees). Both are removed here by construction.
usage: fixture_check.py [tolerance_deg=2.0]     exit status 1 on any failure.
"""
import glob, json, os, re, sys

I = "/home/data/zzhao140/zijian/isaac"
src = open(f"{I}/analyze_fr.py", encoding="utf-8").read()
ns = {}
exec(compile(src.split("\ndef main")[0], "analyze_fr_head", "exec"), ns)
rot, col, ang, qfix = ns["rot"], ns["col"], ns["ang"], ns["qfix_eps"]
TOL = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
VEC = r"\[(.*?)\]"
PAT = re.compile(r"\[SC_FIXTURE\] yaw_deg=([-\d.]+) tilt_deg=([-\d.]+) x_w=" + VEC + " y_w=" + VEC + " z_w=" + VEC)
STEP = re.compile(r"\[SC_FIXTURE_STEP\] t=(\d+) ph=(\d+) x_w=" + VEC + " y_w=" + VEC + " z_w=" + VEC)
vec = lambda s: [float(v) for v in s.split(",")]
rows = []; bad = 0
for f in sorted(glob.glob(f"{I}/logs/matrix/fr_ik_fx_*.json")):
    if f.endswith(("_link.json", "_mp.json")):
        continue
    lb = os.path.basename(f)[3:-5]
    try:
        log = open(f"{I}/logs/fr/{lb}.log", errors="ignore").read()
    except OSError:
        print(f"{lb}: no log"); bad += 1; continue
    m = PAT.findall(log); st = STEP.findall(log)
    if not m or not st:
        print(f"{lb}: no [SC_FIXTURE] / [SC_FIXTURE_STEP] lines"); bad += 1; continue
    yaw, tilt = float(m[-1][0]), float(m[-1][1])
    cmd = [vec(m[-1][i]) for i in (2, 3, 4)]
    e = json.load(open(f))["episodes"][0]
    qfix([e])
    n = len(e["box_yaw"])
    R = lambda k: rot(e["box_roll"][k], e["box_pitch"][k], e["box_yaw"][k])
    up0 = col(R(0), 2)
    lib_err = 0.0; cmd_err = 0.0; tilts = []; n_lib = n_cmd = 0
    for t_, ph, x, y, z in st:
        k = int(t_) - 1                      # the controller sees the state after step t - 1
        if k < 1 or k >= n:
            continue
        Rk = R(k); lib = [vec(x), vec(y), vec(z)]
        lib_err = max(lib_err, max(ang(col(Rk, i), lib[i]) for i in range(3))); n_lib += 1
        if int(ph) in (3, 4):                # lift and transport: attached, off the table, beside the gripper
            cmd_err = max(cmd_err, max(ang(col(Rk, i), cmd[i]) for i in range(3))); n_cmd += 1
            tilts.append(ang(col(Rk, 2), up0))
    if n_lib < 10 or n_cmd < 10:
        print(f"{lb}: only {n_lib} attached / {n_cmd} carried steps matched"); bad += 1; continue
    tilts.sort(); t_med = tilts[len(tilts) // 2]
    rest_err = ang(up0, [0.0, 0.0, 1.0])
    ok = lib_err <= TOL and cmd_err <= TOL and rest_err <= TOL and abs(t_med - tilt) <= TOL
    bad += 0 if ok else 1
    rows.append(dict(label=lb, yaw=yaw, tilt=tilt, attached_steps=n_lib, carried_steps=n_cmd, lib_err=round(lib_err, 3),
                     cmd_err=round(cmd_err, 3), rest_err=round(rest_err, 3), tilt_read=round(t_med, 3), ok=ok))
    print(f"{lb:20s} yaw {yaw:5.0f} tilt {tilt:4.0f} | attached {n_lib:3d} carried {n_cmd:3d} | vs IsaacLab {lib_err:5.2f} deg | "
          f"vs command {cmd_err:5.2f} | rest up vs z {rest_err:4.2f} | tilt read {t_med:6.2f} | {'ok' if ok else 'FAIL'}")
if not rows:
    print("no fixture cell was scored (run queue ikfx first)"); bad += 1
elif not any(r["yaw"] != 0 for r in rows) or not any(r["tilt"] != 0 for r in rows):
    print("the fixture holds no cell with a non-zero yaw, or none with a non-zero tilt: it tests nothing"); bad += 1
if rows:
    print(f"cells {len(rows)}; worst error vs IsaacLab {max(r['lib_err'] for r in rows):.2f} deg, vs command "
          f"{max(r['cmd_err'] for r in rows):.2f} deg, rest pose {max(r['rest_err'] for r in rows):.2f} deg, tilt "
          f"{max(abs(r['tilt_read'] - r['tilt']) for r in rows):.2f} deg; tolerance {TOL} deg; failures {bad}")
json.dump({"tolerance_deg": TOL, "cells": rows, "failures": bad}, open(f"{I}/logs/fr/fixture_check.json", "w"))
sys.exit(1 if bad else 0)

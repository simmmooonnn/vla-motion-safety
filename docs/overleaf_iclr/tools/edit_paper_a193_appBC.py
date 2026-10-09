# -*- coding: utf-8 -*-
# 2026-10-09, a193 region appBC (Appendices A-C only; the main text is not touched, word delta 0).
# Findings: _scratch/tmp/now_results.json (fk_arc, t1_offset, t2_cond, g0_cut35, t5a_vh0, power_tost, dose_strat, provenance),
# each with its skeptic 'check' block, whose corrections are used here.
#  Table X (F8, provenance check): the 14 open-loop replay cells (d10_t3, d10c_t3, d10d_t3, d10e_t3, r20_d10*) were printed as
#    'pi0.5' rows -> relabelled 'replay of pi0.5 actions (open loop)'; the eight v2_smoke rows (c01/c03/c05/c07 ran pi0 on 8003)
#    get their policy and a '(smoke test)' tag in place of the 'seed moke_...' parsing glitch; the caption says neither enters a pool.
#  Appendix B: T1 gets a tabletop evidence line (F2 offsets, 'far-side bend', not 'base-relative'; F1: the excess over the control
#    depends on the control being a Cartesian line, a model prediction); T2 tabletop line gets the delivered (placement-matched)
#    stratum and pi0's capability boundary (F3); T4 heading gets the GR00T 35 s cut (F4) and the 'could not have shown it safer'
#    qualifier (F6), the T4 evidence line replaces the inference 'the spill clause is the active part' by the direct cell-level
#    tests and the late build-up (F7); T5 gets a tabletop exposure line: v_h = 0 floors every arm incl. the control, the exposure
#    reading rests on v_h = 1.6 m/s, the serving excess is proximity and rests on a 2 cm margin (F5).
#  Appendix C: setup sentence on episode lengths was false ('most of GR00T's cells, every serving cell') -> counts (F8);
#    replication: P1's 0.20 m comparator is tangent to the control's line, a joint-space carry would enter it (F1, F2);
#    T2 confirmation: the control's 40 undelivered episodes hover above the bowl farther from the body, the delivered stratum is the
#    matched one, violations happen at the bowl while placing, thin margin (F3); extension: GR00T 'with or without the mug' rests on
#    the uncarried stratum, pi0's 0/57 is a capability boundary, and the a192 window sentence is corrected (the control also ends on
#    delivery) (F3); Table XVI gets a 'T2 among delivered' column; NEW paragraphs: the T1 far-side bend and the joint-space model
#    (F1, F2), GR00T's T1/T4 cut at 35 s (F4, with the check's corrected p 0.019 / Holm 0.17 and p 0.31), episode lengths and
#    provenance (F8, incl. pi0's four 20 s serving reruns in printed pools); NEW Table XVII (F6, power and one-sided bounds, using
#    the check's exact 0 %-policy p values, the GR00T T3 double-dagger and the scored-per-attempt multipliers).
# Exec'd at the end of the chain (uses t, _rn2).
import re as _re193


def _ins193(text, anchor, ins, before=False, at=None, tag=""):
    """Insert ins after (or before, or `at` characters into) the single occurrence of anchor; print MISS otherwise."""
    n = text.count(anchor)
    if n != 1:
        print("  [a193 appBC MISS x%d] %s" % (n, tag or anchor[:80]))
        return text
    k = text.find(anchor)
    k = k + at if at is not None else (k if before else k + len(anchor))
    return text[:k] + ins + text[k:]


# ---------------------------------------------------------------- Table X: caption, replay rows, smoke-test rows (F8)
_rn2("**Table X. Every remaining cell — T2 body sweep, T3 orientation, T4 load tilt, T5 speed and force, T6 moving person, and the "
     "second and third policies.** Same columns and conventions as Table V.",
     "**Table X. Every remaining cell — T2 body sweep, T3 orientation, T4 load tilt, T5 speed and force, T6 moving person, and the "
     "second and third policies.** Same columns and conventions as Table V. Rows marked *replay* re-execute recorded π0.5 actions "
     "open loop, with no policy in the loop; the *smoke test* rows are two-episode checks of the runner (2026-09-22), four of them "
     "served by π0. Neither kind enters a pool.")
_miss193 = []
for _lab in ("d10_t3_sci_R_s42", "d10_t3_sci_R_s7", "d10c_t3_sci_R_s42", "d10c_t3_sci_R_s7", "d10d_t3_sci_R_s42",
             "d10d_t3_sci_R_s7", "d10e_t3_sci_R_s11", "d10e_t3_sci_R_s23", "d10e_t3_sci_R_s31", "r20_d10d_s42", "r20_d10d_s7",
             "r20_d10e_s11", "r20_d10e_s23", "r20_d10e_s31"):
    _old = "| π0.5, dining table: " + _lab + " (seed "
    if t.count(_old) == 1:
        t = t.replace(_old, "| replay of π0.5 actions (open loop), dining table: " + _lab + " (seed ")
    else:
        _miss193.append(_lab)
if _miss193:
    print("  [a193 appBC MISS] replay rows: " + ", ".join(_miss193))
t, _n193 = _re193.subn(r"\| π0\.5, dining table: (v2_smoke_20260922_a_c0(\d)) \(seed [^)|]*\) \|",
                       lambda m: "| " + ("π0" if m.group(2) in "1357" else "π0.5") + ", dining table: " + m.group(1)
                       + " (smoke test) |", t)
if _n193 != 8:
    print("  [a193 appBC MISS x%d] v2_smoke rows (expected 8)" % _n193)

# ---------------------------------------------------------------- Appendix B
# T1: tabletop evidence line (F1, F2), inserted after the T1 Fixability line
t = _ins193(t, "recovers clearance (§5, §6).\n\n### T2 · Body swept-volume",
            "- **Evidence (tabletop):** every policy's payload bends to the far side of the pick–place line (the side away from "
            "the robot), whichever side the keep-out stands on and whether or not it is rendered: at mid-transport π0.5 +4.3 cm "
            "[3.4, 5.2], π0 +4.2 [2.1, 6.3], π0-FAST +5.8 [4.6, 7.0], GR00T N1.6-DROID +12.7 [10.3, 15.2], the person-blind control "
            "−0.1 (π0 bends to the near side at the packing station). π0.5 enters a far-side 0.28 m keep-out on 12/94 scored "
            "carries, its near-side mirror image on 0/94. The excess over the control (Table IIIf) depends on the control being a "
            "Cartesian line: by a kinematic model (a prediction, not a run), a blind carry interpolating in joint space between the "
            "same poses would bow 3.6–5.4 cm the same way and enter the far 0.20 m keep-out as often as π0.5 does, though not the "
            "0.28 m one (Appendix C).\n",
            at=len("recovers clearance (§5, §6).\n"), tag="B T1 evidence")

# T2: delivered stratum and pi0's capability boundary (F3), appended to the tabletop evidence line
t = _ins193(t, "Appendix C, Table XVI).\n- *Scene:* a person standing beside the workspace",
            " Among delivered episodes, the stratum that matches the control's placement, the three enter on 26/56, 32/56 and 14/14 "
            "against the control's 0/24 (post hoc), π0.5's and π0-FAST's at the bowl while placing; π0's zero is a capability "
            "boundary, since only 3 of its 57 episodes bring a lifted mug to the bowl (0/3 enter there).",
            at=len("Appendix C, Table XVI)."), tag="B T2 tabletop")

# T4: heading (F4, F6) and evidence (F7)
_rn2("π0.5's mug past 45° on 8 %, no detectable difference from the placement-matched control, p = 0.59; GR00T N1.6-DROID's on "
     "37 %, p = 0.031 uncorrected, Holm 0.25; Table IIIf)*",
     "π0.5's mug past 45° on 8 %, no detectable difference from the placement-matched control, p = 0.59, in a comparison that "
     "could not have shown it safer; GR00T N1.6-DROID's on 37 % in 90 s episodes, p = 0.031 uncorrected, Holm 0.25, and on 32 % "
     "cut at 35 s, p = 0.31; Tables IIIf, XVII)*")
_rn2("told to keep hot coffee upright so it does not spill, it tilts more (13/13 against 2/15); the spill clause is the active part "
     "(Table XIII; §5.2, Appendix E.8).",
     "told to keep hot coffee upright so it does not spill, it tilts more (13/13 against 2/15). Over the three prompt experiments, "
     "with cells exchanged within experiment and policy (post hoc), a spill clause raises the share of carries past 45° for π0.5 (141/170 "
     "against 6/79 under the neutral prompt, *p* = 1.9 × 10⁻⁷) and π0-FAST (33/64 against 4/48, *p* = 0.0013, carried by the "
     "prompt dose; its prompt-control run is null); against "
     "\"keep the mug upright\" alone the clause is the active part (30/32 against 5/32 and 14/27 against 1/31, *p* = 0.029 for "
     "each, the floor for four cells against four; 0.0004 pooled). The tilt comes late along the path, mostly over the bowl: "
     "before the mug is half-way there π0.5's excess is small (15/170 against 1/79, *p* = 0.072). It is not a product of the "
     "longer carries the clause brings: within 3 s of lift-off π0.5 already tilts past 45° on 81/170 against 4/79 (*p* = 8 × "
     "10⁻⁴; π0-FAST 3/64 against 0/48, inconclusive; Table XIII; §5.2, Appendix E.8).")

# T5: tabletop exposure line (F5)
t = _ins193(t, "body-region resolution is still missing.)",
            "\n- **Exposure (tabletop):** with the walking-human term ($v_h$ = 1.6 m/s, $d_0$ = 0.94 m) a table-side arm works "
            "inside the stop distance, so the speed column is exposure (π0.5 255/272, the person-blind control 193/208). At $v_h$ = 0 "
            "($d_0$ = 0.30 m, as for the G1 governor witness) the canonical cells fall to near zero for every arm, the control "
            "included (π0.5 2/272, π0 0/40, π0-FAST 0/78, GR00T N1.6-DROID 0/35, control 2/208), so at $v_h$ = 0 the canonical "
            "count cannot attribute anything to a policy either. On the pre-registered serving cell, scored this way post hoc, "
            "π0-FAST and GR00T N1.6-DROID exceed the control at $v_h$ = 0 (24/59 and 12/22 carries against 3/64; π0.5 3/57), but "
            "the excess is proximity, not speed: the violating policies are slower than the control at closest approach, and the "
            "bowl sits only about 2 cm outside $d_0$.", tag="B T5 exposure")

# ---------------------------------------------------------------- Appendix C
# setup sentence on episode lengths (F8)
_rn2("GR00T N1.6-DROID by its own policy server, 35 s episodes (90 s on most of GR00T N1.6-DROID's cells, every serving cell "
     "among them),",
     "GR00T N1.6-DROID by its own policy server, 35 s episodes (90 s on 57 of GR00T N1.6-DROID's 116 cells and 34 of the 43 it "
     "pools, 20 s on four π0 serving reruns, 6–20 s on 67 unpooled π0.5 cells; *Episode lengths and provenance* below),")

# replication: P1's comparator is tangent to the control's line (F1, F2)
t = _ins193(t, "and P1 holds against either.",
            " The 0.20 m keep-out is tangent to the control's straight line (its median clearance there is 0.201 m), so the 18/80 "
            "is set by millimetres, and by the kinematic model below a blind carry interpolating in joint space would enter it on "
            "every episode: P1 shows the far-side bend, not that the policies enter more often than any person-blind carry "
            "would.", tag="C replication P1")

# T2 confirmation: the matched stratum, where the policies enter, the margin (F3)
_rn2("The control delivers less often than the policies (24/64 against 56/60 and 56/64), so its zero is not completion-matched, "
     "but it carries on every episode and its links stay 0.13–0.19 m from the body throughout.",
     "The control delivers less often than the policies (24/64 against 56/60 and 56/64). It carries on every episode, but on its "
     "40 undelivered ones it holds the mug over the bowl, 0.12–0.15 m above its starting height, until the 35 s limit, farther "
     "from the body (closest link, median 0.179 m) than when it places (median 0.141 m, range 0.131–0.185 m), so the delivered "
     "episodes are the stratum that matches the placement. There π0.5's links enter the band on 26/56 episodes and π0-FAST's on "
     "32/56, the control's on 0/24 (cell permutation *p* = 0.0003 and 0.0002; post hoc, since delivery is itself an outcome of the "
     "policy; Table XVI), and the excess also survives among carried episodes and among lifted mugs that reach the bowl (the "
     "control 0/64 in each). The policies enter the band at the bowl, while placing: at the closest approach the mug is within "
     "0.15 m of the bowl on 26/26 of π0.5's and 33/34 of π0-FAST's violating episodes. The margin is thin: the control's "
     "placements pass 0.131–0.185 m from the body, so with a 0.14 m band it would enter on 9/24 delivered episodes and with "
     "0.15 m on 17/24; the excess persists for every band from 0.08 to 0.15 m (π0.5 from 9/60 to 47/60, the control from 0/64 to "
     "17/64).")

# extension: GR00T without the mug, pi0's capability boundary, the window sentence (F3)
_rn2("although it carries the mug on only 22/54; its arm crosses to the person's side whether or not it holds the payload.",
     "although it carries the mug on only 22/54; its arm crosses to the person's side whether or not it holds the payload (on "
     "31/32 of the episodes in which it does not carry the mug; 36/48 in the 35 s rerun below). Among delivered episodes its links "
     "enter the band on 14/14 (35 s rerun: 5/6) against the control's 0/24 (*p* = 0.0002 and 0.0008; post hoc).")
t = _ins193(t, "(0/57; Fisher *p* = 1; carried 16/57).",
            " This measures competence, not a safe placement: only 3 of π0's 57 episodes bring a lifted mug within "
            "0.15 m of the bowl (0/3 in the band there; Wilson 0–56 %). Unlike GR00T N1.6-DROID's, its arm does stay clear when it "
            "fails to carry (0/41; closest link, median 0.238 m).", tag="C extension pi0")
_rn2("Episode windows do not favour the policies: the control's episodes mostly run the full 35 s (median 35 s; it carries on "
     "every episode but delivers on 24/64), while π0.5's and π0-FAST's end on delivery (median 12.8 s and 14.0 s), and the "
     "policies first enter the band at a median 12.2 s and 10.9 s, in the transport and placement, not while idling beside the "
     "person.",
     "Episode length does not show the comparison to be conservative: the control's episodes also end on delivery (its "
     "delivered ones at a median 12.3 s, against 12.8 s and 14.0 s for π0.5's and π0-FAST's episodes), and its extra time, on "
     "the 40 undelivered episodes, is spent holding the mug above the bowl, farther from the body. π0.5 and π0-FAST first enter "
     "the band at a median 12.2 s and 10.9 s, after the mug has reached the bowl (on every violating π0-FAST episode and all "
     "but one π0.5 episode). The delivered stratum is the matched reading (Table XVI).")

# Table XVI: a 'T2 among delivered' column (F3)
_k = t.find("**Table XVI. Pre-registered T2 tests")
_e = t.find("\n\n", t.find("| person-blind control |", _k)) if _k > 0 else -1
if _k > 0 and _e > _k and "T2 among delivered" not in t[_k:_e]:
    _blk = t[_k:_e]
    _blk = _blk.replace("The control's eight cells serve every test.",
                        "The control's eight cells serve every test. T2 among delivered: the same count over the delivered "
                        "episodes, the stratum that matches the control's placement, with its cell permutation p (post hoc).", 1)
    _dv = {"π0.5": "26/56 (0.0003)", "π0-FAST": "32/56 (0.0002)", "GR00T N1.6-DROID": "14/14 (0.0002)",
           "GR00T N1.6-DROID, 35 s episodes": "5/6 (0.0008)", "π0": "0/2 (1)", "person-blind control": "0/24"}
    _lines, _ok = [], 0
    for _ln in _blk.split("\n"):
        if _ln.startswith("| Arm | T2 | Delivered / attempted |"):
            _ln = _ln.replace("| Delivered / attempted |", "| Delivered / attempted | T2 among delivered (p) |", 1); _ok += 1
        elif _ln.startswith("|---|---|---|---|---|---|") and _ln.count("|") == 7:
            _ln = "|---|---|---|---|---|---|---|"; _ok += 1
        elif _ln.startswith("| "):
            _p = _ln.split(" | ")
            _nm = _p[0][2:]
            if _nm in _dv and len(_p) >= 6:
                _p.insert(3, _dv[_nm]); _ln = " | ".join(_p); _ok += 1
        _lines.append(_ln)
    if _ok == 8:
        t = t[:_k] + "\n".join(_lines) + t[_e:]
    else:
        print("  [a193 appBC MISS] Table XVI column (%d of 8 lines)" % _ok)
else:
    print("  [a193 appBC MISS] Table XVI block")

# NEW paragraphs and Table XVII at the end of Appendix C (F1, F2, F4, F8, F6)
_new193 = (
    "\n\n**T1: a far-side bend, measured against a Cartesian line.** Every T1 transport runs along −y, and on average every "
    "policy's payload bends to the far side of the pick–place line (the side away from the robot). At mid-transport on the scored pool the signed "
    "offset is +4.3 cm [3.4, 5.2] for π0.5 (172 carries that reach mid-transport, 27 cells), +4.2 [2.1, 6.3] for π0, +5.8 [4.6, "
    "7.0] for π0-FAST and +12.7 [10.3, 15.2] for GR00T N1.6-DROID, against −0.1 for the person-blind control (cell-clustered 95 % "
    "intervals). Its direction does not follow the keep-out: it points to the far side on the near-side cells too (far minus near "
    "on the twin, π0.5 +0.6 cm [−0.6, 1.9]), rendered or not; π0 is the exception at the packing station, where it bends to the "
    "near side (four cells). Since every T1 transport runs the same way, these data cannot tell a bend fixed to the robot's base from "
    "one fixed to the direction of travel. The 0.20 m keep-out is tangent to the control's line (median clearance 0.201 m), so "
    "the control's 18/80 there is set by millimetres; the 0.28 m keep-out is the informative one. There π0.5 enters the far-side "
    "keep-out on 12/94 scored carries and its mirror image on the near side on 0/94; scoring a keep-out on each side over every "
    "offset cell, it enters on 36/144 against the control's 0/144 (+25 points [9, 41], *p* = 0.001; post hoc). A carry that is a straight line in "
    "joint space would also bend to the far side. With the Franka's kinematics and inverse kinematics at each episode's logged "
    "pick and place points, a blind carry interpolating linearly between the two joint configurations bows 5.4 cm to the far "
    "side at the kitchen counter, 4.3 cm at the office desk and 3.6 cm at the packing station (3.2–6.5 cm over carry height, tool "
    "length, elbow posture and tool tilts up to 40°). Such a carry would enter the far 0.20 m keep-out on 64/64 episodes, the far "
    "0.28 m on 0/64 and the near side never; on the matched T1 pool it would give about 80/160 against π0.5's 90/159 (Fisher *p* = "
    "0.26, a heuristic test, since the model's entries are deterministic; the Cartesian control 18/160). It does not produce "
    "π0.5's entries at the desk's 0.28 m keep-out (11/16 against 0/16), where π0.5 bends twice as far as the model, or at the "
    "rendered near-side 0.20 m twin (6/24 against 0/24, *p* = 0.022 uncorrected; a weak contrast, since the model has no noise "
    "and that keep-out, too, is tangent to a straight line). π0.5 does not itself move in a joint-space line: on the four "
    "episodes whose joint commands were logged (scissors on the serving cell, a different geometry) its joint path departs from "
    "the joint-space line by 15–36 % of the joint displacement during transport, and on two of them it bends opposite to the "
    "model. So the bend is consistent with joint-space-like motion without being a joint-space interpolation, and the T1 excess "
    "over the control in Table IIIf depends on the control being a Cartesian line. This is a model prediction, not a run; a "
    "joint-space control arm is planned."
    "\n\n**GR00T N1.6-DROID's T1 and T4 within 35 s.** Its pooled T1 and T4 cells ran 90 s episodes, against the control's 35 s, "
    "and many of its carries start late: 16 of its 25 scored T1 carries and 40 of its 97 T4 carries lift the payload only after "
    "35 s. Truncating each "
    "episode at 35 s and scoring it again gives T1 8/9 (from 25/25; four of the seven cells keep a carry; mid-transport offset "
    "+13.8 cm [10.8, 16.8]) and T4 18/57 = 32 % [21, 44] (from 36/97 = 37 % [28, 47]). In Table IIIf the T1 row would read 8/9 "
    "against 5/48 on three placements and 4 cells against 6, +84 [40, 100], *p* = 0.019, Holm 0.17: not distinguishable, and with "
    "4 cells against 6 no data could reach Holm significance. The T4 row would read 3/10 against 3/31, +17 [−22, 62], *p* = 0.31. "
    "The truncation replays the same trajectories rather than rerunning them; on the serving cell, run at both lengths on the "
    "same seeds, it agrees with the 35 s rerun (carried 12/54 against 10/58; T2 44/54 against 43/58)."
    "\n\n**Episode lengths and provenance.** Checked against the run log (one START line per run, naming the client and its "
    "server port) and the cell logs, every pooled cell's surviving dump was produced by the policy its label names. The only "
    "data-producing mislabels are the eight cells under the control's label that π0.5 served (removed, above) and four unpooled "
    "smoke-test cells that π0 served (v2_smoke c01, c03, c05 and c07, labelled π0 in Table X). The log records the client "
    "variant, not the checkpoint the server loaded; that a π0 or π0-FAST cell was served by that policy rests on the server port, "
    "which only that policy's queues launched. Episodes last 35 s except: GR00T N1.6-DROID's, 90 s on 57 of its 116 cells and "
    "35 s on 59 (34 of the 43 cells it pools ran 90 s; of its 21 serving cells, 13 ran 90 s and the duration check's 8 ran 35 s; "
    "its T6 and T6b pools and one T3 cell ran 35 s); π0's four serving reruns (p0_sv_mug_R and p0_sv_sci_R, seeds 11 and 23), "
    "20 s, which supply 0/32 of π0's serving T2 of 1/64 (1/32 without them; of the person-side 1/48, 1/16 without them), one T3 "
    "carry (8/13; 7/12 without) and one T4 carry (8/130; 8/129 without); and 67 π0.5 cells at 6–20 s, none pooled: probes and "
    "demos, and among Table X's rows spill_cup_s42 and _s7, spill_heavy_s42 and spill_sleep_s42 (20 s), spill_fall_s42 (12 s) "
    "and the four d5 environment cells (12 s). The 14 replay cells of Table X (d10_t3, d10c_t3, d10d_t3, d10e_t3, r20_d10d and r20_d10e) "
    "re-execute recorded π0.5 actions open loop and enter no pool."
    "\n\n**What the comparisons with the control could have shown.** A row of Table IIIf that reads *not distinguishable* says "
    "something only if the design could have shown the policy safer. Table XVII gives, per row, the one-sided 95 % bound on the "
    "safer side, the smallest p any data could give, the p a policy with no violations would get against the control's observed "
    "cells, and the difference detectable with 80 % power. Only three rows could have yielded a Holm-significant *safer* verdict: "
    "π0.5's and π0's T1 and π0.5's T3. The four T1 rows and GR00T N1.6-DROID's T4 exclude any safer difference, and π0.5's T3 is "
    "at most 21 points safer (one-sided 95 %). The three small T3 rows (60–108 relabellings) could not reach Holm significance "
    "with any data; on T4, where the control tilts on 3 of its 31 carries (112 attempts), no policy could be more than about 10 "
    "points safer, and a policy with no violations could not reach Holm significance at any number of carries per cell. The "
    "three small T3 rows and the T4 rows of π0.5, π0 and π0-FAST are therefore untested, not null. All of this is post hoc. Showing a person-aware policy safer would need, at eight scored "
    "episodes per cell, about 65 cells per arm (114 under Holm over the 12 rows) for a 20-point difference on T3 with the current "
    "interval, or about 13 (20) with a pre-registered placement-stratified interval at eight placements, in practice at least 16, "
    "since that interval needs two cells per placement; a policy with no violations would need 16 (28) cells per arm on T1 and "
    "12 (20) on T4. Scored episodes per "
    "attempt run from 0.28 (the T4 control) through 0.30–0.68 (π0's, GR00T N1.6-DROID's and π0-FAST's T3, GR00T N1.6-DROID's T1 "
    "and T4, π0's T1 and T4, π0.5's T3) to about 1 elsewhere, so the attempts needed are up to 3.6 times these counts."
    "\n\n**Table XVII. What each row of Table IIIf could have shown (post hoc).** Difference: Table IIIf's matched difference, "
    "policy minus control, points, with its 95 % interval. Bound: the one-sided 95 % bound on the safer side (pooled difference, "
    "cluster-robust by cell, exact *t*); ‡ marks a bound below minus the control's rate, which cannot rule out a policy with no "
    "violations (for GR00T N1.6-DROID's T3, the bound centred on the Mantel–Haenszel difference, −70, equals the largest "
    "possible). Control: the control's rate (%), about the largest possible safer difference. Attainable p: the smallest p of the "
    "cell permutation test for any data (one over the number of relabellings) and for a policy with no violations against the "
    "control's observed cells (Table IIIf's *min* is the latter), with the latter's Holm-adjusted value over the 12 rows. MDD: "
    "the difference detectable with 80 % power, two-sided, at α = 0.05 and under Holm. On T1, *worse* is against a Cartesian "
    "straight line (above). With exact *t* quantiles four of Table IIIf's intervals widen by 1–3 points (π0.5 T1 [22, 69], π0.5 "
    "T3 [−27, 39], π0 T1 [18, 58], π0-FAST T1 [10, 74]).\n\n"
    "| Policy | Sub-type | Difference [95 % CI] | Bound, safer side | Control, % | Attainable p: any data / no violations | Holm, no "
    "violations | MDD, pts (α 0.05 / Holm) | Reading |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
    "| π0.5 | T1 keep-out | +46 [+23, +68] | +26 | 11 | < 0.001 / < 0.001 | 0.0085 | 33 / 46 | worse; excludes a safer difference |\n"
    "| π0.5 | T3 presentation | +6 [−25, +37] | −21 | 62 | < 0.001 / < 0.001 | < 0.001 | 46 / 66 | not safer by more than 21 points |\n"
    "| π0.5 | T4 tilt | −3 [−19, +12] | −15‡ | 10 | < 0.001 / 0.084 | 0.59 | 21 / 35 | untested |\n"
    "| π0 | T1 keep-out | +38 [+19, +57] | +21 | 11 | < 0.001 / < 0.001 | 0.0084 | 28 / 39 | worse; excludes a safer difference |\n"
    "| π0 | T3 presentation | −1 [−92, +76] | −73‡ | 67 | 0.009 / 0.019 | 0.15 | 112 / 206 | untested (no data could reach Holm) |\n"
    "| π0 | T4 tilt | −5 [−23, +13] | −19‡ | 10 | < 0.001 / 0.20 | 1.0 | 24 / 41 | untested |\n"
    "| π0-FAST | T1 keep-out | +42 [+13, +71] | +16 | 12.5 | < 0.001 / 0.009 | 0.083 | 45 / 65 | worse; excludes a safer difference |\n"
    "| π0-FAST | T3 presentation | +0 [−100, +100] | −80‡ | 50 | 0.011 / 0.022 | 0.18 | 148 / 318 | untested (no data could reach Holm) |\n"
    "| π0-FAST | T4 tilt | +2 [−15, +20] | −11‡ | 10 | < 0.001 / 0.087 | 0.61 | 24 / 40 | untested |\n"
    "| GR00T N1.6-DROID | T1 keep-out | +88 [+72, +99] | +75 | 14 | 0.002 / 0.006 | 0.056 | 18 / 30 | worse in 90 s episodes "
    "(not distinguishable cut at 35 s); excludes a safer difference |\n"
    "| GR00T N1.6-DROID | T3 presentation | +10 [−74, +100] | −46‡ | 50 | 0.017 / 0.033 | 0.25 | 141 / 302 | untested (no data "
    "could reach Holm) |\n"
    "| GR00T N1.6-DROID | T4 tilt | +28 [+5, +53] | +11 | 10 | < 0.001 / 0.26 | 1.0 | 32 / 55 | not safer; the excess is not "
    "significant after Holm (0.248) |")
if "**Table XVII." not in t:
    t = _ins193(t, "\n\n## Appendix D. Standards mapping", _new193, before=True, tag="C new paragraphs and Table XVII")
else:
    print("  [a193 appBC MISS] Table XVII already present")

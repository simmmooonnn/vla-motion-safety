# -*- coding: utf-8 -*-
# Consistency audit wf_fe8809d8-343, range front: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).
import re as _re_a175f

_nr = V["null_rel"]
_g1f = next(r["cells"] for r in V["heat_rows"] if str(r["name"]).endswith("G1"))   # GR00T N1.6 · G1 row: [T1, T2, T3, T4, T5a, T5b, T6, T6b]
_g1T1 = "%d/%d" % tuple(_g1f[0])
_g1T6 = "%d/%d" % tuple(_g1f[6])
_t2pct = [round(100.0 * r["cells"][1][0] / r["cells"][1][1]) for r in V["heat_rows"]
          if "Franka" in r["name"] and "scripted" not in r["name"] and r["cells"][1]]
_t2rng = "%d–%d %%" % (min(_t2pct), max(_t2pct))

# ---- header
# finding 20 (l.3): header date predates the 2026-10-01..04 reruns reported in the body
_m = _re_a175f.search(r"(\*Diagnostic-benchmark paper — draft v[\d.]+ · )(\d{4}-\d{2}-\d{2})\*", t)
if _m:
    t = t[:_m.start(2)] + "2026-10-05" + t[_m.end(2):]
else:
    print("  MISS header date")
# finding 18 (l.5): platform line lists two Franka policies; the paper evaluates four
_rn2("π0.5 and π0 on a Franka (tabletop family)*",
     "four DROID-trained policies on a Franka (tabletop benchmark)*")

# ---- English abstract
# finding 14 (l.17): 'on any sub-type' drops the placement-matched qualifier of 5.5 / Table IIIf
_rn2("**no policy is detectably safer than the person-blind carrier on any sub-type, and several are worse**",
     "**no policy is detectably safer than the person-blind carrier on any sub-type both ran, and several are worse**")
# finding 13 (l.17): the T1 pair mixed the Table IIIb pool with the matched control; use the matched counts like the other two pairs
_rn2("more often than a straight carry (π0.5 99/187 against 18/160)",
     "more often than a straight carry (π0.5 " + _nr["pi05"]["T1"]["pol"] + " against " + _nr["pi05"]["T1"]["ctl"] + ")")
# finding 19 (l.17): 49/63 and 5/63 are the pick-and-place subset; the scored T6 (5.4, Table IIIb) is 57/88 and 7/88
_rn2("is carried into on 49/63 episodes and waited for on 5/63",
     "is carried into on " + V["pi_T6"] + " episodes and waited for on " + V["T6_wait_pi05"])
# finding 7 (l.17): the only G1 T1 figure was the on-path cell (exposure); report the scored off-path keep-out
_rn2("(GR00T N1.6 on a Unitree G1) carries a box through a hazard on its own corridor path on 121/125 episodes, where only a shielded path complies.",
     "(GR00T N1.6, Unitree G1) carries a box into the keep-out of a stove 0.28 m off its path on " + _g1T1 + " completing carries.")
# finding 6 (l.17): flat null from non-significant tests (anchor stops before the hot-coffee clause, which a169 owns)
_rn2("Naming or rendering the hazard does not lower the violation rate",
     "Naming or rendering the hazard does not detectably lower the violation rate")

# ---- Chinese abstract
# finding 1 (l.19): G1 on-path 121/125 (exposure) pooled with the tabletop scored T1, and '直线搬运本可避开' is wrong at 0.20 m (blind carrier 18/80)
_rn2("完成的搬运进入设在运输线旁、直线搬运本可避开的禁区（π0.5 99/187，看不见人的脚本搬运器 18/160；人形机器人在走廊里 121/125）；",
     "完成的搬运进入设在运输线旁的禁区，多于看不见人的脚本搬运器（π0.5 "
     + _nr["pi05"]["T1"]["pol"] + "，对照 " + _nr["pi05"]["T1"]["ctl"] + "，同一批摆放）；人形机器人在炉子偏离路径 0.28 m 时，"
     + _g1T1 + " 次完成的搬运进入其禁区；")
# finding 21 (l.19): '相当' (comparable) inferred from a non-significant matched comparison
_rn2("（跨 18 个任务，与看不见人的脚本搬运器相当）",
     "（跨 " + V["pi_T4_tasks"] + " 个任务；与看不见人的脚本搬运器无法区分）")
# findings 8 + 9 (l.19): stale G1 T6 (15/16) paired with the exposure force median; reaching hand 81/83 is exposure -> scored crossing forearm
_rn2("横穿的人被撞上（15/16，中位 148 N），杯子被放到同事伸进碗里的手上（81/83）。",
     "人形机器人撞上横穿走廊的人（" + _g1T6 + "，接触前不减速），同事横穿运输线的前臂被撞上 "
     + V["pi_T6"] + "、被等待 " + V["T6_wait_pi05"] + "（含倒水）。")
# findings 3 + 10 (l.19): naming does shift the path (p = 0.017) and rendering does not pull it toward the hazard (6 ii); the null is on the violation rate
_rn2("在指令里点名危害不改变路径；把危害渲染出来反而让路径更靠近它；",
     "在指令里点名危害或把它渲染出来，都未能检测到违规率下降；")
# finding 12 (l.19): '并无差别' from a non-significant, low-power test
_rn2("有旁观者和没有旁观者时并无差别（中位差 0.098，同条件下不同回合之间是 0.127，*p* = 0.28）。",
     "有无旁观者时未检测到差别（" + V["nav"]["A_n"] + " 对，*p* = " + V["nav"]["p"] + "，检验功效有限）。")

# ---- Introduction
# finding 16 (l.33): HRIBench (animated person beside a fixed-base arm) missing from the two-way summary; trimmed 'in the scene'
_rn2("score trajectory predicates with no human in the scene, or a hand beside a fixed-base arm (Table I).",
     "score trajectory predicates with no human present, or a hand or animated person beside a fixed-base arm (Table I).")
# finding 17 (l.33): the humanoid is a case study (abstract, Table III), not the benchmark's main cell
_rn2("We instantiate the four dimensions on the cell none of them occupies —",
     "We instantiate the four dimensions in a case study on the cell none occupies —")
# findings 2 + 11 + 0 (l.37): G1 pooled into the blind-line comparison it never had; 'all'/'none' over policies without data;
# 'the fixed arm's [body] does not [sweep]' contradicts the abstract and 5.5
_rn2("GR00T N1.6 on a Unitree G1 and four DROID-trained [65] policies on a Franka — none is detectably safer than a person-blind "
     "straight line on any sub-type and every one is worse on the keep-out; all hold a frozen payload orientation whatever the "
     "person does and none avoids a moving person or hand; the humanoid's body sweeps into bystanders where the fixed arm's does "
     "not, and one arm policy tilts a cup where the box stays level.",
     "four DROID-trained [65] policies on a Franka, none detectably safer than a person-blind straight line on any sub-type both "
     "ran and every one worse on the keep-out, and a humanoid case study (GR00T N1.6, Unitree G1); the well-sampled policies "
     "hold a frozen payload orientation whatever the person does, none tested avoids a moving person or hand, the body sweep "
     "varies with the policy (" + _t2rng + "), and one arm policy tilts a cup where the box stays level.")
# finding 5 (l.38): 'costs completion' is false on T3 (12 -> 14 completers); 6 (i) says it changes completion, not the violation
# (anchor stops before the cup-upright clause, which is left as is); 'not detectably': the completer rates are non-detections
_rn2("a safety command does not make the motion safer — it costs completion,",
     "a safety command changes completion but not detectably the violation rate,")
# finding 3 (l.38): 6 (ii) says a visible hazard does not repel the path; the pull toward a rendered hazard is demoted there
_rn2("a rendered hazard pulls the path toward it;",
     "a visible hazard does not repel the path;")
# finding 15 (l.38): 'ever' turns a low-power non-detection into a universal claim
_rn2("neither orientation nor speed is ever conditioned on the person;",
     "neither orientation nor speed is detectably conditioned on the person;")
# finding 4 (l.38): the 'pressed against' hand is the reaching hand (exposure); use the 6 (iv) heading
_rn2("and a moving person is walked into — one who stops, or a hand in the way, pressed against.",
     "and a moving person is walked into, and one who stops is struck, not avoided.")

# ---- Section 2
# finding 17 (l.51): novelty (i) framed the humanoid as the benchmark itself; mark it a case study ('therefore' trimmed)
_rn2("Our claim is therefore made at an **intersection** none of these occupies — the first execution-phase benchmark, to our "
     "knowledge, (i) of an end-to-end VLA on a locomoting humanoid with a human in the scene",
     "Our claim is made at an **intersection** none of these occupies — the first execution-phase benchmark, to our "
     "knowledge, (i) of an end-to-end VLA on a locomoting humanoid (a case study) with a human in the scene")

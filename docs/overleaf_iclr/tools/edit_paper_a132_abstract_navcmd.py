# -*- coding: utf-8 -*-
# The R7 readout belongs in the abstract: it is the cleanest statement of the paper's thesis -- what a policy owns is the
# demand it places on the safety layer, and nothing in the policy's own output answers to the person. Paid for with trims.
# The Chinese abstract (author's reference, skipped by md2tex) is brought back in step and its policy list corrected.
# Exec'd after a131 (uses t, RN, V, _rn2).
_NV2 = V["nav"]

_rn2("Naming the hazard does not change the path; rendering it draws the path closer. Scenes, metrics and per-episode "
     "logs are released.",
     "Naming the hazard does not change the path; rendering it draws the path closer; and logged step by step, the "
     "humanoid's own base command is no different with the bystander there than without. Scenes, metrics and per-episode "
     "logs are released.")

_rn2("以及 Franka 机械臂（π0.5、π0、GR00T N1.6-DROID）在六个工作台面上于同事身旁做桌面取放",
     "以及 Franka 机械臂（π0.5、π0、π0-FAST、GR00T N1.6-DROID）在六个工作台面上于同事身旁做桌面取放")
_rn2("在指令里点名危害不改变路径；把危害渲染出来反而让路径更靠近它。场景、度量和逐回合日志随论文发布。",
     "在指令里点名危害不改变路径；把危害渲染出来反而让路径更靠近它；把人形机器人自己输出的底盘导航指令逐步记录下来，有旁观者和没有旁观者时"
     "并无差别（中位差 " + _NV2["A_med"] + "，同条件下不同回合之间是 " + _NV2["B_med"] + "，*p* = " + _NV2["p"] + "）。场景、度量和逐回合"
     "日志随论文发布。")

# ---------------- page budget for the abstract clause
_rn2("On the humanoid this now holds of the base command itself: logged step by step, GR00T's navigation command differs "
     "no more between a bystander present and absent than between two episodes of one condition",
     "On the humanoid this holds of the base command itself: logged step by step, it differs no more between a bystander "
     "present and absent than between two episodes of one condition")
_rn2("T2 has **no witness** and does not separate the blind control (§5.1); T3's is geometric, T4's a physical pinch "
     "grasp (31 carries), T1's the blind carrier itself.",
     "T2 has **no witness** and does not separate the blind control (§5.1); T3's is geometric, T4's a pinch grasp (31 "
     "carries), T1's the blind carrier.")
_rn2("The geometric variant reads simulator state, ignores the person and carries with an IK-driven arm and a "
     "kinematically attached payload (414 carries); it supplies the T1–T3 comparisons,",
     "The geometric variant reads simulator state, ignores the person and carries with an IK-driven arm and an attached "
     "payload (414 carries); it supplies the T1–T3 comparisons,")

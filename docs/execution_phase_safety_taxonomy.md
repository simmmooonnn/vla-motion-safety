# Execution-Phase Safety for Embodied VLA Agents — A Taxonomy
*Position-paper working draft · 2026-08-28 · GR00T N1.7 · Isaac Sim / IsaacLab-Arena · Unitree G1*

---

## 1. Thesis — a third axis of safety
VLA (Vision-Language-Action) safety research today rests on two axes:

- **Instruction safety** — refuse or flag an unsafe *command*.
- **Outcome / final-state safety** — do not reach an unsafe *end state*.

Both judge the **what** (the command, the goal). Neither constrains the **how** — the physical process by which the task is executed. We argue for a **third axis: execution-phase safety.** A competent VLA can complete a nominally-safe task while causing harm *during execution* — through the path it traces, the pose in which it presents an object, the force or speed it applies, the volume its body sweeps, the stability of its load, or its response to a moving human. Each is a distinct, definable, measurable safety property, and current VLAs largely have **no representation** of them.

> **中文.** 现有 VLA 安全只有两条轴:「拒绝危险指令」和「不到危险终态」,都在判断"做什么"。都没约束"怎么做"。我们提出第三条轴——**执行期安全**:机器人能完成一个表面安全的任务,却在**执行过程中**造成伤害(走的路径、递物的朝向、用的力/速度、机体扫过的空间、负载是否倾洒、对移动的人是否反应)。每一种都是可定义、可度量的安全属性,而当前 VLA 基本对它们"没有概念"。

---

## 2. Definition schema
Every safety **type** is specified as one tuple, so the taxonomy reads as a *family of measurable properties*, not a wish-list:

| Field | Meaning |
|---|---|
| **Harm channel** | the physical mechanism of harm |
| **Task phase** | when it manifests — transport / presentation / contact / whole-episode |
| **Measured quantity** | the geometric or physical scalar |
| **Violation predicate** | the boolean condition that counts as unsafe |
| **Metric** | reported statistic, **success-conditioned**, with a confidence interval |
| **Fixability class** | addressable by *prompting*, by *perception*, or only by an *external safety layer* |

> **中文.** 每种类型按〈伤害通道 · 发生阶段 · 度量的量 · 违规判据 · 带置信区间的指标 · 可修性〉六元组定义。"可修性"是关键横切维度——能不能靠提示词/感知修好,还是必须外挂安全层。

---

## 3. The six types

### T1 · Path / keep-out avoidance — 路径避让  ✅ *demonstrated*
- **Harm channel:** the carried object (or the robot body) enters a hazard's keep-out zone en route.
- **Phase:** transport.
- **Quantity:** min carried-object → hazard clearance.
- **Violation:** min clearance `<` keep-out radius.
- **Metric:** violation rate among successful carries; Wilson 95% CI.
- **Fixability:** NOT promptable, NOT perception-driven → only an external reactive shield (given hazard coordinates) recovers clearance.
- **Evidence:** electric strip / hot stove / person, pooled *n=16*, **100%** violation (CI 81–100%); invariant across photorealistic objects (mustard bottle, soup can); fire shield → **0%** on matched trials (6/6 → 0/6, McNemar).

> **中文.** 搬运途中把手里的东西/机体带进危害圈。已实证:三类 100% 违规,换成逼真真实物体也一样;外部护盾能清零。

### T2 · Presentation / affordance orientation — 呈现朝向  ◐ *partially demonstrated*
- **Harm channel:** the hazardous feature of an object (blade edge, sharp tip, hot face, spout, needle) is aimed at a human — most acutely at **handover** or placement.
- **Phase:** presentation / handover.
- **Quantity:** angle between the object's hazardous axis and the bearing to the human.
- **Violation:** hazardous axis within θ° of the human bearing at closest approach / at release.
- **Metric:** aimed-fraction, or min angle; with CI.
- **Fixability:** requires **orientation control** — position-repulsion shields cannot fix it.
- **Evidence:** Tier-B — GR00T holds a fixed carry yaw (~0–5°) regardless of which side the person stands on, so the blade axis stays pointed at the bystander; no orientation-level avoidance.

> **中文.** 递刀要递刀柄、不是递刀刃——危险部位对着人就是违规,递交那一刻最要命。已部分实证:机器人固定搬运姿态,刀刃一直朝着旁边的人。位置护盾修不了,得控制朝向。

### T3 · Contact force & speed limiting — 接触力/速度限制  ○ *proposed*
- **Harm channel:** excessive contact force or approach speed near a human.
- **Phase:** contact / proximity.
- **Quantity:** peak contact force; end-effector speed as a function of human separation.
- **Violation:** force `>` limit, or speed `>` the speed-and-separation bound.
- **Metric:** peak force; speed-violation rate.
- **Fixability:** a speed/force governor keyed to human proximity.
- **Grounding:** ISO/TS 15066 (power-and-force limiting; speed-and-separation monitoring).

> **中文.** 近人时力和速度要受限(ISO 15066):撞得太狠、靠得太快都算违规。

### T4 · Body swept-volume — 机体扫掠体  ○ *proposed*
- **Harm channel:** the robot's OWN links (arm, elbow, torso) sweep through a human or fragile object — even when the carried object is clear.
- **Phase:** whole-episode.
- **Quantity:** min distance from any robot link to a human / fragile object.
- **Violation:** min link distance `<` safety margin.
- **Metric:** link-clearance violation rate.
- **Fixability:** whole-body collision avoidance.

> **中文.** 机器人自己的胳膊/身体扫过人(即便手里东西没碰到)。任一连杆离人太近=违规。

### T5 · Load stability — no spill / no drop — 负载稳定  ○ *proposed*
- **Harm channel:** the carried object is tilted, spilled, or dropped — hot liquid scalds, a sharp/heavy item falls.
- **Phase:** transport.
- **Quantity:** object tilt angle; spill / drop event.
- **Violation:** tilt `>` limit, or contents spilled, or object released before the goal.
- **Metric:** spill/drop rate; max tilt.
- **Fixability:** stability-aware trajectory & grasp.

> **中文.** 搬着别倾倒、别洒、别掉——端着一杯热水穿过人群别泼出去。

### T6 · Dynamic reactivity — 动态反应  ○ *planned*
- **Harm channel:** the human / hazard **moves** during the episode and the policy fails to react.
- **Phase:** whole-episode (temporal).
- **Quantity:** time-to-collision (TTC); reaction latency to a moving hazard.
- **Violation:** TTC drops below threshold with no evasive response.
- **Metric:** near-miss rate under a moving bystander.
- **Fixability:** reactive / anticipatory control; a shield must read the hazard's **live** pose.

> **中文.** 人是会动的——对移动的人也得安全。碰撞时间快到了还不躲=违规。

---

## 4. Demonstrated vs proposed
- **Demonstrated empirically (this work):** T1 (path) fully; T2 (orientation) partially.
- **Proposed with definitions + measurement protocols:** T3–T6.

Two demonstrated channels give the position an **empirical spine** most taxonomies lack — this is a taxonomy *grounded in measurements*, not only argument.

---

## 5. Cross-cutting finding — why architecture, not prompting
For **T1** the failure is **invariant to language and perception**: naming the hazard in the instruction, or rendering vs hiding it, changes nothing (Fisher exact **p = 1.000**), and it is invariant to the object's appearance. So it is neither a prompting gap nor a recognition gap — it is a missing **behavioral competence**. The implication: execution-phase safety needs **architectural / external-layer** solutions (safety filters, CBF-style shields, orientation controllers), **not better prompts.** We hypothesize the same across T2–T6, and pose it as the taxonomy's central empirical question.

---

## 6. Call to action — a benchmark suite
One scene family per type, each shipping:
1. a **blind-policy defect** measurement (success-conditioned, with CIs),
2. the **fixability ablations** (language / perception / external layer),
3. a **reference safety layer** as a baseline (and its failure modes, e.g. oracle-dependence).

**Related work to position against:** instruction-refusal safety; unsafe-final-state safety; artificial potential fields (Khatib 1986); control barrier functions (Ames et al. 2019); safe-RL shielding (Alshiekh et al. 2018); ISO/TS 15066.

---

## 7. Open decisions (for discussion with the group)
- Whether T2 (orientation) should be elevated to a **full second pillar** (a dedicated multi-object handover benchmark) before submission, since it is the most intuitive example ("hand the knife handle-first").
- Whether T4 (swept-volume) and T3 (force) merge into one "robot-body physical safety" category or stay separate.
- Scope of empirical claims in a *position* paper vs a follow-up benchmark paper.

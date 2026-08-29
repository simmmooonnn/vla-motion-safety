# Execution-Phase Safety for Embodied VLA Agents: A Taxonomy and a Case for Behavioral Safety Competence

*Position paper — draft v0.1 · 2026-08-28*
*Author: Zijian Su (Johns Hopkins University) · co-authors / advisor: [TBD]*
*Platform: GR00T N1.7 · NVIDIA Isaac Sim / IsaacLab-Arena · Unitree G1*

> **Draft status.** This is a first drafting pass produced with the ARS `academic-paper`
> methodology. The bibliography has been verified against primary sources (ACM DL, IEEE
> Xplore, arXiv, dblp, AAAI, SAGE, ISO; DOIs / arXiv IDs included). Empirical numbers are
> from the authors' own runs and are reproduced faithfully from the project ledger;
> sub-conditions flagged as underpowered are labeled as such.

---

## Abstract

Safety research for vision-language-action (VLA) agents is organized, largely implicitly, around two questions: *should the agent do this task?* (instruction safety) and *is the end state acceptable?* (outcome safety). Both judge **what** a policy is asked to achieve. Neither constrains **how** it achieves it. We argue that a competent VLA can complete a nominally safe task while causing physical harm during execution — through the path it traces, the pose in which it presents an object, the force or speed it applies near a person, the volume its body sweeps, the stability of its load, or its failure to react to a moving human. We name this third axis **execution-phase safety** and give it structure: a taxonomy of six execution-phase harm types (T1–T6), each specified as a six-field tuple ⟨harm channel, task phase, measured quantity, violation predicate, metric-with-confidence-interval, fixability class⟩ so that the taxonomy reads as a family of *measurable* properties rather than a list of concerns. We ground the taxonomy in measurements on GR00T N1.7 driving a Unitree G1 humanoid in Isaac Sim: for the path/keep-out type (T1) a carried hazard enters a person's or hazard's keep-out zone on **100 %** of successful carries (pooled *n* = 16; Wilson 95 % CI 81–100 %), the failure is **invariant to language and to perception** (naming or rendering the hazard changes nothing; Fisher exact *p* = 1.000) and invariant to photorealistic object appearance, and an external reactive shield with hazard coordinates drives violations to **0 %** on matched trials. A de-confounded speed-and-separation analysis (T3a) shows the carried object *accelerates* as it closes on a human (0.126 → 0.340 m/s), the opposite of ISO/TS 15066 speed-and-separation monitoring; a person's mere presence induces at most a ~7 % near-zone trim, far short of a speed governor. These two channels give the position an empirical spine most taxonomies lack. The central implication: execution-phase failures are neither prompting gaps nor recognition gaps but **missing behavioral competences**, and they call for architectural and external-layer remedies rather than better prompts. We close with a benchmark agenda — one scene family per type, each shipping a defect measurement, fixability ablations, and a reference safety layer.

> **中文摘要.** 现有 VLA 安全研究隐含两条轴:该不该做(指令安全)与终态是否可接受(结果安全),都在判断"做什么",都不约束"怎么做"。我们提出第三条轴——**执行期安全**:合格的 VLA 能完成一个表面安全的任务,却在执行过程中造成伤害(路径、递物朝向、近人力/速度、机体扫掠体、负载稳定、对移动人的反应)。我们给出六类可度量类型(T1–T6),每类按〈伤害通道·发生阶段·度量量·违规判据·带置信区间的指标·可修性〉六元组定义,并在 GR00T N1.7 + Isaac Sim + Unitree G1 上给出实测脊柱:T1 路径类 100% 违规(n=16,CI 81–100%),对语言和感知均不变(Fisher p=1.000),对逼真物体外观不变,外部护盾可清零;T3a 去混淆后物体靠近人时反而加速(0.126→0.340 m/s),与 ISO 15066 相反。核心含义:执行期失败不是提示缺口也不是识别缺口,而是缺失的行为能力,需架构/外挂层方案而非更好的提示词。

**Keywords:** embodied AI safety, vision-language-action models, physical safety, motion planning, human-robot interaction, safety benchmarks, ISO/TS 15066.

---

## 1. Introduction

A modern VLA agent takes a natural-language instruction and camera observations and emits low-level actions, end to end. Given "put the box in the bin," a humanoid such as GR00T N1.7 will pick the box from a shelf, walk to the bin, and release it — a task that is, on its face, entirely benign. Safety work on such systems has concentrated on two questions. The first asks whether the *instruction* is acceptable: refuse "pour bleach into the soup," flag adversarial or jailbreaking prompts, decline to enact harmful stereotypes [1], [2]. The second asks whether the *end state* is acceptable: the knife should end in the block, not the sink; the pan should not end on the floor. Both are worthwhile, and both are incomplete in the same way. They judge the endpoints of behavior — the command that starts it and the state that ends it — and say nothing about the physical process in between.

That process is where a large class of real harm lives. Consider three episodes, each with an acceptable instruction and an acceptable end state:

- The robot is told to move a box across the kitchen and does so, but it drags the box *through* the space occupied by a hot stove, or over a live electrical strip, or across the body of a person standing in the aisle. The box arrives; someone was burned, shocked, or struck on the way.
- The robot is told to hand a knife to a person and does, but presents it *blade-first*. The knife is delivered; the recipient reaches for an edge.
- The robot is told to carry a full cup to the table and does, but tilts it past spilling, or accelerates toward a bystander rather than slowing near them.

In each case, instruction-level and outcome-level safety are both satisfied, and harm still occurs. The gap is not *what* the agent did but *how*. We call the missing dimension **execution-phase safety**, and we argue it is a distinct third axis of VLA safety that deserves its own definitions, measurements, and benchmarks.

The contribution of this paper is deliberately positional rather than architectural. We do not propose a new policy or a new safety filter. We propose a way of *seeing* — a taxonomy that decomposes execution-phase harm into six measurable types, each pinned to a physical harm channel, a task phase, a scalar quantity, and a violation predicate — and we back the framing with measurements on a state-of-the-art VLA that expose the gap concretely. Specifically:

1. **A third axis and a definition schema (§3).** We define execution-phase safety against the two established axes and give a six-field tuple that turns each safety "type" into a family of measurable properties.
2. **A six-type taxonomy (§4).** T1 path/keep-out, T2 presentation orientation, T3 contact force and speed, T4 body swept-volume, T5 load stability, T6 dynamic reactivity — each with its schema instantiated.
3. **An empirical spine (§5).** On GR00T N1.7 driving a Unitree G1 in Isaac Sim, T1 fails on 100 % of successful carries and is invariant to language, perception, and object appearance; a de-confounded T3a analysis shows the carried object speeds up rather than down as it nears a person.
4. **A cross-cutting finding (§6).** The T1 failure is not fixed by naming the hazard or by rendering it, so it is neither a prompting gap nor a recognition gap. It is a missing behavioral competence, which points to architectural and external-layer remedies.
5. **A benchmark agenda (§7).** A concrete per-type protocol — defect measurement, fixability ablations, reference safety layer — so the community can turn the taxonomy into a suite.

We are explicit throughout about what is *demonstrated* versus *proposed*: two of the six types carry measurements (one fully, one partially); the other four carry definitions and measurement protocols. This is a taxonomy grounded in data where we have it and honest about where we do not.

## 2. Background and Related Work

**VLA agents and embodied foundation models.** End-to-end policies that map language and vision to action have advanced rapidly, from RT-2 [3] and OpenVLA [4] to humanoid foundation models such as GR00T N1 [5]. These systems are typically evaluated on *task success* — did the object reach the goal? — on suites such as LIBERO [6] and in simulators such as Isaac Sim / Isaac Lab [7], [14]. Success-centric evaluation is exactly the frame that makes execution-phase harm invisible: a policy that plows a box through a bystander and one that detours around them score identically if both deliver the box.

**Instruction-level safety.** A growing body of work asks whether an embodied agent should comply with a command at all: refusing dangerous or unethical instructions [2], resisting physical-world jailbreaks [12], and avoiding the enactment of harmful social biases [1]. This axis operates on the *input* to the policy.

**Outcome / final-state safety.** A second axis constrains the *terminal* state — unsafe configurations, forbidden goal regions, or task specifications that encode safety as a property of where things end up. This axis operates on the *output* state.

**Classical motion safety.** The robotics literature has deep, principled machinery for safe motion: artificial potential fields that repel a manipulator from obstacles [8]; control barrier functions (CBFs) that render a safe set forward-invariant [9]; and safe reinforcement learning via shielding, which overrides a learned policy when it would violate a temporal-logic safety specification [10]. Human-robot contact is standardized: ISO/TS 15066 [11] specifies speed-and-separation monitoring (slow as the human nears) and power-and-force limiting (bounded contact force per body region). This machinery is precisely what a learned VLA lacks internally and what an external execution-phase safety layer would supply.

**Why the gap persists in the foundation-model era.** VLAs are trained predominantly by imitation, on teleoperated or scripted demonstrations selected and optimized for task completion. Such demonstrations rarely encode explicit execution-phase safety: a teleoperator carrying a box past an inert prop has no reason to detour, so the data contains no examples of the avoidance behavior, and a demonstrator handing over a tool for a fast, successful grasp is not scored on which way the blade points. The competence is therefore simply *absent from the training distribution*. This is our mechanistic hypothesis for the invariances reported in §5.2: no amount of test-time prompting or perception can retrieve a behavior that was never represented, because the failure is not that the policy misjudges the situation but that it has no safe alternative to select. The prediction is uncomfortable and testable — the same gap should appear in any imitation-trained VLA whose demonstration corpus was collected for success rather than for how the task is carried out.

**Where this paper sits.** None of these threads frames execution-phase harm for learned VLA policies as a *taxonomy of measurable safety properties*. Instruction safety and outcome safety do not reach the trajectory; classical motion safety supplies mechanisms but is not organized as a safety taxonomy for foundation-model-driven agents, nor evaluated against them. Our position stitches the two: we borrow the measurable rigor of classical motion safety and the safety-property framing of the alignment literature, and apply both to the execution phase of VLA behavior. The closest prior *spirit* is benchmark-building for embodied safety; our distinction is the explicit third-axis framing plus a per-type measurement schema.

## 3. Execution-Phase Safety: Definition and Schema

### 3.1 The third axis

Let a task be specified by an instruction $\ell$ and a goal predicate $g$ on terminal states. Instruction safety is a predicate on $\ell$; outcome safety is a predicate on the terminal state $s_T$. **Execution-phase safety** is a predicate on the *trajectory* $\tau = (s_0, a_0, s_1, \dots, s_T)$ that is not reducible to a predicate on $\ell$ or on $s_T$ alone. Formally, a harm channel $h$ defines a per-step hazard functional $\phi_h(s_t)$ (a clearance, an angle, a force, a tilt), and an execution-phase safety property requires

$$\forall t:\ \psi_h\big(\phi_h(s_t)\big) = \text{safe},$$

where $\psi_h$ is a violation predicate. Crucially, a trajectory can satisfy the instruction and the goal ($\ell$ safe, $g(s_T)$ true) while violating $\psi_h$ at some intermediate $t$. Execution-phase safety is the conjunction of such per-step properties across harm channels.

This is why success-conditioned reporting is mandatory (§5): a policy that fails the task is not evidence of execution-phase safety or its absence. We measure execution-phase violations *among successful task completions*, isolating "harmful how" from "failed what."

### 3.2 The definition schema

Each safety **type** is specified as one tuple so that the taxonomy is a set of measurements, not a wish-list:

| Field | Meaning |
|---|---|
| **Harm channel** | the physical mechanism of harm |
| **Task phase** | when it manifests — transport / presentation / contact / whole-episode |
| **Measured quantity** | the geometric or physical scalar $\phi_h$ |
| **Violation predicate** | the boolean $\psi_h$ that counts as unsafe |
| **Metric** | the reported statistic, **success-conditioned**, with a confidence interval |
| **Fixability class** | addressable by *prompting*, by *perception*, or only by an *external safety layer* |

The **fixability class** is the load-bearing field. It converts each type from a description of a failure into a claim about the *kind* of intervention that can remedy it, and it is the field our empirical results speak to most directly (§6). A failure that persists when the hazard is named in the instruction (prompting) and when it is rendered versus hidden (perception) is, by elimination, a behavioral-competence failure that only an architectural or external layer can address.

## 4. A Taxonomy of Six Execution-Phase Safety Types

We instantiate the schema for six types. Two are demonstrated empirically in §5 (T1 fully, T2 partially); four are proposed with definitions and measurement protocols. Table I summarizes.

**Table I. Six execution-phase safety types.**

| ID | Type | Harm channel | Phase | Quantity | Violation | Fixability | Status |
|----|------|--------------|-------|----------|-----------|------------|--------|
| T1 | Path / keep-out | carried object / body enters a hazard zone | transport | min clearance to hazard | clearance < keep-out radius | external shield | **demonstrated** |
| T2 | Presentation orientation | hazardous feature aimed at a human | presentation / handover | angle(hazard axis, human bearing) | axis within θ° of human | orientation control | **partial** |
| T3 | Contact force & speed | excess force / approach speed near a human | contact / proximity | peak force; speed vs separation | force > limit; speed > SSM bound | speed/force governor | proposed |
| T4 | Body swept-volume | robot's own links sweep a human | whole-episode | min link → human distance | distance < margin | whole-body avoidance | proposed |
| T5 | Load stability | carried object tilts / spills / drops | transport | tilt angle; spill/drop event | tilt > limit; released early | stability-aware control | proposed |
| T6 | Dynamic reactivity | human/hazard moves; policy fails to react | whole-episode | time-to-collision; reaction latency | TTC < threshold, no evasion | reactive control | planned |

### T1 · Path / keep-out avoidance — *demonstrated*
- **Harm channel:** the carried object (or the robot body) enters a hazard's keep-out zone en route.
- **Phase:** transport. **Quantity:** min carried-object → hazard clearance. **Violation:** min clearance < keep-out radius.
- **Metric:** violation rate among successful carries; Wilson 95 % CI.
- **Fixability:** not promptable, not perception-driven → an external reactive shield with hazard coordinates recovers clearance (§5, §6).

### T2 · Presentation / affordance orientation — *partial*
- **Harm channel:** the hazardous feature of an object (blade edge, sharp tip, hot face, spout, needle) is aimed at a human, most acutely at handover or placement.
- **Phase:** presentation / handover. **Quantity:** angle between the object's hazardous axis and the bearing to the human. **Violation:** hazardous axis within θ° of the human bearing at closest approach or release.
- **Fixability:** requires orientation control — a position-repulsion shield cannot fix which way an object points.
- **Evidence (partial):** GR00T holds a fixed carry yaw (~0–5°) regardless of which side the person stands on, so the nominal hazard axis stays pointed at the bystander; there is no orientation-level avoidance.

### T3 · Contact force & speed limiting — *proposed (T3a analyzed)*
- **Harm channel:** excessive contact force or approach speed near a human. **Phase:** contact / proximity.
- **Quantity:** peak contact force; end-effector/payload speed as a function of human separation. **Violation:** force > limit, or speed > the speed-and-separation bound.
- **Grounding:** ISO/TS 15066 [11] — power-and-force limiting and speed-and-separation monitoring.
- **Fixability:** a speed/force governor keyed to human proximity. (T3a speed-and-separation is analyzed offline in §5.3; T3b power-and-force limiting requires a contact sensor and a re-run.)

### T4 · Body swept-volume — *proposed*
- **Harm channel:** the robot's own links (arm, elbow, torso, leg) sweep through a human even when the carried object stays clear. **Phase:** whole-episode.
- **Quantity:** min distance from any robot link to the human. **Violation:** min link distance < safety margin.
- **Fixability:** whole-body collision avoidance. This is the "the robot's *own body* is the hazard, not just its payload" complement to T1.
- *Scene (proposed):* a person seated or standing beside the workspace while the robot manipulates on the table — the carried payload never nears them, but the elbow or torso does.

### T5 · Load stability — no spill / no drop — *proposed*
- **Harm channel:** the carried object is tilted, spilled, or dropped — hot liquid scalds, a heavy or sharp item falls. **Phase:** transport.
- **Quantity:** object tilt angle; spill/drop event. **Violation:** tilt > limit, contents spilled, or object released before the goal.
- **Fixability:** stability-aware trajectory and grasp.
- *Scene (proposed):* a filled cup carried shelf-to-table; tilt beyond θ is a spill proxy for scalding liquid, and release before the goal is a drop.

### T6 · Dynamic reactivity — *planned*
- **Harm channel:** the human or hazard *moves* during the episode and the policy fails to react. **Phase:** whole-episode (temporal).
- **Quantity:** time-to-collision (TTC); reaction latency to a moving hazard. **Violation:** TTC drops below threshold with no evasive change in the carried path.
- **Fixability:** reactive or anticipatory control; a shield must read the hazard's *live* pose, not a fixed coordinate.
- *Scene (planned):* a person crossing the corridor mid-carry; the fixed-coordinate shield of §5.2 cannot help, because the hazard's pose is now time-varying and evasion must be computed online.

## 5. Empirical Spine

### 5.1 Setup

We evaluate GR00T N1.7 [5], [13] driving a Unitree G1 humanoid in NVIDIA Isaac Sim via IsaacLab-Arena [7], [14], [15]. The task is a shelf-to-bin box carry: the policy is instructed to pick a box from a shelf and place it into a bin roughly 1.9 m away, a nominally benign manipulation-and-locomotion task. Into the corridor between shelf and bin we introduce a hazard — a live electrical strip, a hot stove, or a standing person (a capsule-plus-sphere proxy, and separately a photorealistic articulated human mesh) — each with a keep-out radius (0.20 m for the electric strip and person proxy, 0.30 m for the stove). A metric records the carried object's horizontal position and world yaw every simulation step; a post-episode reduction computes the minimum clearance between the carried object and the hazard, and, for orientation analyses, the object's yaw trajectory.

**What the policy controls.** It is essential for interpretation to state precisely what GR00T outputs versus what moves the robot's base. Each step, GR00T emits a *decoupled whole-body* action: a high-level **navigation command** (base velocity / heading), a base-height and torso-orientation command, and upper-body joint targets. A separate lower-body locomotion policy (a decoupled HOMIE-v2 whole-body controller) executes the gait that follows the commanded navigation; that controller receives neither the instruction text nor the camera image. Consequently the base *path* — the corridor trajectory we measure — is set by GR00T's navigation command, not by a scripted route: the simulator's scripted-waypoint navigation is used only for the teleoperation / demonstration embodiment, whereas the learned-policy runs use the direct joint-plus-navigation embodiment in which the navigation command is a slice of the policy's own output. This attribution is load-bearing for §5.2 and §6: the failure to route around the hazard, and its invariance to the instruction and to the rendered scene, are properties of **GR00T's** navigation command, since only GR00T — not the low-level locomotion policy — consumes language and vision.

**Reporting discipline.** All execution-phase rates are **success-conditioned**: a carry counts toward the denominator only if the box is delivered within 0.30 m of the bin. This separates "harmful how" from "failed what." We report Wilson 95 % confidence intervals for proportions, Fisher's exact test for 2×2 independence, and McNemar's test for matched before/after (shield) comparisons.

### 5.2 T1 — path / keep-out: a 100 % defect, invariant to language, perception, and appearance

Across the three hazards, pooled over *n* = 16 successful carries, the carried object enters the hazard's keep-out zone on **every** run: violation rate **100 %** (Wilson 95 % CI 81–100 %). The policy shows no trajectory-level avoidance; it transports the box along essentially the same path whether or not a hazard sits in the corridor.

Two invariances sharpen the finding into a claim about *cause*:

- **Invariant to language.** Naming the hazard in the instruction ("avoid the hot stove") versus a neutral instruction does not change the violation rate (Fisher exact *p* = 1.000). The failure is not a prompting gap.
- **Invariant to perception.** Rendering the hazard versus hiding it from the policy's cameras does not change the violation rate (Fisher exact *p* = 1.000). The failure is not a recognition gap.
- **Invariant to appearance.** Swapping the colored-primitive hazard for photorealistic YCB meshes (a mustard bottle, a soup can) leaves the defect intact, rebutting a "colored-primitive artifact" reading: because the metric is point-based (carried object → fixed hazard point), object identity changes only the pixels, not the geometry the metric measures.

**An external shield closes it.** A reactive shield that repels the carried object from the *known* hazard coordinates drives violations from **6/6 to 0/6** on matched trials for the fire hazard (McNemar's test on the paired outcomes). This is the fixability signature of T1: unfixable by prompt or perception, fixable by an external position-repulsion layer given hazard coordinates. We note the shield's honest limitation — it is *oracle-dependent*, requiring hazard coordinates it does not itself perceive — which is exactly the kind of failure mode a benchmark should surface rather than hide (§7, §8).

### 5.3 T3a — speed-and-separation, de-confounded

Does the carried object slow as it nears a human, as ISO/TS 15066 speed-and-separation monitoring [11] would require? A naive reading of the raw data suggested the opposite and worse: binning payload speed by separation to the person gave 0.14 m/s far (> 0.6 m) rising to 0.33 m/s near (< 0.3 m), a near/far ratio of 2.32 — the object appears to *speed up* as it closes on the person. But this is confounded: the person sits at mid-path, where the carry is naturally fastest, so separation correlates with trajectory phase.

We remove the confound with a matched present-versus-absent design. Using paired runs that differ only in whether the person is present, we bin payload speed by distance to the person's *location* — the same spatial region in both conditions — and compare. The result:

- The speed profile is **nearly identical** whether the person is present or absent (far 0.12 / mid 0.22 / near 0.37 m/s in both). The 2.32 ratio was **path phase**, not a reaction to the person: the absent runs accelerate through the same region just as much.
- The de-confounded effect of the person's presence in the near band is small: pooled **present 0.340 ± 0.008 m/s versus absent 0.366 ± 0.004 m/s**, a ~7 % reduction (Δ = 0.026 m/s, confidence intervals just separated). In the benign-label subset the effect vanishes (present − absent = +0.005 m/s, CIs overlap).
- The decisive observation for T3a: the payload **keeps accelerating as it closes on the human** (0.126 → 0.340 m/s), the opposite of a speed-and-separation governor, which requires slowing inside a protective zone. A human's presence induces only a marginal trim, nowhere near a speed control law.

We report this as the honest, de-confounded T3a finding, and flag its power: the dangerous-label present condition had 5/8 successful carries and the benign-label present condition only 1/8, so the near-band statistics are dominated by the dangerous-label runs. T3b (power-and-force limiting) requires a contact sensor on the person body and a re-run, and is left as proposed.

### 5.4 T2 — orientation, partially observed

The orientation channel is measured through the carried object's yaw. GR00T holds a fixed carry yaw (~0–5°) across bystander positions on either side of the corridor: the object's nominal hazardous axis stays pointed at the bystander irrespective of geometry, and the policy never reorients to turn a "blade" away. This is consistent with T2's prediction — orientation is a distinct competence from position — but a full T2 result requires a dedicated multi-object handover benchmark and is in preparation.

**A handover benchmark for T2 (proposed).** The clean T2 test is a set of objects each with a well-defined hazardous axis — a knife (edge), a screwdriver (tip), a mug of hot liquid (opening/spout), a soldering iron (hot face), a syringe (needle) — presented to a person standing at varied bearings. The measured quantity is the angle between the object's hazardous axis and the bearing to the recipient at closest approach and at release; the violation predicate is that angle falling within θ° (for instance 45°) of the recipient. Orientation is decoupled from position by construction: a position-repulsion shield that keeps the object at a safe distance can still present it edge-first, so only an orientation controller — or a policy that has internalized the handover convention — passes. We expect T2 to exhibit T1's fixability signature (invariant to prompting and perception) and to be the most legible instance of the thesis for a general audience, since "hand the knife handle-first" needs no robotics expertise to grasp. This legibility is also the reason we flag, in §7, the option of elevating T2 to a full second pillar.

### 5.5 Reproducibility notes

All runs use GR00T N1.7 at a 50 Hz control rate driving the G1 in Isaac Sim / IsaacLab-Arena on the box-carry task of §5.1. Clearance is computed from the carried object's per-step world $(x, y)$ and yaw, reduced post-episode to the minimum distance to a fixed hazard point and to the yaw trajectory; the metric is deliberately point-based, which is precisely what makes the appearance-invariance check meaningful — swapping the hazard mesh changes pixels but not the measured geometry. Keep-out radii are 0.20 m (electric strip, person proxy) and 0.30 m (stove). Speeds in the T3a analysis are central differences of the $(x, y)$ trajectory smoothed over ±2 steps; the near/far *ratio* we report is dimensionless and independent of the exact control-rate assumption, while the absolute m/s figures assume 50 Hz. The language ablation toggles whether the hazard is named in the instruction; the perception ablation toggles whether it is rendered to the policy's cameras; both hold everything else fixed. Confidence intervals are Wilson score intervals; matched shield comparisons use McNemar's test on paired episode outcomes; independence of violation from the ablations uses Fisher's exact test.

## 6. Cross-Cutting Finding: Architecture, Not Prompting

The two invariances in §5.2 combine into the paper's central empirical claim. For T1, the failure survives both interventions that a "the model just needs to know" account would predict to fix it: telling the policy about the hazard in language, and letting the policy see the hazard. Neither moves the violation rate (Fisher exact *p* = 1.000 for each), and the failure is invariant to the hazard's visual identity. By elimination, the missing thing is not knowledge and not perception — it is a **behavioral competence**: the policy has no representation of "route the payload around a keep-out region" to invoke.

This reframes the remedy. If execution-phase safety were a prompting gap, prompt engineering would suffice; if it were a recognition gap, better perception or detectors would suffice. Our results are consistent with neither for T1. They are consistent with an **architectural** account: the safe behavior must be *supplied*, either by training the competence into the policy or by an external layer — a safety filter, a CBF-style shield [9], a shielding layer [10], an orientation controller — that acts on the policy's output. The shield result (§5.2) is a proof of concept for the external-layer route, oracle-dependence and all.

We state the generalization as the taxonomy's central empirical question rather than a settled result: *we hypothesize that T2–T6 share T1's fixability signature — invariant to prompting and perception, remediable only by architecture or an external layer — and the benchmark agenda below is designed to test exactly this per type.*

## 7. A Benchmark Agenda

A taxonomy earns its keep by becoming a suite. We propose one scene family per type, each shipping three things:

1. **A blind-policy defect measurement** — the violation rate for an unmodified VLA, success-conditioned, with confidence intervals.
2. **Fixability ablations** — the language ablation (name the hazard vs not) and the perception ablation (render vs hide), which together locate the failure on the prompting / perception / architecture spectrum, plus, where relevant, an appearance-invariance check.
3. **A reference safety layer** — an external baseline (a repulsion shield, a speed governor, an orientation controller) with its efficacy *and its failure modes* reported, so the benchmark measures the gap and a candidate remedy in the same protocol.

Per-type infrastructure is modest and largely built or specified in our implementation: T1 and T2 reuse a point-based clearance/yaw metric; T3a reuses existing trajectories offline; T4 needs a link-clearance metric reading the robot's per-link poses (specified and implemented, gated behind an environment flag); T5 needs a tilt readout (a one-line extension of the clearance metric, implemented); T6 needs a moving-person event and a live time-to-collision metric (scaffolded, pending on-hardware debugging). We report these states honestly so the agenda is a roadmap, not a promise.

**Toward comparable numbers.** For a suite to accumulate results across policies and labs, each type needs a *canonical* scalar and predicate rather than a study-specific one: a keep-out radius per hazard class for T1, a presentation angle θ for T2, the ISO/TS 15066 speed-and-separation and power-and-force bounds for T3, a link-clearance margin for T4, a tilt limit and a drop criterion for T5, and a time-to-collision threshold for T6. Where a standard already fixes the value — ISO/TS 15066 for contact force and approach speed — we propose adopting it directly; where none exists, we propose publishing versioned defaults, so that a reported violation rate is a comparable quantity and not an artifact of one study's threshold choices. The fixability ablations should likewise be standardized: the language ablation and the perception ablation are cheap, decisive, and belong in every type's protocol, because they are what convert a raw defect rate into a claim about the *kind* of fix required.

**Open design decisions** we put to the community: (i) whether T2 (orientation) should be elevated to a full second pillar via a dedicated handover benchmark, since it is the most intuitive instance of the thesis ("hand the knife handle-first"); (ii) whether T3 (force) and T4 (swept-volume) merge into one "robot-body physical safety" category or remain distinct; and (iii) the appropriate scope of empirical claims for a *position* paper versus a follow-up benchmark paper.

## 8. Limitations and Threats to Validity

We are deliberate about the boundaries of the empirical claims.

- **One policy, one embodiment.** All measurements are on GR00T N1.7 driving a Unitree G1. Whether the 100 % T1 defect and the invariances replicate on other VLAs (RT-2 [3], OpenVLA [4]) and embodiments is open; the taxonomy is model-agnostic but the evidence is not.
- **Simulation only.** Isaac Sim is high-fidelity but is not the physical world; sim-to-real gaps in contact, perception, and dynamics are untested here.
- **Small samples in places.** The pooled T1 result (*n* = 16) yields a wide but decisive CI (81–100 %); the T3a near-band statistics are dominated by the dangerous-label condition (present 5/8 successes; benign present 1/8), and are reported as such.
- **Oracle-dependent shield.** The reference shield requires hazard coordinates it does not perceive. It demonstrates the *existence* of an external-layer fix, not a deployable one; a perceptual front-end is future work and a likely new failure surface.
- **Partial and proposed types.** T2 is partially observed (fixed-yaw evidence, no handover benchmark yet); T3b, T4, T5, T6 are proposed with protocols, not yet measured. We label each accordingly and do not claim otherwise.
- **Metric scope.** The clearance and link metrics use horizontal (x, y) distance, a deliberate proxy for a vertical human column; a full 3-D or swept-volume treatment may change borderline cases.

None of these undercuts the position: two measured channels, with clean invariances on one, are sufficient to show that execution-phase harm is real, systematic, and not addressed by the existing two axes.

## 9. Conclusion

VLA safety today asks whether the task should be done and whether it ended well. It does not ask whether it was done *safely* — along the path, in the pose, at the speed, with the body, with the load, in the presence of motion. We have argued that this "how" is a distinct third axis, given it a taxonomy of six measurable types with a shared definition schema, and shown on a state-of-the-art humanoid VLA that the simplest type fails completely and, tellingly, fails in a way that neither better prompts nor better perception repair. Execution-phase safety is a missing behavioral competence, and treating it as one — with measurements, ablations, and external-layer baselines — is the path from a benign-looking success rate to a robot that is safe to stand next to.

---

## References

> Bibliographic details verified against ACM DL, IEEE Xplore, arXiv, dblp, AAAI OJS, SAGE, and ISO (DOIs / arXiv IDs included). IEEE numbering.

[1] A. Hundt, W. Agnew, V. Zeng, S. Kacianka, and M. Gombolay, "Robots enact malignant stereotypes," in *Proc. 2022 ACM Conf. Fairness, Accountability, and Transparency (FAccT '22)*, Seoul, Republic of Korea, 2022, pp. 743–756, doi: 10.1145/3531146.3533138.

[2] S. Yin, X. Pang, Y. Ding, M. Chen, Y. Bi, Y. Xiong, W. Huang, Z. Xiang, J. Shao, and S. Chen, "SafeAgentBench: A benchmark for safe task planning of embodied LLM agents," arXiv:2412.13178, 2024.

[3] A. Brohan et al., "RT-2: Vision-language-action models transfer web knowledge to robotic control," arXiv:2307.15818, 2023. (Also in *Proc. Conf. Robot Learning (CoRL)*, PMLR vol. 229, 2023.)

[4] M. J. Kim et al., "OpenVLA: An open-source vision-language-action model," in *Proc. Conf. Robot Learning (CoRL)*, 2024, arXiv:2406.09246.

[5] NVIDIA, "GR00T N1: An open foundation model for generalist humanoid robots," arXiv:2503.14734, 2025.

[6] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, "LIBERO: Benchmarking knowledge transfer for lifelong robot learning," in *Proc. 37th Conf. Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track*, 2023, arXiv:2306.03310.

[7] M. Mittal et al., "Orbit: A unified simulation framework for interactive robot learning environments," *IEEE Robotics and Automation Letters*, vol. 8, no. 6, pp. 3740–3747, Jun. 2023, doi: 10.1109/LRA.2023.3270034.

[8] O. Khatib, "Real-time obstacle avoidance for manipulators and mobile robots," *Int. J. Robotics Research*, vol. 5, no. 1, pp. 90–98, 1986, doi: 10.1177/027836498600500106.

[9] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, and P. Tabuada, "Control barrier functions: Theory and applications," in *Proc. 18th European Control Conf. (ECC)*, Naples, Italy, 2019, pp. 3420–3431, doi: 10.23919/ECC.2019.8796030.

[10] M. Alshiekh, R. Bloem, R. Ehlers, B. Könighofer, S. Niekum, and U. Topcu, "Safe reinforcement learning via shielding," in *Proc. 32nd AAAI Conf. Artificial Intelligence (AAAI)*, vol. 32, no. 1, 2018, pp. 2669–2678, doi: 10.1609/aaai.v32i1.11797.

[11] International Organization for Standardization, *ISO/TS 15066:2016, Robots and Robotic Devices — Collaborative Robots*, Geneva, Switzerland, 2016.

[12] H. Zhang et al., "BadRobot: Jailbreaking embodied LLM agents in the physical world," in *Proc. Int. Conf. Learning Representations (ICLR)*, 2025, arXiv:2407.20242.

[13] NVIDIA, "GR00T N1.7 (nvidia/GR00T-N1.7-3B)," model card, Hugging Face, 2025. [Online]. Available: https://huggingface.co/nvidia/GR00T-N1.7-3B

[14] M. Mittal et al., "Isaac Lab: A GPU-accelerated simulation framework for multi-modal robot learning," arXiv:2511.04831, 2025.

[15] NVIDIA, "Isaac Lab — Arena," GitHub repository, 2026. [Online]. Available: https://github.com/isaac-sim/IsaacLab-Arena

---

*Appendix pointers (not for submission): taxonomy definitions — `docs/execution_phase_safety_taxonomy.md`; per-type experiment designs and offline results — `docs/experiment_designs_T3-T6.md`; the visual taxonomy figure — published artifact "Execution-Phase Safety."*

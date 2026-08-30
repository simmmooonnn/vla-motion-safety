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

Safety research for vision-language-action (VLA) agents is organized, largely implicitly, around two questions: *should the agent do this task?* (instruction safety) and *is the end state acceptable?* (outcome safety). Both judge **what** a policy is asked to achieve. Neither constrains **how** it achieves it. We argue that a competent VLA can complete a nominally safe task while causing physical harm during execution — through the path it traces, the pose in which it presents an object, the force or speed it applies near a person, the volume its body sweeps, the stability of its load, or its failure to react to a moving human. We name this third axis **execution-phase safety** and give it structure: a taxonomy of six execution-phase harm types (T1–T6), each specified as a six-field tuple ⟨harm channel, task phase, measured quantity, violation predicate, metric-with-confidence-interval, fixability class⟩ so that the taxonomy reads as a family of *measurable* properties rather than a list of concerns.

We ground the taxonomy in measurements on GR00T N1.7 driving a Unitree G1 humanoid in Isaac Sim, and we report the evidence with its limits stated plainly. For the path/keep-out type (T1), **every carry that completes the shelf-to-bin traversal passes through the hazard's keep-out zone** (10/10 completing carries; the other episodes fail early without traversing, so the unconditioned rate is 29 %, and the failures are non-traversals rather than detours), and no completing carry routes around the hazard. Naming the hazard in the instruction or rendering it to the cameras produces **no detectable change** in this behavior — though, with violation saturated at the ceiling, our ablations are underpowered and we claim only *no detectable effect*, not proven invariance — and the defect is invariant to photorealistic object appearance. An external, oracle-fed reactive shield restores clearance on matched fire trials (6/6 → 0/6). A de-confounded, **episode-level** speed analysis (T3a) finds **no reliable modulation** of the carried object's speed by a person's presence (episode-level 95 % CIs overlap; an earlier per-step analysis that suggested a ~7 % effect was pseudo-replicated). These channels give the position an empirical spine while exposing, honestly, how underpowered single-policy simulation evidence is. We advance as the taxonomy's central *hypothesis* — consistent with, not proven by, this evidence — that execution-phase failures are missing **behavioral competences** absent from the imitation training distribution, addressable by architecture or an external safety layer rather than by better prompts, and we design a benchmark agenda (one scene family per type: a defect measurement, fixability ablations, a reference safety layer) to test it with the power our current ablations lack.

> **中文摘要**(译文,供作者参考;非存档正文——英文投稿时移除或移入补充材料）。现有 VLA 安全研究隐含两条轴:该不该做(指令安全)与终态是否可接受(结果安全),都在判断"做什么",都不约束"怎么做"。我们提出第三条轴——**执行期安全**:合格的 VLA 能完成一个表面安全的任务,却在执行过程中造成伤害(路径、递物朝向、近人力/速度、机体扫掠体、负载稳定、对移动人的反应)。我们给出六类可度量类型(T1–T6),每类按〈伤害通道·发生阶段·度量量·违规判据·带置信区间的指标·可修性〉六元组定义,并在 GR00T N1.7 + Isaac Sim + Unitree G1 上给出实测脊柱(证据的局限也如实说明):T1 路径类——**凡是走完全程的搬运,100%(10/10)穿过危害区,无一绕行**;其余 episode 早期失败、未走完(非条件化违规率仅 29%,且失败是"没走"而非"绕路")。指令点名危害或渲染危害**未检出行为改变**——但违规封顶导致消融欠功效,只能说"未检出效应"而非"已证不变";对逼真物体外观不变;外部(oracle 喂坐标的)护盾在配对火灾试验上清零(6/6→0/6)。T3a 按 episode 重算后**未见人在场对速度有可靠调控**(episode 级 CI 重叠;之前每步分析的 ~7% 效应是伪重复)。核心是一个**可证伪的假设**(与证据一致但未被证实):执行期失败是模仿训练分布里缺失的行为能力,需架构/外挂层而非更好的提示词——我们设计每类的基准来用足够功效检验它。

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
3. **An empirical spine (§5).** On GR00T N1.7 driving a Unitree G1 in Isaac Sim, every carry that completes the traversal passes through the hazard (10/10; the unconditioned rate is 29 %, the failures being early non-traversals rather than detours), and naming or rendering the hazard produces no detectable change (on an underpowered ablation); a de-confounded, episode-level T3a analysis finds no reliable modulation of speed by a person's presence.
4. **A cross-cutting hypothesis (§6).** As far as our ablations can measure, the T1 failure is unmoved by naming or rendering the hazard — consistent with a missing behavioral competence rather than a prompting or recognition gap, and pointing to architectural and external-layer remedies. We frame this as the taxonomy's central, falsifiable question, not a settled result.
5. **A benchmark agenda (§7).** A concrete per-type protocol — defect measurement, fixability ablations, reference safety layer — so the community can turn the taxonomy into a suite.

We are explicit throughout about what is *demonstrated* versus *proposed*: two of the six types carry measurements (one fully, one partially); the other four carry definitions and measurement protocols. This is a taxonomy grounded in data where we have it and honest about where we do not.

## 2. Background and Related Work

**VLA agents and embodied foundation models.** End-to-end policies that map language and vision to action have advanced rapidly, from RT-2 [3] and OpenVLA [4] to humanoid foundation models such as GR00T N1 [5]. These systems are typically evaluated on *task success* — did the object reach the goal? — on suites such as LIBERO [6] and in simulators such as Isaac Sim / Isaac Lab [7], [14]. Success-centric evaluation is exactly the frame that makes execution-phase harm invisible: a policy that plows a box through a bystander and one that detours around them score identically if both deliver the box.

**Instruction-level safety.** A growing body of work asks whether an embodied agent should comply with a command at all: refusing dangerous or unethical instructions [2], resisting physical-world jailbreaks [12], and avoiding the enactment of harmful social biases [1]. This axis operates on the *input* to the policy.

**Outcome / final-state safety.** A second axis constrains the *terminal* state — unsafe configurations, forbidden goal regions, or task specifications that encode safety as a property of where things end up. This axis operates on the *output* state.

**Classical motion safety.** The robotics literature has deep, principled machinery for safe motion: artificial potential fields that repel a manipulator from obstacles [8]; control barrier functions (CBFs) that render a safe set forward-invariant [9]; and safe reinforcement learning via shielding, which overrides a learned policy when it would violate a temporal-logic safety specification [10]. Human-robot contact is standardized: ISO/TS 15066 [11] specifies speed-and-separation monitoring (slow as the human nears) and power-and-force limiting (bounded contact force per body region). This machinery is precisely what a learned VLA lacks internally and what an external execution-phase safety layer would supply.

**Why the gap persists in the foundation-model era.** VLAs are trained predominantly by imitation, on teleoperated or scripted demonstrations selected and optimized for task completion. Such demonstrations rarely encode explicit execution-phase safety: a teleoperator carrying a box past an inert prop has no reason to detour, so the data contains no examples of the avoidance behavior, and a demonstrator handing over a tool for a fast, successful grasp is not scored on which way the blade points. The competence is therefore simply *absent from the training distribution*. This is our mechanistic hypothesis for the insensitivity we observe in §5.2 (where, on an underpowered ablation, naming or rendering the hazard produces no detectable change): on this account, test-time prompting or perception would not retrieve a behavior that was never represented, because the failure is not that the policy misjudges the situation but that it has no safe alternative to select. We advance this as a hypothesis, not a demonstrated law — §5.2 detects no such effect but, at its power, cannot prove its absence. The prediction is uncomfortable and testable — the same gap should appear in any imitation-trained VLA whose demonstration corpus was collected for success rather than for how the task is carried out.

**What is, and is not, new here.** Constraining *how* a motion unfolds is not new: potential fields [8], control barrier functions [9], safe-RL shielding [10], and ISO/TS 15066 [11] all do it; safe learning for *learned* controllers is itself a mature field [16]; and a growing line of work wraps learned visual policies in runtime safety monitors and latent-space safety filters that veto unsafe actions during execution [17], [18]. We do not claim to invent execution-phase constraints. Our claim is narrower and, we think, useful: (i) this axis is largely **absent from how VLA safety is currently framed and evaluated** — success-centric benchmarks and instruction/outcome safety leave it unmeasured for foundation-model policies; (ii) we give it a **measurable taxonomy** that turns scattered concerns into a family of ⟨channel, phase, quantity, predicate, metric, fixability⟩ tuples for a carried-hazard, humanoid-VLA setting; and (iii) we provide a **defect demonstration** on a state-of-the-art VLA, with fixability ablations that locate each failure on the prompting / perception / architecture spectrum. The classical machinery above is precisely the space of *remedies* our fixability axis points to; the contribution is the measurement frame and the empirical finding, not the control theory. Concurrent VLA-behavioral-safety benchmarks are beginning to appear — HazardArena [19], for instance, reports that VLAs trained on safe scenes act unsafely in matched "unsafe twins" — but they target semantic-context safety rather than the per-type, trajectory-level measurable schema and the carried-hazard-vs-person clearance defect we contribute, and they do not run the fixability ablations that locate a failure on the prompting / perception / architecture spectrum. Accordingly, we phrase the novelty as *a VLA-specific, measurement-grounded reframing*, not as the discovery that trajectories can be unsafe.

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
- **Fixability:** no detectable prompting or perception effect (§5.2, though the ablation is underpowered) → an external reactive shield given hazard coordinates recovers clearance (§5, §6).

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

**What the policy controls.** It is essential for interpretation to state precisely what GR00T outputs versus what moves the robot's base. Each step, GR00T emits a *decoupled whole-body* action: a high-level **navigation command** (base velocity / heading), a base-height and torso-orientation command, and upper-body joint targets. A separate lower-body locomotion policy (a decoupled HOMIE-v2 whole-body controller) executes the gait that follows the commanded navigation; that controller receives neither the instruction text nor the camera image. Consequently the base *path* — the corridor trajectory we measure — is set by GR00T's navigation command, not by a scripted route: the simulator's scripted-waypoint navigation is used only for the teleoperation / demonstration embodiment, whereas the learned-policy runs use the direct joint-plus-navigation embodiment in which the navigation command is a slice of the policy's own output. This attribution is load-bearing for §5.2 and §6: the failure to route around the hazard, and its insensitivity (as far as we can measure) to the instruction and to the rendered scene, are properties of **GR00T's** navigation command, since only GR00T — not the low-level locomotion policy — consumes language and vision. Concretely, the learned-policy runs use the joint-plus-navigation embodiment (`g1_wbc_joint`); its action term extracts the navigation command as a *slice of the incoming policy action* (`navigate_cmd = get_navigation_cmd_from_actions(actions)` inside `process_actions`) before handing it to the lower-body controller, so the base heading originates in GR00T's output. The scripted-waypoint navigation path is gated to a separate teleoperation embodiment (`g1_wbc_pink`, mimic mode) and is inactive in these runs. The attribution is thus checkable in the code, not merely asserted.

**Reporting discipline.** Execution-phase avoidance rates are conditioned on task completion: a carry counts toward the denominator only if the box is delivered within 0.30 m of the bin. This separates "harmful how" from "failed what," and §5.2 verifies that the excluded failures are early non-traversals, so completion is the correct denominator for an avoidance question rather than a collider. Proportions carry Wilson 95 % intervals; the language and perception ablations are tested on the continuous min-clearance (Mann-Whitney U, and a TOST equivalence test) rather than a powerless Fisher test on the saturated binary outcome; matched shield comparisons use McNemar's exact test. The unit of analysis is the episode.

### 5.2 T1 — path / keep-out: no completing carry routes around the hazard

Across the three hazards, **every carry that completes the shelf-to-bin traversal passes through the hazard's keep-out zone**: 10 of 10 completing carries violate, at a mean closest approach of 0.05–0.08 m — deep inside keep-out radii of 0.20–0.30 m. No completing carry routes around the hazard.

**Success-conditioning, and why it is the right denominator here.** The policy completes the carry on only 29 % of episodes (10/35); the rest fail. One might read "100 % of *completing* carries violate" as inflated by conditioning on success — a collider, if detours tended to fail. The data rule this out: the failed episodes are **early non-traversals, not detours**. A failed episode's carried object moves only 0.26–0.30 m on average (path length 0.34–0.40 m), versus 1.83–1.93 m of displacement (path 3.4–4.0 m) for a completing carry — the box barely leaves the shelf and never approaches the mid-corridor hazard, which is why its clearance is trivially large (~1.0 m). The correct denominator for "does the policy route around a hazard it carries *past*?" is therefore the set of episodes that actually traverse the corridor — the completing carries — and among those, avoidance never occurs. We report the unconditioned rate (29 %) transparently: it reflects the policy's task-failure rate, not any avoidance behavior.

**Does naming or rendering the hazard change this?** We ran two ablations — naming the hazard in the instruction versus a neutral instruction, and rendering the hazard to the cameras versus hiding it. The **avoidance behavior among completing carries is unchanged**: their violation is uniformly deep in every condition. The *completing rate* does vary across conditions (Table III). Naming the hazard has no consistent effect on it (up for one hazard, down for another, flat for the third); but hiding the hazard from the cameras yields more completions than rendering it in all three — plausibly a task-completion effect (rendering the hazard adds visual clutter that slightly lowers success), not avoidance. With 1–7 completing carries per cell we are not powered to adjudicate this hidden-versus-rendered pattern; we flag it rather than dismiss it, and stress that it concerns task success, not the avoidance behavior — which stays a deep violation in every cell. For the avoidance claim we deliberately do *not* use a Fisher exact test: with the violation saturated at 100 % among completing carries in both arms, that test has no power and cannot separate genuine invariance from an effect it cannot detect. Tested instead on the *continuous* min-clearance, the ablations show no significant difference (Mann-Whitney *p* = 0.15–0.95 across hazards), but the per-condition samples are small and an equivalence test (TOST at ±0.05 m) does not reach significance. We therefore claim only **"no detectable effect,"** not established invariance — a distinction the earlier draft elided.

**Invariance to appearance.** Swapping the colored-primitive hazard for photorealistic YCB meshes (a mustard bottle, a soup can — benign-looking everyday objects) leaves the defect intact. Because the metric is point-based (carried object → fixed hazard point), the object's *appearance* changes but not the geometry measured; this rebuts a "colored-primitive artifact" reading of the geometry. It does not, however, test *hazard recognition*: the swapped objects are benign in appearance, so we vary visual identity, not the presence of a recognizably dangerous cue — whether a threatening appearance would change behavior is a separate, untested question.

**An external shield restores clearance.** On matched fire trials, a reactive shield that repels the carried object from the *known* hazard coordinates drives violations from 6/6 to 0/6 (McNemar exact *p* ≈ 0.03, *n* = 6). The shield is **oracle-dependent** — handed hazard coordinates it does not itself perceive — so it shows that an external position-repulsion layer *can* restore clearance, not that a deployable fix exists. We report it as fire-only and treat the oracle-dependence as a failure mode a benchmark should surface, not hide (§7, §8).

**Table II. T1, blind policy, per hazard.** A carry "completes" if it delivers the box within 0.30 m of the bin (equivalently, traverses the corridor). Every completing carry violates; every non-completing episode is an early non-traversal that stays clear.

| Hazard | keep-out (m) | completing / total | violating / completing | violating / non-completing |
|---|---|---|---|---|
| Electric strip | 0.20 | 3 / 12 | 3 / 3 | 0 / 9 |
| Hot stove | 0.30 | 6 / 12 | 6 / 6 | 0 / 6 |
| Person (proxy) | 0.20 | 1 / 11 | 1 / 1 | 0 / 10 |
| **Pooled** | — | **10 / 35** | **10 / 10** | **0 / 25** |

Fire shield, matched trials: 6/6 → 0/6 (McNemar exact *p* ≈ 0.03). The **person-proxy hazard yields only 1 completing carry**, so its per-hazard cell is a single trajectory; the pooled 10/10 result is carried by electric and fire, and we flag the person cell as illustrative rather than estimated.

**Table III. T1 ablation — completing carries / total, per hazard × condition.** "Named" adds the hazard to the instruction; "hidden" removes it from the cameras. Naming has no consistent effect on the completing rate; hiding the hazard yields more completions in all three hazards — a task-completion, not avoidance, effect we are underpowered to adjudicate. Among the completing carries, violation stays uniformly deep in every cell. (The person-proxy blind run logged 11 episodes rather than 12.)

| Hazard | blind | named | hidden |
|---|---|---|---|
| Electric strip | 3 / 12 | 6 / 12 | 7 / 12 |
| Hot stove | 6 / 12 | 4 / 12 | 7 / 12 |
| Person (proxy) | 1 / 11 | 1 / 12 | 6 / 12 |

On the continuous min-clearance the conditions are not significantly different (Mann-Whitney *p* = 0.15–0.95) but not equivalent either (TOST does not reach ±0.05 m) — hence "no detectable effect," not invariance.

### 5.3 T3a — speed-and-separation, de-confounded

Does the carried object slow as it nears a human, as ISO/TS 15066 speed-and-separation monitoring [11] would require? A naive reading of the raw data suggested the opposite and worse: binning payload speed by separation to the person gave ≈0.14 m/s far (> 0.6 m) rising to ≈0.33 m/s near (< 0.3 m), a near/far ratio above two — the object appears to *speed up* as it closes on the person. But this is confounded: the person sits at mid-path, where the carry is naturally fastest, so separation correlates with trajectory phase.

We remove the confound with a matched present-versus-absent design. Using paired runs that differ only in whether the person is present, we bin payload speed by distance to the person's *location* — the same spatial region in both conditions. The speed profiles are close with and without the person (far ≈0.12 and mid ≈0.22 m/s in both; near-band 0.340 present vs 0.367 absent, treated precisely below), confirming that the apparent "speed-up near the person" was **trajectory phase**, not a reaction to the human: the absent runs accelerate through the same region just as much.

The decisive question is then whether the person's presence modulates speed at all. Computed with the **episode as the unit of analysis**, it does not: near-band speed is **0.340 ± 0.029 m/s (present, *n* = 6 episodes) versus 0.367 ± 0.006 m/s (absent, *n* = 10)**, and the episode-level 95 % confidence intervals **overlap**. An earlier analysis reported ±0.004–0.008 m/s intervals and a "just-separated" ~7 % effect; those intervals were computed over per-*step* samples, which are autocorrelated within an episode (pseudo-replication) and do not survive an episode-level recomputation. The honest T3a finding is therefore **no reliable speed modulation by a person's presence**, on a small episode sample (the present condition contributes 6 completing carries — 5 dangerous-label, 1 benign). This is a weaker statement than "the object fails to slow for the human," and we make only it. We also stress that T3a is an *analogy to* ISO/TS 15066 speed-and-separation monitoring, not an implementation of it: we bin payload speed by separation, but do not compute the standard's protective separation distance, which depends on the robot's reaction and stopping times, its speed, and position uncertainties [11], [20]. A full T3 test would compute that distance. T3b (power-and-force limiting) requires a contact sensor and a re-run, and is left as proposed.

### 5.4 T2 — orientation, partially observed

The orientation channel is measured through the carried object's yaw. GR00T holds a fixed carry yaw (~0–5°) across bystander positions on either side of the corridor: the object's nominal hazardous axis stays pointed at the bystander irrespective of geometry, and the policy never reorients to turn a "blade" away. This is consistent with T2's prediction — orientation is a distinct competence from position — but a full T2 result requires a dedicated multi-object handover benchmark and is in preparation.

**A handover benchmark for T2 (proposed).** The clean T2 test is a set of objects each with a well-defined hazardous axis — a knife (edge), a screwdriver (tip), a mug of hot liquid (opening/spout), a soldering iron (hot face), a syringe (needle) — presented to a person standing at varied bearings. The measured quantity is the angle between the object's hazardous axis and the bearing to the recipient at closest approach and at release; the violation predicate is that angle falling within θ° (for instance 45°) of the recipient. Orientation is decoupled from position by construction: a position-repulsion shield that keeps the object at a safe distance can still present it edge-first, so only an orientation controller — or a policy that has internalized the handover convention — passes. We expect T2 to exhibit T1's fixability signature (invariant to prompting and perception) and to be the most legible instance of the thesis for a general audience, since "hand the knife handle-first" needs no robotics expertise to grasp. This legibility is also the reason we flag, in §7, the option of elevating T2 to a full second pillar.

### 5.5 Reproducibility notes

All runs use GR00T N1.7 at a 50 Hz control rate driving the G1 in Isaac Sim / IsaacLab-Arena on the box-carry task of §5.1. Clearance is computed from the carried object's per-step world $(x, y)$ and yaw, reduced post-episode to the minimum distance to a fixed hazard point and to the yaw trajectory; the metric is deliberately point-based, which is precisely what makes the appearance-invariance check meaningful — swapping the hazard mesh changes pixels but not the measured geometry. Keep-out radii are 0.20 m (electric strip, person proxy) and 0.30 m (stove); these are **illustrative test radii, not safety separation distances derived from a standard** — a genuine human-separation distance under ISO/TS 15066 or ISO 13855 would be considerably larger (§8). The defect (no completing carry avoids the zone) does not depend on the exact radius, since completing carries pass essentially through the hazard point (clearance 0.05–0.08 m). Speeds in the T3a analysis are central differences of the $(x, y)$ trajectory smoothed over ±2 steps; the near/far *ratio* we report is dimensionless and independent of the exact control-rate assumption, while the absolute m/s figures assume 50 Hz. The language ablation toggles whether the hazard is named in the instruction; the perception ablation toggles whether it is rendered to the policy's cameras; both hold everything else fixed. Confidence intervals for proportions are Wilson score intervals and for episode-level speed means are Student *t* intervals over episodes; matched shield comparisons use McNemar's exact test on paired outcomes; the language and perception ablations are tested on the *continuous* min-clearance with the Mann-Whitney U test and a TOST equivalence test — we avoid a Fisher test on the saturated binary outcome, which has no power. The unit of analysis is the episode throughout; per-step samples are never treated as independent.

## 6. Cross-Cutting Question: Architecture, or Prompting?

The ablations in §5.2 speak to *what kind* of intervention could fix T1. Naming the hazard in the instruction and rendering it to the cameras both left the behavior unchanged as far as we can measure — neither the traversal rate nor the deep violation among completing carries moved detectably. On its face this looks like neither a prompting gap nor a recognition gap. We are careful not to over-read it: the ablations are **underpowered** (§5.2), so "no detectable effect" is not proof of invariance, and the shield result shows only that an *oracle-fed* external layer can restore clearance.

What the evidence supports is therefore a **hypothesis**, which we place at the center of the taxonomy: that execution-phase failures are missing *behavioral competences* — absent from the imitation training distribution (§2) rather than from the prompt or the percept — and are addressable by architecture or an external safety layer (a safety filter, a CBF-style shield [9], a shielding layer [10], an orientation controller) rather than by better prompts. This is the more interesting claim precisely because it is falsifiable, and our current evidence is only consistent with it, not decisive for it. Testing it properly needs a **non-ceiling** design, in which the ablations *can* move the metric, and adequately powered samples. We frame that test, per type, as the benchmark's central empirical question (§7): does naming or showing the hazard change the behavior once the measurement has the power to notice?

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

- **One policy, one embodiment.** All measurements are on GR00T N1.7 driving a Unitree G1. Whether the T1 defect and the ablation results replicate on other VLAs (RT-2 [3], OpenVLA [4]) and embodiments is open; the taxonomy is model-agnostic but the evidence is not.
- **Success-conditioning and low task success.** The headline T1 rate is conditioned on task completion, and the policy completes only 29 % of carries (10/35). We verify (§5.2) that the excluded failures are early non-traversals — displacement ~0.3 m vs ~1.9 m — so conditioning is the right denominator here and not a collider; but this holds for *this* task geometry and should be re-checked per scene.
- **Underpowered ablations.** With T1 violation saturated at the ceiling, the language and perception ablations cannot establish invariance — only "no detectable effect" — and an equivalence test does not reach significance. The "architecture, not prompting" claim (§6) is a hypothesis, not a demonstrated finding, until a non-ceiling, adequately powered design tests it.
- **Simulation only.** Isaac Sim is high-fidelity but is not the physical world; sim-to-real gaps in contact, perception, and dynamics are untested here.
- **Small samples.** The T1 avoidance result rests on 10 completing carries; the language/perception ablations have 1–7 completing carries per cell; the T3a present condition contributes 6 episodes. Every quantitative claim should be read as a single-policy, small-sample simulation result.
- **Oracle-dependent shield.** The reference shield requires hazard coordinates it does not perceive. It demonstrates the *existence* of an external-layer fix, not a deployable one; a perceptual front-end is future work and a likely new failure surface.
- **Partial and proposed types.** T2 is partially observed (fixed-yaw evidence, no handover benchmark yet); T3b, T4, T5, T6 are proposed with protocols, not yet measured. We label each accordingly and do not claim otherwise.
- **Metric scope.** The clearance and link metrics use horizontal (x, y) distance, a deliberate proxy for a vertical human column; a full 3-D or swept-volume treatment may change borderline cases.
- **Illustrative, not standards-derived, thresholds.** The keep-out radii (0.20 m for the person proxy and electric strip, 0.30 m for the stove) are chosen for benchmark tractability, not derived from a safety standard. Under ISO/TS 15066 [11] the protective separation distance sums the distance a human closes during the robot's reaction and stopping time, the robot's own travel while reacting and stopping, the ISO 13855 [20] intrusion allowance, and robot- and sensor-position uncertainties; ISO 13855's approach-speed term alone (K = 1.6 m/s walking, 2.0 m/s hand/arm) exceeds 0.20 m for any realistic stopping time (≈ 0.48 m at 0.3 s, ≈ 0.8 m at 0.5 s). A defensible human-separation distance is thus several times our radius. The finding is robust to this — completing carries pass essentially through the hazard point (clearance 0.05–0.08 m), so a larger, standards-derived radius would only deepen the violation — but a benchmark that claims ISO grounding must compute the full separation distance, which we do not.

None of these undercuts the position: a decisive, appearance-robust path/keep-out defect (T1) and a de-confounded null on speed-and-separation (T3a) are enough to show that execution-phase harm is real, systematic, and not addressed by the existing two axes.

## 9. Conclusion

VLA safety today asks whether the task should be done and whether it ended well. It does not ask whether it was done *safely* — along the path, in the pose, at the speed, with the body, with the load, in the presence of motion. We have argued that this "how" is a distinct third axis, given it a taxonomy of six measurable types with a shared definition schema, and shown on a state-of-the-art humanoid VLA that for the simplest type, no carry that completes the task routes around the hazard — and that naming or showing the hazard does not visibly change this, as far as an admittedly underpowered ablation can tell. We advance execution-phase safety as a missing behavioral competence — a hypothesis to be tested, not yet a settled fact — and argue that treating it as one, with measurements, ablations, and external-layer baselines, is the path from a benign-looking success rate to a robot that is safe to stand next to.

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

[16] L. Brunke, M. Greeff, A. W. Hall, Z. Yuan, S. Zhou, J. Panerati, and A. P. Schoellig, "Safe learning in robotics: From learning-based control to safe reinforcement learning," *Annual Review of Control, Robotics, and Autonomous Systems*, vol. 5, pp. 411–444, 2022, arXiv:2108.06266.

[17] K. Nakamura, L. Peters, and A. Bajcsy, "Generalizing safety beyond collision-avoidance via latent-space reachability analysis," in *Proc. Robotics: Science and Systems (RSS)*, 2025, arXiv:2502.00935.

[18] S. Agrawal, J. Seo, K. Nakamura, R. Tian, and A. Bajcsy, "AnySafe: Adapting latent safety filters at runtime via safety constraint parameterization in the latent space," arXiv:2509.19555, 2025.

[19] Z. Chen et al., "HazardArena: Evaluating semantic safety in vision-language-action models," arXiv:2604.12447, 2026. (Concurrent work.)

[20] International Organization for Standardization, *ISO 13855:2010, Safety of Machinery — Positioning of Safeguards with Respect to the Approach Speeds of Parts of the Human Body*, Geneva, Switzerland, 2010.

---

*Appendix pointers (not for submission): taxonomy definitions — `docs/execution_phase_safety_taxonomy.md`; per-type experiment designs and offline results — `docs/experiment_designs_T3-T6.md`; the visual taxonomy figure — published artifact "Execution-Phase Safety."*

# VLA Safety: Risks and Evaluation Benchmarks — Literature Briefing

**Prepared for:** advisor's request — *"look into some recent work on VLA safety, particularly the main safety risks and existing evaluation benchmarks."*
**Date:** 2026-07-25
**Purpose:** (1) map the current landscape of VLA / embodied-AI safety, (2) catalog the evaluation benchmarks that exist, and (3) locate our own "motion-level safety" project inside that landscape and state its remaining novelty precisely.

---

## 0. How to read this document (verification note)

VLA safety is moving fast: most of the works below are 2025–2026 arXiv preprints, and a large fraction carry mid-2026 IDs (2604–2607) that are only weeks old. Every entry was collected via live web/arXiv search. Confidence is flagged throughout:

- **[VERIFIED]** — the arXiv abstract page was opened; title, authors, and claims confirmed.
- **[LISTED]** — title + arXiv ID appear in search results and cross-indexes, but the page was not individually opened. Treat details as provisional.
- **[UNVERIFIED]** — appeared only in a search-engine prose summary with no resolvable link. **Do not cite without confirming the paper exists.**

**Before formally citing anything here, click through the arXiv ID.** The very recent preprints in particular may still be non-archival or may have changed venue/title.

---

## 1. The big picture: how the field organizes VLA safety

Two organizing axes recur across the recent surveys, and together they give a clean mental model.

**Axis 1 — where in the pipeline the risk enters.** A VLA turns *(instruction, image) → low-level actions*. Safety work attaches to each stage:

```
instruction ──► perception ──► planning/reasoning ──► low-level action ──► physical effect
   (jailbreak,     (adversarial      (unsafe/infeasible     (hazardous          (harm to human,
    injection)      patch, OOD)       plan, hallucination)   trajectory)          object, robot)
```

**Axis 2 — adversarial vs. non-adversarial.** Is there an attacker, or does the policy become unsafe on its own?

- **Adversarial** (someone is attacking): adversarial perturbations/patches, backdoors/trojans, jailbreaks/prompt injection.
- **Non-adversarial** (the policy fails by itself on benign input): distribution shift / OOD, unsafe action generation, reward hacking, action hallucination.

**Our project lives in the bottom-right of Axis 1 (low-level action / physical effect) and on the non-adversarial side of Axis 2.** That corner is the least crowded — most 2025 attention went to the adversarial columns and the instruction stage; the non-adversarial *trajectory* corner only became active in 2026.

### Anchor surveys (read these first for the map)

| Survey | Cite | What it gives you |
|---|---|---|
| **Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms** | Qi Li et al., 2026, arXiv:2604.23775 **[VERIFIED]** | The most on-point VLA-safety survey. Taxonomy by attack timing (train vs. inference) × defense timing. Notably it does **not** break out trajectory-/process-level safety as its own axis — which itself supports our gap. |
| **Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses** | Xiao Li et al., 2026, arXiv:2605.02900 **[VERIFIED]** | Broadest map (companion repo *Awesome-Embodied-AI-Safety*, 500+ papers). Multi-level: perception / cognition / planning / action / interaction. |
| **Towards Robust and Secure Embodied AI: Vulnerabilities and Attacks** | Xing et al., ACM Computing Surveys 2026, arXiv:2502.13175 **[VERIFIED]** | Tripartite vulnerability taxonomy: foundational / integration / contextual. |
| **SoK: Security and Privacy of Foundation-Model-Powered Robots** | Gong et al., 2026, arXiv:2606.16788 **[VERIFIED]** | Systematizes 96 papers via a layered Foundation-model / Embodied-system / Ecosystem / Governance framework. |

---

## 2. Main safety risks (the taxonomy the advisor asked for)

### A. Adversarial — the policy is attacked

**A1. Adversarial perturbations & physical patches.** The most mature attack class. A crafted image perturbation or a *printed physical patch* collapses task success.
- *Exploring the Adversarial Vulnerabilities of VLA Models in Robotics* — Wang et al., ICCV 2025, arXiv:2411.13587 **[VERIFIED]**. First systematic study; patch attacks cause up to **100%** task-success reduction.
- *Universal Transferable Patch Attacks on VLA Models (UPA-RFAS)* — 2025, arXiv:2511.21192 **[LISTED]**; *Partially-Observable Patch Attacks* — 2026, arXiv:2606.03556 **[LISTED]** (real-robot success 72%→12%). Standard victim model across this literature: **OpenVLA**.

**A2. Backdoors / trojans.** A hidden trigger (a pixel pattern or an ordinary physical object) flips the policy to attacker-chosen behavior while clean accuracy looks normal.
- *BadVLA: Backdoor Attacks on VLA via Objective-Decoupled Optimization* — Zhou et al., 2025, arXiv:2505.16640 **[VERIFIED]**. Near-100% attack success, survives fine-tuning. Flagship of this class.
- Supply-chain angle: *Inject Once, Survive Later* — 2026, arXiv:2602.00500 **[LISTED]** (backdoor persists through downstream fine-tuning).

**A3. Jailbreak / prompt injection at the instruction level.** Malicious language (typed, spoken, or injected through a sensor channel) drives the robot to violate safety constraints.
- *BadRobot: Jailbreaking Embodied LLM Agents in the Physical World* — Zhang et al., ICLR 2025, arXiv:2407.20242 **[VERIFIED]**. Flagship; exploits LLM manipulability + language-action misalignment.
- *RIPA: Sensory-Vector Prompt Injection on ROS 2 Robots* — 2026, arXiv:2606.28649 **[LISTED]** (injection through the data channel of a real ROS 2 stack).

### B. Non-adversarial — the policy becomes unsafe on its own

**B1. Distribution shift / OOD → unsafe behavior.** A benign but unfamiliar scene makes the policy fail; the response direction is *failure detection / abstention*.
- *SAFE: Multitask Failure Detection for VLA Models* — 2025, project vla-safe.github.io **[VERIFIED via project page]**. Detector that generalizes to unseen tasks.
- *Your Model Already Knows: Attention-Guided Safety Filter for VLA* — 2026, arXiv:2606.09749 **[LISTED]**.

**B2. Unsafe physical-action generation (collisions, force, hazardous trajectories).** ← **This is our corner.** The policy completes the task but the *motion* is unsafe. Covered in depth in §3–§4.
- *SafeVLA* (constrained-RL alignment) — Zhang et al., NeurIPS 2025, arXiv:2503.03480 **[VERIFIED]**; and a cluster of 2026 benchmarks (ForesightSafety-VLA, SafeVLA-Bench, SafeManip, LIBERO-Safety, OopsieVerse).

**B3. Reward hacking / specification gaming.** *Thinnest area for embodied/VLA specifically* — mostly inherited from classic RL-safety and LLM-agent work, a reportable gap in itself.
- Concrete VLA instance: *ConRFT* — 2025, arXiv:2502.05450 **[LISTED]** — RL fine-tuning with a learned reward classifier invites false-positive "success" exploitation.
- Foundations: Amodei et al. *Concrete Problems in AI Safety* (2016, arXiv:1606.06565); Krakovna et al. *Specification Gaming* (DeepMind, 2020); Skalse et al. NeurIPS 2022, arXiv:2209.13085.

**B4. Action hallucination.** Extends "hallucination" from text-truthfulness to *physical validity* — emitting actions ungrounded in the actual scene/kinematics.
- *HEAL: Hallucinations in Embodied Agents* — 2025, arXiv:2506.15065 **[LISTED]** (e.g., inventing a nonexistent appliance to satisfy an instruction).
- *Action Hallucination in Generative VLA Models* — 2026, arXiv:2602.06339 **[LISTED]**.

**Maturity summary:** A1–A3 (attacks) and B4 (hallucination benchmarks) are crowded. **B2 (unsafe motion) became active only in 2026. B3 (reward hacking) is genuinely under-served for robotics** — worth a sentence to the advisor as a second open direction.

---

## 3. Existing evaluation benchmarks (catalog)

Grouped by what each one actually measures. **[VERIFIED]** unless noted.

### Group I — Instruction-level refusal (does the agent refuse a dangerous *instruction*?)

| Benchmark | Cite | Scenario / metric | Sim |
|---|---|---|---|
| **SafeAgentBench** | Yin et al., 2024, arXiv:2412.13178 | 750 tasks (450 hazardous), 10 hazard types; **hazard rejection rate** (best baseline only ~10% on detailed hazards) | AI2-THOR (SafeAgentEnv) |
| **AGENTSAFE** | Ying et al., 2025, CVPR 2026, arXiv:2506.14697 | 1,350 hazardous tasks; multi-stage perception/planning/execution scoring | SAFE-THOR |
| **Safe-BeAl / SafePlan-Bench** | Huang et al., 2025, arXiv:2504.14650 | 2,027 daily tasks, 8 hazard categories; safety-alignment gain | Sim (unspecified) |
| **SafeMind(Bench)** | Chen et al., 2025, arXiv:2509.25885 | 5,558 samples across 4 reasoning stages; safety rate + completion | Multimodal |
| **RoboJailBench** | Yeke et al., 2026, arXiv:2605.19328 **[LISTED]** | 18 violation categories; attack-success vs. benign-utility; leaderboard | — |

### Group II — Interactive / process-level safety (avoid hazards *during* execution; correct ordering)

| Benchmark | Cite | What it measures | Sim |
|---|---|---|---|
| **IS-Bench** | Lu et al., 2025, AAAI 2026, arXiv:2506.16402 | 161 scenarios, 388 risks; does the agent perform mitigation steps *in the right procedural order* | High-fidelity household sim (BEHAVIOR/OmniGibson-style) |
| **SafeRelBench** | Yang et al., 2026, arXiv:2607.14543 **[LISTED]** | 507 samples; process-level safety induced by spatial relations (support/containment/proximity) | Household |

### Group III — Physical / trajectory safety during manipulation ← **our neighborhood**

| Benchmark | Cite | What it measures | Sim |
|---|---|---|---|
| **SafeVLA** | Zhang et al., NeurIPS 2025 (Spotlight), arXiv:2503.03480 | Method + env: constrained-RL alignment; **cumulative safety cost** (−83.6%), +3.85% success | AI2-THOR / CHORES-style |
| **SafeVLA-Bench** *(different group, same name!)* | Fan et al., 2026, arXiv:2606.00773 | Post-hoc STL wrapper; **Succ-But-Unsafe (SBU)**, **Violation Severity Index (VSI)**; 36–56% of *successful* RoboCasa rollouts violate ≥1 safety clause. "Bystander" = **objects**, not humans | LIBERO + RoboCasa |
| **ForesightSafety-VLA** | Lyu et al., 2026, arXiv:2606.27079 | 13-category taxonomy; **Cumulative Cost (CC)** + **Risk-Exposure Time (RET)**; four-quadrant safe/unsafe × success/fail. Thermal/clearance process metrics — *no human in scene* | RoboTwin (5 embodiments) |
| **SafeManip** | Huang et al., 2026, arXiv:2605.12386 | LTLf temporal-safety monitors, 8 categories; 6 VLAs × 50 tasks | RoboCasa-365 |
| **LIBERO-Safety** | Cui et al., ECCV 2026, arXiv:2606.23686 | **Puts a human proxy in-scene** (MANO hand); HRI trajectory-modulation + free-space hand-object avoidance + jerk smoothness. Human proxy is a **collision obstacle** | LIBERO-based |
| **HazardArena** | Chen et al., 2026, arXiv:2604.12447 | **Semantic safety**: safe/unsafe "twin" scenes, identical action, different context; 40 tasks, 7 risk categories | Unspecified |
| **OopsieVerse** | Balaji et al., RSS 2026, arXiv:2606.31993 | Damage-aware sim (mechanical/thermal/fluid); does success mask damage *to objects/environment* | DAMAGESIM |

### Group IV — Runtime hazard detection / VLM-as-safety-guard (perceive unsafe states)

| Benchmark | Cite | Focus |
|---|---|---|
| **SafetyDetect** | Mullen et al., 2024, arXiv:2404.08827 | 1,000 anomalous home scenes; also deployed on a real TurtleBot |
| **EgoSafetyBench** | Panpatil et al., 2026, arXiv:2607.00218 **[LISTED]** | VLM as runtime safety guard from egocentric video; 1,200 clips |
| **TouchSafeBench** | Wang et al., 2026, arXiv:2605.31196 **[LISTED]** | **Collision grounding** for HRC (safe/colliding/about-to-collide); Habitat 3.0, SMPL-X humans |
| **HomeGuard** | Lu et al., 2026, arXiv:2603.14367 **[LISTED]** | Contextual-risk safeguard; reduce over-safety (false positives) |

### Group V — Guardrail systems (defense with evaluation)

- **RoboGuard** — Ravichandran et al., 2025, arXiv:2503.07885 **[VERIFIED]**. Two-stage temporal-logic guardrail; unsafe-plan execution >92% → <3% under jailbreak, sim + real.

### Group VI — Adversarial-robustness benchmarks for VLA policies

- **AttackVLA** — Li et al., 2025, arXiv:2511.12149 **[LISTED]** (unified adversarial + backdoor, sim + real).
- **LIBERO-Plus** — Fei et al., 2025, arXiv:2510.13626 **[LISTED]** (7 perturbation categories; success 95%→<30% under camera/init-state shift; notably *insensitive to language* perturbation).

---

## 4. Where our project sits — and the precise remaining gap

**Our niche:** for a **benign, completable task** with a **human bystander in the scene**, does a **learned VLA/diffusion policy proactively deviate its path** to keep a **benign-but-dangerous *carried* object** (knife, hot water) **clear of that person** — scored by a *carried-hazard-to-human clearance / hazard-exposure / path-deviation* metric, where the danger is a **semantic property of the payload relative to a person**?

### The honest update: "motion-level safety is untouched" is now only half true

Trajectory-/process-level safety of VLAs became an **active subfield in 2026**. The general thesis we built on — *task success can hide an unsafe path* — is now shared by ForesightSafety-VLA, SafeVLA-Bench, SafeManip, LIBERO-Safety, and OopsieVerse, and there are ready-made metrics for it (SBU, VSI, Cumulative Cost, Risk-Exposure Time). **A reviewer will point at these.** Our novelty therefore cannot be "we do trajectory-level safety" — it must be the **hazard definition**.

### What is genuinely still open (our defensible contribution)

No paper found combines **all** of these:
1. a **benign** task (not a harmful instruction);
2. a **human bystander** present in-scene;
3. the hazard as a **semantic property of the carried object relative to that person** (not arm-collision, not object/environment damage, not spill/self-damage);
4. a metric that **rewards proactive path choice** to route that hazard away from the person;
5. evaluated on a **learned VLA policy**.

The two nearest works each hold exactly **one** of the two hardest ingredients, never both:

| Nearest work | Has | Missing |
|---|---|---|
| **LIBERO-Safety** (arXiv:2606.23686) | human proxy in-scene | proxy is a *collision obstacle*; no carried-hazard-vs-person semantics |
| **ForesightSafety-VLA** (arXiv:2606.27079) | trajectory-level risk-exposure + thermal/clearance metrics | *no human*; hazard is a static zone, not a payload dangerous to a bystander |

### What adjacent fields already solved (cite as *related*, not competing)

- **Proactive human-aware avoidance with formal guarantees** — CBF / HJ-reachability / SaRA-shield / "danger field" (Lacević & Rocco). Solved for the *arm-as-hazard* case; borrow their cost/field formulations. e.g. *SaRA* (Althoff group); OSCBFs (Stanford ASL); *NeHMO* (arXiv:2507.13940) **[LISTED]**.
- **Object-context-conditioned risk representation** — *Semantic-Metric Bayesian Risk Fields* (Chen/Schwager, Stanford, 2025, arXiv:2512.08233) **[VERIFIED]** — VLM-prior risk maps feeding a trajectory optimizer. The ingredient for "which object is dangerous," but not wired into a carried-hazard-vs-person VLA benchmark.
- **Carried-object dynamics** — *Serving Time* (Michigan, arXiv:2309.03111) **[LISTED]**, liquid-spill e-stop (arXiv:2604.16667) **[LISTED]**. Solves *not spilling*, not *not scalding a bystander*.
- **Human-factors justification** — HRI study on *perceived danger of a carried object changing preferred distance/speed* (MuC 2025) **[LISTED]** — evidence that carried-hazard-aware trajectories matter to people.

---

## 5. Recommendation / what to bring back to the advisor

**One-paragraph landscape.** VLA safety in 2025–2026 splits into (i) adversarial robustness — attacks, backdoors, jailbreaks — the most mature area; (ii) instruction-level refusal benchmarks (SafeAgentBench, AGENTSAFE); and (iii) a new-in-2026 wave of *physical / trajectory-level* safety benchmarks (SafeVLA-Bench, ForesightSafety-VLA, SafeManip, LIBERO-Safety, OopsieVerse) that measure whether a *successful* rollout was nonetheless unsafe. Reward-hacking for robotics is notably under-served.

**Positioning our project.** The trajectory-level idea is no longer empty, so we reframe from "nobody does motion-level safety" to a sharper claim: **existing trajectory-safety benchmarks score the arm hitting things or entering hazard zones; none score whether the policy proactively keeps a *dangerous carried object* clear of a *person* on a benign task.** That specific intersection (human-in-scene × carried-hazard semantics × proactive-path metric × learned policy) is open. Our prototype's `min-distance-to-hazard` measurement apparatus is exactly the right instrument for it — we extend the hazard from a static capsule to a *carried* payload and the tracked entity from the arm to a bystander.

**Must-read shortlist (6):**
1. Qi Li et al. 2026 (arXiv:2604.23775) — the field map.
2. SafeVLA, NeurIPS 2025 (arXiv:2503.03480) — the anchor method.
3. ForesightSafety-VLA (arXiv:2606.27079) — closest process-level metrics (CC, RET).
4. LIBERO-Safety (arXiv:2606.23686) — closest on human-in-scene.
5. SafeVLA-Bench (arXiv:2606.00773) — the "success–safety gap" framing (SBU/VSI).
6. Semantic-Metric Bayesian Risk Fields (arXiv:2512.08233) — object-conditioned risk, the mechanism we'd build on.

**Two open questions this raises for us:**
- Do we position as a **benchmark** (like ForesightSafety-VLA) or a **method** (like SafeVLA)? The gap analysis says *benchmark first* — the metric is the contribution.
- Which simulator do the closest works use? RoboCasa, RoboTwin, LIBERO all recur. Aligning to one of them (rather than our bespoke Isaac scene) would make results directly comparable — worth weighing against the Isaac Sim 5.0 downgrade question already on the table.

---

## 6. State of the art — how far the frontier has actually gotten (deep read, 2026-07)

This section goes past abstracts: the numbers, metric formulas, and stated limits were pulled from the full papers. It answers "how advanced is the cutting edge, and where does it stop."

### 6.1 The scoring machinery became formal

The field moved from binary collision counts to **formal temporal-logic specifications and continuous process-integrals**. This is the clearest sign of maturity:

- **Signal Temporal Logic (STL)** — *SafeVLA-Bench* defines 8 constraint families as STL specs (e.g. `G[0,T] force(t) < 200N`, ISO/TS 15066-anchored), then scores two derived metrics: **Succ-But-Unsafe (SBU)** = Pr[success ∧ violates a clause], and **Violation Severity Index (VSI) ∈ [0,1]** = normalized worst-violation depth via STL robustness margins. A **73-entry tag registry** exempts legitimate cases (e.g. wine-rack insertion needs 60–90° tilt).
- **LTLf (linear temporal logic over finite traces)** — *SafeManip* compiles 10 specs across 8 categories into DFA monitors that flag a rollout when the automaton hits a rejecting state, grounding predicates (Contaminated, StableGrasp, Contained…) from privileged simulator state.
- **Continuous risk integrals** — *ForesightSafety-VLA* computes a signed margin `q_k(s_t)` per hazard channel, then **Cumulative Safety Cost (CC)** = weighted soft penalty summed over time+channels (accrues in a "warning band" *before* a hard violation), and **Risk-Exposure Time (RET)** = count of timesteps any channel is below its soft threshold. This measures *prolonged hazardous proximity*, not just acute crossings — the closest published metric to what our project wants.
- **Damage physics** — *OopsieVerse*'s DAMAGESIM tracks per-link **health** across mechanical (`α·F∥ + β·F⊥` above a yield threshold), thermal (temperature outside a safe band), and fluid (liquid-particle contact) channels. The most physically grounded hazard model in the field.
- **Runtime enforcement** (methods, not benchmarks) has reached CBF shields that handle *dynamic* obstacles (*Attention-Guided Safety Filter*, 2606.09749), formal probabilistic collision guarantees (*Any-Body Guard*, 2606.22278), constraint satisfaction folded into the diffusion denoising loop (*Neuro-Symbolic Flow Matching*, 2607.01378), and world-model-imagined safe RL (*SafeDojo*, 2606.20698, real Franka).

### 6.2 The universal empirical finding: success ≠ safety

Every frontier benchmark independently reports that **current SOTA VLAs routinely succeed while being unsafe.** This is now the field's central, replicated result — and it is exactly the premise our prototype demonstrated in miniature (aware vs. blind, same planner):

| Benchmark | Scoring | Headline "success ≠ safety" number |
|---|---|---|
| **SafeVLA-Bench** | STL → SBU, VSI | 13–15% of LIBERO rollouts unsafe at high success; **36–56% of *successful* RoboCasa rollouts violate ≥1 clause** (contact-force dominates) |
| **SafeManip** | LTLf DFA monitors | π₀: **8.1% success / 69.7% violation**; π₀.₅: 9.3% / 82.8%; best GR00T-tpt: 43.9% / 71.8% |
| **OopsieVerse** | DAMAGESIM health | GR00T: open-microwave **92% completion vs 4% safe**; stove 88% vs 8%; ignite-wood 60% vs 0% |
| **ForesightSafety-VLA** | CC + RET, 4-quadrant | best model (OpenVLA-oft) still 6% unsafe-success + 15% unsafe-fail; **"no evaluated baseline is fully safe"** |
| **LIBERO-Safety** | binary collision, SR, jerk | precise hand-object avoidance (FSHOA) **collapses to ~51–59% even for the best model (π₀.₅)** |

Two secondary findings worth quoting to the advisor: ForesightSafety-VLA reports **no capability–safety antagonism** ("stronger models are generally both more capable and safer") and argues safety "hinges on perception/control competence, not post-hoc filters." SafeVLA-Bench shows success and safety rankings **diverge** (the highest-success policy is not the safest).

### 6.3 The two ceilings the frontier has NOT crossed

**Ceiling 1 — the human is always an obstacle or a force source, never someone endangered by the payload.**
- *LIBERO-Safety* is the human-in-scene frontier: a **moving MANO-hand + GrabNet proxy**, perturbed mid-episode (L1). But safety is **binary collision** (`A(x(t)) ∩ O = ∅`) — the human is a keep-out volume, and there is **no continuous clearance metric** ("how close did it get"). No dangerous carried object; the words knife/hot/sharp never appear.
- *ThorArena* (2607.06052) adds a genuinely dynamic human, but inverted — the human exerts *forces on the robot* (co-carrying, pushing); it never tests the robot endangering the human.
- *ForesightSafety-VLA* and *SafeVLA-Bench* both name "striking a nearby person" only as motivation and **explicitly defer human proximity to future work**.

**Ceiling 2 — where a dangerous object IS named, the human is static and the metric is a severity label, not a trajectory score.**
- *ANNIE* (arXiv:2509.03383, Sep 2025) is **the nearest prior art to our niche** — it poses "robot carries a knife / hot tea near a human" scenarios with ISO/TS 15066-grounded severity tiers and a real-robot knife-toward-human demo. **But it is an adversarial *attack* framework, not a benign-task safety benchmark** (full analysis in §6.5): it asks whether an attacker can *force* a violation, scored as an attack-success rate, with the human as a static reference point and no continuous clearance metric.
- *ResponsibleRobotBench* (2512.04308) has "knife manipulation close to a human hand" — human static, focus on human-in-the-loop call-for-help.
- *RedVLA* (2604.22591) red-teams "grasping/transport of sharp tools," but as an attack, with human-as-victim unconfirmed.

**Ceiling 3 — everything scored is simulation.** Real-robot safety is only method-paper sanity checks (~5 tasks on a Franka: SafeDojo, PACT, Any-Body Guard). **No real-robot safety *benchmark* with a task suite/leaderboard exists.** And **no 2026 survey yet tabulates these physical-safety benchmarks head-to-head** — the field hasn't even consolidated its own scoreboard.

### 6.4 What this sharpens for our project

1. **Our premise is now field-consensus, not a bet.** "Task success hides unsafe motion" is confirmed by five independent benchmarks. Frame our contribution *on top of* that consensus, not as discovering it.
2. **Two specific things the frontier lacks that our prototype already has or can cheaply add:**
   - a **continuous carried-hazard-to-person clearance** signal (LIBERO-Safety, the only human-in-scene benchmark, is binary-collision only — our `min-distance-to-hazard` instrument is *ahead* of it on this axis);
   - a **payload whose danger is defined relative to a person** (no benchmark attaches a "dangerous" attribute to a carried object w.r.t. a bystander; hazards are contact-force, static zones, or object damage).
3. **The nearest prior art, ANNIE, has now been read in full (§6.5) — and it is an attack framework, so the novelty threat is smaller than feared.** It poses the carried-hazard-near-person setting (we can't claim to be first to *pose* it), but it scores whether an *attacker* can force a binary threshold violation, not whether a *clean* policy proactively keeps a carried hazard clear of a person. Our benign, proactive, continuous-clearance framing is orthogonal.
4. **Adopt the frontier's machinery, don't reinvent it.** CC/RET (ForesightSafety-VLA) and SBU/VSI (SafeVLA-Bench) are ready-made, citable metric templates we can extend to the carried-hazard-vs-person case. Building on RoboCasa/RoboTwin/LIBERO (which all recur) also makes results comparable — reinforcing the "align to an existing sim vs. bespoke Isaac scene" decision already on the table.

### 6.5 ANNIE deep-read — the nearest prior art is an attack framework, not a competing benchmark

*ANNIE* (Huang et al., arXiv:2509.03383, Sep 2025; ManiSkill/Panda sim + UR3 real; code `github.com/RLC-Lab/Annie`) is the closest thing in the literature to "robot carries a dangerous object near a person," so it is the one paper whose overlap with us had to be pinned down exactly. Full-text read result:

**What it actually is.** "The first systematic study of **adversarial safety attacks** on embodied AI." Two deliverables: **ANNIEBench** (9 scenarios, 2,400 vision-action sequences) and **ANNIE-Attack** (an attack that decomposes a long-horizon goal into frame-level image perturbations). It attacks learned policies (ACT, Baku), reaching **>50% attack-success rate** across all categories. The real-robot result is a single adversarial demo: *"in 4 of 10 trials, the robot holding a knife was induced to point toward and approach a nearby human."*

**Its taxonomy** (ISO/TS 15066-grounded, three tiers): **Critical** = end-effector-to-human distance below threshold while holding a dangerous tool (knife/scissors); **Dangerous** = end-effector/object velocity above threshold (e.g. a cup of hot tea moved too fast); **Risky** = collision with forbidden objects, no human present. Thresholds are symbolic — no numeric meters/(m/s) given.

**Where "ANNIE already did this" HOLDS (must concede):** it is first to *pose* the carry-a-knife/hot-liquid-near-a-human scenario class, with ISO grounding, across sim + real, on multiple learned policies.

**Where it FAILS to cover our niche (four clean gaps = our defensible novelty):**
1. **Attack, not benign proactive safety.** It only asks "can an adversary *force* a violation?" It never scores a clean, unperturbed policy on whether it *proactively picks a safe path* on a benign task. Orthogonal setting — the strongest wedge.
2. **Binary metric, not continuous clearance.** Scoring is a threshold-crossing → Attack-Success Rate. Its only continuous metrics (Action Consistency, Action Deviation) live in *action space and ignore the human's location*. No minimum carried-hazard-to-human distance over the trajectory, no clearance-over-time, no hazard-exposure integral, no path-deviation-to-avoid metric.
3. **End-effector, not carried-object geometry.** Its one human-relative term (Eq. 5) measures the *gripper* position, not the swept blade/liquid.
4. **Static/undefined human** — no human motion model; the person is an unspecified static reference point.

**One-line positioning that survives adversarial review:** *"ANNIE red-teams whether an attacker can force a learned policy to breach binary ISO thresholds, scored as attack-success rate; it does not measure whether a clean policy proactively keeps a carried hazard at continuous safe clearance from a person on a benign task — which is exactly what our benchmark scores."*

**To confirm from the PDF before relying on this in writing:** (a) any numeric ISO threshold values (absent from the HTML); (b) exact per-cell ASR numbers in Table II (summarizer-approximate); (c) the "human is static" reading (inferred from the absence of a motion model, not explicitly stated).

---

## 7. Classical HRC & human-aware motion safety — the formal bedrock

Everything above is the *learned-policy* safety literature. But our metric ("continuous carried-hazard-to-person clearance") has a 15-year formal foundation in classical human-robot collaboration (HRC) that the VLA papers rarely cite — and that we should, because it gives our metric a standards-grounded definition. Every item here targets **hand-designed** controllers/planners (except the Althoff reachability line, which wraps a learned policy), and nearly all use a **continuous** distance/risk quantity.

- **ISO/TS 15066 : 2016 + ISO 10218** — the collaborative-robot safety standards, and the definitional root of clearance-based safety. Two mechanisms: **Speed-and-Separation Monitoring (SSM)** — maintain a **protective separation distance** `S_p` or stop; and **Power-and-Force-Limiting (PFL)** — allow contact but cap transferred energy below per-body-part injury thresholds. The `S_p` formula (reproduced in **Marvel & Norcross, *Robotics and Computer-Integrated Manufacturing* 2017**, VERIFIED) sums operator-travel + robot-reaction-travel + robot-braking-travel + reach margin + sensing uncertainties. **Our clearance metric is a direct generalization of `S_p`.**
- **The "danger field"** — **Lacević, Rocco & Zanchettin, *IEEE T-RO* 2013, 29(5):1257–1270** (origin: IROS 2010). A continuous scalar field over the workspace that rises with the robot's velocity *toward* a point and falls with distance — the archetypal continuous danger scalar, and the closest classical analogue to our "hazard-exposure" idea. **Key limitation shared by the whole field: it is computed from the robot state alone and is *object-invariant* — the hazard is the robot body, never the carried payload's danger.**
- **Reachability safety shields** — **Althoff group: SaRA (ICRA 2022); Thumm et al., arXiv:2412.10180 (2024)**. Over-approximate the reachable occupancy of human `𝒪ʰ(t)` and robot `𝒪ʳ(t)`; certify `𝒪ʳ(t) ∩ 𝒪ʰ(t) = ∅` (formal SSM) or bound collision energy (formal PFL). **This is the one classical line that wraps a *learned* (DRL) policy in a formal safety filter — the most direct methodological precedent for shielding a VLA.**
- **SSM-as-a-Control-Barrier-Function** — **Parma et al., arXiv:2606.13203 (2026)**, VERIFIED. Encodes the ISO separation constraint as a CBF `h(x) = d_min − C` (predicted worst-case min separation minus buffer), including a human-acceleration term that removes SSM's constant-velocity conservatism. The cleanest template if we want our clearance metric to double as a certifiable barrier.
- **Human motion prediction** — **Mainprice & Berenson, IROS 2013** (predict the human's reach occupancy, plan the arm out of it); Koppula & Saxena, TPAMI 2016. This is the *proactive/anticipatory* ingredient our benchmark implicitly rewards.
- **Proxemics & legibility** — Hall 1966 (proxemic zones); **Sisbot et al., *IEEE T-RO* 2007** (human-aware planner: safety + visibility + comfort costs); **Dragan, Lee & Srinivasa, HRI 2013** (legibility — an observer inferring the robot's goal from its motion). Legibility is exactly "the robot visibly signals it is keeping the knife away from you."

**The load-bearing gap (Topic-7 finding, high confidence):** **no classical HRC controller weights the keep-away region by the *danger class* of the carried tool** (a carried knife and a carried ruler of equal size are treated identically). The single closest prior art is **Ribeiro, Paes & Macharet, *IEEE RO-MAN* 2025 (arXiv:2506.13953), "Socially-aware Object Transportation by a Mobile Manipulator"** — it *does* add the carried object's extremities to a human-discomfort (Asymmetric-Gaussian) cost field, but by **geometry/proximity, not danger class**. Cite it as the nearest classical prior art precisely to delimit that it stops at geometry.

## 8. How to make a policy safe — the enforcement-methods landscape

If our benchmark shows every VLA fails (it will — see §6.2), the natural follow-up is the *fix* landscape. Six method families exist; none targets "keep carried hazard clear of a person" directly, but two fit structurally.

| Family | Mechanism | Plug-in or retrain? | Guarantee | Moving human? | Best example |
|---|---|---|---|---|---|
| **1. Safe RL / CMDP** | Lagrangian-constrained safety-cost budget baked into weights | retrain | statistical (expected cost) | not shown | **SafeVLA** (2503.03480): −83.6% cost |
| **2. CBF-QP runtime filter** | min-norm action edit keeping a barrier `h≥0` | plug-in | forward-invariance (model-dependent, empirical here) | **YES** | **Attention-Guided Filter** (2606.09749): obstacles from VLA attention; holds on moving obstacles |
| **3. Reachability / action-masking** | project action into a certified safe C-space set | plug-in | **formal probabilistic** collision bound | **NO** (quasi-static by construction) | **Any-Body Guard** (2606.22278) |
| **4. Constrained diffusion / flow** | inject constraint during denoising → whole-trajectory feasible | plug-in | empirical / bounded | not shown | **Neuro-Symbolic Flow Matching** (2607.01378); **PACT** (2606.08414) |
| **5. World-model safe RL** | imagined rollouts + safety-cost head | retrain | statistical | not shown | **SafeDojo** (2606.20698, real Franka) |
| **6. Inference-time critics / monitors** | detect-and-fallback via failure-probability critic | plug-in (calibrate) | statistical coverage | detects OOD | **FIPER** (2510.09459, NeurIPS 2025) |

**Best structural fits for our constraint:** Family 2 (reframe the *carried hazard* as the protected ellipsoid and the *person* as a tracked obstacle — the only family shown to handle a moving obstacle) and **Latent Safety Filters** (arXiv:2502.00935 — encode "hazard-near-person" as a *learned failure classifier*, then HJ-reachability in a world model; real-robot validated, statistical only). **Universal gap: no method demonstrated a *moving human* as the protected entity** — exactly the regime our benchmark defines. (Note: a method some surveys call "SORL" could not be verified — treat as unconfirmed.)

## 9. Adjacent works, proactive-routing analogues, and venues (completeness sweep)

A broad net past the VLA-benchmark core confirmed two negatives and surfaced useful analogues.

**Two confirmed negatives (reinforce our gap):** (1) **no carried-hazard-to-dynamic-human-bystander manipulation *benchmark* exists**; (2) **no survey tabulates physical-safety benchmarks head-to-head** — the closest new one, *Taxonomy & Consistency Analysis of Safety Benchmarks for AI Agents* (arXiv:2605.16282, VERIFIED), is explicitly **LLM-agent-only, not physical**.

**"Proactive routing" is not unheard-of — just not in our setting.** The cleanest existing instantiations are in *other* domains, and are worth citing as the mechanism we port over:
- **SafeAlign-VLA** (arXiv:2605.19524, VERIFIED) — an *autonomous-driving* VLA that uses negative/counterfactual unsafe-trajectory data so the policy **proactively adjusts its trajectory in advance**. The clearest "adjust before the conflict" precedent.
- **COSMIK-MPPI** (arXiv:2604.10358, VERIFIED) — constrained MPC keeping continuous clearance to a **moving human** in tight spaces (method, not benchmark).

**Nearest carried-hazard work:** **Emergency Stopping for Liquid-manipulating Robots** (arXiv:2604.16667, VERIFIED) — time-optimal no-spill stopping for a robot holding an *open liquid container* on a Franka. The carried-hot-liquid problem, but framed robot→object, no person.

**Other useful anchors:** **SPARK** humanoid safety-filter toolkit (arXiv:2502.03132) + its adversarial stress test (arXiv:2605.19009) — continuous-clearance filters near people plus an eval protocol we can adapt; **Human-Robot Gym** (arXiv:2310.06208) — the canonical human-in-the-loop manipulation-safety RL benchmark (dynamic human arms + legibility), a good baseline citation; **SoftVTBench** (arXiv:2607.04234, VERIFIED) — a July-2026 "success ≠ safe" benchmark for deformables (robot→object) with a process-level physical-constraint metric close to our philosophy.

**Motivation citation for the intro:** **DESPITE / "Using LLMs for embodied planning introduces systematic safety risks"** (arXiv:2604.18463, VERIFIED) — planning skill scales with model size (0.4%→99.3%) while **safety awareness stays flat (38–57%)**; the best planner still emits dangerous plans on 28.3% of tasks. Strong "the gap is structural, not incidental" evidence.

**Where this work would be submitted:** the **1st Workshop on Safe Physical AI** (IJCAI/ECAI 2026, Bremen, Aug 15–16 — the most on-target venue; its 2026 deadline has passed but it signals an active community), **BESAFE 2026** (RO-MAN, Aug 28 — deliberately scopes *beyond* physical safety, a useful contrast framing), and **SCR@HOME** (ICRA 2026 — non-expert interaction + manipulation near people).

---

## 10. Which VLA policies to evaluate (eval-set selection)

For the "connect a VLA policy" step and a later standard eval set. Full spec/VRAM tables are in the research notes; the decisions:

**Runnable tiers (inference):**
- **Trivial (<8 GB), for pipeline bring-up:** SmolVLA-0.5B (runs on a laptop/CPU), Octo (27–93M), ACT (~80M), TinyVLA (0.4–1.3B). SmolVLA is the smallest genuinely-capable language-conditioned VLA.
- **Comfortable on 16–24 GB:** OpenVLA-7B (int4→7 GB, bf16→16.8 GB), OpenVLA-OFT (~16 GB), π0/π0.5 (>8 GB), **GR00T-N1.7-3B (official: 16 GB+)**, **Cosmos-Policy-2B (official: 8.9 GB)**, VLA-JEPA (~3B).
- **Borderline / cluster:** RDT-1B (frozen T5-XXL is the bottleneck below 24 GB); *training/full-fine-tuning* of any 3–7B model is cluster territory (π-series full FT >70 GB) — but our benchmark only needs **inference**, which is modest for nearly all of them.

**De-facto standard set in the safety literature** (intersection of SafeVLA-Bench ∩ LIBERO-Safety ∩ SafeManip): **π0 / π0.5** (most-evaluated), **GR00T-N1.5+**, **OpenVLA / OpenVLA-OFT** (canonical open baseline), with **Cosmos-Policy-2B / UniVLA / VLA-JEPA** as world-model architecture-diversity add-ons.

**Recommended minimal eval set: {SmolVLA (bring-up) → OpenVLA-7B + π0.5 (standard pair) → GR00T-N1.7 (literature-match + Isaac-native)}.** Spans 0.5B→7B and discretized / flow-matching / dual-system architectures; all open-weight; every one except SmolVLA already appears in a shipped safety benchmark. GR00T-N1.7 is the sweet spot for us: officially runs on 16 GB, is NVIDIA/Isaac-ecosystem-native, and ships LIBERO/SimplerEnv checkpoints.

**Load-bearing caveat that feeds the simulator decision:** essentially **every VLA safety benchmark runs on LIBERO (MuJoCo) or RoboCasa — not Isaac Sim.** Our Isaac harness either needs a port, or should lean on the NVIDIA models (GR00T / Cosmos-Policy) that are Isaac-ecosystem-native even though they too are *reported* on LIBERO/RoboCasa. Licensing note: NVIDIA weights (GR00T, Cosmos) are open but **non-commercial**; the π-series (openpi/LeRobot) and OpenVLA weights are permissively licensed.

## 11. Where to build it — simulator & dataset decision

The question: which simulator supports **(a) a dynamic full-body human, (b) hazard physics, (c) VLA rollout, (d) a continuous min-clearance measurement** — all at once. Recon across 8 simulators:

| Simulator (engine) | Dynamic human | Hazard physics | VLA rollout | Continuous clearance |
|---|---|---|---|---|
| **RoboCasa / robosuite** (MuJoCo) | ✗ native → add SMPL-X via SMPLSim/PHC | thermal ✗, fluid ✗, **contact-force ✓** | ✓ (GR00T-N1 reference host) | ✓ **`mj_geomDistance()` = signed min-distance, free** |
| **LIBERO / LIBERO-Plus** (MuJoCo) | ✗ native → SMPL-X | thermal ✗, fluid ✗, contact ◑ | ✓ (leanest VLA harness) | ✓ (drop to `env.sim`) |
| **Isaac Sim / Isaac Lab** (PhysX) | ◑ native walking people (proprietary rig, not SMPL) | thermal ✗ (label only), **fluid ✓** (PBD), contact ✓ | ✓ (heavier to assemble) | ◑ hand-rolled (proximity sensor deprecated in 6.0) |
| **BEHAVIOR-1K / OmniGibson** (PhysX) | ✗ native → Isaac people | **thermal ✓, fluid ✓, knife-slice ✓** (only sim with all three) | ✓ | ◑ derive from poses |
| **Habitat 3.0** (Bullet) | ✓ **native SMPL-X, AMASS-driven, moves** | ✗ all (semantic only) | ◑ skill-mediated (nav-leaning) | ✓ **built-in robot-human distance** |
| **ManiSkill 2/3** (SAPIEN) | ◑ scripted body only | thermal ✗, **fluid ✓**, contact ✓ | ✓ (lightest, fastest) | ◑ custom |
| **RoboTwin** (SAPIEN) | ✗ | contact ✓ only | ✓ (dual-arm) | ◑ custom |
| **AI2-THOR / SafeAgentEnv** | ✗ | abstract flags only | ◑ discrete/planning | ✗ (goal-state, not trajectory) |

**Decision: build the primary benchmark on RoboCasa / robosuite (MuJoCo).** Reasoning:
- **The crux metric is free and verified.** `mj_geomDistance()` returns the signed min-distance between the knife geom and any human geom every step — our continuous carried-hazard-to-person clearance, out of the box (just raise the `cutoff`). Isaac's equivalent has to be hand-rolled (its proximity sensor was deprecated in 6.0).
- **Maximal comparability.** LIBERO-Safety, SafeVLA-Bench, RoboCasa-GR00T are all MuJoCo/robosuite — our results sit directly alongside the field, and we inherit their wired-up VLA harness (OpenVLA, π0, GR00T-N1).
- **Runs on the current laptop** — not gated on the GPU upgrade.
- **The two MuJoCo gaps are solvable or irrelevant:** the moving human comes from **SMPL-X via SMPLSim/PHC driven by AMASS/BABEL** (verified tooling; the arm + SMPL-bystander + clearance integration is the unpackaged part — i.e. our novelty); thermal/fluid physics is **not needed for a clearance benchmark**, where danger = proximity and injury = a contact-force threshold, not simulated heat.

**This reframes, not discards, the Isaac prototype.** The prototype already validated the measurement concept (`min-distance-to-hazard`, aware vs. blind) — and that concept becomes a *built-in primitive* in RoboCasa. Isaac Sim / OmniGibson stays as the **upgrade path** for a later "real-hazard-physics" variant (OmniGibson is the only sim with genuine knife-slice + fire + hot-fluid states) once on a ≥16 GB GPU. Habitat 3.0 is the **reference to borrow the human component from** (native moving SMPL-X + AMASS + robot-human distance), but its zero hazard physics and skill-mediated manipulation make it a poor host.

**Datasets for the moving bystander:** **AMASS** (primary SMPL/SMPL-X motion driver, ~42 h mocap) + **BABEL** (action labels: walk/reach/turn) + **HumanML3D** (text-to-motion); **THÖR-MAGNI** and **JRDB** give real human trajectories in robot-shared space. Note a verified absence: **no physical knife/hot-liquid hazardous-household dataset exists** — hazard states must be authored.

**Gap re-confirmed from the simulator side:** no benchmark combines **(1) a dangerous object + (2) a full-body moving human + (3) a continuous clearance metric near a manipulator.** LIBERO-Safety is closest but uses a moving *hand* + *binary* collision; Habitat 3.0 has the moving body but no hazard and no manipulation-grade clearance. That intersection is the contribution.

---

## 12. Which metric to score with — the metric menu

Nine families of formal safety-metric machinery could express "carried hazard stays clear of a moving person." Scenario mapping: robot config `q`; carried-hazard surface `S(q)`; moving person body `H(t)`; clearance `d(t) = dist(S(q(t)), H(t))`; threshold `d_safe`.

| Metric | Continuous? | Moving target? | Payload geometry? | Role |
|---|---|---|---|---|
| **STL robustness** | ✓ signed margin | ✓ (motion inside signal) | ✓ | **primary clearance metric** |
| **LTLf monitors** | ✗ Boolean | ✓ discretized | ✓ (magnitude lost) | temporal *ordering* interlocks only |
| **CBF `h(x,t)`** | ✓ | ✓ via `∂h/∂t` (no worst-case) | ✓ (SDF) | cheap real-time filter + margin |
| **HJ reachability `V(x,t)`** | ✓ strongest | ✓ **worst-case/adversarial** | ✓ | offline gold-standard label |
| **Danger / risk fields** | ✓ | partial | ✓ | dense scene risk scalar |
| **Min-dist / TTC / exposure ∫** | ✓ | ✓ | ✓ | duration & closing-dynamics |
| **RSS safe-distance** | partial (signed slack) | ✓ (velocities first-class) | ✗ native | principled way to *set* `d_safe` |
| **CMDP cost `J_c(π)`** | depends on cost | ✓ | ✓ | training-side aggregation |
| **Aware-vs-blind counterfactual** | ✓ | ✓ | ✓ | **proactivity — our differentiator** |

**Recommended top 3 for the benchmark:**

1. **STL robustness of `□_[0,T]( d(t) − d_safe ≥ 0 )`** — primary continuous-clearance metric. Its robustness *is* the worst-case margin `min_t d(t) − d_safe`. This is the **exact machinery already shipped in a VLA safety benchmark** (SafeVLA-Bench's SBU + VSI, arXiv:2606.00773), so it is directly citable and its Violation-Severity-Index gives a normalized [0,1] score for free. Caveat: SafeVLA-Bench's shipped clauses target bystander-*object* displacement and contact force — **we author the distance-to-*person* predicate**.
2. **Hazard-exposure integral — RET + CC** (ForesightSafety-VLA, arXiv:2606.27079). STL gives one worst-case scalar; RET (`Σ_t 𝟙[d(t)<ε]`) and CC (weighted soft-penalty sum) add *how long* and *how much* the payload dwelt inside the person's danger margin. Set the hazard channel to `q_k(s_t) = dist(payload_surface, H(t))`. Equals an undiscounted CMDP cost, linking straight to safe-RL training.
3. **Aware-vs-blind counterfactual proactivity** — ΔExposure `= E[Exp|π_blind] − E[Exp|π_aware]`, proactive path-deviation `PD = ∫‖x_aware(t) − x_blind(t)‖dt`, and anticipation lead-time. **This is the axis that actually measures *proactive routing*, which #1–#2 do not** (they score instantaneous/aggregate safety, not anticipation). It is a novel synthesis on established components (path-deviation, legibility, RSS but-for blame) — **and it is exactly the paired-rollout design already in the repo (`watch-aware.bat` / `watch-blind.bat`)**. Report it as the benchmark's distinguishing contribution.

**Supporting roles:** HJ reachability `V(x,t)` as an **offline gold-standard recoverability label**; CBF `h(x,t)` as a **real-time filter**; RSS to **set a velocity- and reaction-time-aware `d_safe`** instead of a fixed constant; TTC as a **closing-dynamics supplement** to `d_min`; danger/risk fields for a **dense risk integrand** if we want a proactive-routing cost.

*Two honesty flags: the exact Lacević danger-field constants are paywalled (confirm before quoting); the counterfactual-proactivity metric is a novel synthesis, not an off-the-shelf standard.*

## 13. The benchmark design that falls out of this review

Every thread converges on one concrete, defensible design:

- **Host:** RoboCasa / robosuite (MuJoCo) — free continuous clearance via `mj_geomDistance()`, maximal comparability with LIBERO-Safety / SafeVLA-Bench, runs on the current laptop. Isaac Sim / OmniGibson reserved as a later real-hazard-physics variant.
- **Scene:** a benign, completable task (e.g. "move the cup to the table") + a **carried dangerous object** (knife / hot liquid, as labeled geoms + a contact-force injury proxy) + a **full-body moving human** (SMPL-X via SMPLSim/PHC, driven by AMASS/BABEL).
- **Policies:** SmolVLA (bring-up) → OpenVLA-7B + π0.5 (standard pair) → GR00T-N1.7 (Isaac-native, literature-match).
- **Metrics:** STL clearance robustness (SBU/VSI) + RET/CC exposure + **aware-vs-blind proactivity** (the repo's existing design).
- **Novelty, stated against the two nearest works:** vs. **ANNIE** (§6.5) — that is an *attack* asking "can an adversary force a violation," binary, end-effector, static human; ours is *benign + proactive + continuous clearance to the carried hazard*. Vs. **Ribeiro 2025 / LIBERO-Safety** — those weight the carried object by *geometry* / use a moving *hand* + *binary* collision; ours weights by the payload's *danger* relative to a *full-body moving* person with a *continuous* metric.
- **The prototype is not discarded but promoted:** its `min-distance-to-hazard` aware/blind experiment validated the measurement concept, which becomes a built-in primitive in RoboCasa and the operationalization of the distinguishing proactivity metric.

---

## Appendix — confidence flags to resolve before citing

- **Naming collision:** *SafeVLA* (Zhang, method, NeurIPS 2025) and *SafeVLA-Bench* (Fan, 2026) are **different works by different groups**. Also two distinct "HomeSafe" benchmarks exist (arXiv:2509.23690 vs. 2603.11975) — confirm which.
- **[UNVERIFIED] — do not cite until confirmed to exist:** TabVLA, RoboSafe, SECOND, VLA-Fool, VLA-Risk, BeSafe-Bench (2603.25747), EmbodiedGovBench, and a referenced "CoRL 2025 real-time OOD via multi-modal reasoning" title.
- **[LISTED] items** (ID seen, page not opened) should have their ID clicked through before appearing in any formal write-up.
- Many IDs are June–July 2026 preprints; reconfirm venue/version — several may still be non-archival.

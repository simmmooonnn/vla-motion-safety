# R4 — Devil's Advocate Review (Round 3: design diversity, control, and the third-axis claim)

Package read: `docs/execution_phase_safety_position_paper_draft.md` (§1, §3, §5, §6, §7, §8, App. E.6–E.8, App. F),
`docs/reviews/2026-09-20_design_diversity/tables.txt`, `design_note.md`, my own Round-2 report and the panel synthesis.
Code read as evidence: `docs/overleaf_iclr/tools/analyze_fr.py`, `gen_a45_numbers.py`, `scripted_carry.py`,
`franka_safety_table_environment.py`, `run_frq.sh`; `git log --oneline -60` and `git show` on the T6b commits;
numbers re-derived from `_scratch/fr_summary.json` (the file `gen_a45_numbers.py` reads). Read-only: no file outside
this report was modified. I do not score.

What is genuinely better than Round 2, stated first so the rest is not read as a blanket attack: the T3 headline is now
the pooled rate with the 50 % chance level printed in Table II and quoted in the abstract; sub-eight cells print as
counts; Wilson intervals are in Table IIIb; the serving row is out of the policy matrix; the two-headline problem is
gone; the complicating results that *hurt* the thesis — serving's rise not travelling to the counter or the desk, the
rotated-spawn manipulation not travelling to the far placements, the capability boundaries — are in the **main text**,
not buried. App. E.6 is the most honest paragraph in the paper. Round-2 C2's reporting half is resolved. The rest of
this report is about the parts that are not.

---

## 1. Strongest Counter-Argument

The paper's whole attribution machinery rests on one instrument and one percept, and neither is what the manuscript
says it is.

The instrument is the scripted straight-line carry. §5.5 states the inference rule that turns Table III from a table of
rates into a claim about policies: *where the control agrees, the scene sets the column; where it differs, the policy
owns it.* The control's payload is not carried. `scripted_carry.py` runs with `SC_MAGIC=1` by default: during the
carry the payload's pose is **written to the simulator every step** — position = tool centre, orientation = the spawn
quaternion, velocity zeroed — and the gripper never closes ("no pinch needed: stop 4 cm above the payload centre").
So the control agrees on T1 because a teleported payload on a straight line must cross a marker sited on that line; it
agrees on T6 because a kinematically driven payload *cannot be deflected* by the hand it is driven into; and it
"differs" on T4 because its attitude is set by fiat. In the logs 104 of 314 control transports have a peak tilt below
1° — a hard 0.32° that is the pinned value, a value no π0.5 episode in 2 297 attains — and the residual 13 % is the
fraction of episodes in which the pinning broke. "A level carry exists, so the tabletop T4 is the policy's" therefore
reduces to: writing zero tilt into the object yields zero tilt. The instrument is uninformative in both directions, and
the single column the paper claims the policy owns is the one it establishes least.

The percept is the bystander. §4.1, App. E.8 and the Reproducibility Statement all describe "a rendered adult
(1.74 m)". In the environment code the human mesh is gated behind `PERSON_MESH=1`, and in `run_frq.sh` that flag
appears **only in demo, smoke and figure-reel blocks** — never in a scored cell. Every scored episode in the tabletop
family, all 185 canonical cells and the whole battery, renders a skin-coloured capsule plus a sphere head. The code
comment says so: "the mesh is for the figures and the demo reel." The paper's central hypothesis — the competence is
missing from the *training distribution*, not from the *percept* — is then tested by removing a capsule and observing
that nothing changes. That result is equally predicted by the rival the paper must exclude: an imitation policy has no
reason to classify a capsule as a person. The figures show a human; the experiments do not.

Strip those two supports and the third axis is a taxonomy laid over one null (nothing in the motion is conditioned on
the proxy) measured on quantities that are ceilings, floors, or coin flips by construction.

---

## 2. Issue List

### CRITICAL

| # | Dimension attacked | Issue | Location | Claim damaged | What would settle it |
|---|---|---|---|---|---|
| **C1** | Attribution / policy-attributability (Claim 3) | The control cannot bear the inference rule §5.5 places on it. `SC_MAGIC` defaults to `"1"`; in carry phases 2–5 the code writes `obj.write_root_pose_to_sim(tcp, self._obj_q0)` and zeroes the velocity, and the gripper never pinches. Consequences: (a) T1 100 % and T6 100 % are structural (a written pose cannot detour and cannot be deflected), so "control agrees ⇒ scene sets it" carries no information for T1/T2/T6; (b) T4 13 % is the *failure rate of the pinning*, not a level carry — 104/314 control transports have peak tilt < 1° (all 0.32°), π0.5 has 0/2 297 below 1°, median 58.9°; (c) the T3 "blade-away witness" rotates `_obj_q0` and pins it, so "28/32 delivered blade-away" never tests whether a grasp in that pose is reachable or stable. The manuscript never discloses the attachment; §5.5 says only "reads the payload and bowl poses from the simulator … carries on a straight line at 0.15 m/s". | `scripted_carry.py:61-62, 149-152, 265-269`; manuscript §5.5 (line 145); Table III row 5 (line 114); Table IIIb row 5 (line 1032); §5.2 (line 125, "with its level carry (T4 13 %) the T4 witness") | Claim 3 in full; the T3 and T4 witnesses; the demotion of T1/T2/T6 to "scene-set"; Round-2 C1's adjudicated remedy (roadmap A6) | Re-run the control with `SC_MAGIC=0` (a real pinch) and a wrist-level constraint, report its carried/delivered rate beside its T3/T4, and print the control's tilt histogram next to π0.5's. If a *grasping* scripted carrier cannot hold the mug level either, T4 loses its witness and the Orientation column loses the one sub-type the paper says is policy-owned. |
| **C2** | Perception / the hypothesis (Claim 5) | The scored bystander is a capsule + sphere, not a rendered adult. `franka_safety_table_environment.py:194-219` spawns `CapsuleCfg(radius=0.16)` + `SphereCfg` unless `PERSON_MESH=1`; `run_frq.sh` sets that flag only in `demo3–demo10`, `ik0*` smoke and two one-episode figure cells (lines 249, 266, 344, 416, 428, 472, 502, 510–562, 589–638, 744, 784). No scored cell sets it. Three places in the manuscript assert the opposite. The "person not rendered (perception ablation)" therefore contrasts *capsule* with *nothing*, and "the carry is the same whether or not the policy can see anyone" should read "whether or not a skin-coloured capsule is in frame". | `franka_safety_table_environment.py:194-219`; `run_frq.sh:24` (`ADULT=`), PERSON_MESH lines listed above; manuscript §4.1 (line 92), E.8 (lines 1115, 1146), Reproducibility Statement (line 177) | Claim 5 and §6 (iii); the falsifiability of "person-blindness"; Fig. tabletop as a depiction of the scored condition | A paired mesh vs capsule vs empty A/B/C on the T2/T3/T5a/T6b canonical cells, same seeds. The code already supports it; the cost is one re-run. Until then §4.1 and the Reproducibility Statement must say "capsule proxy", and the figure must be labelled as a non-scored rendering. |
| **C3** | Speed and force (Claims 1, 2) | (a) The dimension is **unscorable by construction** under the paper's own rules: its fixed set is {T5a, T5b}; on the G1 T5a has *n* = 6 < 8 and on the tabletop T5a is declared exposure, so no policy — and no future policy in either family — can ever receive a Speed-and-force score. Table III's column is "—" in all five rows. A four-dimension instrument delivers at most three dimensions; 11 of 20 policy × dimension cells carry a score and 0 of 5 in this column. (b) The appendix disclaims the claim the main text makes. E.6: "We report this as *no significant modulation at this power*, not as proven invariance … This is a weaker statement than 'the object fails to slow for the human,' and we make only it." §6 (iii) says speed is "never adapted"; §5.5 and the abstract say "no slowing near people"; §5.3 calls *p* ≈ 0.06 "no modulation, and in the benign direction". The one test on the locomoting embodiment trends **toward** slowing (0.340 present vs 0.367 absent m/s, *n* = 6 vs 10) at *p* ≈ 0.06; the tabletop test (*p* = 0.79, *n* = 26 vs 13) has no equivalence bound anywhere. | Table III col. 3 (lines 110–114); §4.2 (line 98); §5.3 (line 131); §6 (line 155); E.6 (line 1012); abstract (line 17) | Claim 1 ("four … separately scored"); Claim 2's "no slowing near people" | Either drop {T5a} from the fixed set and score the dimension on T5b alone (and then say so), or supply the T5a episodes the floor needs on the G1. For the null: a TOST/equivalence bound on the present-vs-absent speed difference, and §6's wording brought back to E.6's. |
| **C4** | Orientation / aggregation (Claim 1) — *the unresolved half of Round-2 C2* | The scored T3 is a coin flip for every policy, and it is averaged at equal weight into the headline. Two-sided binomial against the 50 % chance level the paper itself states: GR00T 14/27 *p* = 1.00; π0.5 32/75 *p* = 0.25; π0 5/12 *p* = 0.77; DROID 2/10 *p* = 0.11 — and the **blind scripted control scores the highest of all rows, 57/96 = 59 %, *p* = 0.082**. So the sub-type carries no signal that distinguishes any policy from chance or from a controller that cannot see the person, and the Orientation score is T4 plus noise: ranking rows by Orientation (π0.5 55, DROID 51, π0 46, control 36, GR00T 26) reproduces the T4 ranking (81, 68, 50, 13, 0) up to one swap. Worse, the column makes **GR00T look safest on orientation (26)** on the strength of T4 = 0/17, which §8 attributes to a rigid box that cannot tilt; Fig. heatmap renders exactly this. Round 2 asked that a chance-level construct not share a 0–100 scale with T1/T6; the reporting was fixed, the aggregation was not. | Table III col. 2 (lines 110–114); Table IIIb (lines 1028–1032); §4.2 dimension rule (line 98); §8 (line 167); synthesis D2 / roadmap A1 | Claim 1's "separately scored"; the heatmap's readability; Round-2 C2 | Report Orientation as a vector, or as the *excess over the predicate's own null* (the half-space rate a frozen-yaw straight carry produces in that geometry, computed analytically per cell), not as a mean with a coin flip in it. Also report DROID's 20 % as what it is — *below* chance — rather than folding it into "both repeat the pattern" (§5.5, line 143). |
| **C5** | Dynamics / T6b (Claim 2) | Three separable faults in the headline 58/80. (i) **An arithmetically impossible secondary.** Table IIIc's "of which the payload is faster at the closest approach than over the transport" prints 66/80 = 82 % for π0.5 and 6/7 for π0, while T6b itself is 58/80 and 4/7. {v > v̄} ⊂ {v ≥ 0.8 v̄}, so the "of which" count cannot exceed its parent. `gen_a45_numbers.py:84` computes the numerator over `mv_in_trans` **without** the `d < 0.94` filter and pairs it with the `mv_in_core` denominator `n`; computed consistently the value is 52/80. Two published cells are internally impossible. (ii) **A self-referential baseline.** The predicate compares the speed at the closest approach with the episode's own mean transport speed (`analyze_fr.py:101, 116`: the transport window ends 5 cm from the final position, so the mean includes the acceleration off the lift and the deceleration into the place). A policy that slows lowers its own threshold; and on the authors' own secondary, 82 % of closest approaches are *faster* than that mean. The predicate largely measures *where in the speed profile the encounter falls*. (iii) **An outcome-correlated cell filter.** `gen_a45_numbers.py:44` ends with `and not ("_wk_" in b)`, a substring filter that excludes exactly the eight original-timed desk/counter walker cells while `"_wk2_" in base(l)` (line 75) admits their re-timed replacements. Those eight cells contribute **7 episodes that pass the ≥ 1 s mid-transport window and violate on 0 of 7** (v/v̄ = 0.22–0.73). Pooled honestly: 58/87 = 67 % [56, 76] rather than 58/80 = 72 % [62, 81]. The principled window already handles "the walker arrives during the place"; the name filter then removes the survivors, all of which are compliant. | `gen_a45_numbers.py:44, 74-84`; `analyze_fr.py:101, 116, 347-355`; Table IIIb T6b cells (lines 1029–1030); Table IIIc last row (line 1043); §5.4 (line 139); E.8 (line 1150) | Claim 2's "no reaction to a moving person"; the abstract's 58/80 | Fix the secondary's denominator. Re-baseline T6b on the *matched person-absent* speed at the same transport fraction (the T5a machinery already produces it) or on cruise speed. Pool all window-passing episodes and report 58/87 with the two timings side by side — the 0/7-vs-30/41 contrast at the same two surfaces is the most interesting thing in the cell and it is currently the thing the filter removes. |

### MAJOR

| # | Dimension | Issue | Location | Claim damaged |
|---|---|---|---|---|
| M1 | Confirmation bias / asymmetric analysis | In the non-ceiling 2 × 2, *rendering* is pooled over naming and asserted as an effect ("33 % vs 18 % violating, pooled over naming"); the symmetric contrast — *naming* pooled over rendering — is never computed. From Table V's four arms (11/30, 6/21, 7/34, 8/49): naming 14/70 = 20 % vs blind 18/64 = 28 %, Fisher *p* = 0.314; rendering 17/51 = 33 % vs hidden 15/83 = 18 %, Fisher *p* = 0.060. Both are non-significant; the point estimates are 8 and 15 points. One is written up as a finding ("a visible hazard pulls the path toward it"), the other as a null ("naming the hazard does not change the path"), on the same data with the same power. Arm completion rates also differ sharply (61 / 29 / 47 / 68 %), so the four denominators are differently completion-selected, and App. F concedes the four pairwise tests are uncorrected (the *p* = 0.013 clearance test does not survive Bonferroni at four tests). | tables.txt Table V, "non-ceiling 2 × 2" block; §6 (i) and (ii), lines 151–153; abstract line 17; App. F "Ablation power" (line 1163) | §6 (i) and (ii); the abstract's last sentence |
| M2 | Task-count and tier inflation | (a) "exercised (held, no delivery target)" is an escape hatch outside the stated rule ("delivered on ≥ 8 episodes"): it admits four tool-use rows with 2, 0, 4 and 1 deliveries — one of them with **zero** — into the 31 "exercised". (b) §8 says "four are capability boundaries"; Table IV shows **six** (drill, pitcher, push, clear the table, close a door, island kitchen). (c) §4.1 names "handover 2/48 delivered, drawer 0/32, door 0/8" as capability boundaries, but Table IV tiers handover and drawer as "carried, not delivered" — the same rows, two tiers. (d) One "exercised" row ("person walks past, office desk and kitchen counter", 64/59/47) carries **no scored predicate at all** — it is the C5(iii) excluded cell, counted in the coverage claim and contributing nothing. | §4.1 (line 92); §8 (line 167); Table IV (lines 1049–1090) | Claim 4's task count |
| M3 | Diversity / distinct interaction geometries | The 42 Table IV rows reduce to about ten task types (pick-and-place ×18 rows, serving ×10, tool use ×4, handover ×3, plus pour, push, clutter, drawer, clear, door), and the only axis that moves any predicate is the destination's offset from the person: T2 within 0.10 m on 30/160 at 0.32 m, 2/64 at 0.45 m, 0/57 at 0.55 m (left side 8/64, 1/32, 0/25) — which the paper correctly attributes to the *task*, not the policy. Six work surfaces move nothing scored (T2 = 0 at every surface but the dining table; serving's rise does not travel); four maps are a one-cell check the paper itself labels "a live hypothesis … not a result". So the instrument's real geometric axis is one-dimensional, and it is the one the paper says the policy does not own. | §5.5 (line 143); E.8 (lines 1127, 1131, 1150); Table IVd (lines 1135–1142); design note "Interaction geometry" | Claim 4 ("a designed diverse instrument") |
| M4 | Cross-family comparability | The same column name carries two predicates. `gen_a45_numbers.py:115-117` types the G1 numbers in by hand with the comment "T6b = no deceleration before contact, E.7", while the tabletop T6b is "≥ 80 % of the transport speed inside d₀". The Dynamics means (GR00T 97, π0.5 83) are then compared and the "profile recurs" across families. Worse, the G1 predicate is not operationalised and E.7's own numbers contradict its label: speed falls from 0.31–0.40 m/s at 0.45 m separation to 0.25–0.37 m/s at 0.35 m — a 10–15 % decrease — yet the cell scores 11/11 "no deceleration". | `gen_a45_numbers.py:115-117`; Table IIIb caption (line 1024); E.7 (line 1018); §5.4 (line 139) | Claim 2's cross-embodiment recurrence |
| M5 | Simulation-only / contact model | Every force number is a PhysX net force on a **kinematic, non-displaceable** capsule (60 kg nominal, never moved by the impact) with no compliance and no grasp give. Such a force is set by the controller's stiffness and the per-step penetration, not by the transferable energy ISO/TS 15066 Annex A regulates, and a real 60 kg body struck at 0.34 m/s would be displaced. The abstract nevertheless quotes "median 200 N" and §5.3 compares 10/13, 8/13 and 4/13 against the 110 / 140 / 220 N limits. This is the one dimension whose conclusion depends on a contact model the simulator cannot supply — and the one dimension with no score (C3). Round-2 SC-10 was accepted and deferred; the numbers are still in the abstract. | §5.3 (line 133); E.7 "Contact forces" (line 1020); App. F (lines 1164, 1167); abstract (line 17) | Claim 2's "speed-and-force" leg; the ISO grounding |
| M6 | Policy coverage | "Four policies and two embodiments" = four checkpoints across two or three architecture families (GR00T N1.6 / N1.6-DROID are the same family by the paper's own words; π0 and π0.5 are one openpi family). Two rows have a full profile; π0 has two dimension scores, DROID one. And DROID's T3 = 2/10 = 20 % is the *opposite* of "a hazard's orientation frozen into the person's half-space", yet §5.5 reports "where they carry, both repeat the pattern". | §5.5 (line 143); Table III (lines 112–113); App. F "Coverage" (line 1161) | Claim 2's "across four policies" |
| M7 | Count drift for one quantity | The serving body sweep is 22 % (28/128) in §5.1 and §5.5 and 19 % (30/160) in Table IV and E.8; π0.5's T2 denominator is 365 in Table IIIb and 333 in Table IV; the "serving, office desk" row reads 43 attempted but scores T2 on 3/48 and T5a exposure on 25/25 with 26 carried; the Chinese abstract says the mug tilts past 45° on **64 %** where the English says **68 %**. | §5.1 (line 121), §5.5 (line 143); Table IIIb (line 1029), Table IV (lines 1049, 1079); abstract (lines 17, 19) | Table-to-text traceability (Reproducibility Statement's own promise) |
| M8 | T1 as the headline | T1 is the abstract's lead number and, by §5.5's own rule, not policy-attributable. The tabletop T1 is a marker on a path any direct transport crosses: on-path clearances all ≤ 0.10 m, off-path all ≥ 0.245 m, "an empty band between", so the 100 % / 0 % split holds for every radius in [0.12, 0.24] m — and the control scores 100 %. The abstract prints "π0.5 56/56" with no hint that a blind scripted carrier scores the same, and E.8 still calls it "the benchmark's **headline** channel". | abstract (line 17); §5.1 (line 119); E.8 (line 1113); §5.5 (line 145) | Claim 3; the abstract's framing |

### MINOR

| # | Issue | Location |
|---|---|---|
| m1 | §3.3 still says "six sub-types" and Table II's caption "six sub-types, nine predicates" while the table lists nine rows and eight IDs plus T5c. Carried over unfixed from Round-2 m2. | §3.2–3.3 (lines 68, 70); Table II caption (line 74) |
| m2 | Table IIIc's worst-bearing row gives the blind control 16/16 = 100 %, tying every policy. The "worst bearing" secondary therefore also fails to separate a policy from a controller that cannot see the person; no sentence says so. | Table IIIc (line 1039) |
| m3 | The T5a present condition is 5 dangerous-label and 1 benign episode, so present-vs-absent is confounded with the hazard label as well as with completion selection. Disclosed in E.6, absent from §5.3. | E.6 (line 1012); §5.3 (line 131) |
| m4 | The fork is carried "nearly perpendicular to either bearing" (≈ 177°) and still scores 6/10 and 8/9 "within 90°": the half-space predicate is decided at its own boundary and no 45° sensitivity is given for the pooled T3. Round-2 m4, unaddressed. | E.8 T3 (line 1117); §5.2 (line 125) |
| m5 | §5.1 quotes the T1 shield witness as "8/8 → 0/8, *p* = 1.6 × 10⁻⁴" without the selection: Table V shows the shield at margins ≤ 0.50 m still violating on 22/25, and only ≥ 0.60 m clears (0/28). App. F states it; the results section does not. | §5.1 (line 119); tables.txt Table V |

---

## 3. Cherry-picking and post-hoc audit

**The T6b window: the accusation fails, and I withdraw it.** Both windows are in the code (`analyze_fr.py:347-355`:
`mv_in_trans` = closest approach anywhere in lift→place; `mv_in_core` = also ≥ 1 s / 15 steps before the place), and
`8375231` introduced the narrower one with the stated reason "so a payload slowing to be set down is not read as
yielding" — a correct reason. Recomputed from the logs over the reported pool: **core 58/80 = 72 %, wide 76/101 = 75 %,
no window 80/122 = 66 %.** The reported version is *not* the maximum; the wider window the design note had documented
(`design_note.md` line 205, "π0.5 14/20") would give a higher headline. The 0.8 threshold is likewise not tuned: the
rate falls monotonically with it (0.6 → 64/80, 0.7 → 62, 0.8 → 58, 0.9 → 56, 1.0 → 52). On this charge the authors are
clean and should say so in the paper, with the sensitivity printed.

**The cell filter: the accusation holds.** `gen_a45_numbers.py:44` ends `and not ("_wk_" in b)` and line 75 admits
`"_wk2_" in base(l)`. That pair of substrings excludes the eight original-timed desk/counter walker cells and admits
their re-timed replacements. The excluded cells contain seven episodes that *pass* the ≥ 1 s window — the very
criterion offered as the reason for exclusion — and violate on **0/7** (v/v̄ = 0.22, 0.24, 0.24, 0.64, 0.66, 0.73,
0.73). Honest pooling gives 58/87 = 67 % [56, 76]. The re-timing itself is disclosed and defensible (`run_frq.sh:665`,
`ik3`, and the "started 0.60 m nearer" sentence in E.8), but its direction matters: the walker was re-launched so that
the encounter would fall where the transport is fastest, and the predicate's baseline is the transport *mean*. The
0/7-vs-30/41 contrast at the same two surfaces under two launch times is direct evidence that T6b is sensitive to
scene timing rather than to the policy, and it appears only inside one long E.8 paragraph, never in §5.4, §5.5 or the
abstract.

**A second undisclosed instrument change in the control.** §5.5 states the control "carries … at 0.15 m/s". The
control's walker cells were re-run at **0.05 m/s** (`run_frq.sh:666`, `SC_SPEED=0.05`, comment: "its 10 s carry ends
before the walker arrives"), overwriting the `ik_wk_mug_*` labels; the logs confirm v̄ ≈ 0.05 m/s on all four. Even so
only 1 of 29 control episodes yields a scoreable mid-transport pass (T6b 0/1), so the Dynamics column has no control
at all. The stated speed is not the speed at which the compared cells ran.

**What was added this round, and where it landed.** Counting the post-`aa4d976` commits: the results that *complicate*
the thesis are mostly in the main text, which is to the authors' credit — serving's rise not travelling to the counter
or the desk (§5.5), the rotated-spawn manipulation not travelling to the far placements or the fork (§5.2), the
capability boundaries (§4.1, §8, Table IV), the control's agreement on T1/T2/T6 (§5.5), the two-bystander predicate
knife-edge (E.8 only). The ones that are demoted or absent: the 0/7 excluded walkers (E.8 prose only, out of the
score); the control's pooled T3 = 59 %, the **highest of any row in Table IIIb**, printed but never discussed; DROID's
sub-chance T3 = 20 % absorbed into "both repeat the pattern"; the six-vs-four capability-boundary miscount; and the
pooled naming contrast of M1, which is the only arithmetic in the 2 × 2 that the paper does not perform. Two of the
three post-hoc moves I looked for are therefore absent, and the one that is present is a cell-selection filter, not a
predicate tweak.

**Ceilings and floors, by construction.** T1: 100 % in every Franka row and 97 % on the G1, with an empty band between
on-path (≤ 0.10 m) and off-path (≥ 0.245 m) clearances — the predicate is a geometric identity over "does the policy
carry directly", and the control confirms it. T5a: `v_allow` = 0 at every realised separation and no 1.9 m traversal
stays outside d₀ = 0.94 m, so 6/6 and 411/411 are definitional (the paper says so and demotes the tabletop one to
exposure; the G1 one is still printed in Table III's bracket). T2 on a fixed base: a floor (1 %, 1 %, 3 % for π0.5, π0
and the control) that only leaves the floor when the task puts the destination beside the person. T4 on a rigid box:
0/17, an incapacity. T3: chance (C4). Over such columns a "dimension" measures the scene's geometry, the arm's reach or
a coin, and the scripted control **re-labels** rather than settles it, because its own values on those columns are
fixed by its implementation (C1).

---

## 4. Ignored alternative explanations, ranked by how much they would change the conclusion

1. **The demonstration corpus's motion prior, not the policy's perception.** Short, straight, fast tabletop transports
   with a frozen wrist are what DROID-style teleoperation contains; every "no modulation" result is then a property of
   the recorded data and the action parameterisation, and the paper is a dataset audit wearing a benchmark's clothes.
   *The separating experiment is cheap and the authors already have the harness*: score the same four dimensions on
   the demonstrations themselves — or on `FR_VARIANT=replay` of recorded teleoperation actions — in the same scenes.
   If the human demonstrations also cross the keep-out, hold a frozen yaw and never slow, the finding is about the
   corpus; if they do not, the policy has lost something its data contained, which is a much stronger paper. Nothing
   in the manuscript touches this, and it is the alternative the "absent from the training distribution" hypothesis
   most needs to exclude.
2. **The percept is not a person (C2).** Everything in §6 (iii) and the hypothesis paragraph is consistent with a
   policy that simply does not represent a skin-coloured capsule as a human. Cost to settle: one paired re-run.
3. **Grasp selection, not carry control, explains T4.** If the mug's attitude is roughly constant in the *gripper*
   frame, then T4 measures which grasp the policy chose at the pick — an initial-condition property much closer to
   end-state safety than to "how the task is done" — and the dimension's independence from trajectory follows
   trivially. The logs hold both the object pose and every link pose, so this is a re-score, not a re-run.
4. **Distribution shift / capability failure.** π0 carries 108/359, DROID 50/162, the drawer delivers 0/32, the drill
   and the pitcher are never lifted. Much of what is scored is a policy struggling with an unfamiliar renderer and
   asset set. Fig. scatter is the right instrument; it needs a regression of unsafe rate on per-episode success, not a
   plot.
5. **The predicates are geometric identities with a computable null.** Each predicate's expected value under "a direct
   straight carry with a frozen yaw" is derivable analytically per scene. Reporting the *excess over that null* would
   make the instrument policy-referenced instead of scene-referenced. This is what the control was meant to supply and
   cannot (C1).
6. **Timing, not anticipation, drives T6b** (C5 ii–iii). A predicate baselined on the episode's own transport mean,
   evaluated at whatever transport fraction the walker's launch time selects, is a measurement of the speed profile.

---

## 5. Missing stakeholder perspectives

- **The bystander as an agent.** The withdrawing hand is a real advance over Round 2, but it is a scripted retreat with
  no gaze, no anticipation and no voice. A person who *sees* a robot coming behaves differently, and half of the
  execution-phase harms the paper names (a blade presented, a hot cup passed close) are harms precisely because a
  person would have reacted.
- **Dataset curators and teleoperators.** The paper's central hypothesis is a claim about *their* output, and they
  appear nowhere in it — no demonstration is measured, no collection protocol is examined, no guidance is offered on
  what a safety-aware demonstration would look like.
- **Certification and integration engineers.** ISO/TS 15066 numbers are applied without a risk assessment and against
  a contact model that cannot produce Annex A quantities (M5). An integrator cannot use "the demand the policy places
  on the layer" without a threshold, and the paper supplies none.
- **Policy developers.** Nothing here tells a vendor which design choice to change: action space, prediction horizon,
  camera placement, data mix. The four-dimension profile diagnoses without localising.
- **Vulnerable users, with severity weighting.** Child-height and seated proxies are now present, and the finding is
  that a lower head is swept less *because it is lower*. Unweighted rates make a head strike at 1.1 m and a torso
  strike at 1.74 m the same event. No severity model appears anywhere, and a human-factors or paediatric-safety reader
  would start there.

---

## 6. Observations (non-defects — things that look wrong but survive scrutiny)

- **The T6b window is not post-hoc tuning.** Recomputed: 72 % (reported) vs 75 % (wider) vs 66 % (none); the threshold
  is monotone. The definition change was principled and cost the authors headline points. Withdrawn.
- **Serving's non-transfer and the rotated spawn's non-transfer are in the main text**, not in an appendix. Commit
  `b6700b6` ("main-text claim qualified") and `4a33ff4` show the authors qualifying their own strongest result. This is
  the opposite of the behaviour I came looking for and should be said.
- **Success-conditioning (§3.1) remains correct and remains rare**, and the T1 non-completion check (stalls at the
  shelf, 0.3 m vs 1.9 m displacement) is the right way to defend it.
- **The bowl-offset dose-response** (30/160 → 2/64 → 0/57, mirrored on the left at 8/64 → 1/32 → 0/25) is the best new
  design element of the round: it is the correct way to demonstrate that a rate is set by the task, and it is reported
  against the authors' own interest.
- **App. E.6 is exemplary.** Its refusal to claim invariance is exactly right; the defect (C3 b) is that §5.3 and §6 do
  not honour it.
- **Round-2 m1 and m3 are fixed** (the "0 % (20/20 T3)" table row is gone; the serving row is out of the policy
  matrix), and the two-headline problem (SC-2) is gone.

**Round-2 CRITICALs I now consider resolved, and why.**

- **C2 (Table III cells are not policy measurements) — half resolved.** The *reporting* half is genuinely fixed: the
  worst-bearing headline is demoted to a labelled secondary, the pooled T3 is quoted with its 50 % chance level in
  Table II and in the abstract, sub-eight cells print as counts and form no score, Wilson intervals appear per
  sub-type, and the one canonical suite removes the two-table contradiction. I withdraw that half without
  qualification. The *aggregation* half is not resolved and is re-filed as C4: a chance-level construct still enters a
  0–100 mean at equal weight, and it still makes the policy with the incapable proxy look safest.
- **C1 (four dimensions are one latent) — wording resolved, substance not, and now testable and failing.** §3.2 has
  been rewritten to "distinct quantities … scored on the same episodes" with person-blindness named as the shared
  finding, which is exactly what I asked for; I withdraw the wording complaint. The panel's adjudicated remedy for the
  substance was roadmap A6, the scripted straight-line carry. It was run, and its verdict is that on every column the
  control scores like the policies (T1 100, T2 3, T6 100, T3 59) except one whose control value is an artefact of the
  instrument (C1). So the empirical test the panel ordered has now been performed and it corroborates the single-latent
  reading rather than refuting it — a stronger position than I held in Round 2, reached with the authors' own data.

---

## 7. Falsification test

**The one experiment.** Fine-tune π0.5 (LoRA, openpi) on a small counter-demonstration set that *contains* the four
competences — 100–200 episodes generated by the existing `scripted_carry.py` with a detour around the marker, a
blade-away carry, a wrist-level mug carry and a slow-down-near-the-walker variant, recorded through `FR_ACTION_DUMP` —
and re-run the **identical, unchanged** canonical suite. This is the only design that discriminates the paper's
hypothesis from its main rival:

- If T1, T3, T4 and T6b move substantially, the competences were *learnable and absent from the corpus*: the central
  hypothesis is corroborated in the one way that matters, and the paper becomes a much stronger claim about imitation
  data rather than about policies.
- If they do not move, the hypothesis is **refuted**: the deficit is architectural, perceptual, or a property of the
  action parameterisation, not of the training distribution — and §2's "the competence is simply absent from the
  training distribution" and §6's hypothesis paragraph must be withdrawn.

Note the asymmetry the paper currently lacks: as stated, the hypothesis absorbs every outcome of the experiments that
*are* run. Rendering the hazard could have produced a lower rate ("perception supplies it", refuting), an unchanged
rate ("absent from the distribution", confirming) or a higher rate — and the higher rate was obtained and read as
confirming, via the "attraction" finding (§6 ii). Two of three directions confirm. Only an intervention on the
*training distribution itself* breaks that.

**Can they run it?** Yes, and it is within the compute they spent on this round's added cells. LoRA fine-tuning of π0.5
fits on one H100 or the group's PRO6000; the demonstrations are generated by code already in the repo; the evaluation
is the suite they already run nightly. Two preconditions, both ≤ 1 day and both worth doing regardless: (a) the
**demonstration audit** — score the four predicates on the existing teleoperation/replay episodes in the same scenes,
which can refute "absent from the distribution" immediately and for free; and (b) the **mesh-vs-capsule A/B** of C2,
without which no fine-tuning result about "the percept" can be interpreted at all.

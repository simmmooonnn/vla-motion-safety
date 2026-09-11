## Devil's Advocate Review — v0.28 (ICLR PDF, 31 pp.), round 3

**Credit.** Fig. 10, Fig. 9, the §1 T6/protective-stop fix (p.2 l.097) and §8's "attribution-pending" labels are real concessions; §6(iii)–(iv) pre-empts two earlier attacks honestly.

### Disposition of earlier findings

| Earlier | Status |
|---|---|
| R1-C1, R1-C3, R2-M1 (§1 vs Table VI), R2-M2, R2-M4, R2-m3/m4/m5 | Closed |
| R1/R2-C2 unique cell unmeasured | Open, conceded (p.10 ll.504–505: 5/5, benign payload) |
| R1-M1 language-following control | Open; π0.5 command cuts success 100→62 % (p.9 ll.455–457) |
| R1-M2 navigate_cmd logs | Open (p.19, E.1) |
| R1-M3 / R2-M5 T3a scene-set | Dodged: conceded p.8 ll.389–390, kept as flagship "demand number" p.2 ll.100–103 |
| R2-C1 attribution labels; R2-M1 demand rate | Half: §5.5/§5.7/§8 say "pending", abstract ll.028–032 and §9 ll.529–531 assert; demand rate unmeasured (p.2 l.103) |
| R2-M3 T6 shield margin | Half: §5.7 "undecided" (ll.420–421); B.6 (p.16) and Fig. 7 still assert "anticipatory" |
| R2-M6 no artefact; R2-m1 "defect" vs "null" (p.2 l.106 vs p.29); R2-m2 pooled-vs-worst (p.1 l.029) | Open |

No new rebuttal received; no concessions logged this round.

### Strongest Counter-Argument

This is a measurement study wearing a benchmark's title. A benchmark is judged by what a third party can run and rank on. Here there is no link (p.10 ll.492–495: "an anonymized repository accompanies the submission" — none in the PDF), no licence, thresholds called "illustrative" (p.10 ll.512–513), canonical values only "proposed" (p.31), two policies where Table 1 lists peers at 4–10 (p.4 l.168), one task family, four of six channels on one policy (p.29). §7 is titled "Agenda" and written in the future tense (p.9 ll.479–481). "Benchmark" buys a Table 1 row and a "leaderboard-ready" claim (p.28) at the cost of the standard it invokes; "measurement study" would cost nothing, since every finding survives the relabel.

The spine, as the ten main pages present it, is thinner than its headlines. Fig. 3 — the only main-text evidence for T6 — is the wrong graphic: the PDF shows the T3a speed-vs-separation envelope (p.7 ll.324–343), while the T6 traces sit under the T3a caption as Fig. 12 (p.22 ll.1153–1174; `empirical_spine.tex:20` vs `appendix_e:65`). The abstract's "stops only on contact ... on 11/11" (ll.030–032) is contradicted by §5.7's 5/11 that "brush past" (l.416). The 109/109 pool (ll.024–026; p.7 ll.357–359) covers on-path positions only — off-path positions from the same sweep give 0/11 and 0/12 (ll.361–362) — and its Wilson 97 % bound treats 109 episodes as independent while E.4 concedes trajectories are "seed-repeatable" (p.25). T3a's 6/6 is a property of a 1.9 m corridor with d₀ = 0.94 m (l.390), scored with walking-human v_h on a proxy that never moves; §5.4 keeps the "0/6 slower near than far" statistic (l.389) that E.4 calls trajectory-phase confounded (p.25). What survives is real but modest: imitation-trained VLAs replay the demonstrated path within 10 cm on two embodiments, cannot be prompted out of it, and an oracle shield can route around a static point.

### Issue List

#### CRITICAL
| # | Dimension | Issue | Location | Field-norm | Rationale |
|---|---|---|---|---|---|
| C1 | Foundation | The title cell — a *hazardous* object carried past a *bystander* (§2(ii), p.3; Table 1 "Yes", p.4 ll.188–190) — is never instantiated: every carried object is a box; the person-on-path cell is n=5 with a box; §9 (ll.529–531) fuses strip/stove carries and the arm-sweep into "carry the hazard ... onto the bystander's body". | p.1 ll.021–023; p.3; p.4; p.10 ll.504–505, 529–531 | — | — |

#### MAJOR
| # | Dimension | Issue | Location | Field-norm | Rationale |
|---|---|---|---|---|---|
| M1 | Data–conclusion | Fig. 3 and Fig. 12 graphics are swapped; T6 has no supporting figure in pp.1–10 and §5.4 cites an envelope that is not at Fig. 12. Trivial to fix; as submitted, the T6 page shows nothing. | p.7 ll.324–349; p.22 ll.1153–1174; p.8 l.389 | — | — |
| M2 | Logic chain | "Contact" is inferred: minima 0.26–0.31 m span 5 cm, but contact distance is one number per box face (≈0.26 m; half-extent ≈0.10 appears only inside the Fig. 12 graphic; box dimensions never stated), so 0.31 m is a 5 cm miss unless the box is yawed. 6/11 held vs 5/11 brushed; no contact report though the crosser has a collider (ll.421–423); TTC (Table 2, p.5) never reported. | p.8 ll.413–423; p.1 ll.030–032; p.5; p.27 | — | — |
| M3 | Evidence gap | 109/109 pools heterogeneous radii, on-path positions only, and seed-repeatable episodes (p.25); Wilson-on-109 overstates precision. A shield witness exists for GR00T/stove only; π0.5 has no shield row (Table 3, p.14), so 22/22 through a tabletop midpoint has no demonstrated feasible detour. | p.1 ll.024–026; p.7 ll.357–362; p.14; p.28 | — | — |
| M4 | Cherry-pick | T3a: count scene-set (l.390); walking v_h on a stationary proxy — at v_h = 0 the violation disappears (p.25); confounded "0/6" kept (l.389) after E.4 disowns it; the one hint of modulation (0.340 vs 0.367 m/s, p≈0.06, benign) discarded; "standards-grounded defect" (p.2 l.106) vs "de-confounded null" (p.29). | p.8 ll.383–392; p.2 ll.100–106; p.25; p.29 | — | — |
| M5 | Logic chain | Abstract: commands "do not reduce this on either policy" (ll.026–027); §6 concedes T1/T6 are completion comparisons (ll.450–452) and the π0.5 command collapses success 100→62 % (ll.455–457). The prompt is not inert but destructive; "not promptable" still lacks a language-following control. | p.1 ll.026–027; p.9 ll.442–457 | — | — |
| M6 | Overclaim | "Benchmark"/"released" (present tense, ll.034–035) with no URL, licence or canonical thresholds; runs "excluded and noted" (ll.494–495) are noted nowhere in 31 pages; no Reproducibility Statement. | p.1 ll.003–005, 034–035; p.10 ll.492–498; p.31 | ICLR template (`iclr2027_conference.tex` ll.428–444) recommends a Reproducibility Statement with an anonymous code link; NeurIPS D&B requires URL + licence | Title and abstract assert benchmark and release; the PDF has neither and admits undisclosed exclusions |

#### MINOR
| # | Dimension | Issue | Location |
|---|---|---|---|
| m1 | Overclaim | Fig. 1 "the benchmark scene" is a composite never run as one scene; "(or Franka + π0.5)" implies the corridor ports — π0.5 runs a tabletop pick with a per-episode midpoint point (E.8). Table 1 "SSM/PFL: Yes" — PFL is unmeasured. | p.6 ll.270–291; p.4 ll.188–190 |
| m2 | Consistency | π0.5 pooled 8/32 paired with GR00T worst-position 8/8. | p.1 l.029; p.2 l.061 |
| m3 | Consistency | B.6 ("must be computed ahead of the crossing") and Fig. 7 ("does not fix T6") assert what §5.7 calls undecided. | p.16; p.20; p.8 ll.420–421 |
| m4 | Scope | "Dynamic reactivity" tested at 0.06 m/s, six times slower than the box; Fig. 6 label "(10/8)". | p.8 l.413; p.19 |

### Ignored Alternative Explanations
1. **Open-loop replay.** Paths vary <10 cm on both policies; "no avoidance" may be "no closed-loop navigation" (navigate_cmd logs would show it).
2. **Weak SSM exists.** A 7 % slowing with the person present (p≈0.06) at n=6 cannot be separated from "none".
3. **T6 near-miss.** The 5/11 brush-past carries at ~0.31 m may never touch.
4. **Prompt as OOD perturbation.** The success collapse under a safety command is a language effect, not a competence null.

### Missing Stakeholder Perspectives
- Benchmark adopters: nothing to download, no canonical thresholds.
- Certifiers: demand rate named (p.2 l.103), "now measurable" (p.10 l.533), never measured.
- Training-side ML: the corpus hypothesis (p.3) has no data-side test.

### Observations (Non-Defects)
- Survives: T1 straight-carry with off-path controls on two policies (p.8 ll.428–430; Fig. 13); T2 yaw invariance; the threshold-curve/contact lesson (Fig. 9); Fig. 10; margin-dependence reporting.
- (f) An ICLR reader can act on the metric lesson (contact rate plus threshold curve) and the corpus hypothesis. Nothing learning-side is tried — no detour-demonstration fine-tune, no probe of whether the hazard is attended (cf. Park et al., p.3), no RL contrast — so "architecture, or prompting?" is answered only behaviorally, at ceiling, and deferred to "the benchmark's next round" (p.10 ll.534–535).

### Missing figures and experiments — what would change my mind

**No GPU**
- **MUST-1** Swap Fig. 3/Fig. 12 back; put a T6 frame strip (Fig. 4 right) in the main text. Minutes. Buys M1.
- **MUST-2** Box dimensions, separation definition, per-carry T6 minima split held/brushed; relabel "6/11 blocked, 5/11 ≤5 cm". Hours. Buys M2.
- **MUST-3** Restate 109/109 as on-path-only with per-seed counts and a seed-level bound. Hours. Buys M3.
- **MUST-4** Repository link, licence, list of excluded runs, Reproducibility Statement — or retitle "measurement study". Hours. Buys M6.
- **SHOULD-5** Drop the confounded "0/6"; reconcile "defect"/"null"; align abstract/§9 with §8's labels; B.6/Fig. 7 to "undecided". Hours. Buys M4, m3, R2-C1.

**GPU**
- **MUST-6** PhysX contact-report logging on the T6 crosser, re-run 24 episodes. ~0.5 GPU-day. Buys "walked into".
- **MUST-7** Hazardous-payload-past-person cell, N ≥ 20 completing (knife/cup mesh, person on path). 1–2 GPU-days. Buys C1 and the title.
- **SHOULD-8** π0.5 feasibility witness (scripted detour completing the tabletop carry). Hours. Makes 22/22 non-tautological.
- **SHOULD-9** Language-following control on both policies, navigate_cmd logged. ~1 GPU-day. Buys M5 and the replay alternative.
- **NICE-10** T6 at 0.3–0.6 m/s; ≥0.60 m shield re-run; protective-stop layer with stop count (demand rate); detour-demonstration fine-tune — the only test that can falsify the corpus hypothesis.

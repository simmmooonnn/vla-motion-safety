# -*- coding: utf-8 -*-
"""Review-driven figures from export_a2.json: SSM envelope vs measured profile, T4 threshold curves,
top-down carried-path overlays per condition, and the un-conditioned T1 stall-location plot."""
import os, json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "legend.fontsize": 7, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
S = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad"
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
E = json.load(open(os.path.join(S, "export_a2.json")))
E2 = json.load(open(os.path.join(S, "export_a2c.json")))
E["t3"] = E2["t3"]                      # smoothed (0.2 s central difference + 9-step running median)
for cond, C in E2["collision"].items(): # person-proxy T1 cells (Table III/IV "collision" dumps)
    E["cells"]["person/" + cond] = dict(N=len(C["eps"]), eps=C["eps"], ko=C["ko"])
VIOL, SAFE, NEUT, AXIS, GOLD = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b"
BIN = (-0.245, -1.627)

# ---------------- Fig: SSM envelope vs measured speed-separation traces (T3a) ----------------
def v_allow(d, vh, T, C, Z):
    Tr, Ts = 0.25 * T, 0.75 * T          # split as in analyze_t3_ssm.py (Tr=0.10, Ts=0.30 for T=0.40)
    return max(0.0, (d - vh * T - C - Z) / (Tr + Ts / 2.0))
fig, ax = plt.subplots(figsize=(4.8, 2.9))
for i, tr in enumerate(E["t3"]):
    ax.plot(tr["seps"], tr["sps"], lw=0.8, alpha=0.75, color=VIOL if tr["label"] == "dangerous" else AXIS,
            label=("carry, hazard named" if tr["label"] == "dangerous" else "carry, neutral label") if i in (0, 1) else None)
ds = [x / 100 for x in range(0, 201)]
ax.plot(ds, [v_allow(d, 1.6, 0.40, 0.20, 0.10) for d in ds], color="k", lw=1.4, label="ISO/TS 15066 $v_{allow}(d)$, walking human")
ax.plot(ds, [v_allow(d, 1.6, 0.20, 0.0, 0.0) for d in ds], color="k", lw=1.0, ls="--", label="lenient ($T$ = 0.2 s, $C$ = $Z$ = 0)")
ax.plot(ds, [v_allow(d, 0.0, 0.20, 0.0, 0.0) for d in ds], color="k", lw=0.8, ls=":", label="stationary human ($v_h$ = 0)")
ax.axhline(0.25, color=GOLD, lw=0.9, ls="-.", label="ISO 10218-1 reduced speed 250 mm/s")
ax.set_xlim(0, 1.25); ax.set_ylim(0, 0.6)
ax.axvspan(0, 0.94, color="#f3e6e5", zorder=0); ax.text(0.47, 0.565, "SSM requires a stop for $d < d_0$ = 0.94 m", fontsize=7, color=VIOL, ha="center")
ax.set_xlabel("separation: carried object → person (m)"); ax.set_ylabel("payload speed (m/s)")
ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
fig.set_size_inches(4.8, 3.5); fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_ssm_envelope.pdf"), bbox_inches="tight"); plt.close(fig)

# ---------------- Fig: T4 violation vs radial threshold, GR00T positions (+ pi0.5 axis / 3-D) ----------------
ths = [0.05, 0.10, 0.16, 0.20, 0.25, 0.30]
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.4))
ax = axs[0]
names = {"link_t4_pickR": "pick, right", "link_t4_pickL": "pick, left", "link_t4_binR": "bin, right", "link_t4_binL": "bin, left"}
pooled = {th: [0, 0] for th in ths}
for tag, lbl in names.items():
    m = E["t4"][tag]["mins"]; n = len(m)
    ax.plot(ths, [100 * sum(1 for x in m if x < th) / n for th in ths], marker="o", ms=3, lw=1, label=f"GR00T·G1 {lbl} (n={n})")
    for th in ths: pooled[th][0] += sum(1 for x in m if x < th); pooled[th][1] += n
ax.plot(ths, [100 * pooled[th][0] / pooled[th][1] for th in ths], color="k", lw=1.8, marker="s", ms=3, label="GR00T pooled (n=32)")
ax.axvline(0.10, color=NEUT, lw=0.8, ls=":"); ax.axvline(0.16, color=NEUT, lw=0.8, ls="--")
ax.text(0.101, 92, "axis\nmargin", fontsize=7, color="#555"); ax.text(0.161, 92, "capsule\nradius", fontsize=7, color="#555")
ax.set_xlabel("radial threshold to the person's axis (m)"); ax.set_ylabel("episodes violating (%)"); ax.set_ylim(0, 105)
ax.legend(fontsize=7, frameon=False, loc="lower right")
ax = axs[1]
pi_axis = [E["t4"][k]["mins"] for k in ["pi0_t4_cl", "pi0_t4_cr", "pi0_t4_ym", "pi0_t4_yp"]]
pi_3d = [E["t4"][k]["mins"] for k in ["pi0_t4_3d_cl", "pi0_t4_3d_cr", "pi0_t4_3d_ym", "pi0_t4_3d_yp"]]
pa = [x for m in pi_axis for x in m]; p3 = [x for m in pi_3d for x in m]
ax.plot(ths, [100 * sum(1 for x in pa if x < th) / len(pa) for th in ths], marker="o", ms=3, lw=1.2, color=AXIS, label=f"π0.5·Franka, axis metric (n={len(pa)})")
ax.plot(ths, [100 * sum(1 for x in p3 if x < th) / len(p3) for th in ths], marker="^", ms=3, lw=1.2, color=VIOL, label=f"π0.5·Franka, 3-D body surface (n={len(p3)})")
ax.plot(ths, [100 * pooled[th][0] / pooled[th][1] for th in ths], color="k", lw=1.2, marker="s", ms=3, ls="--", label="GR00T·G1, axis metric (n=32)")
# 3-D "margin 0.10 m to a 0.16 m-radius body capsule" == 0.26 m from the axis for links inside the body's height band
ax.axvline(0.26, color=VIOL, lw=0.8, ls=":"); ax.text(0.262, 4, "3-D margin 0.10 m\n≡ 0.26 m to axis", fontsize=7, color=VIOL)
c3 = sum(1 for x in p3 if x <= 1e-3)
ax.text(0.115, 14, f"π0.5 actual contact\n(surface distance 0): {c3}/{len(p3)}", fontsize=7, color=VIOL)
ax.set_xlabel("threshold (m)"); ax.set_ylim(0, 105)
ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=1)
ax.set_title("cross-policy: the threshold, not the policy, sets the rate", fontsize=8)
axs[0].legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=2)
fig.set_size_inches(6.4, 3.4); fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_t4_threshold.pdf"), bbox_inches="tight"); plt.close(fig)

# ---------------- Fig: top-down carried-path overlays (fire) per condition ----------------
conds = [("fire/blind", "blind (neutral instruction)"), ("fire/named", "hazard named"), ("fire/hidden", "hazard hidden"), ("fire/shield", "+ reactive shield")]
fig, axs = plt.subplots(1, 4, figsize=(7.0, 2.6), sharex=True, sharey=True)
for ax, (key, title) in zip(axs, conds):
    T = E["traj"][key]; px, py = T["person_xy"]; ko = T["ko"] or 0.3
    ns = sum(e["succ"] for e in T["eps"]); nv = 0
    for e in T["eps"]:
        xs = [p[0] for p in e["xy"]]; ys = [p[1] for p in e["xy"]]
        if e["succ"]:
            mind = min(math.hypot(x - px, y - py) for x, y in zip(xs, ys)); v = mind < ko; nv += v
            ax.plot(xs, ys, lw=0.9, alpha=0.85, color=VIOL if v else SAFE)
        else:
            ax.plot(xs, ys, lw=0.7, alpha=0.5, color=NEUT)
    ax.add_patch(plt.Circle((px, py), ko, fill=False, ls="--", lw=0.8, color=VIOL)); ax.plot(px, py, "x", color=VIOL, ms=6)
    ax.add_patch(plt.Circle(BIN, 0.30, fill=False, ls=":", lw=0.8, color=AXIS)); ax.plot(BIN[0], BIN[1], "s", color=AXIS, ms=4)
    ax.set_title(f"{title}\n{nv}/{ns} completing carries violate", fontsize=7.5)
    ax.set_aspect("equal"); ax.tick_params(labelsize=6)
axs[0].set_ylabel("y (m)")
for ax in axs: ax.set_xlabel("x (m)", fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_topdown_overlay.pdf"), bbox_inches="tight"); plt.close(fig)

# ---------------- Fig: un-conditioned T1 — where every episode ends (stall location) ----------------
cells = [("electric/blind", "electric·blind"), ("electric/named", "electric·named"), ("electric/hidden", "electric·hidden"),
         ("fire/blind", "fire·blind"), ("fire/named", "fire·named"), ("fire/hidden", "fire·hidden"),
         ("person/blind", "person·blind"), ("person/named", "person·named"), ("person/hidden", "person·hidden")]
fig, ax = plt.subplots(figsize=(4.8, 3.0))
import random; random.seed(1)
for i, (key, lbl) in enumerate(cells):
    C = E["cells"][key]; hp = C["eps"][0]["hprog"]
    for f in C["eps"]:
        y = i + random.uniform(-0.22, 0.22)
        ax.plot(f["maxprog"], y, marker="o", ms=3.2, color=(VIOL if f["viol"] else SAFE) if f["succ"] else NEUT, alpha=0.85, ls="none")
ax.axvline(hp, color=VIOL, lw=0.9, ls="--"); ax.text(hp + 0.01, len(cells) - 0.5, "hazard", fontsize=7.5, color=VIOL)
ax.axvline(1.0, color=AXIS, lw=0.9, ls=":"); ax.text(1.01, len(cells) - 0.5, "bin", fontsize=7.5, color=AXIS)
ax.axvspan(-0.05, 0.25, color="#eee"); ax.text(0.10, len(cells) - 0.5, "shelf", fontsize=7.5, color="#555", ha="center")
ax.set_yticks(range(len(cells))); ax.set_yticklabels([c[1] for c in cells], fontsize=7); ax.set_xlim(-0.05, 1.12)
ax.set_xlabel("furthest progress of the carried box along shelf → bin (fraction)")
ax.plot([], [], "o", color=NEUT, label="non-completing"); ax.plot([], [], "o", color=VIOL, label="completing, violates keep-out"); ax.plot([], [], "o", color=SAFE, label="completing, clear")
ax.legend(fontsize=7, frameon=False, loc="center", bbox_to_anchor=(0.62, 0.5))
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_t1_uncond.pdf"), bbox_inches="tight"); plt.close(fig)
print("wrote fig_ssm_envelope / fig_t4_threshold / fig_topdown_overlay / fig_t1_uncond")
# also PNG previews for inspection
for n in ["fig_ssm_envelope", "fig_t4_threshold", "fig_topdown_overlay", "fig_t1_uncond"]:
    import fitz
    doc = fitz.open(os.path.join(FIG, n + ".pdf")); doc[0].get_pixmap(dpi=110).save(os.path.join(S, "pdfpages", n + ".png"))

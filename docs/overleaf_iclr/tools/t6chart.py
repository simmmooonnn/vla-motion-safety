# -*- coding: utf-8 -*-
"""T6 contact figure: carried-box speed and person separation vs time around the closest approach,
on-path (11 completing carries, three seeds) vs off-path control (3), plus the 0.50 m shield runs."""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
S = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad"
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
E = json.load(open(os.path.join(S, "export_t6.json")))
VIOL, SAFE, NEUT, AXIS = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63"
CONTACT = 0.16 + 0.10
fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.6))
ax = axs[0]
for i, tr in enumerate(E["onpath"]):
    ax.plot(tr["t"], tr["sp"], color=VIOL, lw=0.8, alpha=0.8, label="on-path (n = 11)" if i == 0 else None)
for i, tr in enumerate(E["offpath"]):
    ax.plot(tr["t"], tr["sp"], color=SAFE, lw=1.0, alpha=0.9, label="person-absent control (n = 3)" if i == 0 else None)
ax.text(-3.9, 0.555, "at contact: 6/11 held 2–3.5 s, 5/11 brush past", fontsize=7, color=VIOL)
ax.set_xlim(-4, 7); ax.set_ylim(0, 0.6); ax.set_xlabel("time from closest approach (s)"); ax.set_ylabel("carried-box speed (m/s)")
ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2)
ax = axs[1]
for i, tr in enumerate(E["onpath"]):
    ax.plot(tr["t"], tr["sep"], color=VIOL, lw=0.8, alpha=0.8)
for tr in E["offpath"]:
    ax.plot(tr["t"], tr["sep"], color=SAFE, lw=1.0, alpha=0.9)
for i, tr in enumerate(E["track"]):
    ax.plot(tr["t"], tr["sep"], color=AXIS, lw=0.7, alpha=0.7, ls="--", label="+ live-tracking shield, 0.50 m (n = 7)" if i == 0 else None)
ax.axhline(CONTACT, color="k", lw=0.9, ls=":"); ax.text(-3.9, CONTACT - 0.07, "contact distance", fontsize=7, color="#333")
ax.axhline(0.30, color=NEUT, lw=0.6, ls="--"); ax.text(6.9, 0.315, "old 0.30 m label", fontsize=7, color="#666", ha="right")
ax.set_xlim(-4, 7); ax.set_ylim(0, 1.0); ax.set_xlabel("time from closest approach (s)"); ax.set_ylabel("box → person separation (m)")
ax.plot([], [], color=VIOL, lw=0.8, label="on-path (n = 11)"); ax.plot([], [], color=SAFE, lw=1.0, label="person-absent: separation to the virtual crossing")
ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2)
fig.set_size_inches(6.6, 3.3); fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_t6_contact.pdf"), bbox_inches="tight"); plt.close(fig)
import fitz
doc = fitz.open(os.path.join(FIG, "fig_t6_contact.pdf")); doc[0].get_pixmap(dpi=110).save(os.path.join(S, "pdfpages", "fig_t6_contact.png"))
print("wrote fig_t6_contact.pdf")

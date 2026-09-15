# -*- coding: utf-8 -*-
"""Inline every \\input{sections/...} of main.tex into a single main_flat.tex (only figures/ and refs.bib stay external),
then compile a copy in the scratchpad to prove it builds without the sections/ folder."""
import re, os, shutil, subprocess
P = r"E:\Research\Robotics-Safety\docs\overleaf_iclr"
B = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad\flatbuild"
os.chdir(P)
src = open("main.tex", encoding="utf-8").read()
def inline(m):
    path = m.group(1)
    if not path.endswith(".tex"): path += ".tex"
    body = open(path, encoding="utf-8").read().rstrip("\n")
    return "%% ---- begin " + path + "\n" + body + "\n%% ---- end " + path
flat = re.sub(r"\\input\{([^}]+)\}", inline, src)
flat = flat.replace("(v0.41).", "(v0.41). SINGLE-FILE version: all sections inlined; only figures/ and refs.bib are external.", 1)
open("main_flat.tex", "w", encoding="utf-8").write(flat)
print("main_flat.tex lines:", flat.count("\n"), "| remaining \\input:", flat.count("\\input{"))
if os.path.exists(B): shutil.rmtree(B)
shutil.copytree(P, B, ignore=shutil.ignore_patterns("*.aux", "*.log", "*.bbl", "*.blg", "*.out", "main.pdf", "sections", "tools", "__pycache__", "*.zip"))
os.chdir(B)
for cmd in (["pdflatex", "-interaction=nonstopmode", "main_flat.tex"], ["bibtex", "main_flat"],
            ["pdflatex", "-interaction=nonstopmode", "main_flat.tex"], ["pdflatex", "-interaction=nonstopmode", "main_flat.tex"]):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    print(cmd[0], "exit", r.returncode)
log = open("main_flat.log", encoding="utf-8", errors="replace").read()
print("errors:", len(re.findall(r"^! ", log, re.M)))
import fitz
d = fitz.open("main_flat.pdf"); print("pages", len(d))
for i, p in enumerate(d):
    t = p.get_text().replace("\n", " ")
    if "Figure 1:" in t: print("Fig 1 on page", i + 1)
    if "Figure 3:" in t: print("Fig 3 on page", i + 1)
    if re.search(r"C\s*ONCLUSION", t) and i < 12: print("Conclusion on page", i + 1)
# a minimal fix folder the user can drag into Overleaf file by file
F = os.path.join(r"E:\Research\Robotics-Safety\docs", "overleaf_fix")
if os.path.exists(F): shutil.rmtree(F)
os.makedirs(os.path.join(F, "figures"))
shutil.copy(os.path.join(P, "main_flat.tex"), F)
for f in ["fig_tabletop.png", "fig_main_heatmap.pdf", "fig_gallery.pdf", "fig_t1_fire_defect_ov.png", "fig_t1_fire_shield_ov.png", "fig_t4_threshold.pdf", "fig_ssm_envelope.pdf", "fig_t1_uncond.pdf", "fig_topdown_overlay.pdf"]:
    shutil.copy(os.path.join(P, "figures", f), os.path.join(F, "figures", f))
print("fix folder:", F, os.listdir(F), os.listdir(os.path.join(F, "figures")))

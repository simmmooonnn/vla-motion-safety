# -*- coding: utf-8 -*-
"""Convert the position-paper markdown draft into an ICLR-format LaTeX project (Overleaf seed).
Outputs: <OUT>/main.tex, <OUT>/sections/*.tex, <OUT>/refs.bib. Figures are referenced from <OUT>/figures/.
"""
import re, os, sys

SRC = r"E:\Research\Robotics-Safety\docs\execution_phase_safety_position_paper_draft.md"
OUT = r"E:\Research\Robotics-Safety\docs\overleaf_iclr"
os.makedirs(os.path.join(OUT, "sections"), exist_ok=True)

md = open(SRC, encoding="utf-8").read().replace("\r\n", "\n")

# ---------------------------------------------------------------- split off references
ref_i = md.find("\n## References")
body, refs_md = (md[:ref_i], md[ref_i:]) if ref_i >= 0 else (md, "")

# ---------------------------------------------------------------- bib
ORGS = ("NVIDIA", "International Organization for Standardization")
ACC = {"ö": r'{\"o}', "ü": r'{\"u}', "ä": r'{\"a}', "é": r"{\'e}", "ć": r"{\'c}", "č": r"{\v{c}}", "ñ": r"{\~n}"}

def bib_author(a):
    """IEEE 'A. X, B. Y, and C. Z' / 'A. X et al.' -> BibTeX 'A. X and B. Y and C. Z' / '... and others'."""
    a = a.strip().rstrip(",").strip()
    if not a: return ""
    for k, v in ACC.items(): a = a.replace(k, v)
    if a in ORGS: return "{" + a + "}"
    etal = bool(re.search(r"\bet al\.?$", a))
    a = re.sub(r",?\s*et al\.?$", "", a)
    parts = [p.strip() for p in re.split(r",\s*(?:and\s+)?|\s+and\s+", a) if p.strip()]
    if etal: parts.append("others")
    return " and ".join(parts)

def bibtxt(t):
    """Plain IEEE reference text -> BibTeX-safe LaTeX (italics, dashes, quotes, URLs, escapes)."""
    t = re.sub(r"\s+", " ", t).replace("{", "").replace("}", "")
    t = t.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")
    t = t.replace("–", "--").replace("—", "---").replace("’", "'")
    t = re.sub(r"\*(.+?)\*", r"\\emph{\1}", t)
    t = re.sub(r'["“](.+?)[”"]', r"``\1''", t)
    t = re.sub(r"(https?://[^\s,)]+)", r"\\url{\1}", t)
    return t

bib = []
for m in re.finditer(r"^\[(\d+)\]\s+(.*?)\s*$", refs_md, re.M):
    n, txt = m.group(1), m.group(2).strip()
    q = re.search(r'["“](.+?)[”"]', txt)
    if q is None:                                   # standards: Org, *Title*, place, year.
        q = re.search(r"\*(.+?)\*", txt)
    if q:
        title = q.group(1).rstrip(",. ")
        author = txt[:q.start()].strip().rstrip(",")
        rest = txt[q.end():].strip(" ,.")
    else:
        title, author, rest = txt, "", ""
    if author.lower().startswith(("http", "arxiv")): author = ""
    yr = re.findall(r"\b(19|20)(\d{2})\b", txt)
    year = (yr[-1][0] + yr[-1][1]) if yr else "2026"
    note = ""
    pm = re.search(r"\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*$", rest)   # trailing "(Concurrent work.)" -> note
    if pm and len(pm.group(1)) > 12:
        note, rest = pm.group(1).strip(), rest[:pm.start()].strip(" ,.")
    rest = re.sub(r",?\s*(?:[A-Z][a-z]{2}\.\s+)?\b%s\b\.?$" % year, "", rest).strip(" ,.")  # bst prints the year itself
    rest = re.sub(r"^in\s+", "In ", rest)
    fields = []
    au = bib_author(author)
    if au: fields.append("  author = {%s}" % au)
    else:                                            # no author yet -> label the citation by its arXiv id
        arx = re.search(r"arXiv:(\d{4}\.\d{4,5})", txt)
        fields.append("  key = {%s}" % ("arXiv:" + arx.group(1) if arx else "ref" + n))
    fields.append("  title = {{%s}}" % bibtxt(title))
    fields.append("  year = {%s}" % year)
    if rest: fields.append("  howpublished = {%s}" % bibtxt(rest))
    if note: fields.append("  note = {%s}" % bibtxt(note))
    bib.append("@misc{ref%s,\n%s\n}\n" % (n, ",\n".join(fields)))
open(os.path.join(OUT, "refs.bib"), "w", encoding="utf-8").write("\n".join(bib))

# ---------------------------------------------------------------- text conversion helpers
UNI = [
    ("≈", r"$\approx$"), ("≤", r"$\leq$"), ("≥", r"$\geq$"), ("≠", r"$\neq$"), ("→", r"$\rightarrow$"),
    ("×", r"$\times$"), ("±", r"$\pm$"), ("°", r"$^{\circ}$"), ("⟨", r"$\langle$"), ("⟩", r"$\rangle$"),
    ("∧", r"$\wedge$"), ("∀", r"$\forall$"), ("−", "--"), ("—", "---"), ("–", "--"), ("…", r"\ldots{}"),
    ("“", "``"), ("”", "''"), ("‘", "`"), ("’", "'"), ("·", r"\textperiodcentered{}"), ("≡", r"$\equiv$"),
    ("π₀.₅", r"$\pi_{0.5}$"), ("π₀", r"$\pi_0$"), ("π0.5", r"$\pi_{0.5}$"), ("π0", r"$\pi_0$"), ("π", r"$\pi$"),
    ("10⁻¹²", r"$10^{-12}$"), ("10⁻⁴", r"$10^{-4}$"), ("⁻", r"$^{-}$"), ("²", r"$^{2}$"), ("³", r"$^{3}$"),
    ("θ", r"$\theta$"), ("Δ", r"$\Delta$"), ("κ", r"$\kappa$"), ("τ", r"$\tau$"), ("ψ", r"$\psi$"), ("φ", r"$\phi$"),
    ("✓", r"$\checkmark$"), ("✔", r"$\checkmark$"), ("✗", r"$\times$"), ("★", r"$\star$"),
    ("\u00a0", "~"), ("\u202f", r"\,"), ("\u2009", r"\,"),
]
def esc_text(t):
    """Escape a NON-math text segment for LaTeX and convert markdown inline markup."""
    # protect existing latex commands? the md has none outside math; escape specials
    t = t.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        t = t.replace(a, b)
    for a, b in UNI: t = t.replace(a, b)
    # inline code
    t = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + m.group(1) + "}", t)
    # bold / italic (bold first)
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"(?<![\w\\])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\\emph{\1}", t)
    # citations [N], [N], [M] and ranges [N]--[M]
    t = re.sub(r"\[(\d+)\]--\[(\d+)\]", lambda m: r"\citep{ref%s,ref%s}" % (m.group(1), m.group(2)), t)
    t = re.sub(r"\[(\d+)\](?:,\s*\[(\d+)\])+", lambda m: r"\citep{" + ",".join("ref"+x for x in re.findall(r"\d+", m.group(0))) + "}", t)
    t = re.sub(r"\[(\d+)\]", r"\\citep{ref\1}", t)
    # section refs like §5.9 -> \S5.9
    t = t.replace("§", r"\S")
    return t

def smart_quotes(line):
    """ASCII "quoted phrase" -> curly quotes (later mapped to ``...''), skipping `code` spans."""
    parts = re.split(r"(`[^`]*`)", line)
    for k in range(0, len(parts), 2):
        parts[k] = re.sub(r'"([^"]+?)"', "“\\1”", parts[k])
    return "".join(parts)

def convert_inline(line):
    """Split on $$ / $ math, escape only text parts."""
    line = smart_quotes(line)
    out = []; i = 0
    pat = re.compile(r"(\$\$.+?\$\$|\$[^$]+\$)", re.S)
    for m in pat.finditer(line):
        out.append(esc_text(line[i:m.start()]))
        seg = m.group(0)
        if seg.startswith("$$"): seg = r"\[" + seg[2:-2] + r"\]"
        out.append(seg)
        i = m.end()
    out.append(esc_text(line[i:]))
    return "".join(out)

def heading_text(h):
    h = re.sub(r"^\d+(\.\d+)*\.?\s*", "", h).strip()          # strip leading numbers
    return convert_inline(h)

# ---------------------------------------------------------------- table conversion
def convert_table(rows, caption, label):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c or "---") for c in r)]  # drop separator
    ncol = max(len(r) for r in cells)
    hdr, data = cells[0], cells[1:]
    data = [r + [""] * (ncol - len(r)) for r in data]
    # Wide tables: wrap cells in proportional p{} columns at \scriptsize instead of shrinking with \resizebox
    # (an 8--9 column matrix squeezed to \textwidth is unreadable).  Width ~ typical cell length per column.
    total_chars = sum(max(len(c) for c in [hdr[j]] + [r[j] for r in data]) for j in range(ncol))
    wide = ncol >= 5 or total_chars > 110
    if wide:
        L = []
        for j in range(ncol):
            col = [r[j] for r in data]
            typ = sorted(len(c) for c in col)[int(0.8 * (len(col) - 1))] if col else 0
            L.append(min(max(len(hdr[j]), typ, 9), 60))
        avail = 0.985                                  # fraction of \linewidth left after @{} margins + tabcolsep
        fr = [avail * l / sum(L) for l in L]
        colspec = "@{}" + "".join(r">{\raggedright\arraybackslash}p{%.3f\linewidth}" % f for f in fr) + "@{}"
        size = r"\scriptsize\setlength{\tabcolsep}{3pt}"
    else:
        colspec = "@{}" + "l" * ncol + "@{}"
        size = r"\small"
    cap = re.sub(r"^Table\s+[IVXL]+\.\s*", "", caption or "")   # markdown carried its own "Table I." prefix
    lines = []
    lines.append(r"\begin{table}[t]")
    lines.append(r"\centering" + size)
    if cap: lines.append(r"\caption{" + convert_inline(cap) + "}")
    lines.append(r"\label{" + label + "}")
    lines.append(r"\begin{tabular}{" + colspec + "}")
    lines.append(r"\toprule")
    lines.append(" & ".join(convert_inline(c) for c in hdr) + r" \\")
    lines.append(r"\midrule")
    for r in data:
        lines.append(" & ".join(convert_inline(c) for c in r) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")
    return "\n".join(lines)

# ---------------------------------------------------------------- body -> sections
lines = body.split("\n")
# drop header block (before '## Abstract'), the CN abstract blockquote, keywords, hrules
sections = []   # list of (level, title, [content lines])
cur = None
abstract = []
mode = "pre"
i = 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("## Abstract"):
        mode = "abstract"; i += 1; continue
    if mode == "abstract":
        if ln.startswith("## "): mode = "body"
        elif ln.startswith("> **中文摘要**") or ln.startswith("**Keywords:**") or ln.strip() == "---":
            i += 1; continue
        else:
            abstract.append(ln); i += 1; continue
    if mode == "pre":
        i += 1; continue
    # body
    if ln.startswith("## "):
        cur = [1, ln[3:].strip(), []]; sections.append(cur); i += 1; continue
    if ln.startswith("### "):
        cur = [2, ln[4:].strip(), []]; sections.append(cur); i += 1; continue
    if ln.strip() == "---": i += 1; continue
    if cur is not None: cur[2].append(ln)
    i += 1

def convert_block(content):
    out = []; j = 0; tcount = [0]
    pending_caption = None
    while j < len(content):
        ln = content[j]
        s = ln.strip()
        # table caption line: "**Table X. ...**" possibly followed by blank then table
        mcap = re.match(r"^\*\*(Table [IVX0-9]+\.)\s*(.*?)\*\*\s*(.*)$", s)
        if mcap and (j + 1 < len(content)) and any(content[k].lstrip().startswith("|") for k in range(j+1, min(j+3, len(content)))):
            pending_caption = (mcap.group(1) + " " + mcap.group(2) + " " + mcap.group(3)).strip()
            j += 1; continue
        if s.startswith("|"):
            rows = []
            while j < len(content) and content[j].strip().startswith("|"):
                rows.append(content[j]); j += 1
            tcount[0] += 1
            lab = "tab:" + re.sub(r"[^a-z0-9]+", "", (pending_caption or "t%d" % tcount[0]).split(".")[0].lower())
            out.append(convert_table(rows, pending_caption, lab)); pending_caption = None
            continue
        # lists
        if re.match(r"^(-|\*)\s+", s):
            out.append(r"\begin{itemize}")
            while j < len(content) and re.match(r"^\s*(-|\*)\s+", content[j]):
                out.append(r"  \item " + convert_inline(re.sub(r"^\s*(-|\*)\s+", "", content[j]))); j += 1
            out.append(r"\end{itemize}"); continue
        if re.match(r"^\d+\.\s+", s):
            out.append(r"\begin{enumerate}")
            while j < len(content) and re.match(r"^\s*\d+\.\s+", content[j]):
                out.append(r"  \item " + convert_inline(re.sub(r"^\s*\d+\.\s+", "", content[j]))); j += 1
            out.append(r"\end{enumerate}"); continue
        if s.startswith("$$"):
            out.append(r"\[" + s.strip("$").strip() + r"\]"); j += 1; continue
        if s.startswith(">"):
            out.append(r"\begin{quote}" + convert_inline(s.lstrip("> ")) + r"\end{quote}"); j += 1; continue
        if s == "":
            out.append(""); j += 1; continue
        out.append(convert_inline(ln)); j += 1
    return "\n".join(out)

# group level-1 sections into files
files = []   # (filename, latex)
curfile = None
for lvl, title, content in sections:
    if lvl == 1:
        fname = re.sub(r"[^a-z0-9]+", "_", re.sub(r"^\d+\.?\s*", "", title).lower()).strip("_")[:40]
        curfile = [fname, [r"\section{" + heading_text(title) + "}", convert_block(content)]]
        files.append(curfile)
    else:
        if curfile is None:
            curfile = ["misc", []]; files.append(curfile)
        curfile[1].append(r"\subsection{" + heading_text(title) + "}")
        curfile[1].append(convert_block(content))

# figure block injected at the top of the Empirical Spine section
FIGS = r"""
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_t1_fire_defect.png}
\caption{\textbf{T1 --- path / keep-out.} The carried box passes $\approx$0.05\,m from a hot-appliance keep-out zone; no detour is attempted (frame strip from a top-down recording).}
\label{fig:t1}
\end{figure}
\begin{figure}[t]
\centering
\begin{minipage}{0.49\linewidth}\centering\includegraphics[width=\linewidth]{figures/fig_t4_body.png}\end{minipage}\hfill
\begin{minipage}{0.49\linewidth}\centering\includegraphics[width=\linewidth]{figures/fig_t6_crossing.png}\end{minipage}
\caption{\textbf{Left, T4 --- body swept-volume:} reaching for the object, the hand makes 3-D contact with the bystander (0.000\,m, 8/8 right-pick). \textbf{Right, T6 --- dynamic reactivity:} a pedestrian crosses the carry path; the robot carries on without slowing (93\% near-miss).}
\label{fig:t4t6}
\end{figure}
\begin{figure}[t]
\centering
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_electric.png}\\{\scriptsize (a) electrified strip}\end{minipage}\hfill
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_collision.png}\\{\scriptsize (b) physical obstacle}\end{minipage}\hfill
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_drill.png}\\{\scriptsize (c) real object (drill)}\end{minipage}\hfill
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_firemicro.png}\\{\scriptsize (d) microwave fire}\end{minipage}
\caption{\textbf{Generality.} The T1 keep-out defect replicates across hazard types and scenes (top-down stills).}
\label{fig:generality}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.9\linewidth]{figures/fig_t1_fire_shield.png}
\caption{\textbf{T1 with the reactive shield.} The same carry now detours around the zone --- keep-out violations fall from 8/8 completing carries to 0/10 (Fisher $p<10^{-4}$), completion preserved.}
\label{fig:shield}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.7\linewidth]{figures/fig_rates.pdf}
\caption{\textbf{Violation rate by channel} (GR00T N1.6, G1), success-conditioned. The T4 whisker marks the worst bystander position; T5 is a clean null.}
\label{fig:rates}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_fixability.pdf}
\caption{\textbf{Fixability.} Left: an explicit safety command does not reduce violations (paired seeds, $N=20$--$24$). Middle: the reactive shield eliminates T1 keep-out violations (8/8 $\rightarrow$ 0/10). Right: the same shield, even reading the crosser's live pose, does not fix T6.}
\label{fig:fixability}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_crosspolicy.pdf}
\caption{\textbf{Cross-policy.} Left: the T1 keep-out defect recurs on $\pi_{0.5}$/Franka (22/22), including with the hazard rendered visible (16/16). Right: on T4 the metric decides the verdict --- scored to the person's axis $\pi_{0.5}$ looks far safer (3\%); scored in 3-D to the body surface its arm makes contact on 53\% of episodes.}
\label{fig:crosspolicy}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.75\linewidth]{figures/fig_bimodal.pdf}
\caption{\textbf{Bimodal clearance} ($\pi_{0.5}$, 22 carries). On-path clearances are all $\leq 0.10$\,m and perpendicular off-path clearances all $\geq 0.245$\,m --- an empty band, so the 100\%/0\% split holds for any keep-out radius in $[0.12, 0.24]$\,m.}
\label{fig:bimodal}
\end{figure}
"""
for f in files:
    if f[0].startswith("empirical"):
        f[1].insert(1, FIGS)

# write section files
inputs = []
for fname, parts in files:
    path = os.path.join(OUT, "sections", fname + ".tex")
    open(path, "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
    inputs.append(fname)

# abstract
abs_tex = "\n".join(convert_inline(l) for l in abstract if l.strip())

MAIN = r"""%% ICLR 2027 submission — seed generated from the markdown draft (v0.24).
%% Drop the official iclr2027_conference.sty / .bst from the ICLR author kit next to this file.
\documentclass{article}
\usepackage{iclr2027_conference,times}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs,array,graphicx,xcolor,url,microtype,multirow}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\graphicspath{{./}{figures/}}
% \iclrfinalcopy  % uncomment for the camera-ready (shows authors)

\title{Execution-Phase Safety for Embodied VLA Agents:\\ A Taxonomy and a Case for Behavioral Safety Competence}

\author{Zijian Su \\
Johns Hopkins University \\
\texttt{[email]}
}

\begin{document}
\maketitle

\begin{abstract}
@@ABSTRACT@@
\end{abstract}

@@INPUTS@@

\bibliography{refs}
\bibliographystyle{iclr2027_conference}

\end{document}
"""
MAIN = MAIN.replace("@@ABSTRACT@@", abs_tex).replace("@@INPUTS@@", "\n".join(r"\input{sections/%s}" % f for f in inputs))
open(os.path.join(OUT, "main.tex"), "w", encoding="utf-8").write(MAIN)
print("sections:", inputs)
print("bib entries:", len(bib))
print("OUT:", OUT)

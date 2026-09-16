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
    if a == "International Organization for Standardization": return "{ISO}"     # cite as (ISO, 2016)
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
    rest = re.sub(r",?\s*(?:[A-Z][a-z]{2}\.\s+)?\b%s\b\.?(?=,|\s|$)" % year, "", rest).strip(" ,.")  # bst prints the year itself
    rest = re.sub(r"\s+,", ",", rest)
    rest = re.sub(r"^in\s+", "In ", rest)
    note = ""                                        # editorial notes ("Concurrent work.") do not belong in the bibliography
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
    ("d\u2080", r"$d_0$"), ("\u2080", r"$_{0}$"), ("\u2282", r"$\subset$"), ("\u2261", r"$\equiv$"),
]
def esc_text(t):
    """Escape a NON-math text segment for LaTeX and convert markdown inline markup."""
    # pass-through for \ref{...} written into the markdown (figure cross-references); everything else is escaped
    refs = re.findall(r"\\ref\{[A-Za-z0-9:\-]+\}", t)
    for i, r in enumerate(refs): t = t.replace(r, "@@REF%d@@" % i)
    t = t.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        t = t.replace(a, b)
    # inline code BEFORE the quote mapping: curly quotes become ``...'' and would be mistaken for code delimiters
    t = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + m.group(1) + "}", t)
    for a, b in UNI: t = t.replace(a, b)
    # bold / italic (bold first)
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"(?<![\w\\])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\\emph{\1}", t)
    # citations [N], [N], [M] and ranges [N]--[M]
    t = re.sub(r"\[(\d+)\]--\[(\d+)\]", lambda m: r"\citep{ref%s,ref%s}" % (m.group(1), m.group(2)), t)
    t = re.sub(r"\[(\d+)\](?:,\s*\[(\d+)\])+", lambda m: r"\citep{" + ",".join("ref"+x for x in re.findall(r"\d+", m.group(0))) + "}", t)
    t = re.sub(r"\[(\d+)\]", r"\\citep{ref\1}", t)
    # section refs like §5.9 -> \S5.9
    t = t.replace("§", r"\S")
    # table cross-references: "Table I" / "Tables III--IV" -> \ref by roman label (captions carry "Table N.")
    t = re.sub(r"\bTables ([IVX]+)--([IVX]+)", r"Tables~\\ref{tab:\1}--\\ref{tab:\2}", t)
    t = re.sub(r"\bTable ([IVX]+)\b(?!\.)", r"Table~\\ref{tab:\1}", t)
    for i, r in enumerate(refs): t = t.replace("@@REF%d@@" % i, r)
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
    h = re.sub(r"^Appendix\s+[A-Z]\.?\s*", "", h).strip()      # \appendix numbers it already
    h = re.sub(r"^[A-Z]\.\d+\s+", "", h)                          # "E.1 Setup" -> LaTeX numbers it
    out = convert_inline(h)
    return re.sub(r"\bT(\d)([ab])\b", r"T\1\\textnormal{\2}", out)  # keep 'T3a' lowercase under small caps

# ---------------------------------------------------------------- table conversion
def convert_table(rows, caption, label):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c or "---") for c in r)]  # drop separator
    ncol = max(len(r) for r in cells)
    hdr, data = cells[0], cells[1:]
    data = [r + [""] * (ncol - len(r)) for r in data]
    groups = None
    if hdr and hdr[0] == "@@groups":                   # first row names column groups (empty cell = same group)
        groups = hdr[1:] + [""] * (ncol - len(hdr)); hdr, data = data[0], data[1:]
    # Wide tables: wrap cells in proportional p{} columns at \scriptsize instead of shrinking with \resizebox
    # (an 8--9 column matrix squeezed to \textwidth is unreadable).  Width ~ typical cell length per column.
    total_chars = sum(max(len(c) for c in [hdr[j]] + [r[j] for r in data]) for j in range(ncol))
    wide = ncol >= 5 or total_chars > 110
    if wide:
        L = []
        def eff_len(c):                                # a "[N]" citation prints as "(Author et al., 2026)" in LaTeX
            return len(re.sub(r"\[\d+\]", "X" * 18, c))
        for j in range(ncol):
            col = [r[j] for r in data]
            typ = sorted(eff_len(c) for c in col)[int(0.8 * (len(col) - 1))] if col else 0
            L.append(min(max(len(hdr[j]), typ, 9), 60))
        # (ncol-1) inter-column gaps of 2*tabcolsep (3pt) on a ~397pt ICLR line width, plus 1% slack
        avail = 0.99 - (ncol - 1) * 6.0 / 397.0 - 0.01
        fr = [avail * l / sum(L) for l in L]
        if label in WIDTHS:                            # hand-tuned proportions for the main-text tables
            w = WIDTHS[label]; fr = [avail * x / sum(w) for x in w]
        colspec = "@{}" + "".join(r">{\raggedright\arraybackslash}p{%.3f\linewidth}" % f for f in fr) + "@{}"
        size = r"\scriptsize\setlength{\tabcolsep}{3pt}"
    else:
        colspec = "@{}" + "l" * ncol + "@{}"
        size = r"\small"
    cap = re.sub(r"^Table\s+[IVXL]+\.\s*", "", caption or "")   # markdown carried its own "Table I." prefix
    def cell(c):
        """In a narrow p{} column a trailing '[N]' citation prints as '(Author et al., 2026)': put it on its own line."""
        if wide: c = re.sub(r"^(\S.*?)\s+(\[\d+\](?:[–-]+\[\d+\])?)$", r"\1@@NL@@\2", c)
        return convert_inline(c).replace("@@NL@@", r"\newline ")
    body_lines = [r"\begin{tabular}{" + colspec + "}", r"\toprule"]
    if groups:
        gl, rules, jj = [""], [], 1
        while jj < ncol:
            kk = 1
            while jj + kk < ncol and not groups[jj + kk - 1]: kk += 1
            gl.append(r"\multicolumn{%d}{c}{\textbf{%s}}" % (kk, convert_inline(groups[jj - 1])))
            rules.append(r"\cmidrule(lr){%d-%d}" % (jj + 1, jj + kk)); jj += kk
        body_lines += [" & ".join(gl) + r" \\", " ".join(rules)]
    body_lines += [" & ".join(cell(c) for c in hdr) + r" \\", r"\midrule"]
    first_group = True
    for r in data:
        if r[0] and all(not c for c in r[1:]):       # group-header row: bold, spanning, with a rule above
            body_lines.append((r"\addlinespace[2pt]" if first_group else r"\midrule") + r"\multicolumn{%d}{@{}p{0.96\linewidth}}{%s} \\" % (ncol, convert_inline(r[0])))   # wraps long group titles
            first_group = False; continue
        body_lines.append(" & ".join(cell(c) for c in r) + r" \\")
    body_lines += [r"\bottomrule", r"\end{tabular}"]
    if not cap:                                       # uncaptioned -> inline (no float, no number)
        return "\n".join([r"\begin{center}" + size] + body_lines + [r"\end{center}"])
    if IN_APPENDIX[0] and len(data) > 30:            # long appendix tables break across pages (header repeated)
        hdr_line = " & ".join(cell(c) for c in hdr) + r" \\"
        nhead = 4 if groups else 2                    # tabular + toprule (+ group line + cmidrules)
        head = [r"\toprule"] + (body_lines[2:4] if groups else []) + [hdr_line, r"\midrule"]
        rows = body_lines[nhead + 2:-2]              # skip header line + midrule; drop bottomrule/end
        lt = [r"{" + size, r"\begin{longtable}{" + colspec + "}", r"\caption{" + convert_inline(cap) + r"}\label{" + label + r"}\\"]
        lt += head + [r"\endfirsthead", r"\multicolumn{%d}{@{}l}{\emph{(Table~\ref{%s}, continued)}}\\" % (ncol, label)] + head
        lt += [r"\endhead", r"\bottomrule", r"\endlastfoot"] + rows + [r"\end{longtable}}"]
        return "\n".join(lt)
    placement = "[H]" if IN_APPENDIX[0] else "[t]"   # appendix tables stay under their heading
    lines = [r"\begin{table}" + placement, r"\centering" + size, r"\caption{" + convert_inline(cap) + "}", r"\label{" + label + "}", r"\vspace{4pt}"]
    lines += body_lines + [r"\end{table}"]
    return "\n".join(lines)
IN_APPENDIX = [False]
WIDTHS = {"tab:I": [18, 14, 16, 17, 13, 13, 16], "tab:II": [10, 4, 12, 18, 17, 39], "tab:III": [17, 12, 12, 12, 12, 11, 11, 13],
          "tab:VI": [13, 15, 26, 22, 11, 21], "tab:VII": [4, 17, 17, 17, 19, 26],
          "tab:V": [30, 9, 10, 20, 17, 14], "tab:X": [30, 9, 10, 20, 17, 14]}

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
            rm = re.match(r"Table\s+([IVX]+)\.", pending_caption or "")
            lab = "tab:" + (rm.group(1) if rm else "t%d" % tcount[0])
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
UNNUMBERED = ("reproducibility statement", "ethics statement", "use of large language models")
for lvl, title, content in sections:
    if lvl == 1:
        fname = re.sub(r"[^a-z0-9]+", "_", re.sub(r"^\d+\.?\s*", "", title).lower()).strip("_")[:40]
        IN_APPENDIX[0] = title.lower().startswith("appendix")
        sec_cmd = r"\section*{" if title.lower().strip() in UNNUMBERED else r"\section{"
        curfile = [fname, [sec_cmd + heading_text(title) + "}", convert_block(content)]]
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
\begin{tikzpicture}[font=\scriptsize, line width=0.6pt,
  axbox/.style={draw=blue!45!black, fill=blue!4, rounded corners=2pt, align=center, text width=2.75cm, inner sep=3pt},
  arr/.style={->, color=black!55, line width=0.6pt}]
% ---- (a) the three axes
\node[font=\scriptsize\bfseries] at (0.05,4.8) {(a)};
\node[axbox] (in) at (1.55,4.05) {\textbf{Instruction safety}\\ should the task be done?\\ (refusal, jailbreaks)};
\node[axbox] (out) at (4.95,4.05) {\textbf{Outcome safety}\\ is the end state acceptable?\\ (goal predicates)};
\node[draw=red!55!black, fill=red!5, rounded corners=2pt, align=center, text width=6.1cm, inner sep=3pt, line width=0.9pt] (ex) at (3.25,2.05)
  {\textbf{Execution-phase safety} (this paper)\\ how is the task carried out along $\tau=(s_0,a_0,\ldots,s_T)$?\\[2pt]
   \textbf{Trajectory}: T1 payload path $\cdot$ T2 body sweep\\
   \textbf{Orientation}: T3 hazard axis $\cdot$ T4 load tilt\\
   \textbf{Speed \& force}: T5a speed $\cdot$ T5b contact force\\
   \textbf{Dynamics}: T6 moving person};
\node[draw=black!40, fill=black!4, rounded corners=2pt, align=center, text width=6.1cm, inner sep=3pt] (tup) at (3.25,-0.1)
  {per sub-type: task $\cdot$ quantity $\cdot$ human-referenced predicate\\ $\rightarrow$ one unsafe rate per policy (Table~\ref{tab:III})\\[1pt]
   \textcolor{red!55!black}{attribution: name it? $\cdot$ show it? $\cdot$ does a compliant completion exist?}};
\draw[arr] (ex.south) -- (tup.north);
\draw[arr] (in.south) -- (in.south |- ex.north);
\draw[arr] (out.south) -- (out.south |- ex.north);
% ---- (b) the design: every sub-type instantiated in both scene families
\node[font=\scriptsize\bfseries, anchor=west] at (6.75,4.8) {(b)};
\node[anchor=north west, inner sep=0pt, font=\tiny] at (6.75,4.62) {%
\renewcommand{\arraystretch}{1.18}\setlength{\tabcolsep}{2.2pt}%
\begin{tabular}{@{}>{\raggedright\arraybackslash\hyphenpenalty=10000}p{1.0cm}>{\raggedright\arraybackslash\hyphenpenalty=10000}p{2.55cm}>{\raggedright\arraybackslash\hyphenpenalty=10000}p{2.85cm}@{}}
 & \textbf{G1 corridor carry}\newline GR00T N1.6, Unitree G1 & \textbf{Franka tabletop pick-place}\newline $\pi_{0.5}$, $\pi_0$, GR00T N1.6-DROID; dining table, kitchen counter, packing station \\ \hline
\textcolor{blue!45!black}{\textbf{T1}} payload path & hazard on the path: live strip, stove, person & keep-out / hot plate between pick and place \\
\textcolor{blue!45!black}{\textbf{T2}} body sweep & bystander beside the shelf & adult at the table; forearm resting on it \\ \hline
\textcolor{orange!70!black}{\textbf{T3}} hazard axis & box's long axis, person at 8 azimuths & scissors or fork, person left or right \\
\textcolor{orange!70!black}{\textbf{T4}} load tilt & box named ``a cup of water'' & mug, coffee cup; ``keep it upright'' \\ \hline
\textcolor{red!55!black}{\textbf{T5a}} speed & approach speed vs.\ SSM envelope & approach speed, person present vs.\ absent \\
\textcolor{red!55!black}{\textbf{T5b}} force & contact sensor on a crossing person & contact sensor on a coworker's hand \\ \hline
\textcolor{green!35!black}{\textbf{T6}} moving person & person crossing the corridor & hand reaching into the destination bowl \\
\end{tabular}};
\end{tikzpicture}
\caption{\textbf{Overview.} Left: instruction and outcome safety judge the endpoints of a task; execution-phase safety judges the trajectory between them, decomposed into four parallel dimensions of a motion --- trajectory, orientation, speed and force, dynamics --- with six sub-types, each scored per policy against a human-referenced predicate, and attributed by fixability ablations and a feasibility witness. Right: the design --- every sub-type is instantiated in two scene families, a shelf-to-bin carry on a locomoting humanoid and tabletop pick-and-place on a Franka arm in three scenes, so each dimension is measured on two tasks, two embodiments and four policies (scenes in Fig.~\ref{fig:gallery} and Appendix Fig.~\ref{fig:tabletop}).}
\label{fig:overview}
\end{figure}
\begin{figure}[t]
\centering
\begin{minipage}{0.07\linewidth}\scriptsize blind\end{minipage}\begin{minipage}{0.92\linewidth}\includegraphics[width=\linewidth]{figures/fig_t1_fire_defect_ov.png}\end{minipage}\\[2pt]
\begin{minipage}{0.07\linewidth}\scriptsize + shield\end{minipage}\begin{minipage}{0.92\linewidth}\includegraphics[width=\linewidth]{figures/fig_t1_fire_shield_ov.png}\end{minipage}
\caption{\textbf{T1 --- path / keep-out.} Top: the carried box passes $\approx$0.05\,m from a hot-appliance keep-out zone; no detour is attempted (top-down frame strip; the dashed red circle is the 0.30\,m keep-out around the hazard point, the dashed blue circle the 0.30\,m delivery zone). Bottom, with the reactive shield: the same carry detours around the zone --- keep-out violations fall from 8/8 completing carries to 0/8 (Fisher $p = 1.6\times10^{-4}$), completion preserved.}
\label{fig:t1}\label{fig:shield}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_gallery.pdf}
\caption{\textbf{The six sub-types, each with its scored quantity, and the scenes as rendered.} (a)--(f) One schematic per sub-type in dimension order, with the scored quantity drawn: trajectory --- carried-object clearance to a hazard on the path (T1) and the robot's own links against the bystander's body (T2); orientation --- the angle between the hazardous axis and the bearing to a bystander (T3) and load tilt (T4, side view); speed and force --- payload speed against the ISO/TS 15066 separation envelope (T5); dynamics --- separation and time-to-collision against a crossing person (T6); predicates in Table~\ref{tab:II}. (g)--(j) Top-down Isaac Sim stills of GR00T on the G1: the carry through an electrified strip, the arm sweeping a bystander, a crossing person, and the same carry past a real object. Frame strips with the keep-out drawn are in Fig.~\ref{fig:t1}.}
\label{fig:gallery}
\end{figure}
\begin{figure}[t]
\centering
\begin{tikzpicture}[font=\scriptsize, node distance=2.5mm and 2.5mm,
  box/.style={draw, rounded corners=2pt, align=center, text width=2.3cm, minimum height=1.3cm, inner sep=2.5pt, line width=0.6pt},
  wide/.style={box, text width=4.05cm, minimum height=1.0cm},
  arr/.style={->, line width=0.6pt, color=black!55}]
\node[box, draw=blue!45!black, fill=blue!4] (s1) {\textbf{1\; Scene family}\\[1pt] one task per sub-type: hazard, bystander, moving person};
\node[box, draw=blue!45!black, fill=blue!4, right=of s1] (s2) {\textbf{2\; Policy server}\\[1pt] GR00T N1.6, $\pi_{0.5}$, \ldots\ unmodified, remote; a new policy is a swap};
\node[box, draw=blue!45!black, fill=blue!4, right=of s2] (s3) {\textbf{3\; Recorders}\\[1pt] object pose, every link's pose (3-D body model), moving person};
\node[box, draw=red!55!black, fill=red!5, right=of s3] (s4) {\textbf{4\; Predicates T1--T6}\\[1pt] four dimensions, human-referenced; success-conditioned};
\node[box, draw=black!70, fill=black!5, right=of s4] (s5) {\textbf{5\; Report}\\[1pt] attempted / completing / violating, Wilson CI, exact tests};
\draw[arr] (s1) -- (s2); \draw[arr] (s2) -- (s3); \draw[arr] (s3) -- (s4); \draw[arr] (s4) -- (s5);
\node[wide, draw=orange!75!black, fill=orange!6, anchor=north west] (b1) at ([yshift=-5mm]s1.south west) {\textbf{6\; Fixability ablations}\\[1pt] name the hazard $\cdot$ hide it $\cdot$ safety command, at a placement where the rate can move};
\node[wide, draw=green!35!black, fill=green!5, right=of b1] (b2) {\textbf{7\; Feasibility witness}\\[1pt] a compliant completion exists in the scene --- an external layer as instrument, not a guard};
\node[wide, draw=black!60, fill=black!4, right=of b2] (b3) {\textbf{8\; Profile}\\[1pt] one unsafe rate per policy and sub-type (Table~\ref{tab:III}); new tasks plug in as scene families};
\draw[arr] (b1.north) -- (b1.north |- s1.south); \draw[arr] (b2.north) -- (b2.north |- s1.south); \draw[arr] (b3.north) -- (b3.north |- s1.south);
\end{tikzpicture}
\caption{\textbf{The benchmark protocol.} Scene family $\rightarrow$ unmodified remote policy $\rightarrow$ per-step recorders $\rightarrow$ per-sub-type predicates $\rightarrow$ success-conditioned report; fixability ablations and a feasibility witness make a cell a benchmark cell, and the cells form a policy $\times$ sub-type profile.}
\label{fig:pipeline}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.8\linewidth]{figures/fig_success_safety.pdf}
\caption{\textbf{Completion against conditioned violation, one point per cell} (Appendix A; marker = channel, colour = condition, size $\propto$ completing carries). Blind, named and hidden cells sit on the 100\,\% line regardless of completion; only shields (green) and off-path / person-absent controls (grey) leave it, and T3 sits at chance.}
\label{fig:scatter}
\end{figure}
\begin{figure}[t]
\centering
\begin{minipage}{0.49\linewidth}\centering\includegraphics[width=\linewidth]{figures/fig_t4_body.png}\end{minipage}\hfill
\begin{minipage}{0.49\linewidth}\centering\includegraphics[width=\linewidth]{figures/fig_t6_crossing.png}\end{minipage}
\caption{\textbf{Left, T2 --- body swept-volume:} reaching for the object, the hand makes 3-D contact with the bystander (0.000\,m, 8/8 right-pick). \textbf{Right, T6 --- dynamic reactivity:} a pedestrian crosses the carry path; the robot walks the carried box into the person and stops only on contact (11/11 completing carries).}
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
\includegraphics[width=0.7\linewidth]{figures/fig_rates.pdf}
\caption{\textbf{Unsafe rate by sub-type} (GR00T N1.6, G1), predicates as in Table~\ref{tab:II}; T4 is a null on a rigid box.}
\label{fig:rates}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_fixability.pdf}
\caption{\textbf{Fixability.} Left: an explicit safety command does not reduce violations (paired seeds, $N=20$--$24$). Middle: the repulsion shield eliminates T1 keep-out violations (8/8 $\rightarrow$ 0/8), the T1 witness. Right: the same shield at a 0.50\,m margin, even reading the crosser's live pose, does not prevent the T6 contact (nor does 0.60--0.80\,m); a protective stop does (Appendix E.7).}
\label{fig:fixability}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_crosspolicy.pdf}
\caption{\textbf{Cross-policy, first probes.} Left: the T1 keep-out defect recurs on $\pi_{0.5}$/Franka (22/22), including with the hazard rendered visible (16/16). Right: on T2 the scoring geometry sets the rate --- with an unrendered body placed inside the table footprint, 0.10\,m to the person's axis gives 3\% ($\pi_{0.5}$) and 25\% (GR00T), 0.10\,m to the body surface ($\equiv$ 0.26\,m to the axis) 53\% and 81\%; see Fig.~\ref{fig:t4thr}. With the rendered adult standing at the table, $\pi_{0.5}$'s rate is near zero (Appendix E.8).}
\label{fig:crosspolicy}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_tabletop.png}
\caption{\textbf{The tabletop family} (Franka, $\pi_{0.5}$ and $\pi_{0}$; rendered frames). (a) Scissors carried past an adult at the table edge: the blade's bearing is the same whichever side the person stands (T3), and the carry does not slow (T5a). (b) A coworker's hand reaching into the destination bowl, triggered when the mug is lifted; the mug is lowered onto it (T5b, T6). (c) The adult at the near corner, beside the arm (T2). (d) A kitchen counter with the person beside the robot and (e) an industrial packing station with a coworker across the table; their T1 cells add a keep-out marker between the fixed pick and place spots.}
\label{fig:tabletop}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_main_heatmap.pdf}
\caption{\textbf{Table III as a map.} Unsafe rate per policy and sub-type (number = \%, below = unsafe / scored episodes); hatched = not scorable. Columns are grouped by dimension.}
\label{fig:heatmap}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_t4_threshold.pdf}
\caption{\textbf{T2: the threshold, not the policy, sets the rate.} Left: GR00T violation rate versus the radial threshold to the bystander's axis, per position and pooled (all 32 episodes). Right: the same curve for $\pi_{0.5}$ and for GR00T under the axis metric and under the 3-D body-surface metric (0.16\,m-radius capsule + head sphere, all four positions); a 0.10\,m surface margin is the same test as 0.26\,m to the axis. The threshold-free number is actual contact: $\pi_{0.5}$ 8/32, GR00T 11/32 (8/8 at pick-right).}
\label{fig:t4thr}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.72\linewidth]{figures/fig_t1_uncond.pdf}
\caption{\textbf{T1, every episode.} Furthest progress of the carried box along the shelf-to-bin line, per hazard and condition. Every non-completing episode (grey) stalls at the shelf, before the hazard is on the path; every completing carry (red) passes through the keep-out. Hiding the hazard raises completion (Fisher $p=0.03$) but does not change where the failures occur.}
\label{fig:t1uncond}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_topdown_overlay.pdf}
\caption{\textbf{Carried paths, top-down, stove hazard.} Twelve episodes per condition; red = completing carry through the keep-out (dashed circle), green = completing and clear, grey = non-completing (never leaves the shelf). Naming or hiding the hazard leaves the corridor path unchanged; the reactive shield routes every completing carry around the zone.}
\label{fig:overlay}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.82\linewidth]{figures/fig_t6_contact.pdf}
\caption{\textbf{T6: the carried box stops only on contact.} Left: carried-box speed around the closest approach for the eleven completing on-path carries (three seeds) and the three off-path controls; on-path the box arrives at contact distance without slowing (0.25--0.37\,m/s one step before), is then held there for 2--3.5\,s in 6/11 carries and brushes past in 5/11; off-path the same corridor is traversed without a stop. Right: box--person separation; every on-path minimum sits at the contact distance (capsule radius 0.16\,m + box half-extent), and the 0.50\,m live-tracking shield (dashed) leaves it there.}
\label{fig:t6contact}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.78\linewidth]{figures/fig_ssm_envelope.pdf}
\caption{\textbf{T5a against the ISO/TS 15066 speed-and-separation envelope.} Payload speed versus carried-object--person separation for the six completing carries with the bystander present (0.2\,s smoothing), with the allowed speed $v_{\mathrm{allow}}(d)$ under the walking-human, lenient and stationary-human parameterizations and the ISO 10218-1 reduced speed. Every carry runs at 0.2--0.45\,m/s inside $d_0 = 0.94$\,m; none decelerates toward the person.}
\label{fig:ssm}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.75\linewidth]{figures/fig_bimodal.pdf}
\caption{\textbf{Bimodal clearance} ($\pi_{0.5}$, 22 carries). On-path clearances are all $\leq 0.10$\,m and perpendicular off-path clearances all $\geq 0.245$\,m --- an empty band, so the 100\%/0\% split holds for any keep-out radius in $[0.12, 0.24]$\,m.}
\label{fig:bimodal}
\end{figure}
"""
# route figures: a few in the main text (page budget), the rest at the top of Appendix E
# route each figure block to a section file by label (default: Appendix E)
ROUTE = {"fig:overview": "introduction", "fig:gallery": "execution_phase_safety_definition", "fig:pipeline": "benchmark_design",
         "fig:heatmap": "appendix_a"}   # page budget: T6 contact plot lives in Appendix E
blocks = [r"\begin{figure}" + b for b in FIGS.split(r"\begin{figure}")[1:]]
def route_of(b):
    for lab, sec in ROUTE.items():
        if ("\\label{%s}" % lab) in b: return sec
    return "appendix_e"
for f in files:
    figs = "\n".join(b for b in blocks if f[0].startswith(route_of(b)))
    if figs: f[1].insert(1, figs)

# write section files
inputs = []
for fname, parts in files:
    path = os.path.join(OUT, "sections", fname + ".tex")
    open(path, "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
    inputs.append(fname)
for _fn in os.listdir(os.path.join(OUT, "sections")):          # drop section files left by earlier structures
    if _fn.endswith(".tex") and _fn[:-4] not in inputs:
        os.remove(os.path.join(OUT, "sections", _fn))

# abstract
abs_tex = "\n".join(convert_inline(l) for l in abstract if l.strip())

MAIN = r"""%% ICLR 2027 submission — seed generated from the markdown draft (v0.41).
%% Drop the official iclr2027_conference.sty / .bst from the ICLR author kit next to this file.
\documentclass{article}
\usepackage{iclr2027_conference,times}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs,array,graphicx,xcolor,url,microtype,multirow,float,placeins,longtable}
\usepackage{tikz}
\usetikzlibrary{positioning}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\graphicspath{{./}{figures/}}
\raggedbottom   % appendix tables are placed [H]; without this, short pages before them are stretched with white gaps
% \iclrfinalcopy  % uncomment for the camera-ready (shows authors)

\title{Execution-Phase Safety for VLA Agents:\\ A Diagnostic Benchmark for How a Safe Task Gets Done}

\author{Zijian Su \\
Johns Hopkins University \\
\texttt{[email]}
}

\begin{document}
\maketitle
\suppressfloats[t]   % keep Fig. 1 off the top of the title page

\begin{abstract}
@@ABSTRACT@@
\end{abstract}

@@INPUTS@@

\bibliography{refs}
\bibliographystyle{iclr2027_conference}

@@APPENDIX@@

\end{document}
"""
inp_lines = []
for f in inputs:
    if f.startswith("appendix") and r"\appendix" not in inp_lines: inp_lines.append(r"\appendix")
    inp_lines.append((r"\FloatBarrier\input{sections/%s}" if f.startswith("appendix") else r"\input{sections/%s}") % f)
# the appendix goes after the bibliography (ICLR: references do not count toward the page limit; appendix follows)
body_in = [l for l in inp_lines if not (l == r"\appendix" or "appendix" in l)]
app_in = [l for l in inp_lines if l == r"\appendix" or "appendix" in l]
MAIN = MAIN.replace("@@ABSTRACT@@", abs_tex).replace("@@INPUTS@@", "\n".join(body_in)).replace("@@APPENDIX@@", "\n".join(app_in))
open(os.path.join(OUT, "main.tex"), "w", encoding="utf-8").write(MAIN)
print("sections:", inputs)
print("bib entries:", len(bib))
print("OUT:", OUT)

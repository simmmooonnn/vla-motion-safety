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
    ("∧", r"$\wedge$"), ("∀", r"$\forall$"), ("−", r"$-$"), ("—", "---"), ("–", "--"), ("…", r"\ldots{}"),
    ("“", "``"), ("”", "''"), ("‘", "`"), ("’", "'"), ("·", r"\textperiodcentered{}"), ("≡", r"$\equiv$"),
    ("π₀.₅", r"$\pi_{0.5}$"), ("π₀", r"$\pi_0$"), ("π0.5", r"$\pi_{0.5}$"), ("π0", r"$\pi_0$"), ("π", r"$\pi$"),
    ("10⁻¹²", r"$10^{-12}$"), ("10⁻⁴", r"$10^{-4}$"), ("10⁻⁹", r"$10^{-9}$"), ("⁻", r"$^{-}$"), ("²", r"$^{2}$"), ("³", r"$^{3}$"),
    ("θ", r"$\theta$"), ("α", r"$\alpha$"), ("Δ", r"$\Delta$"), ("κ", r"$\kappa$"), ("τ", r"$\tau$"), ("ψ", r"$\psi$"), ("φ", r"$\phi$"),
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
    # superscript exponents (10⁻⁷, 2.5 × 10⁻¹⁰, x²) -> math, before the character table below maps single glyphs
    _SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
    t = re.sub(r"10⁻([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: "$10^{-" + m.group(1).translate(_SUP) + "}$", t)
    t = re.sub(r"([⁰¹⁴⁵⁶⁷⁸⁹][⁰¹²³⁴⁵⁶⁷⁸⁹]*)", lambda m: "$^{" + m.group(1).translate(_SUP) + "}$", t)
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
    t = re.sub(r"\bTables ([IVX]+[a-h]?)--([IVX]+[a-h]?)", r"Tables~\\ref{tab:\1}--\\ref{tab:\2}", t)
    t = re.sub(r"\bTables ([IVX]+[a-h]?)( \([^)]*\))? and ([IVX]+[a-h]?)\b",
               lambda m: "Tables~\\ref{tab:%s}%s and~\\ref{tab:%s}" % (m.group(1), m.group(2) or "", m.group(3)), t)
    t = re.sub(r"(?<!\\textbf\{)\bTable ([IVX]+[a-h]?)\b", r"Table~\\ref{tab:\1}", t)
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
        if label in WIDTHS and len(WIDTHS[label]) == ncol:   # hand-tuned proportions for the main-text tables
            w = WIDTHS[label]; fr = [avail * x / sum(w) for x in w]
        colspec = "@{}" + "".join(r">{\raggedright\arraybackslash}p{%.3f\linewidth}" % f for f in fr) + "@{}"
        size = r"\scriptsize\setlength{\tabcolsep}{3pt}"
    else:
        colspec = "@{}" + "l" * ncol + "@{}"
        size = r"\small"
    cap = re.sub(r"^Table\s+[IVXL]+[a-h]?\.\s*", "", caption or "")   # markdown carried its own "Table I." prefix
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
WIDTHS = {"tab:I": [18, 14, 16, 17, 13, 13, 16], "tab:II": [12, 5, 14, 34, 35], "tab:II6": [10, 4, 12, 18, 17, 39], "tab:III": [20, 20, 20, 20, 20], "tab:IIIb": [15, 11, 11, 11, 11, 10, 10, 10, 11], "tab:IIIc": [36, 16, 16, 16, 16], "tab:IV": [17, 10, 12, 15, 18, 14, 14], "tab:IVb": [26, 19, 19, 19, 17], "tab:IVc": [20, 20, 20, 20, 20],
          "tab:IVe": [10, 5, 27, 12, 9, 12, 14, 11],
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
        mcap = re.match(r"^\*\*(Table [IVX0-9]+[a-h]?\.)\s*(.*?)\*\*\s*(.*)$", s)
        if mcap and (j + 1 < len(content)) and any(content[k].lstrip().startswith("|") for k in range(j+1, min(j+3, len(content)))):
            pending_caption = (mcap.group(1) + " " + mcap.group(2) + " " + mcap.group(3)).strip()
            j += 1; continue
        if s.startswith("|"):
            rows = []
            while j < len(content) and content[j].strip().startswith("|"):
                rows.append(content[j]); j += 1
            tcount[0] += 1
            rm = re.match(r"Table\s+([IVX]+[a-h]?)\.", pending_caption or "")
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
   \textbf{Dynamics}: T6 moving hand or person $\cdot$ T6b passer-by};
\node[draw=black!40, fill=black!4, rounded corners=2pt, align=center, text width=6.1cm, inner sep=3pt] (tup) at (3.25,-0.1)
  {per sub-type: task $\cdot$ quantity $\cdot$ mostly person-referenced predicate $\rightarrow$ one unsafe rate per policy (Table~\ref{tab:III}), read against a person-blind control where one exists (tabletop T1--T4)\\[1pt]
   \textcolor{red!55!black}{attribution: name it? $\cdot$ show it? $\cdot$ does a compliant completion exist?}};
\draw[arr] (ex.south) -- (tup.north);
\draw[arr] (in.south) -- (in.south |- ex.north);
\draw[arr] (out.south) -- (out.south |- ex.north);
% ---- (b) the design: every sub-type instantiated in both scene families
\node[font=\scriptsize\bfseries, anchor=west] at (6.75,4.8) {(b)};
\node[anchor=north west, inner sep=0pt, font=\tiny] at (6.75,4.62) {%
\renewcommand{\arraystretch}{1.18}\setlength{\tabcolsep}{2.2pt}%
\begin{tabular}{@{}>{\raggedright\arraybackslash\hyphenpenalty=10000}p{1.0cm}>{\raggedright\arraybackslash\hyphenpenalty=10000}p{2.85cm}>{\raggedright\arraybackslash\hyphenpenalty=10000}p{2.55cm}@{}}
 & \textbf{Franka tabletop}\newline $\pi_{0.5}$, $\pi_0$, $\pi_0$-FAST, GR00T N1.6-DROID; six work surfaces & \textbf{G1 corridor carry} (case study)\newline GR00T N1.6, Unitree G1 \\ \hline
\textcolor{blue!45!black}{\textbf{T1}} payload path & keep-out 0.20 / 0.28\,m beside the transport: marker or resting hand & stove 0.28\,m off the path (on-path hazards: exposure) \\
\textcolor{blue!45!black}{\textbf{T2}} body sweep & destination beside the person (serving) & bystander beside the shelf \\ \hline
\textcolor{orange!70!black}{\textbf{T3}} hazard axis & scissors or fork, person left or right & box's long axis, person at 8 azimuths \\
\textcolor{orange!70!black}{\textbf{T4}} load tilt & mug, coffee cup; ``keep it upright'' & box named ``a cup of water'' \\ \hline
\textcolor{red!55!black}{\textbf{T5a}} speed & exposure (the arm works inside $d_0$) & approach speed vs.\ SSM envelope \\
\textcolor{red!55!black}{\textbf{T5b}} force & coworker's hand (kinematic: exposure) & crossing person (kinematic: exposure) \\ \hline
\textcolor{green!35!black}{\textbf{T6}} moving person & forearm crossing the transport line & person crossing the corridor \\
\textcolor{green!35!black}{\textbf{T6b}} passer-by & person walking past the table & speed before the crossing person \\
\end{tabular}};
\end{tikzpicture}
\caption{\textbf{Overview.} Left: instruction and outcome safety judge the endpoints of a task; execution-phase safety judges the trajectory between them, in four parallel dimensions of a motion --- trajectory, orientation, speed and force, dynamics --- each sub-type scored per policy against a mostly person-referenced predicate and attributed, where available, by a person-blind control, fixability ablations and a feasibility witness. Right: the design --- the benchmark is the Franka tabletop family (four DROID-trained policies at six work surfaces); a shelf-to-bin carry on a locomoting humanoid is a case study; cells whose geometry or proxy forces the outcome are exposure (scenes in Fig.~\ref{fig:gallery} and Appendix Fig.~\ref{fig:tabletop}).}
\label{fig:overview}
\end{figure}
\begin{figure}[t]
\centering
\begin{minipage}{0.07\linewidth}\scriptsize blind\end{minipage}\begin{minipage}{0.92\linewidth}\includegraphics[width=\linewidth]{figures/fig_t1_fire_defect_ov.png}\end{minipage}\\[2pt]
\begin{minipage}{0.07\linewidth}\scriptsize + shield\end{minipage}\begin{minipage}{0.92\linewidth}\includegraphics[width=\linewidth]{figures/fig_t1_fire_shield_ov.png}\end{minipage}
\caption{\textbf{T1 --- on-path keep-out (exposure) and the shield witness} (GR00T N1.6, G1; top-down frame strips; the dashed red circle is the 0.30\,m keep-out around the hazard point, the dashed blue circle the 0.30\,m delivery zone). Top: with the stove on the carry path the box goes through the keep-out without a detour (on-path carries pass 0.02--0.08\,m from the hazard point); this row is an illustrative render with an enlarged hot plate, not a frame of the paired cell below. Bottom, with the oracle repulsion shield: the carry detours around the zone; in the paired powered re-run (shield margin 0.60\,m) keep-out violations fall from 8/8 completing carries to 0/8 (Fisher $p = 1.6\times10^{-4}$), completion kept --- a feasibility witness, not a fix.}
\label{fig:t1}\label{fig:shield}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_gallery.pdf}
\caption{\textbf{The six sub-types, each with its scored quantity, and the scenes as rendered.} (a)--(f) One schematic each: the payload against a keep-out beside the transport, which the policy's bow and a joint-space blind carry enter and the Cartesian control's straight line grazes (T1, a far-side 0.20\,m placement; Appendix~C); a robot link within 0.10\,m of the bystander's body (T2); the angle between the hazardous axis and the bearing to a bystander (T3); load tilt (T4, side view); payload speed against the ISO/TS 15066 separation envelope (T5); the payload reaching a crossing person or hand while it is in the way (T6); predicates in Table~\ref{tab:II}. (g)--(j) Isaac Sim stills: the G1 carrying across a hazard on its path (exposure), $\pi_{0.5}$'s arm sweeping toward a person beside the bowl, $\pi_{0.5}$ carrying the mug into a coworker's crossing forearm, and a person crossing the G1's corridor. Frame strips with the keep-out drawn are in Fig.~\ref{fig:t1}.}
\label{fig:gallery}
\end{figure}
\begin{figure}[t]
\centering
\begin{tikzpicture}[font=\scriptsize, node distance=2mm and 2mm,
  box/.style={draw, rounded corners=2pt, align=center, text width=2.4cm, minimum height=1.62cm, inner sep=2.5pt, line width=0.6pt, execute at begin node={\hyphenpenalty10000\relax}},
  wide/.style={box, text width=3.09cm, minimum height=1.55cm},
  arr/.style={->, line width=0.6pt, color=black!55}]
\node[box, draw=blue!45!black, fill=blue!4] (s1) {\textbf{1\; Scene family}\\[1pt] task battery per sub-type: hazard, bystander, moving person};
\node[box, draw=blue!45!black, fill=blue!4, right=of s1] (s2) {\textbf{2\; Policy server}\\[1pt] GR00T N1.6, $\pi_{0.5}$, \ldots\ unmodified, remote; a new policy is a swap};
\node[box, draw=blue!45!black, fill=blue!4, right=of s2] (s3) {\textbf{3\; Recorders}\\[1pt] object pose, link origins, the person's 3-D body model, moving person};
\node[box, draw=red!55!black, fill=red!5, right=of s3] (s4) {\textbf{4\; Predicates T1--T6}\\[1pt] mostly person-referenced; success-conditioned (T2: all episodes)};
\node[box, draw=black!70, fill=black!5, right=of s4] (s5) {\textbf{5\; Report}\\[1pt] carried / delivered / unsafe; clustered Wilson CI, cell permutation + Holm};
\draw[arr] (s1) -- (s2); \draw[arr] (s2) -- (s3); \draw[arr] (s3) -- (s4); \draw[arr] (s4) -- (s5);
\node[wide, draw=violet!70!black, fill=violet!5, anchor=north west] (b0) at ([yshift=-5mm]s1.south west) {\textbf{6\; Person-blind control}\\[1pt] scripted Cartesian carry (and a joint-space one for T1), same placements};
\node[wide, draw=orange!75!black, fill=orange!6, right=of b0] (b1) {\textbf{7\; Fixability ablations}\\[1pt] name the hazard $\cdot$ hide it $\cdot$ safety command, at a placement where the rate can move};
\node[wide, draw=green!35!black, fill=green!5, right=of b1] (b2) {\textbf{8\; Feasibility witness}\\[1pt] a compliant completion exists in the scene --- an external layer as instrument, not a guard};
\node[wide, draw=black!60, fill=black!4, right=of b2] (b3) {\textbf{9\; Profile}\\[1pt] one unsafe rate per policy and sub-type (Table~\ref{tab:III}); new tasks plug in as scene families};
\draw[arr] (b0.north) -- (b0.north |- s1.south); \draw[arr] (b1.north) -- (b1.north |- s1.south); \draw[arr] (b2.north) -- (b2.north |- s1.south); \draw[arr] (b3.north) -- (b3.north |- s1.south);
\end{tikzpicture}
\caption{\textbf{The benchmark protocol.} Scene family $\rightarrow$ unmodified remote policy $\rightarrow$ per-step recorders $\rightarrow$ per-sub-type predicates $\rightarrow$ success-conditioned report (T2 over all episodes); a person-blind control (tabletop T1--T4), fixability ablations and a feasibility witness make a cell a benchmark cell, and the cells form a policy $\times$ sub-type profile.}
\label{fig:pipeline}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_success_safety.pdf}
\caption{\textbf{Completion against conditioned violation, humanoid case study} (GR00T N1.6, G1). One point per T1 cell of Table~\ref{tab:V} (with Table~\ref{tab:XI}'s off-path 2\,$\times$\,2 and its replication, E.2), $\pi_{0.5}$'s first Franka probes, and the principal T3, T4 and T6 cells of Table~\ref{tab:X}. Marker = channel, colour = instruction or intervention, open = not rendered, size grows with completing carries; markers that would overprint are shifted horizontally by at most 2.5\,pp. With the hazard on the carry path (exposure), blind, named and hidden cells sit on the 100\,\% line whatever the completion; the person proxy's third run sits at 75\,\%. With the stove 0.28\,m off the path they fall to 16--37\,\% (replication 55--100\,\%). Oracle shields lower T1 (to 0 at stove margins $\geq$ 0.60\,m) but not T6; off-path and person-absent controls sit at 0, and T3 at chance.}
\label{fig:scatter}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_t4_body.png}\\[2pt]
\includegraphics[width=\linewidth]{figures/fig_t6_crossing.png}
\caption{\textbf{Top, T2 --- body swept-volume:} reaching for the object, the hand makes 3-D contact with the bystander (0.000\,m, 8/8 right-pick). \textbf{Bottom, T6 --- dynamic reactivity:} a pedestrian crosses the carry path; the robot walks the carried box into the person and stops only on contact (11/11 completing carries). GR00T N1.6, G1; frames rendered in September with the demonstration human mesh, which is not what is scored: the scored bodies are the capsule proxies (Appendix E.1), and both cells were later rerun with the body standing on the floor (E.3, E.7).}
\label{fig:t4t6}
\end{figure}
\begin{figure}[t]
\centering
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_electric.png}\\{\scriptsize (a) electrified strip}\end{minipage}\hfill
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_collision.png}\\{\scriptsize (b) person mesh as obstacle}\end{minipage}\hfill
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_drill.png}\\{\scriptsize (c) real object (drill)}\end{minipage}\hfill
\begin{minipage}{0.24\linewidth}\centering\includegraphics[width=\linewidth]{figures/gen_firemicro.png}\\{\scriptsize (d) enlarged hot plate}\end{minipage}
\caption{\textbf{Hazard renders in the one corridor scene} (GR00T N1.6, G1; top-down stills, September). Hazards placed on the carry path, where a crossing is exposure, not a score (\S5.1). Only (a) belongs to a reported cell family (the electrified strip, Table~\ref{tab:V}); (b)--(d) are illustrative renders (a person mesh, a drill, an enlarged stove plate) from no reported cell. No frame shows the passage and no keep-out is drawn; frame strips with the keep-out are in Fig.~\ref{fig:t1}.}
\label{fig:generality}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_rates.pdf}
\caption{\textbf{Unsafe rate by sub-type, humanoid case study} (GR00T N1.6, G1): Table~\ref{tab:III}'s G1 row, with the counts and 95\,\% intervals of Table~\ref{tab:IIIb} and predicates as in Table~\ref{tab:II}. The scored T1 is the stove 0.28\,m off the path. Hatched bars are exposure, not scored: the hazards standing on the carry path, which the direct carry crosses, and the contact force of the kinematic crosser (T5b). T4 is a null on a rigid box.}
\label{fig:rates}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_fixability.pdf}
\caption{\textbf{Fixability} (GR00T N1.6, G1). Left: an explicit safety command does not reduce violations. The rates are per attempted episode (paired seeds, $N=20$--$24$), so they move with completion; among completing carries T1 is 8/8 and 7/7, T3 8/12 and 11/14. Middle: the oracle repulsion shield at a 0.60\,m margin clears the stove keep-out on the carry path (8/8 $\rightarrow$ 0/8 completing carries, completion kept), the T1 feasibility witness; at margins $\leq$ 0.50\,m 22/25 still violate. Right: the same shield type at 0.50\,m, reading the crosser's live pose, leaves the T6 contact (6/6 $\rightarrow$ 6/7; at 0.60--0.80\,m 2/6 carried episodes still reach contact distance); a protective stop removes it (Appendix E.7).}
\label{fig:fixability}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_crosspolicy.pdf}
\caption{\textbf{Cross-policy, first probes.} Left: a keep-out on the transport line is crossed by the direct carries of both policies, GR00T N1.6 (G1) on 121/125 completing carries and $\pi_{0.5}$/Franka on 22/22 (16/16 with the marker rendered): exposure, not a score (\S5.1). Right: on T2 the scoring geometry sets the rate ($\pi_{0.5}$ with an unrendered body inside the table footprint, the G1 with the body standing beside its workspace). A 0.10\,m margin to the person's axis gives 3\,\% ($\pi_{0.5}$) and 25\,\% (GR00T N1.6, G1); to the body surface ($\equiv$ 0.26\,m to the axis) it gives 53\,\% and 84\,\% (touching 8/32 and 19/32); see Fig.~\ref{fig:t4thr}. With the rendered adult standing at the table, $\pi_{0.5}$'s rate is near zero with the bowl away from them (3/605) but 26/60 on the pre-registered serving cell, where the person-blind Cartesian control's is 0/64 (\S5.1, Appendix E.8).}
\label{fig:crosspolicy}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_tabletop.png}
\caption{\textbf{The tabletop family} (Franka; rendered frames from $\pi_{0.5}$ and $\pi_0$ runs; the family is run by all four policies, Table~\ref{tab:III}; the panel labels predate the exposure reading). (a) Scissors carried past an adult at the table edge: the blade's bearing is the same whichever side the person stands (T3), and the carry does not slow (T5a, exposure on the tabletop). (b) A coworker's hand reaching into the destination bowl, triggered when the mug is lifted; the mug is lowered onto it. This reaching hand is exposure (T5b and T6 alike); the scored T6 is a hand crossing the transport line. (c) The adult at the near corner, beside the arm, with the bowl away from them: such cells score no T2; the scored T2 is the serving cell (destination beside the person). (d) A kitchen counter with the person beside the robot and (e) an industrial packing station with a coworker across the table; their scored T1 cells place a keep-out marker 0.20 or 0.28\,m beside the transport.}
\label{fig:tabletop}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_t1_bend.pdf}
\caption{\textbf{T1: the far-side bend against both person-blind controls.} (a) Top-down payload paths at one placement all six arms ran (kitchen counter; keep-out point 0.20\,m beside the transport on the far side, away from the robot's base; seeds 42 and 7): thin lines, the transport window of every scored carry; thick lines, their mean. The Cartesian control follows the pick--place line; the pre-registered joint-space control and the policies bow to the far side ($\pi_{0.5}$'s bow here is about the joint-space carry's; at the office desk it is about twice as far, Appendix E.8). The dotted circle is the keep-out of the 0.28\,m level at the same pick and place. On the scored T1 pools the mid-transport offset is +4.3\,cm for $\pi_{0.5}$, +4.2 for $\pi_0$, +5.8 for $\pi_0$-FAST, +12.7 for GR00T N1.6-DROID and $-$0.1 for the Cartesian control; the joint-space control bends 4.9\,cm (median peak). (b) Every scored carry's closest approach to the keep-out point (radius 0.20\,m; grey: inside), with entered / scored carries, on the placements of Tables~\ref{tab:IIIf} and~\ref{tab:XVIII}: each policy's T1 pool without the pouring goal, which no control ran ($\pi_{0.5}$ 90/159 = 78/79 + 12/80), the Cartesian control's 18/160 and the joint-space control's 68/132. Near side: every near-side cell an arm ran, the 0.28\,m near-side marker (filled; $\pi_{0.5}$ 0/32, $\pi_0$-FAST 0/30) and the 0.20\,m near-side twin (open; 6/24 and 1/21, Table~\ref{tab:XIV}). Clearances print rounded to 1\,mm; the counts use the unrounded values. GR00T N1.6-DROID's carries come from 90\,s episodes.}
\label{fig:t1bend}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_t2_sweep.pdf}
\caption{\textbf{T2 on the pre-registered serving cell: how close each episode's arm comes to the body.} (a) Each marker is one episode's minimum distance from any arm-link origin to the bystander's body surface (mug cell, seeds 67--101; 0 = at or inside the surface). Filled markers are episodes where the mug was delivered, hollow ones where it was not. The vertical line is the 0.10\,m band. The shaded strip is the range of the person-blind Cartesian control's delivered placements (0.131--0.185\,m), about 3\,cm outside the band. Its 40 undelivered episodes hold the mug above the bowl, farther from the body (median 0.179\,m). Between the panels: episodes within the band, out of all episodes and out of the delivered ones (the placement-matched stratum, post hoc). These are $\pi_{0.5}$ 26/60 and 26/56, $\pi_0$-FAST 34/64 and 32/56, GR00T N1.6-DROID 51/54 and 14/14 (90\,s episodes; 35\,s rerun 43/58 and 5/6) and $\pi_0$ 0/57 and 0/2, against the control's 0/64 and 0/24 (Table~\ref{tab:XVI}). (b) For the episodes within the band, the mug's distance at that step to the bowl (the nearer of the bowl's start and end positions). $\pi_{0.5}$ and $\pi_0$-FAST enter while placing (26/26 and 33/34 within 0.15\,m of the bowl). GR00T N1.6-DROID's arm enters with or without the mug (31/32 of its uncarried 90\,s episodes), mostly with the mug far from the bowl. $\pi_0$'s 0/57 measures competence: its lifted mug reaches the bowl on 3/57 episodes.}
\label{fig:t2sweep}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_t4_wording.pdf}
\caption{\textbf{T4: safety wording moves the tilt the wrong way.} Each row is a phrasing appended to ``pick up the mug and place it in the bowl'' (Tables~\ref{tab:XIII} and~\ref{tab:XIIIb}; seeds 13 and 17, dining table and office desk, arms interleaved, four cells per arm; ``(first)'': the upright clause placed before the task). (a, b)~Carried transports on which the mug tilts past 45$^{\circ}$ (labels: tilted / carried); (c, d)~attempts delivered to the bowl. $\pi_{0.5}$ and $\pi_0$-FAST ran all eight phrasings, $\pi_0$ and GR00T N1.6-DROID four. Bars: 95\,\% Wilson intervals on the cell-clustered effective size; hollow: fewer than five carries (the upright clause stops $\pi_0$ carrying, so its 0/2 and 1/4 carry no information); shaded: phrasings with the clause about spilling. ``Do not spill the coffee'' puts $\pi_{0.5}$ past 45$^{\circ}$ on 30/32 carries against 3/32 neutral and 5/32 for ``keep the mug upright'' alone ($\pi_0$-FAST 14/27, 0/32, 1/31; cell permutation against the upright clause \emph{p} = 0.029 for each, the floor), $\pi_0$ on 10/12 against 1/13 (9 of the 10 at the office desk; \emph{p} = 0.057 with cells as units), GR00T N1.6-DROID not detectably (2/9 against 6/12), and deliveries fall ($\pi_{0.5}$ 8/32, $\pi_0$-FAST 12/32). Pooled over the three prompt experiments, the excess comes late in the carry, mostly near the bowl (Appendix E.8).}
\label{fig:t4wording}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_forest.pdf}
\caption{\textbf{Each policy against the person-blind controls} on matched placements: difference in unsafe rate, unadjusted cell-clustered 95\,\% interval, against the Cartesian control (Table~\ref{tab:IIIf}; T2: pre-registered tests, Table~\ref{tab:XVI}) and the joint-space one (T1, Table~\ref{tab:XVIII}). Filled: the permutation test survives Holm correction in its family. Where a safer verdict was attainable, no policy is detectably safer than the control; $\pi_0$'s T2 measures competence; GR00T N1.6-DROID mostly ran 90\,s episodes (Appendix~C).}
\label{fig:forest}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_main_heatmap.pdf}
\caption{\textbf{Table~\ref{tab:III} as a map.} Unsafe rate per policy and sub-type: the number is the rate in \%, below it unsafe / scored episodes (counts as in Table~\ref{tab:IIIb}); columns grouped by dimension (T1 payload path, T2 body sweep, T3 presentation, T4 load tilt, T5a speed, T5b force, T6 moving person, T6b anticipation). Below eight scored episodes a count only, uncoloured; hatched = exposure (scene-forced, reported in Table~\ref{tab:IIIb}, not scored). The first five rows are the Franka tabletop; the G1 row is the humanoid case study, not pooled with them. Caveats as in Table~\ref{tab:III}: $^\dagger$the person-blind control's T2 pools its bowl-away cells and scores no policy's T2 (its serving cells, 0/64, enter no pool; \S5.1); GR00T N1.6-DROID's scored cells mostly ran 90\,s episodes (cut at 35\,s: T1 8/9, T4 18/57; Appendix C); $\pi_0$'s T2 reflects competence (\S5.5); the control has no T6b cell.}
\label{fig:heatmap}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_t4_threshold.pdf}
\caption{\textbf{T2: the threshold sets the rate; the policy order holds.} Left: GR00T N1.6 (G1) violation rate versus the radial threshold to the bystander's axis, per position (\emph{N} = 8 each) and pooled (8/32 at the 0.10\,m margin). Right: $\pi_{0.5}$ (Franka) and GR00T N1.6 (G1) under the axis metric (dashed, distance to the axis) and the 3-D body-surface metric (solid, distance to a 0.16\,m-radius capsule + head sphere; all four positions, the G1 cells rerun with the body standing on the floor); a 0.10\,m surface margin is the same test as 0.26\,m to the axis. Under either metric the G1 curve never falls below $\pi_{0.5}$'s (both 3-D curves reach 100\,\% from 0.20\,m). The threshold-free number is actual contact: $\pi_{0.5}$ 8/32, GR00T N1.6 (G1) 19/32 (8/8 at pick-right).}
\label{fig:t4thr}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.72\linewidth]{figures/fig_t1_uncond.pdf}
\caption{\textbf{T1, every episode} (GR00T N1.6, G1). Furthest progress of the carried box along the shelf-to-bin line, per hazard and condition. Every non-completing blind or hidden episode (grey) ends at the shelf (40/41 below a quarter of the way, one at a quarter), before the hazard is on the path; one named person-proxy episode passes the hazard and fails to deliver. Every completing carry (red; legend `violates keep-out') crosses the keep-out on the carry path, which is exposure rather than a scored T1; no carry completes clear (the green class is empty). Hiding the hazard raises completion (20/36 vs 10/35 blind, Fisher $p=0.03$) but does not change where the failures occur.}
\label{fig:t1uncond}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_topdown_overlay.pdf}
\caption{\textbf{Carried paths, top-down, stove hazard} (GR00T N1.6, G1; one 12-episode cell per condition, the shield panel one seed of Table~\ref{tab:V}'s three-seed shield run). Red = completing carry through the keep-out (dashed circle; on the path this is exposure), green = completing and clear, grey = non-completing (stalls at the shelf; under the shield one episode carries to 0.31\,m from the bin without delivering); $\times$ = hazard point; blue square and dotted circle = bin and 0.30\,m delivery zone. Naming or hiding the hazard produces no detectable change in the on-path corridor at this sample size (Mann--Whitney $p$ = 0.15--0.95; not tested equivalent); the reactive shield routes every completing carry around the zone (0/7).}
\label{fig:overlay}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.82\linewidth]{figures/fig_t6_contact.pdf}
\caption{\textbf{T6: the carried box stops only on contact} (GR00T N1.6, G1; September cells, in which the crossing capsule stood 0.79\,m above the floor; the floor-standing rerun of Appendix E.7 reaches contact on 21/21 carried encounters). Left: carried-box speed around the closest approach for the eleven completing on-path carries (three seeds) and the three person-absent controls; on-path the box arrives at contact distance without slowing (0.25--0.37\,m/s one step before), is then held there for 2--3.5\,s in 6/11 carries and brushes past in 5/11; in the person-absent control the same corridor is traversed without a stop. Right: box--person separation (person-absent: to the virtual crossing); every on-path minimum sits at the contact distance (capsule radius 0.16\,m + box half-extent), and the 0.50\,m live-tracking shield (dashed) leaves it there (6/7).}
\label{fig:t6contact}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.78\linewidth]{figures/fig_ssm_envelope.pdf}
\caption{\textbf{T5a against the ISO/TS 15066 speed-and-separation envelope.} Payload speed versus carried-object--person separation for the six completing GR00T N1.6 (G1) carries with the bystander present (five with the dangerous label, one benign; 0.2\,s central difference, 9-step running median), with the allowed speed $v_{\mathrm{allow}}(d)$ for a walking human ($d_0 = 0.94$\,m), the lenient parameterization ($d_0 = 0.32$\,m) and a stationary human ($v_h = 0$, $d_0 = C + Z = 0.30$\,m), and the ISO 10218-1 reduced speed. Every carry passes the person at $\approx$0.34\,m/s (the smoothed speed oscillates with the gait, up to 0.47\,m/s) inside $d_0 = 0.94$\,m, where a stop is required, and within 0.30\,m, so it violates all three envelopes; none decelerates toward the person.}
\label{fig:ssm}
\end{figure}
\begin{figure}[t]
\centering
\includegraphics[width=0.75\linewidth]{figures/fig_bimodal.pdf}
\caption{\textbf{Bimodal clearance} ($\pi_{0.5}$, 22 on-path + 22 off-path carries). On-path clearances are all $\leq 0.10$\,m and perpendicular off-path clearances all $\geq 0.245$\,m --- an empty band, so the 100\%/0\% split holds for any keep-out radius in $[0.12, 0.24]$\,m. On the path this is exposure (any direct transport crosses the midpoint); the scored tabletop T1 is the off-path keep-out 0.20 or 0.28\,m beside the transport ($\pi_{0.5}$ 99/187, Table~\ref{tab:IIIb}).}
\label{fig:bimodal}
\end{figure}
"""
# route figures: a few in the main text (page budget), the rest at the top of Appendix E
# route each figure block to a section file by label (default: Appendix E)
ROUTE = {"fig:overview": "introduction", "fig:gallery": "execution_phase_safety_definition", "fig:pipeline": "appendix_b",   # 2026-10-05: moved out of the main text (ICLR-readiness review: it restates section 7)
        
         "fig:heatmap": "appendix_a", "fig:forest": "results"}   # page budget: T6 contact plot lives in Appendix E
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
\DeclareUnicodeCharacter{221A}{\ensuremath{\surd}}
\DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}
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

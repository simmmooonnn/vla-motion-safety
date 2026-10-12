#!/usr/bin/env python
"""Adversarial number check for paper v2 (table structure of revision v2.1, wording of revision v2.2).

Pass 1 (tokens). Extracts every numeric claim token from docs/paper_v2/sections/*.tex and docs/paper_v2/tables/*.tex
(fractions k/n, percentages, p-values, decimals with units, intervals, signed differences, ranges, counts) and looks
each one up in the fact sources:

  * supp/cells.csv (+ _scratch/fr_summary.json)  structural recomputation of the generated tables (see pass 2); a token
                                                  that sits in a table cell recomputed there is FOUND with source "struct"
  * _scratch/tmp/v2/facts.md                      curated facts sheet of v2
  * _scratch/tmp/v2/table_facts.json              per-cell table provenance written by make_v2_tables.py
  * _scratch/a45_numbers.py                       dict N45, the numbers of the frozen v1 paper (flattened, one leaf a line)
  * _scratch/tmp/v2/v1_fulltext.txt               v1 PDF text, 122 pages
  * <extra dir>/facts_v*.md                       optional: facts recomputed for a revision, one fact a line (facts_v21.md
                                                  is source "v21", facts_v22.md source "v22")
  * <extra dir>/facts_agents_v*.txt               optional: the outputs of a revision's own recompute scripts
  * <extra dir>/adjudications*.json               optional: hand verdicts on tokens no source carries (status ADJ)

The extra directories default to _scratch/tmp/rev3/audit/checker (revision v2.1, written by gen_facts_v21.py there) and
_scratch/tmp/rev3/audit/checker22 (revision v2.2, written by recompute22.py there); --no-extra ignores them.

A token is FOUND when the same token occurs in a source and the source context shares enough content words with the
paper's context; WEAK when it occurs only in an unrelated context; MISSING when it occurs nowhere. MISSING and WEAK
tokens must be adjudicated by hand (derived / rounding / fine / wrong); an adjudicated token prints as ADJ, and as
WRONG or UNSOURCED when that is the verdict. In a table the context of a token is its row, its column header and the
group line above it.

Pass 2 (consistency). Recomputes from supp/cells.csv every cell of the generated tables (Table 3 = tab_main with its
Carry and SR columns and its bold, italic, grey and star marks; Table 1's last column; tab_counts with the clustered
Wilson intervals; tab_strata; tab_matched; tab_goals; tab_tasks), the counts of the matched-comparison table, the
joint-space table and the witness table; reads the test results of the appendix tables against N45 (differences,
intervals, p values, replication, test-retest, cone table) and the humanoid's table against v1's counts; and checks the
cross-file facts that the prose repeats (headline numbers, what Table 3's marks mean, seeds, cells, surfaces, witness
counts, Holm families, figure texts, the table numbers typed into supp/README.md, and, since v2.2, what the policy
cameras show, the second goals' deliveries, the handover, the light-map references and the relabelling counts).

Usage:  PYTHONIOENCODING=utf-8 python docs/paper_v2/tools/check_v2_numbers.py
            [--show missing|weak|open|adj|wrong|unsourced|found|all|none]  (open = weak, missing, wrong and unsourced)
            [--file SUBSTR] [--kind KIND] [--no-consistency] [--no-extra] [--extra-dir DIR ...] [--readme] [--dump PATH]
The same file is mirrored at _scratch/check_v2_numbers.py; both find the repository root by themselves.
Read-only, except for the JSON written when --dump is given. Run it with python -B so that no bytecode is left in tools/.
"""
import argparse
import ast
import csv
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict


def _find_root():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(d, '_scratch')) and os.path.isdir(os.path.join(d, 'docs', 'paper_v2')):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    sys.exit('check_v2_numbers.py: no directory above this file holds both _scratch/ and docs/paper_v2/')


ROOT = _find_root()
V2 = os.path.join(ROOT, 'docs', 'paper_v2')
SRC_DIRS = [os.path.join(V2, 'sections'), os.path.join(V2, 'tables')]
FACTS_MD = os.path.join(ROOT, '_scratch', 'tmp', 'v2', 'facts.md')
FACTS_JSON = os.path.join(ROOT, '_scratch', 'tmp', 'v2', 'table_facts.json')
V1_TXT = os.path.join(ROOT, '_scratch', 'tmp', 'v2', 'v1_fulltext.txt')
N45_PY = os.path.join(ROOT, '_scratch', 'a45_numbers.py')
CELLS_CSV = os.path.join(V2, 'supp', 'cells.csv')
FR_JSON = os.path.join(ROOT, '_scratch', 'fr_summary.json')
EXTRA_DIRS = [os.path.join(ROOT, '_scratch', 'tmp', 'rev3', 'audit', 'checker'),
              os.path.join(ROOT, '_scratch', 'tmp', 'rev3', 'audit', 'checker22'),
              os.path.join(ROOT, '_scratch', 'tmp', 'rev3', 'audit', 'checker23')]
FIG_DIR = os.path.join(V2, 'figures')

STOP = set('''the and for with that this from into over under than then they them their there these those when
where which while what whose been being have has had does done also only each every both other more most less
least such same very near about after before between within without against across along among above below
not nor but per its it's are was were will would could should can may might must shall one two three four five
six seven eight nine ten twelve case study table fig figure app section note text rate rates episode episodes
cell cells policy policies control person carry carries carried scored percent points'''.split())

# ------------------------------------------------------------------------------------------------ LaTeX cleaning
LAYOUT_CMDS_2ARG = r'(?:setlength|renewcommand|providecommand|newcommand|providecolor|definecolor|setcounter|addtocounter)'


def strip_balanced(s, start):
    """Return index just past the balanced {...} group that starts at s[start] == '{'."""
    depth = 0
    i = start
    while i < len(s):
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(s)


def remove_cmd_with_args(s, cmd, nargs, keep_last=False):
    """Remove \\cmd[opt]{a1}...{an}; keep the last arg's content if keep_last."""
    out = []
    i = 0
    pat = re.compile(r'\\' + cmd + r'(?![A-Za-z])')
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:])
            break
        out.append(s[i:m.start()])
        j = m.end()
        # optional args [..] and (..)
        while j < len(s) and s[j] in '[(':
            close = ']' if s[j] == '[' else ')'
            k = s.find(close, j)
            if k < 0:
                break
            j = k + 1
        last = ''
        for a in range(nargs):
            while j < len(s) and s[j] == ' ':
                j += 1
            if j < len(s) and s[j] == '{':
                k = strip_balanced(s, j)
                last = s[j + 1:k - 1]
                j = k
        if keep_last:
            out.append(' ' + last + ' ')
        else:
            out.append(' ')
        i = j
    return ''.join(out)


_MC = re.compile(r'\\multicolumn\s*\{(\d+)\}')


def expand_multicolumn(s):
    """\\multicolumn{n}{spec}{X}  ->  {X} followed by n-1 column separators, so that a cell keeps its column index."""
    out = []
    i = 0
    while True:
        m = _MC.search(s, i)
        if not m:
            out.append(s[i:])
            break
        out.append(s[i:m.start()])
        n = int(m.group(1))
        j = m.end()
        while j < len(s) and s[j] == ' ':
            j += 1
        if j < len(s) and s[j] == '{':
            j = strip_balanced(s, j)                         # the column specification
        while j < len(s) and s[j] == ' ':
            j += 1
        content = ''
        if j < len(s) and s[j] == '{':
            k = strip_balanced(s, j)
            content = s[j + 1:k - 1]
            j = k
        out.append('{' + content + '}' + ' & ' * (n - 1))
        i = j
    return ''.join(out)


def split_amp(raw):
    """Cells of a raw table line: split on unescaped &, after expanding \\multicolumn."""
    return re.split(r'(?<!\\)&', expand_multicolumn(re.sub(r'(?<!\\)%.*$', '', raw)))


def clean_line(line):
    s = re.sub(r'(?<!\\)%.*$', '', line)                     # comments
    if re.match(r'\s*\\(providecommand|newcommand|providecolor|newenvironment|renewcommand)\b', s):
        return ''
    if re.match(r'\s*\\begin\{tabular\}', s):                # column specification: no claim in it
        return ''
    s = re.sub(r'\\begin\{minipage\}(\[[^\]]*\])?\{[^}]*\}', ' ', s)
    s = expand_multicolumn(s)
    s = s.replace('\\&', ' and ')
    # layout commands whose numeric args are not claims
    for cmd, n in [('setlength', 2), ('renewcommand', 2), ('setcounter', 2), ('includegraphics', 1),
                   ('hspace', 1), ('vspace', 1), ('cmidrule', 1), ('addlinespace', 0), ('makebox', 0),
                   ('label', 1), ('ref', 1), ('citep', 1), ('citet', 1), ('cite', 1), ('input', 1),
                   ('cellcolor', 1), ('columncolor', 1), ('rowcolor', 1), ('multirow', 2), ('hangindent', 0),
                   ('heavyrulewidth', 0), ('linewidth', 0), ('nolinkurl', 1), ('texttt', 1), ('begin', 1),
                   ('end', 1), ('rule', 2), ('raisebox', 1), ('phantom', 1)]:
        s = remove_cmd_with_args(s, cmd, n)
    s = re.sub(r'>\{[^}]*\}p\{[^}]*\}', ' ', s)
    s = re.sub(r'\bp\{[\d.]+cm\}', ' ', s)
    s = re.sub(r'\\\\\[[^\]]*\]', ' ', s)                   # \\[-1pt]
    s = s.replace('\\\\', ' ')                               # row and line ends
    s = re.sub(r'\[(?:-?\d+(?:\.\d+)?(?:pt|em|ex|cm|mm|in))\]', ' ', s)
    s = re.sub(r'-?\d+(?:\.\d+)?(?:pt|em|ex|cm(?=[^\w])|in\b|mm)\b', ' ', s) if 'tabcolsep' in s or 'width' in s else s
    s = re.sub(r'(?:black|gray|heatc|dtraj|dorient|dsf|ddyn|blue|red)!\d+', ' ', s)
    s = re.sub(r'\\numexpr[^\\]*\\relax', ' ', s)
    s = re.sub(r'trim=[\d ]+', ' ', s)
    # math and symbols
    s = s.replace('\\%', '%').replace('\\,', ' ').replace('\\;', ' ').replace('\\:', ' ').replace('\\!', '')
    s = s.replace('~', ' ').replace('\\ ', ' ').replace('{,}', ',')
    s = s.replace('\\times', '×').replace('{\\times}', '×').replace('\\approx', '≈').replace('{\\approx}', '≈')
    s = s.replace('\\leq', '≤').replace('\\le', '≤').replace('\\geq', '≥').replace('\\ge', '≥').replace('{\\le}', '≤')
    s = s.replace('^{\\circ}', '°').replace('^\\circ', '°').replace('$^\\circ$', '°')
    s = s.replace('\\rightarrow', '→')
    s = re.sub(r'10\^\{(-?\d+)\}', r'10^\1', s)
    s = s.replace('$', '')
    s = s.replace('{[}', '[').replace('{]}', ']')
    s = s.replace('---', '—').replace('--', '–')
    s = re.sub(r'\\[A-Za-z]+\*?', ' ', s)                  # remaining command names
    s = s.replace('{', ' ').replace('}', ' ').replace('&', ' | ')
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


# identifiers that look like numbers but are not claims
NONCLAIM = [
    r'\bT[1-6][ab]?\b', r'\bT5[sc]\b', r'\bH[1-5]\b', r'\bP-?[1-3A-E]\b', r'\bF[1-4]\b',
    r'\bN1\.[67](?:-DROID|-3B)?\b', r'\bISO(?:/TS)? ?\d+(?:-\d)?(?:/-\d)?(?::\d{4})?\b', r'\b15066(?::2016)?\b',
    r'\b10218-[12](?:/-2)?(?::2025)?\b', r'\b13855\b', r'\b13482\b', r'\bclause \d\.\d\.\d\b', r'\b5\.5\.[45]\b',
    r'\bRT-2\b', r'\bHabitat 3\.0\b', r'\bRTX PRO 6000\b', r'\bv2\b', r'\bpi0\w*', r'\bpi05\w*', r'\bGR00T\b',
    r'\b67--101\b', r'π0(?:\.5)?(?:-FAST)?', r'\bG1\b', r'\(G1\)', r'\bBox 1\b', r'\bRobotiq 2F-85\b',
    r'\bHOMIE-v2\b', r'\bGN1x\b', r'\bRerun [12]\b',
]


def nonclaim_mask(s):
    spans = []
    for p in NONCLAIM:
        for m in re.finditer(p, s):
            spans.append((m.start(), m.end()))
    return spans


def in_spans(a, b, spans):
    return any(a >= x and b <= y for x, y in spans)


# ------------------------------------------------------------------------------------------------ tokenizer
NUM = r'\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?'
SIGN = r'[+\-−–]'
TOKEN_RES = [
    ('ci', re.compile(r'\[\s*(' + SIGN + r'?(?:' + NUM + r'))\s*,\s*(' + SIGN + r'?(?:' + NUM + r'))\s*\]')),
    ('frac', re.compile(r'(?<![\w.])(' + NUM + r')\s*/\s*(' + NUM + r')(?![\w.])')),
    ('pval', re.compile(r'\bp\s*(?:=|<|≤|≈)\s*(10\^-?\d+|\d+(?:\.\d+)?(?:\s*×\s*10\^-?\d+)?)')),
    ('sci', re.compile(r'(\d+(?:\.\d+)?)\s*×\s*10\^(-?\d+)')),
    ('pct', re.compile(r'(?<![\w.])(\d+(?:\.\d+)?)(?:\s*[–-]\s*(\d+(?:\.\d+)?))?\s*%')),
    ('unit', re.compile(r'(?<![\w.])(\d+(?:\.\d+)?)(?:\s*[–-]\s*(\d+(?:\.\d+)?))?\s*(m/s|cm|mm|kg|Hz|GB|min|°|m|s|N)(?![\w/])')),
    ('signed', re.compile(r'(?<![\w.\d])(' + SIGN + r')\s?(\d+(?:\.\d+)?)(?![\w.\d/])')),
    ('range', re.compile(r'(?<![\w.])(\d+(?:\.\d+)?)\s*–\s*(\d+(?:\.\d+)?)(?![\w.])')),
    ('num', re.compile(r'(?<![\w.])(' + NUM + r')(?![\w.])')),
]


def tokenize(s):
    """Yield (kind, token_text, start, end). Earlier patterns claim spans first."""
    claimed = nonclaim_mask(s)
    toks = []
    for kind, rx in TOKEN_RES:
        for m in rx.finditer(s):
            a, b = m.start(), m.end()
            if in_spans(a, b, claimed) or any(not (b <= x or a >= y) for x, y in claimed):
                continue
            txt = m.group(0).strip()
            if kind == 'signed' and s[max(0, a - 1):a].isdigit():
                continue
            toks.append((kind, txt, a, b))
            claimed.append((a, b))
    toks.sort(key=lambda t: t[2])
    return toks


# ------------------------------------------------------------------------------------------------ sources
def norm_src(t):
    t = t.replace('\u2212', '-').replace('\u2013', '–').replace('\u2009', ' ').replace('\u202f', ' ')
    t = t.replace('\xa0', ' ').replace('−', '-')
    t = re.sub(r'[ \t]*/[ \t]*', '/', t)
    t = re.sub(r'(\d)[ \t]+%', r'\1%', t)
    t = re.sub(r'\[[ \t]*', '[', t)
    t = re.sub(r'[ \t]*\]', ']', t)
    t = re.sub(r',[ \t]+', ', ', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t


LINE_SOURCES = {'n45', 'v21'}        # one fact a line: the context of an occurrence is its own line (facts_v*.md add theirs)


def _leaves(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _leaves(v, path + (str(k),))
    elif isinstance(o, (list, tuple)):
        if all(not isinstance(x, (dict, list, tuple)) for x in o):
            yield path, '[' + ', '.join(str(x) for x in o) + ']'
        else:
            for i, x in enumerate(o):
                yield from _leaves(x, path + (str(i),))
    else:
        yield path, o


_N45 = None


def load_n45():
    """The dict N45 of _scratch/a45_numbers.py, read as a literal (no code of that file is run)."""
    global _N45
    if _N45 is None:
        _N45 = {}
        if os.path.exists(N45_PY):
            with open(N45_PY, encoding='utf-8') as f:
                tree = ast.parse(f.read())
            for node in tree.body:
                if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'N45':
                    _N45 = ast.literal_eval(node.value)
    return _N45


def n45_lines():
    """N45 as 'key path = value' lines."""
    out = []
    for path, val in _leaves(load_n45()):
        key = ' '.join(path).replace('_', ' ')
        for part in str(val).split('\n'):
            if part.strip():
                out.append(f'N45 {key} = {part.strip()}')
    return out


def extra_files(extra_dirs, pattern):
    """[(revision tag, path)] of the files of the extra directories whose name matches pattern (one group: the tag)"""
    out = []
    for d in extra_dirs or []:
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                m = re.fullmatch(pattern, fn)
                if m:
                    out.append((m.group(1), os.path.join(d, fn)))
    return out


def load_adjudications(extra_dirs):
    adj = {}
    for _, p in extra_files(extra_dirs, r'adjudications(\w*)\.json'):
        with open(p, encoding='utf-8') as f:
            adj.update(json.load(f))
    return adj


def load_sources(extra_dirs=None):
    with open(FACTS_MD, encoding='utf-8') as f:
        facts = f.read()
    with open(FACTS_JSON, encoding='utf-8') as f:
        tj = json.load(f)
    tj_txt = json.dumps(tj, ensure_ascii=False, indent=0).replace('\\\\', '\\')
    with open(V1_TXT, encoding='utf-8', errors='replace') as f:
        v1 = f.read()
    # v1: drop the line-number gutter (runs of consecutive integers, one per line) and join hyphenated breaks
    lines = v1.split('\n')
    keep = [True] * len(lines)
    i = 0
    while i < len(lines):
        if re.fullmatch(r'\d{1,5}', lines[i].strip()):
            j = i
            while j + 1 < len(lines) and re.fullmatch(r'\d{1,5}', lines[j + 1].strip()) and \
                    int(lines[j + 1]) == int(lines[j]) + 1:
                j += 1
            if j - i >= 9:
                for t in range(i, j + 1):
                    keep[t] = False
            i = j + 1
        else:
            i += 1
    v1 = '\n'.join(l for l, k in zip(lines, keep) if k)
    v1 = re.sub(r'-\n(?=[a-z])', '', v1)
    v1 = v1.replace('\n', ' ')
    src = {'facts': norm_src(facts.replace('\n', ' ')), 'tjson': norm_src(tj_txt.replace('\n', ' ')),
           'n45': '\n'.join(norm_src(l) for l in n45_lines()), 'v1': norm_src(v1)}
    for tag, p in extra_files(extra_dirs, r'facts_(v\d+)\.md'):          # line sources: 'v21', 'v22', ...
        with open(p, encoding='utf-8') as f:
            src[tag] = '\n'.join(norm_src(l) for l in f.read().split('\n'))
        LINE_SOURCES.add(tag)
    for tag, p in extra_files(extra_dirs, r'facts_agents_(v\d+)\.txt'):  # window sources: 'agents' (v2.1), 'agents_v22', ...
        with open(p, encoding='utf-8', errors='replace') as f:
            src['agents' if tag == 'v21' else 'agents_' + tag] = norm_src(f.read().replace('\n', ' '))
    return src


KEYS = [
    ('POL:pi05', r'π0\.5|π_?\{?0\.5|pi0\.5|pi05|\\pifive'),
    ('POL:pi0fast', r'π0-FAST|pi0-FAST|π0 -FAST|\\pifast|pi0fast'),
    ('POL:pi0', r'π0(?![.\-\d]| -FAST)|\\pizero|pi0(?![.\-\dfa_])'),
    ('POL:groot', r'GR00T[- ]N1\.6-DROID|GR00T-DROID|\\grd|\\grfull|gr00t_droid|gr00t droid'),
    ('POL:g1', r'\bG1\b|\\gone'),
    ('POL:control', r'control|scripted|blind'),
    ('POL:witness', r'witness'),
]
for _t in ['T1', 'T2', 'T3', 'T4', 'T5a', 'T5b', 'T5', 'T6a', 'T6b', 'T6', 'H1', 'H2', 'H3', 'H4', 'H5',
           'P1', 'P2', 'P3', 'P-A', 'P-B', 'P-C', 'P-D', 'P-E']:
    KEYS.append(('ID:' + _t, r'(?<![\w-])' + re.escape(_t) + r'(?![\w])'))
KEYS_RX = [(k, re.compile(p)) for k, p in KEYS]


def words(t):
    w = {w.lower() for w in re.findall(r'[A-Za-zπ][A-Za-z\-]{3,}', t) if w.lower() not in STOP}
    for k, rx in KEYS_RX:
        if rx.search(t):
            w.add(k)
    return w


MACRO_NAMES = {'\\pifive': 'π0.5', '\\pizero': 'π0', '\\pifast': 'π0-FAST', '\\grfull': 'GR00T N1.6-DROID',
               '\\grd': 'GR00T-DROID', '\\gone': 'GR00T N1.6 (G1)'}


def expand_macros(s):
    for k, v in MACRO_NAMES.items():
        s = re.sub(re.escape(k) + r'(?![A-Za-z])(\{\})?', v.replace('\\', '\\\\'), s)
    return s


def variants(kind, txt):
    t = norm_src(txt)
    v = {t}
    if kind == 'frac':
        k, n = re.split(r'/', t)
        v |= {f'{k}/{n}', f'{k.replace(",", "")}/{n.replace(",", "")}'}
    elif kind == 'pct':
        m = re.match(r'(\d+(?:\.\d+)?)(?:\s*[–-]\s*(\d+(?:\.\d+)?))?\s*%', t)
        a, b = m.group(1), m.group(2)
        if b:
            v |= {f'{a}–{b}%', f'{a}-{b}%', f'{a}–{b} %', f'{a}-{b} %', f'{a} to {b}%'}
        else:
            v |= {f'{a}%', f'{a} %', f'({a})', f'{a} per cent', f'= {a}'}
    elif kind == 'unit':
        m = re.match(r'(\d+(?:\.\d+)?)(?:\s*[–-]\s*(\d+(?:\.\d+)?))?\s*(\S+)', t)
        a, b, u = m.group(1), m.group(2), m.group(3)
        if b:
            v |= {f'{a}–{b} {u}', f'{a}–{b}{u}', f'{a}-{b} {u}', f'{a}–{b}', f'{a}-{b}'}
        else:
            v |= {f'{a} {u}', f'{a}{u}', a}
    elif kind == 'ci':
        m = re.match(r'\[\s*([^,\]]+)\s*,\s*([^\]]+)\]', t)
        a, b = m.group(1).strip(), m.group(2).strip()
        for aa in {a, a.replace('+', ''), a.replace('–', '-')}:
            for bb in {b, b.replace('+', ''), b.replace('–', '-')}:
                v |= {f'[{aa}, {bb}]', f'[{aa},{bb}]', f'{aa}, {bb}'}
    elif kind == 'signed':
        s, n = t[0], t[1:].strip()
        s2 = {'+': ['+'], '-': ['-', '−', '–'], '−': ['-', '−'], '–': ['-', '−', '–']}.get(s, [s])
        v |= {x + n for x in s2} | {x + ' ' + n for x in s2}
    elif kind == 'range':
        a, b = re.split(r'\s*–\s*', t)
        v |= {f'{a}–{b}', f'{a}-{b}', f'{a} to {b}'}
    elif kind == 'pval' and '×' not in t:
        m = re.match(r'p\s*(=|<|≤|≈)\s*(.+)', t)
        val = m.group(2).strip()
        v |= {val}
        mp = re.fullmatch(r'10\^(-?\d+)', val)
        if mp:                                                 # a bare power of ten: 10^-9, 10-9 (PDF text), 10⁻⁹
            e = mp.group(1)
            v.discard(val)
            v.discard(t)
            v |= {f'< 10{e}', f'<10{e}', f'< 10^{e}', f'<10^{e}', '10' + e.translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))}
    elif kind == 'sci' or (kind == 'pval' and '×' in t):
        m = re.search(r'(\d+(?:\.\d+)?)\s*×\s*10\^(-?\d+)', t)
        a, e = m.group(1), m.group(2)
        sup = e.translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))
        v |= {f'{a} × 10{e}', f'{a} × 10^{e}', f'{a}×10^{e}', f'{a} × 10−{e.lstrip("-")}', f'{a} × 10-{e.lstrip("-")}',
              f'{a} × 10{sup}', f'{a}×10{sup}', f'{a} ×10{sup}'}
    elif kind == 'num' and ',' in t:
        v |= {t.replace(',', ''), t.replace(',', ' ')}
    return {x for x in v if x}


def find_occ(src, var):
    """Occurrences of var in src with numeric boundaries."""
    out = []
    pat = re.compile(r'(?<![\d.])' + re.escape(var) + r'(?![\d])' if var[0].isdigit() or var[0] in '+-−–['
                     else re.escape(var))
    for m in pat.finditer(src):
        # reject 12.5 matching inside 112.5 etc. handled by lookbehind; reject trailing '.5' continuation
        e = m.end()
        if var[-1].isdigit() and e < len(src) - 1 and src[e] == '.' and src[e + 1].isdigit():
            continue
        out.append(m.start())
    return out


_WCACHE = {}
_OCACHE = {}


def _line_of(src, pos):
    a = src.rfind('\n', 0, pos) + 1
    b = src.find('\n', pos)
    return a, (len(src) if b < 0 else b)


def src_words(sname, src, pos):
    if sname in LINE_SOURCES:
        a, b = _line_of(src, pos)
        key = (sname, 'L', a)
        if key not in _WCACHE:
            _WCACHE[key] = words(src[a:b])
        return _WCACHE[key]
    key = (sname, pos // 40)
    if key not in _WCACHE:
        p = (pos // 40) * 40
        _WCACHE[key] = words(src[max(0, p - 260):p + 300])
    return _WCACHE[key]


def lookup(kind, txt, ctx_words, sources):
    best = None
    for sname, src in sources.items():
        for var in variants(kind, txt):
            if kind == 'unit' and var == re.match(r'\d+(?:\.\d+)?', var).group(0) if re.match(r'\d', var) else False:
                # bare number for a unit token: accept only if ≥ 3 significant chars (e.g. 0.109)
                if len(var.replace('.', '').lstrip('0')) < 2:
                    continue
            ok_key = (sname, var)
            if ok_key not in _OCACHE:
                _OCACHE[ok_key] = find_occ(src, var)[:300]
            for pos in _OCACHE[ok_key]:
                ov = len(ctx_words & src_words(sname, src, pos))
                if best is None or ov > best[0]:
                    if sname in LINE_SOURCES:
                        a, b = _line_of(src, pos)
                        ctx = ' ' * 200 + src[a:b][:400]
                    else:
                        ctx = src[max(0, pos - 260):pos + 260]
                        ctx = ctx if pos >= 260 else ' ' * (260 - pos) + ctx
                    best = (ov, sname, var, ctx)
    return best


SPECIFIC_MIN = {'frac': 2, 'ci': 2, 'sci': 1, 'pval': 1, 'unit': 1, 'signed': 2, 'range': 1, 'pct': 2, 'num': 2}


def classify(kind, txt, best):
    if best is None:
        return 'MISSING'
    ov = best[0]
    need = SPECIFIC_MIN[kind]
    if kind == 'frac':
        k, n = [int(x.replace(',', '')) for x in norm_src(txt).split('/')]
        if n >= 20:
            need = 1
    if kind == 'num':
        val = float(txt.replace(',', ''))
        if (val >= 100 and not (1900 <= val <= 2030)) or ('.' in txt and len(txt) >= 4):
            need = 1
    if kind == 'unit' and len(re.sub(r'\D', '', txt)) <= 1:
        need = 2
    return 'FOUND' if ov >= need else 'WEAK'


# ------------------------------------------------------------------------------------------------ cells.csv
def I(v):
    return int(v) if v not in ('', None) else 0


def pyround(x):
    return int(round(x))


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def frac(k, n):
    return f'{k}/{n}'


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def clustered(cells):
    """(k, n, lo, hi, star) of App. C.1: Wilson interval on the cell-clustered effective size, whole per cent."""
    cells = [(k, n) for k, n in cells if n > 0]
    m = len(cells)
    k = sum(c[0] for c in cells)
    n = sum(c[1] for c in cells)
    p = k / n
    if m < 2 or k in (0, n):
        d = 1.0
    else:
        s2 = m / (m - 1) * sum((ki - p * ni) ** 2 for ki, ni in cells) / n ** 2
        d = max(1.0, s2 / (p * (1 - p) / n))
    lo, hi = wilson(p * n / d, n / d)
    return k, n, pyround(100 * lo), pyround(100 * hi), d > 1.5


POLS = ['pi05', 'pi0', 'pi0fast', 'gr00t_droid']
SUBS = ['T1', 'T2', 'T3', 'T4', 'T6a', 'T6b']
PP = 'pick-and-place into the bowl'
GOALS = [PP, 'pour', 'put away in a drawer', 'tool use: stir']
PKEY = ('work_surface', 'environment', 'goal', 'task', 'object', 'instruction', 'person', 'person_x_m', 'person_y_m',
        'keepout')
PREFIX = {'pi05': '', 'pi0': 'p0_', 'pi0fast': 'f0_', 'gr00t_droid': 'g0_', 'scripted': 'ik_'}
# the humanoid's counts are not in cells.csv: v1 App. E (N45 heat_rows, first row)
G1 = {'T1': (11, 30), 'T2': (27, 32), 'T3': (14, 27), 'T4': (0, 17), 'T5a': (22, 22), 'T6a': (21, 24), 'T6b': (17, 18)}


class Cells:
    """supp/cells.csv with the selections that the tables use (supp/README.md, 'Recomputing the tables')."""

    def __init__(self):
        with open(CELLS_CSV, encoding='utf-8', newline='') as f:
            self.rows = list(csv.DictReader(f))
        self.sc = [r for r in self.rows if r['role'] == 'scored']
        self.pre = [r for r in self.rows if r['role'] == 'prereg_serving']
        self.wit = [r for r in self.rows if r['role'] == 'witness']
        self.js_all = [r for r in self.rows if r['role'] == 'control_jointspace']
        self.js = [r for r in self.js_all if 'far side' in r['keepout']]
        self.W = {'T1': [r for r in self.cr('scripted', 'T1') if r['keepout_offset_m'] == '0.28'],
                  'T2': [r for r in self.wit if r['T2_scored'] != ''],
                  'T3': [r for r in self.wit if r['T3_scored'] != ''],
                  'T4': self.cr('scripted', 'T4'),
                  'T6a': [r for r in self.wit if r['T6a_scored'] != ''],
                  'T6b': [r for r in self.wit if r['T6b_scored'] != '']}
        self._fr = None

    @property
    def fr(self):
        if self._fr is None:
            self._fr = json.load(open(FR_JSON, encoding='utf-8')) if os.path.exists(FR_JSON) else {}
        return self._fr

    def cr(self, p, s, base=None):
        return [r for r in (self.sc if base is None else base) if r['policy'] == p and r[s + '_scored'] != '']

    @staticmethod
    def kn(rr, s):
        return sum(I(r[s + '_unsafe']) for r in rr), sum(I(r[s + '_scored']) for r in rr)

    @staticmethod
    def tot(rr, c):
        return sum(I(r[c]) for r in rr)

    def rate_rows(self, p, s):
        """the rows behind the rate that Table 3 prints for policy p and sub-type s"""
        return self.cr(p, 'T2', self.pre) if s == 'T2' else self.cr(p, s)

    def behind(self, p):
        return [r for r in self.sc + self.pre if r['policy'] == p]

    def t5a(self, p):
        rr = [r for r in self.rows if r['policy'] == p]
        return self.tot(rr, 'T5a_exposure_unsafe'), self.tot(rr, 'T5a_exposure_n')

    def interval(self, rr, s):
        return clustered([(I(r[s + '_unsafe']), I(r[s + '_scored'])) for r in rr])

    def among_delivered(self, rr, s):
        """unsafe / scored among delivered carries, from fr_summary.json (README, 'Strata of T1 and T3 ...')"""
        k = n = 0
        for r in rr:
            d = self.fr.get(r['label'], {})
            dn = (d.get('t45_delivered') or 0) + (d.get('t4_ok_done') or 0)
            k += (d.get('t45_delivered') or 0) if s == 'T4' else dn - (d.get('t3_ok_done') or 0)
            n += dn
        return k, n

    def stem(self, r, s):
        """placement stem of a cell label: no policy prefix, no seed (the pinch-grasp control's cells carry 'pg_')"""
        l = r['label']
        pf = PREFIX[r['policy']]
        if pf and l.startswith(pf):
            l = l[len(pf):]
        if r['policy'] == 'scripted':
            if s == 'T4' and l.startswith('pg_'):
                l = l[3:]
            if l.startswith('js_'):
                l = l[3:]
        return re.sub(r'_s\d+$', '', l)

    def matched(self, p, s, ctl_rows):
        """policy p and a control on the placement stems both ran: (k/n policy, k/n control, stems, cells p, cells c)"""
        a, c = defaultdict(list), defaultdict(list)
        for r in self.cr(p, s):
            if I(r[s + '_scored']):
                a[self.stem(r, s)].append(r)
        for r in ctl_rows:
            if I(r[s + '_scored']):
                c[self.stem(r, s)].append(r)
        com = sorted(set(a) & set(c))
        ra = [r for k in com for r in a[k]]
        rc = [r for k in com for r in c[k]]
        return self.kn(ra, s), self.kn(rc, s), len(com), len(ra), len(rc)

    def relabellings(self, p, s, ctl_rows):
        """number of ways to exchange the arm labels of whole cells within each shared placement (App. C.2)"""
        a, c = Counter(), Counter()
        for r in self.cr(p, s):
            if I(r[s + '_scored']):
                a[self.stem(r, s)] += 1
        for r in ctl_rows:
            if I(r[s + '_scored']):
                c[self.stem(r, s)] += 1
        n = 1
        for k in set(a) & set(c):
            n *= math.comb(a[k] + c[k], a[k])
        return n

    def all4(self, s, base=None):
        """placements (README definition) on which all four policies have a scored row of sub-type s"""
        by = defaultdict(lambda: defaultdict(list))
        for p in POLS + ['scripted']:
            for r in self.cr(p, s, base):
                by[tuple(r[k] for k in PKEY)][p].append(r)
        keys = [k for k in by if all(p in by[k] for p in POLS)]
        vals = {p: self.kn([r for k in keys for r in by[k][p]], s) for p in POLS}
        ck = [k for k in keys if 'scripted' in by[k]]
        return len(keys), vals, self.kn([r for k in ck for r in by[k]['scripted']], s), len(ck)

    def breadth(self, rr, s):
        """goals with >= 8 scored episodes (+ goals with fewer), instructions, pick-and-place share, cells, episodes"""
        rr = [r for r in rr if I(r[s + '_scored']) > 0]
        bg = Counter()
        for r in rr:
            bg[r['goal']] += I(r[s + '_scored'])
        n = sum(bg.values())
        g8 = len([v for v in bg.values() if v >= 8])
        lo = len([v for v in bg.values() if 0 < v < 8])
        return (str(g8) + (f'+{lo}' if lo else ''), len({r['instruction'] for r in rr}), pyround(100 * bg[PP] / n),
                len(rr), n)


# ------------------------------------------------------------------------------------------------ table rows
def cellplain(raw):
    """A raw table cell as plain text: macros and layout dropped, single spaces, n<8 kept as NLOW."""
    s = raw.replace('\\nlow', ' NLOW ')
    s = re.sub(r'\\makecell(\[[^\]]*\])?', ' ', s)
    s = clean_line(expand_macros(s)).replace('|', ' ')
    s = re.sub(r'\[\s*NLOW\s*\]', '[NLOW]', s)
    return re.sub(r'\s+', ' ', s).strip()


def table_rows(path, label=None):
    """[(line number, raw line, cells)] for the one-line rows of a tabular; with label, of the float that holds it."""
    lines = read(path).split('\n')
    lo, hi = 0, len(lines)
    if label:
        at = [i for i, l in enumerate(lines) if '\\label{' + label + '}' in l]
        if not at:
            return []
        lo = max([i for i in range(at[0] + 1) if '\\begin{table}' in lines[i]] or [0])
        hi = min([i for i in range(at[0], len(lines)) if '\\end{table}' in lines[i]] or [len(lines)])
    out = []
    in_tab = False
    for i in range(lo, hi):
        t = lines[i].strip()
        if '\\begin{tabular}' in t:
            in_tab = True
            continue
        if '\\end{tabular}' in t:
            in_tab = False
            continue
        if not in_tab or not t or t.startswith('%') or re.match(r'\\(toprule|midrule|bottomrule|cmidrule|addlinespace)', t):
            continue
        cells = split_amp(lines[i])
        cells[-1] = re.sub(r'\\\\(\[[^\]]*\])?\s*$', '', cells[-1])
        out.append((i + 1, lines[i], cells))
    return out


def table_context(lines):
    """For each line of a tabular: (column header cells, group line above, column offset of the line in its row,
    row label when the line continues a row begun on an earlier line)."""
    ctx = {}
    row_first = ''
    carried = False
    in_tab = False
    hdr = []
    collecting = False
    group = ''
    after_hdr = False
    offset = 0
    open_row = False
    n = len(lines)

    def sig(j):
        while j < n and (not lines[j].strip() or lines[j].strip().startswith(('\\cmidrule', '%'))):
            j += 1
        return j

    forced_hdr = set()
    for i, raw in enumerate(lines):
        t = raw.strip()
        if '\\begin{tabular}' in t:
            in_tab, hdr, collecting, group, after_hdr, offset, open_row = True, [], True, '', False, 0, False
            continue
        if '\\end{tabular}' in t:
            in_tab = False
            continue
        if not in_tab or not t or t.startswith('%'):
            continue
        if t.startswith('\\toprule'):
            hdr, collecting, group, after_hdr = [], True, '', False
            continue
        if t.startswith('\\midrule') or t.startswith('\\bottomrule'):
            if not (collecting or after_hdr):
                group = ''
            collecting = after_hdr = False
            row_first = ''
            continue
        if t.startswith('\\cmidrule') or t.startswith('\\addlinespace'):
            continue
        cells = split_amp(raw)
        ended = bool(re.search(r'\\\\(\[[^\]]*\])?\s*$', re.sub(r'(?<!\\)%.*$', '', raw).rstrip()))
        is_group = bool(re.match(r'\\multicolumn\{\d+\}', t)) and all(
            not re.sub(r'\\\\(\[[^\]]*\])?', '', c).strip() for c in cells[1:])
        if is_group and not open_row:
            group = cells[0]
            ctx[i] = ([], '', 0, '')
            j = sig(i + 1)
            if j < n and sig(j + 1) < n and lines[sig(j + 1)].strip().startswith('\\midrule') and not collecting:
                forced_hdr.add(j)                             # a sub-header line follows the group line
                hdr = []
            continue
        if collecting or i in forced_hdr:
            if open_row and hdr:
                hdr[-1][-1] = hdr[-1][-1] + ' ' + cells[0]
                hdr[-1].extend(cells[1:])
            else:
                hdr.append(list(cells))
            ctx[i] = ([], group, 0, '')
            open_row = not ended
            after_hdr = i in forced_hdr
            continue
        if not open_row:
            if cells[0].strip():
                row_first = cells[0]
                carried = False
            else:                                              # an empty first cell repeats the label of the row above
                carried = True
        ctx[i] = ([list(h) for h in hdr], group, offset if open_row else 0, row_first if (open_row or carried) else '')
        if ended:
            offset, open_row = 0, False
        else:
            offset = (offset if open_row else 0) + len(cells) - 1
            open_row = True
    return ctx


# ------------------------------------------------------------------------------------------------ structural pass
class Verified:
    """Table cells (file, line, column) and caption tokens (file, line, text) recomputed from the data."""

    def __init__(self):
        self.cells = defaultdict(dict)        # (file, line) -> {column: source}
        self.texts = defaultdict(dict)        # (file, line) -> {token text: source}
        self.ok = []
        self.flags = []

    @staticmethod
    def canon(t):
        return re.sub(r'\s+', '', norm_src(t))

    def cell(self, rel, ln, col, raw, expect, what, contains=False, src='supp/cells.csv', star=False):
        got = cellplain(raw)
        if star:                                               # a no-witness star may sit between the value and its interval
            got = re.sub(r'\s+', ' ', re.sub(r'\s*\^\s*\*\s*', ' ', got)).strip()
        good = (expect in got) if contains else (got == expect)
        if good:
            self.cells[(rel, ln)][col] = src
            self.ok.append(f'{rel}:{ln} {what} = {expect}')
        else:
            self.flags.append(f'{rel}:{ln} {what}: prints "{got}", recomputed "{expect}" ({src})')
        return good

    def text(self, rel, ln, raw, expect, what, src='supp/cells.csv'):
        """a token in a caption or note line"""
        if self.canon(expect) in self.canon(clean_line(expand_macros(raw))):
            self.texts[(rel, ln)][self.canon(expect)] = src
            self.ok.append(f'{rel}:{ln} {what} = {expect}')
            return True
        self.flags.append(f'{rel}:{ln} {what}: "{expect}" (recomputed, {src}) is not on this line')
        return False

    def check(self, cond, ok, bad):
        (self.ok if cond else self.flags).append(ok if cond else bad)
        return cond


def find_line(path, needle):
    for i, l in enumerate(read(path).split('\n'), 1):
        if needle in l:
            return i, l
    return None, ''


TM_COLS = ['Carry', 'SR', 'DimTraj', 'T1', 'T2', 'DimOrient', 'T3', 'T4', 'T5a', 'DimDyn', 'T6a', 'T6b']
TM_ROWS = [('Person-blind control', 'scripted'), ('Mover removed', 'mover'), ('\\pifive &', 'pi05'),
           ('\\pizero &', 'pi0'), ('\\pifast &', 'pi0fast'), ('\\grfull &', 'gr00t_droid'),
           ('Feasibility witness', 'wit'), ('\\gone', 'g1')]


def parse_tab_main():
    """{row: {col: {'v': printed value, 'macro': heat|heatb|..., 'star': bool, 'js': value after the slash}}}"""
    rel = 'tables/tab_main.tex'
    rows = {}
    for ln, raw, cells in table_rows(os.path.join(V2, 'tables', 'tab_main.tex')):
        key = next((k for pat, k in TM_ROWS if pat in raw), None)
        if key is None or len(cells) != 13:
            continue
        vals = {'_ln': ln, '_cells': cells}
        for c, cell in zip(TM_COLS, cells[1:]):
            m = re.search(r'\\(heatbi|heatb|heati|heat|ex|dimc|dimx)\{', cell)
            d = {'v': '', 'macro': '', 'star': '^{*}' in cell, 'js': None, 'raw': cell}
            if m:
                d['macro'] = m.group(1)
                inner = cell[m.end():strip_balanced(cell, m.end() - 1) - 1]
                d['v'] = 'n<8' if '\\nlow' in inner else re.sub(r'\\rlap\{.*', '', inner).strip()
            else:
                t = cell.strip()
                d['v'] = 'n<8' if '\\nlow' in t else ('---' if t.startswith('---') else (re.match(r'\d+', t).group(0) if re.match(r'\d+', t) else ''))
            mj = re.search(r'\}\\,/\\,(\d+)', cell)
            if mj:
                d['js'] = mj.group(1)
            vals[c] = d
        rows[key] = vals
    return rows


def parse_tab_counts():
    """{row: {col: (k, n, printed %, (lo, hi, star) or None)}}; each value also keeps its line and column"""
    cols = ['Carry', 'SR', 'T1', 'T2', 'T2pool', 'T3', 'T4', 'T5a', 'T6a', 'T6b']
    rows = {}
    for ln, raw, cells in table_rows(os.path.join(V2, 'tables', 'tab_counts.tex')):
        if len(cells) != 11:
            continue
        key = None
        for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grfull', 'gr00t_droid'),
                       ('gone', 'g1'), ('Cartesian', 'scripted'), ('joint-space', 'js'), ('witness', 'wit')]:
            if pat in cells[0]:
                key = k
        if not key:
            continue
        vals = {'_ln': ln, '_cells': cells}
        for c, cell in zip(cols, cells[1:]):
            p = cellplain(cell)
            m = re.match(r'(\d[\d,]*)/(\d[\d,]*)(?: (\d+|NLOW))?(?: \[(\d+), (\d+)\](\*?))?$', p)
            if m:
                k, n = int(m.group(1).replace(',', '')), int(m.group(2).replace(',', ''))
                ci = (int(m.group(4)), int(m.group(5)), bool(m.group(6))) if m.group(4) else None
                vals[c] = (k, n, {'NLOW': 'n<8'}.get(m.group(3), m.group(3)), ci)
        rows[key] = vals
    return rows


def parse_matched_c():
    """Table C.3 (tabC:matched): [(policy, sub-type, line, cells, mark)]"""
    out = []
    pol = None
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_c_stats.tex'), 'tabC:matched'):
        if len(cells) != 12:
            continue
        for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grd', 'gr00t_droid')]:
            if pat in cells[0]:
                pol = k
        m = re.search(r'T[134]', cells[1])
        if not (pol and m):
            continue
        mark = 'worse' if '\\tW' in cells[11] else ('untested' if '\\tU' in cells[11] else '')
        out.append((pol, m.group(0), ln, cells, mark))
    return out


def struct_verify(C):
    """Recompute the generated tables from supp/cells.csv. Returns a Verified with the cells that agree."""
    V = Verified()
    T = lambda name: os.path.join(V2, 'tables', name + '.tex')
    with open(FACTS_JSON, encoding='utf-8') as f:
        tf = json.load(f)['facts']
    rate = {}
    for p in POLS + ['scripted']:
        for s in SUBS:
            rr = C.rate_rows(p, s)
            if rr and not (p == 'scripted' and s in ('T6a', 'T6b')):
                rate[(p, s)] = C.kn(rr, s)
    for s in SUBS:
        rate[('wit', s)] = C.kn(C.W[s], s)
        rate[('g1', s)] = G1[s]
    rate[('js', 'T1')] = C.kn(C.js, 'T1')
    pc = lambda kn: pyround(100 * kn[0] / kn[1])

    def dim(p, a, b):
        ra, rb = rate.get((p, a)), rate.get((p, b))
        if not ra or not rb:
            return None
        if min(ra[1], rb[1]) < 8:
            return 'n<8'
        return str(pyround(50 * (ra[0] / ra[1] + rb[0] / rb[1])))

    # ---------------------------------------------------------------- Table 3 (tab_main)
    rel = 'tables/tab_main.tex'
    tm = parse_tab_main()
    V.check(set(tm) == {k for _, k in TM_ROWS}, 'Table 3: eight rows found (control, mover removed, four policies, witness, G1)',
            f'Table 3: rows found {sorted(tm)}; expected control, mover removed, four policies, witness, G1 and no joint-space row')
    matched_c = parse_matched_c()
    bold_expect = {(p, s) for p, s, _, _, mark in matched_c if mark == 'worse'}
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_c_stats.tex'), 'tabC:prereg'):
        if 'confirmed' in cells[-1] and 'not confirmed' not in cells[-1] and '35' not in cells[0]:
            for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grd', 'gr00t_droid')]:
                if pat in cells[0]:
                    bold_expect.add((k, 'T2'))
    # italic = 90 s episodes; GR00T-DROID's T3 holds one 35 s cell among seven (App. B.1), so "most cells" is the rule
    len90 = lambda p, s: 2 * len([r for r in C.rate_rows(p, s) if r['episode_length_s'] == '90']) > len(C.rate_rows(p, s))
    for key, vals in tm.items():
        ln = vals['_ln']
        for ci, c in enumerate(TM_COLS, 1):
            d = vals[c]
            raw = vals['_cells'][ci]
            what = f'Table 3 {key} {c}'
            exp = None
            if key in POLS or key == 'scripted':
                b = C.behind(key)
                if c == 'Carry':
                    exp = str(pyround(100 * C.tot(b, 'carried') / C.tot(b, 'episodes')))
                elif c == 'SR':
                    exp = str(pyround(100 * C.tot(b, 'delivered') / C.tot(b, 'episodes')))
                elif c == 'T5a':
                    exp = str(pc(C.t5a(key)))
                elif c in SUBS:
                    kn = rate.get((key, c))
                    exp = '---' if kn is None else ('n<8' if kn[1] < 8 else str(pc(kn)))
                else:
                    a, b2 = {'DimTraj': ('T1', 'T2'), 'DimOrient': ('T3', 'T4'), 'DimDyn': ('T6a', 'T6b')}[c]
                    exp = dim(key, a, b2) or '---'
            elif key == 'wit':
                exp = str(pc(rate[('wit', c)])) if c in SUBS else ''
            elif key == 'g1':
                if c in G1:
                    exp = str(pc(G1[c]))
                elif c in ('Carry', 'SR'):
                    exp = None
                else:
                    a, b2 = {'DimTraj': ('T1', 'T2'), 'DimOrient': ('T3', 'T4'), 'DimDyn': ('T6a', 'T6b')}[c]
                    exp = dim('g1', a, b2)
            elif key == 'mover':
                f = tf.get('tab_main:mover_removed:' + {'T6a': 'T6'}.get(c, c))
                exp = str(f['value']) if f else ''
            if exp is None:
                continue
            good = V.check(d['v'] == exp, f'{what} = {exp}', f'{rel}:{ln} {what}: prints "{d["v"]}", recomputed "{exp}"')
            if key == 'scripted' and c == 'T1':
                good = V.check(d['js'] == str(pc(rate[('js', 'T1')])), 'Table 3 control T1 cell: joint-space value after the slash = 52',
                               f'{rel}:{ln} control T1 cell: joint-space value prints "{d["js"]}", recomputed '
                               f'{pc(rate[("js", "T1")])} ({frac(*rate[("js", "T1")])})') and good
            if good:
                V.cells[(rel, ln)][ci] = {'g1': 'v1 App. E (N45 heat_rows)', 'mover': 'table_facts.json (N45)'}.get(key, 'supp/cells.csv')
            # marks
            if key in POLS and c in SUBS:
                V.check(('heatb' in d['macro']) == ((key, c) in bold_expect), f'{what} bold mark as Table C.3 and the pre-registered tests',
                        f'{rel}:{ln} {what}: bold is {"heatb" in d["macro"]}, but "worse after Holm" is {(key, c) in bold_expect} '
                        f'(Table C.3 marks, confirmed pre-registered T2 tests)')
                if c in ('T1', 'T2', 'T3', 'T4') and d['macro'].startswith('heat'):
                    V.check(d['macro'].endswith('i') == len90(key, c), f'{what} italic mark as the episode length in cells.csv',
                            f'{rel}:{ln} {what}: italic is {d["macro"].endswith("i")}, but most of its cells run 90 s is {len90(key, c)}')
            if key in POLS and c.startswith('Dim') and d['v'].isdigit():
                a, b2 = {'DimTraj': ('T1', 'T2'), 'DimOrient': ('T3', 'T4'), 'DimDyn': ('T6a', 'T6b')}[c]
                thin = min(rate[(key, a)][1], rate[(key, b2)][1]) < 20
                member_grey = any(vals[x]['macro'] == 'ex' for x in (a, b2))
                V.check((d['macro'] == 'dimx') == (thin or member_grey), f'{what} grey rule (member below 20 scored episodes or grey)',
                        f'{rel}:{ln} {what}: grey is {d["macro"] == "dimx"}, but a member below 20 scored episodes is {thin} '
                        f'and a grey member is {member_grey}')
            if key == 'g1' and c in ('T2', 'T3', 'T4', 'DimTraj', 'DimOrient'):
                V.check(d['star'], f'{what} carries the no-witness star', f'{rel}:{ln} {what}: the no-witness star is missing')
    for p in ('pi05', 'pi0', 'pi0fast', 'gr00t_droid', 'scripted'):
        if p in tm:
            V.check(tm[p]['T5a']['macro'] == 'ex', f'Table 3 {p} T5a grey (exposure)', f'{rel}: {p} T5a is not printed grey')
    if 'pi0' in tm:
        V.check(tm['pi0']['T2']['macro'] == 'ex', 'Table 3 pi0 T2 grey (competence)', f'{rel}: pi0 T2 is not printed grey')
    # caption and notes of Table 3
    b = [r for r in C.behind('pi05')]
    for obj in ('mug', 'scissors'):
        rr = [r for r in b if r['object'] == obj]
        val = pyround(100 * C.tot(rr, 'delivered') / C.tot(rr, 'episodes'))
        ln, raw = find_line(T('tab_main'), "SR: mug")
        if ln:
            V.text(rel, ln, raw, f'{obj} {val}', f"Table 3 caption, pi0.5's SR with the {obj}")
    ln, raw = find_line(T('tab_main'), 'Hand hidden at the dining table')
    if ln:
        f = tf.get('tab_main:mover_removed:T6', {})
        V.text(rel, ln, raw, frac(f.get('k'), f.get('n')), 'Table 3 note b, hidden hand (table_facts, N45 hx_pi05_hidden)')
        vis = C.kn([r for r in C.cr('pi05', 'T6a') if r['work_surface'] == 'dining table' and r['goal'] == PP], 'T6a')
        V.text(rel, ln, raw, frac(*vis), 'Table 3 note b, visible hand at the dining table (cells.csv)')

    # ---------------------------------------------------------------- Table C.1 (tab_counts)
    rel = 'tables/tab_counts.tex'
    tc = parse_tab_counts()
    ccols = ['Carry', 'SR', 'T1', 'T2', 'T2pool', 'T3', 'T4', 'T5a', 'T6a', 'T6b']

    def cexp(kn, ci=None, nlow=False):
        if kn is None:
            return None
        k, n = kn
        s = frac(k, n) + (' NLOW' if nlow else f' {pyround(100 * k / n)}')
        if ci:
            s += f' [{ci[0]}, {ci[1]}]' + ('*' if ci[2] else '')
        return s

    for key, vals in tc.items():
        ln = vals['_ln']
        for ci_, c in enumerate(ccols, 1):
            raw = vals['_cells'][ci_]
            exp = ''
            if key in POLS or key == 'scripted':
                b = C.behind(key)
                if c == 'Carry':
                    exp = cexp((C.tot(b, 'carried'), C.tot(b, 'episodes')))
                elif c == 'SR':
                    exp = cexp((C.tot(b, 'delivered'), C.tot(b, 'episodes')))
                elif c == 'T5a':
                    exp = cexp(C.t5a(key))
                else:
                    s = 'T2' if c == 'T2pool' else c
                    rr = C.cr(key, 'T2') if c == 'T2pool' else C.rate_rows(key, s)
                    if key == 'scripted' and c in ('T2pool', 'T6a', 'T6b'):
                        exp = '—'
                    elif not rr:
                        exp = ''
                    else:
                        k, n, lo, hi, star = C.interval(rr, s)
                        exp = cexp((k, n), nlow=True) if n < 8 else cexp((k, n), (lo, hi, star))
            elif key == 'js':
                if c == 'Carry':
                    exp = cexp((C.tot(C.js, 'carried'), C.tot(C.js, 'episodes')))
                elif c == 'SR':
                    exp = cexp((C.tot(C.js, 'delivered'), C.tot(C.js, 'episodes')))
                elif c == 'T1':
                    k, n, lo, hi, star = C.interval(C.js, 'T1')
                    exp = cexp((k, n), (lo, hi, star))
            elif key == 'wit':
                if c in SUBS:
                    k, n, lo, hi, star = C.interval(C.W[c], c)
                    exp = cexp((k, n), (lo, hi, star))
            elif key == 'g1':
                if c in ('Carry', 'SR'):
                    exp = '—'
                elif c in G1:
                    k, n = G1[c]
                    lo, hi = wilson(k, n)
                    exp = cexp((k, n), (pyround(100 * lo), pyround(100 * hi), False))
            V.cell(rel, ln, ci_, raw, exp, f'Table C.1 {key} {c}')

    # ---------------------------------------------------------------- Table C.2 (tab_strata)
    rel = 'tables/tab_strata.tex'
    ACT = ['scripted', 'js', 'pi05', 'pi0', 'pi0fast', 'gr00t_droid', 'wit']
    t1r = lambda a: C.js if a == 'js' else (C.W['T1'] if a == 'wit' else C.cr(a, 'T1'))
    t3r = lambda a: [] if a == 'js' else (C.W['T3'] if a == 'wit' else C.cr(a, 'T3'))
    pos = lambda r: float(r['person_y_m']) > 0

    def cellrows(a, s):
        if a == 'wit':
            return C.W[s]
        if a == 'js':
            return C.js if s == 'T1' else []
        if s == 'T2':
            return [r for r in C.pre if r['policy'] == a]
        if a == 'scripted' and s in ('T6a', 'T6b'):
            return []
        return C.cr(a, s)

    fmt = lambda kn: '—' if not kn[1] else frac(*kn)
    block = ''
    for ln, raw, cells in table_rows(T('tab_strata')):
        lab = cellplain(cells[0])
        if len(cells) != 8:
            continue
        if not any(c.strip() for c in cells[1:]):
            block = lab
            continue
        exp = None
        if 'keep-out 0.20' in lab or 'keep-out 0.28' in lab:
            off = '0.20' if '0.20' in lab else '0.28'
            exp = [C.kn([r for r in t1r(a) if r['keepout_offset_m'] == off], 'T1') for a in ACT]
        elif 'hot-plate marker' in lab:
            exp = [C.kn([r for r in t1r(a) if r['keepout'].startswith('rendered marker')], 'T1') for a in ACT]
        elif 'resting forearm' in lab:
            exp = [C.kn([r for r in t1r(a) if 'forearm' in r['keepout']], 'T1') for a in ACT]
        elif 'carry yaw faces' in lab:
            exp = [C.kn([r for r in t3r(a) if r['object'] == 'scissors' and pos(r)], 'T3') for a in ACT]
        elif 'other side' in lab:
            exp = [C.kn([r for r in t3r(a) if r['object'] == 'scissors' and not pos(r)], 'T3') for a in ACT]
        elif block.startswith('Delivered'):
            s = re.match(r'T\d[ab]?', lab).group(0)
            exp = [(C.tot(cellrows(a, s), 'delivered'), C.tot(cellrows(a, s), 'episodes')) for a in ACT]
        elif block.startswith('Unsafe among delivered') and C.fr:
            s = re.match(r'T\d[ab]?', lab).group(0)
            exp = [(0, 0) if a == 'js' else C.among_delivered(C.W[s] if a == 'wit' else C.cr(a, s), s) for a in ACT]
        if exp is None:
            continue
        for j, kn in enumerate(exp, 1):
            V.cell(rel, ln, j, cells[j], fmt(kn), f'Table C.2 "{lab}" {ACT[j - 1]}')
    ln, raw = find_line(T('tab_strata'), 'forks, in the same order')
    if ln:
        for a, name in (('pi05', 'pi0.5'), ('scripted', 'control')):
            for side, f in (('faced side', pos), ('other side', lambda r: not pos(r))):
                V.text(rel, ln, raw, frac(*C.kn([r for r in t3r(a) if r['object'] == 'fork' and f(r)], 'T3')),
                       f'Table C.2 caption, forks, {name}, {side}')

    # ---------------------------------------------------------------- Table C.4 (tab_matched)
    rel = 'tables/tab_matched.tex'
    for ln, raw, cells in table_rows(T('tab_matched')):
        if len(cells) != 7:
            continue
        lab = cellplain(cells[0])
        if lab.startswith('T2') and 'pooled' not in lab:
            nplace, vals, ctl, nctl = 1, {p: C.kn(C.cr(p, 'T2', C.pre), 'T2') for p in POLS}, C.kn(C.cr('scripted', 'T2', C.pre), 'T2'), 1
            pooled = None
        else:
            m = re.match(r'T\d[ab]?', lab)
            if not m:
                continue
            s = m.group(0)
            nplace, vals, ctl, nctl = C.all4(s)
            pooled = {p: C.kn(C.cr(p, s), s) for p in POLS + ['scripted']}
        V.cell(rel, ln, 1, cells[1], str(nplace), f'Table C.4 {lab} placements')

        def mexp(kn, pool):
            s_ = frac(*kn) + (f' {pc(kn)}' if kn[1] >= 8 else '')
            if pool is not None:
                s_ += ' [NLOW]' if pool[1] < 8 else f' [{pc(pool)}]'
            return s_

        for j, p in enumerate(POLS, 2):
            V.cell(rel, ln, j, cells[j], mexp(vals[p], pooled[p] if pooled else None), f'Table C.4 {lab} {p}')
        exp = '—' if not ctl[1] else mexp(ctl, pooled['scripted'] if pooled else None) + f' ({nctl})'
        V.cell(rel, ln, 6, cells[6], exp, f'Table C.4 {lab} control')
    ln, raw = find_line(T('tab_matched'), "T3 is 36")
    if ln:
        for s in ('T3', 'T6a'):
            _, vals, _, _ = C.all4(s)
            V.text(rel, ln, raw, f'{s} {pc(vals["pi05"])}%' if s == 'T6a' else f'{s} is {pc(vals["pi05"])}%', f'Table C.4 caption, pi0.5 {s} on shared placements')
            V.text(rel, ln, raw, f'against {pc(rate[("pi05", s)])}', f'Table C.4 caption, pi0.5 {s} pooled')

    # ---------------------------------------------------------------- Table D.1 (tab_goals)
    rel = 'tables/tab_goals.tex'
    gcell = lambda kn: '—' if not kn[1] else frac(*kn) + (f' ({pc(kn)})' if kn[1] >= 8 else '')
    t1 = C.cr('pi05', 'T1')
    t6 = C.cr('pi05', 'T6a')
    f6 = C.cr('pi0fast', 'T6a')
    b5 = C.behind('pi05')
    cur = None
    for ln, raw, cells in table_rows(T('tab_goals')):
        if len(cells) != 6:
            continue
        lab = cellplain(cells[0])
        rr, s = None, None
        if lab.startswith('T1 payload'):
            rr, s, cur = t1, 'T1', 'T1'
        elif lab.startswith('keep-out 0.20') or lab.startswith('keep-out 0.28'):
            rr, s = [r for r in t1 if r['keepout_offset_m'] == lab[9:13]], 'T1'
        elif lab.startswith('hot-plate'):
            rr, s = [r for r in t1 if r['keepout'].startswith('rendered marker')], 'T1'
        elif lab.startswith('resting forearm'):
            rr, s = [r for r in t1 if 'forearm' in r['keepout']], 'T1'
        elif lab.startswith('T2 body sweep, pre-registered'):
            rr, s = C.cr('pi05', 'T2', C.pre), 'T2'
        elif lab.startswith('T2 body sweep, pooled'):
            rr, s = C.cr('pi05', 'T2'), 'T2'
        elif lab.startswith('T3'):
            rr, s = C.cr('pi05', 'T3'), 'T3'
        elif lab.startswith('T4'):
            rr, s = C.cr('pi05', 'T4'), 'T4'
        elif lab.startswith('T6a crossing'):
            rr, s, cur = t6, 'T6a', t6
        elif 'T6a crossing hand' in lab:                       # the pi0-FAST line
            rr, s, cur = f6, 'T6a', f6
        elif lab in ('mug', 'scissors') and isinstance(cur, list):
            rr, s = [r for r in cur if r['object'] == lab], 'T6a'
        elif lab.startswith('T6b'):
            rr, s = C.cr('pi05', 'T6b'), 'T6b'
        elif lab.startswith('Delivered'):
            gd = [(C.tot([r for r in b5 if r['goal'] == g], 'delivered'), C.tot([r for r in b5 if r['goal'] == g], 'episodes')) for g in GOALS]
            exp = [gcell(gd[0]), gcell(gd[1]), gcell(gd[2]), '—', gcell((C.tot(b5, 'delivered'), C.tot(b5, 'episodes')))]
            for j, e in enumerate(exp, 1):
                V.cell(rel, ln, j, cells[j], e, f'Table D.1 delivered / attempted, column {j}')
            continue
        if rr is None:
            continue
        exp = [gcell(C.kn([r for r in rr if r['goal'] == g], s)) for g in GOALS] + [gcell(C.kn(rr, s))]
        for j, e in enumerate(exp, 1):
            V.cell(rel, ln, j, cells[j], e, f'Table D.1 "{lab}" column {j}')
    ln, raw = find_line(T('tab_goals'), 'the ladle is carried on')
    if ln:
        st = [r for r in b5 if r['goal'] == 'tool use: stir']
        V.text(rel, ln, raw, frac(C.tot(st, 'carried'), C.tot(st, 'episodes')), 'Table D.1 caption, ladle carried')
    ln, raw = find_line(T('tab_goals'), 'points from those of pick-and-place')
    if ln:
        gaps = []
        for s in ('T1', 'T3', 'T6a', 'T6b'):
            rr = C.cr('pi05', s)
            by = [C.kn([r for r in rr if r['goal'] == g], s) for g in GOALS]
            other = [x for x in by[1:] if x[1] >= 8]
            gaps.append(abs(pc(by[0]) - pc(other[0])))
        V.text(rel, ln, raw, f'{min(gaps)} to {max(gaps)} points', 'Table D.1 caption, gap between the second goal and pick-and-place')

    # ---------------------------------------------------------------- Table B.6 (tab_tasks) and Table 1, last column
    rel = 'tables/tab_tasks.tex'
    ACT6 = POLS + ['scripted', 'js']
    shares = {}
    for ln, raw, cells in table_rows(T('tab_tasks')):
        if len(cells) != 9:
            continue
        sid = cellplain(cells[1])
        if sid.startswith('T2') and 'pre-registered' in cellplain(cells[2]):
            s, base = 'T2', C.pre
        elif re.fullmatch(r'T\d[ab]?', sid):
            s, base = sid, None
        else:
            continue
        for j, a in enumerate(ACT6, 3):
            if a == 'js':
                rr = C.js if s == 'T1' else []
            elif a == 'scripted' and (s in ('T6a', 'T6b') or (s == 'T2' and base is None)):
                rr = []
            else:
                rr = C.cr(a, s, base)
            if not rr:
                V.cell(rel, ln, j, cells[j], '—', f'Table B.6 {sid} {a}')
                continue
            g, i, sh, c, n = C.breadth(rr, s)
            if a == 'pi05' and base is None and s != 'T2':
                shares[s] = sh
            V.cell(rel, ln, j, cells[j], f'{g} / {i} / {sh}% {c} / {n}', f'Table B.6 {sid} {a}')
    ln, raw = find_line(T('tab_tasks'), 'pick-and-place supplies')
    if ln and shares:
        V.text(rel, ln, raw, f'{min(shares.values())}–{max(shares.values())} %', "Table B.6 caption, pick-and-place share of pi0.5's scored episodes")
    rel = 'tables/tab_taxonomy.tex'
    for ln, raw, cells in table_rows(T('tab_taxonomy')):
        if len(cells) != 6:
            continue
        sid = cellplain(cells[0])
        if sid not in SUBS:
            continue
        g, i, sh, c, n = C.breadth(C.cr('pi05', sid), sid)
        if sid == 'T2':
            g0, i0, sh0, _, _ = C.breadth(C.cr('pi05', 'T2', C.pre), 'T2')
            ok1 = V.cell(rel, ln, 5, cells[5], f'{g0} / {i0} / {sh0}%', 'Table 1 last column, T2 pre-registered cell', contains=True)
            ok2 = V.cell(rel, ln, 5, cells[5], f'{g} / {i} / {sh}%', 'Table 1 last column, T2 pooled', contains=True)
            if not (ok1 and ok2):
                V.cells[(rel, ln)].pop(5, None)
        else:
            V.cell(rel, ln, 5, cells[5], f'{g} / {i} / {sh}%', f'Table 1 last column, {sid}')

    # ---------------------------------------------------------------- Table C.3: counts on shared placements
    rel = 'sections/app_c_stats.tex'
    for p, s, ln, cells, mark in matched_c:
        ka, kc, nst, na, nc = C.matched(p, s, C.cr('scripted', s))
        V.cell(rel, ln, 2, cells[2], frac(*ka), f'Table C.3 {p} {s} policy count')
        V.cell(rel, ln, 3, cells[3], frac(*kc), f'Table C.3 {p} {s} control count')
        V.cell(rel, ln, 4, cells[4], str(nst), f'Table C.3 {p} {s} placements')
        V.cell(rel, ln, 5, cells[5], f'{na} : {nc}', f'Table C.3 {p} {s} cells')
    V.check(len(matched_c) == 12, 'Table C.3 has 12 rows', f'Table C.3 has {len(matched_c)} rows, not 12')

    # ---------------------------------------------------------------- Table B.4 (witnesses)
    rel = 'sections/app_b_setup.tex'
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_b_setup.tex'), 'tabB:witness'):
        s = cellplain(cells[0])
        if s not in SUBS or len(cells) != 7:
            continue
        V.cell(rel, ln, 4, cells[4], frac(*C.kn(C.W[s], s)), f'Table B.4 {s} unsafe')
        V.cell(rel, ln, 5, cells[5], frac(C.tot(C.W[s], 'delivered'), C.tot(C.W[s], 'episodes')), f'Table B.4 {s} delivered')
        if s in ('T3', 'T4', 'T6b') and C.fr:
            comp = sum(C.fr[r['label']].get({'T3': 't3_ok_done', 'T4': 't4_ok_done', 'T6b': 't6b_ok_done'}[s]) or 0 for r in C.W[s])
        else:                                                  # no violation at all: every delivery is compliant
            comp = C.tot(C.W[s], 'delivered') if C.kn(C.W[s], s)[0] == 0 else None
        if comp is not None:
            V.cell(rel, ln, 6, cells[6], frac(comp, C.tot(C.W[s], 'episodes')), f'Table B.4 {s} compliant and delivered',
                   src='supp/cells.csv, fr_summary.json')

    # ---------------------------------------------------------------- Table B.1: every tabletop cell of a row, from fr_summary.json
    if C.fr:
        misrun = {f'ik_{c}_s{sd}' for c in ('sv_mug_R', 'sv_sci_R', 'spill_cup', 'spill_mug') for sd in (42, 7)}   # run under a wrong label
        skip = ('probe', 'smoke', 'still', 'demo', 'd4_', 'd5_', 'd6_', 'd7_', 'd8_', 'd9_', 'posetest', 'oak', '_fx_')
        agg = defaultdict(lambda: [0, 0, 0])
        reel = Counter()                                       # counted single-episode recordings for the demonstration videos
        reel_n1 = True
        for l, v in C.fr.items():
            if l in misrun or not isinstance(v, dict) or not v.get('N') or any(x in l for x in skip) or 'diag_' in l:
                continue
            p = 'pi0fast' if l.startswith('f0_') else 'pgbin' if l.startswith('pb_') else 'pi0' if l.startswith('p0_') else \
                'gr00t_droid' if l.startswith('g0_') else 'scripted' if l.startswith('ik_') else 'pi05'
            agg[p][0] += v['N']
            agg[p][1] += v.get('carried') or 0
            agg[p][2] += v.get('completed') or 0
            if re.match(r'(d1\d|r16|r20|p20h)', re.sub(r'^(f0_|p0_|g0_|ik_|pb_)', '', l)):     # label families of the later recordings
                reel[p] += 1
                reel_n1 = reel_n1 and v['N'] == 1
        # v2.2: the caption of Table B.1 says how many of these recordings its totals hold
        ln, raw = find_line(os.path.join(V2, 'sections', 'app_b_setup.tex'), 'later single-episode cells')
        if ln:
            want = (f'but {sum(reel.values())} later single-episode cells, run for demonstration videos and their render checks, are counted '
                    f'({reel["pi05"]} for π0.5, {reel["scripted"]} for the control)')
            src = 'fr_summary.json, counted cells of the label families d10-d19, r16, r20, p20h'
            if V.check(reel_n1 and set(reel) <= {'pi05', 'scripted'} and want in clean_line(expand_macros(raw)),
                       f'Table B.1 caption: {sum(reel.values())} later single-episode cells counted ({reel["pi05"]} for pi0.5, {reel["scripted"]} for the control)',
                       f'sections/app_b_setup.tex:{ln} Table B.1 caption should read "{want}" ({src}; rows {dict(reel)}, one episode each: {reel_n1})'):
                for t in (sum(reel.values()), reel['pi05'], reel['scripted']):
                    V.texts[('sections/app_b_setup.tex', ln)][V.canon(str(t))] = src
        for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_b_setup.tex'), 'tabB:policies'):
            if len(cells) != 6:
                continue
            p = next((k for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grfull', 'gr00t_droid'),
                                       ('Person-blind control', 'scripted')] if pat in cells[0]), None)
            if not p:
                continue
            a_, c_, d_ = agg[p]
            src = 'fr_summary.json, every tabletop cell of the row (rule of v1 Table 21)'
            V.cell(rel, ln, 3, cells[3], f'{a_:,}', f'Table B.1 {p} attempted', src=src)
            V.cell(rel, ln, 4, cells[4], f'{c_:,} ({pyround(100 * c_ / a_)})', f'Table B.1 {p} carried', src=src)
            V.cell(rel, ln, 5, cells[5], f'{d_:,} ({pyround(100 * d_ / a_)})', f'Table B.1 {p} delivered', src=src)

    # ---------------------------------------------------------------- Table B.5 (task library): the totals row
    lib = [(ln, cells) for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_b_setup.tex'), 'tabB:library') if len(cells) == 7]
    num = lambda c: 0 if cellplain(c) in ('—', '') else int(cellplain(c).replace(',', ''))
    body_rows = [c for ln, c in lib if cellplain(c[0]) not in ('All', 'Family', '')]
    for ln, cells in lib:
        if cellplain(cells[0]) == 'All':
            for j in (2, 3, 4, 6):
                tot_ = sum(num(c[j]) for c in body_rows)
                V.cell(rel, ln, j, cells[j], f'{tot_:,}' if j == 6 else str(tot_), f'Table B.5 totals row, column {j}', src='sum of the rows above')

    # ---------------------------------------------------------------- Table C.6 (joint-space control)
    rel = 'sections/app_c_stats.tex'
    js20 = [r for r in C.js if r['keepout_offset_m'] == '0.20']
    js28 = [r for r in C.js if r['keepout_offset_m'] == '0.28']
    near = [r for r in C.js_all if r not in C.js]
    pol = None
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_c_stats.tex'), 'tabC:js'):
        if len(cells) != 7:
            continue
        lab = cellplain(cells[0])
        exp = None
        if lab in ('P-A', 'P-B', 'P-C'):
            k, n, lo, hi, star = C.interval({'P-A': js20, 'P-B': js28, 'P-C': near}[lab], 'T1')
            exp = f'{k}/{n} [{lo}, {hi}]' + ('*' if star else '')
        elif lab == 'P-D':
            ka, kc = C.matched('pi05', 'T1', C.js)[:2]
            exp = f'{frac(*ka)} vs {frac(*kc)}'
        elif lab == 'P-E':
            ka, kc = C.matched('pi05', 'T1', js28)[:2]
            exp = f'{frac(*ka)} vs {frac(*kc)}'
        else:
            pol = next((k for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grd', 'gr00t_droid')] if pat in cells[0]), None)
            if pol and 'vs' in cells[3]:
                ka, kc = C.matched(pol, 'T1', C.js)[:2]
                exp = f'{frac(*ka)} vs {frac(*kc)}'
        if exp:
            V.cell(rel, ln, 3, cells[3], exp, f'Table C.6 {lab or pol} unsafe / scored')

    # ---------------------------------------------------------------- Tables C.3, C.5, C.6, C.7: test results as in N45 (v1)
    n45 = load_n45()
    sgn = lambda x: ('+' if x > 0 else ('-' if x < 0 else '+')) + str(abs(x))
    diffci = lambda d: f'{sgn(d["rd"])} [{sgn(d["ci"][0])}, {sgn(d["ci"][1])}]'
    p3 = lambda x: f'{x:.3f}'
    hol = lambda x: ('%.3f' % x).rstrip('0').rstrip('.') if x < 1 else '1.0'
    nr = n45.get('null_rel', {})
    for p, s, ln, cells, mark in matched_c:
        d = nr.get(p, {}).get(s)
        if not d:
            continue
        V.cell(rel, ln, 6, cells[6], diffci(d), f'Table C.3 {p} {s} difference and interval', src='N45 null_rel (v1 Table 20)')
        exp = '<0.001 (<0.005)' if d['p'] == 0 else f'{p3(d["p"])} ({hol(d["p_holm"]) if d["p_holm"] < 1 else "1.0"})'
        V.cell(rel, ln, 7, cells[7], exp, f'Table C.3 {p} {s} permutation p (Holm)', src='N45 null_rel (v1 Table 20)')
        V.check((mark == 'worse') == (d.get('sig') == 'above'), f'Table C.3 {p} {s} "worse after Holm" mark as N45 null_rel',
                f'{rel}:{ln} Table C.3 {p} {s}: the "worse" mark is {mark == "worse"}, N45 null_rel sig is {d.get("sig")}')
    a2 = n45.get('a2js', {})
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_c_stats.tex'), 'tabC:js'):
        if len(cells) != 7:
            continue
        lab = cellplain(cells[0])
        d = {'P-D': a2.get('PD'), 'P-E': a2.get('PE')}.get(lab)
        if d is None:
            pol_ = next((k for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grd', 'gr00t_droid')] if pat in cells[0]), None)
            d = a2.get('vs_policies', {}).get(pol_) if pol_ and 'vs' in cells[3] else None
        if d:
            V.cell(rel, ln, 4, cells[4], diffci(d), f'Table C.6 {lab} difference and interval', src='N45 a2js (v1 Table 9)')
            V.cell(rel, ln, 5, cells[5], f'{p3(d["p"])} ({p3(d["p_holm"])})', f'Table C.6 {lab} p (Holm)', src='N45 a2js (v1 Table 9)')
    t2c = {'H1': n45.get('t2conf', {}).get('pi05'), 'H2': n45.get('t2conf', {}).get('pi0fast'), 'H3': n45.get('t2conf_b', {}).get('gr00t_droid'),
           'H4': n45.get('t2conf_b', {}).get('pi0'), 'H5': n45.get('t2conf_e35')}
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_c_stats.tex'), 'tabC:prereg'):
        if len(cells) != 7:
            continue
        m = re.match(r'H[1-5]', cellplain(cells[0]))
        d = t2c.get(m.group(0)) if m else None
        if 'Cartesian control' in cells[0]:
            k, n, lo, hi, star = C.interval(C.cr('scripted', 'T2', C.pre), 'T2')
            V.cell(rel, ln, 1, cells[1], f'{k}/{n} [{lo}, {hi}]' + ('*' if star else ''), 'Table C.5 control, within 0.10 m')
            V.cell(rel, ln, 4, cells[4], frac(C.tot(C.cr('scripted', 'T2', C.pre), 'delivered'), C.tot(C.cr('scripted', 'T2', C.pre), 'episodes')), 'Table C.5 control delivered')
        if not d:
            continue
        w = d['wilson']
        rr = [r for r in C.rows if r['role'] == 'prereg_serving_35s'] if m.group(0) == 'H5' else \
            C.cr({'H1': 'pi05', 'H2': 'pi0fast', 'H3': 'gr00t_droid', 'H4': 'pi0'}[m.group(0)], 'T2', C.pre)
        k, n, lo, hi, star = C.interval(rr, 'T2')
        V.cell(rel, ln, 1, cells[1], f'{k}/{n} [{lo}, {hi}]' + ('*' if star else ''), f'Table C.5 {m.group(0)} within 0.10 m, clustered interval')
        V.check(d['kn'] == frac(k, n) and list(w[:2]) == [lo, hi], f'Table C.5 {m.group(0)}: cells.csv agrees with N45',
                f'{rel}:{ln} Table C.5 {m.group(0)}: cells.csv gives {k}/{n} [{lo}, {hi}], N45 has {d["kn"]} {w}')
        V.cell(rel, ln, 4, cells[4], frac(C.tot(rr, 'delivered'), C.tot(rr, 'episodes')), f'Table C.5 {m.group(0)} delivered')
        if d['rd'] or d.get('confirmed'):
            V.cell(rel, ln, 2, cells[2], f'{sgn(d["rd"])} [{sgn(d["ci"][0])}, {sgn(d["ci"][1])}]', f'Table C.5 {m.group(0)} difference and interval', src='N45 t2conf (v1 Table 7)')
            hp = f'{d["p_holm"]:.4f}' if 'p_holm' in d else 'single'
            V.cell(rel, ln, 3, cells[3], f'{d["p_perm"]:.4f} ({hp})', f'Table C.5 {m.group(0)} p (Holm)', src='N45 t2conf (v1 Table 7)')
    pg = n45.get('prereg', {})
    keymap = [('far keep-out at 0.20', 'T1_20'), ('far keep-out at 0.28', 'T1_28'), ('T2, serving', 'T2'), ('person on the left', 'T3_L'),
              ('person on the right', 'T3_R'), ('T6a, carried', 'T6'), ('T6a, waited', 'T6w')]
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_c_stats.tex'), 'tabC:repl'):
        if len(cells) != 6:
            continue
        lab = cellplain(cells[1])
        key = next((k for pat, k in keymap if pat in lab), 'T4' if lab == 'T4' else None)
        for j, p in ((3, 'pi05'), (4, 'pi0fast')):
            d = pg.get(p, {})
            if key and key in d.get('kn', {}):
                w = d['wilson'][key]
                V.cell(rel, ln, j, cells[j], f'{d["kn"][key]} [{w[0]}, {w[1]}]{w[2]}', f'Table C.7 {lab} {p}', src='N45 prereg (v1 Table 6)')

    # ---------------------------------------------------------------- Table C.8 (test-retest)
    ret = {d['cell']: d for d in n45.get('retest', [])}
    order = ['sc_kit_t1o20_s42', 'sv_mug_R_s42', 't3_sci_L_s42', 't3_sci_R_s42', 't4_mug_neutral_s42', 'hx_mug_s42', 't6_hand_s42b', 'wk_mug_s42']
    spec = {'sc_kit_t1o20_s42': ('viol_t1', 'n_t1'), 'sv_mug_R_s42': ('t2_viol', 't2_n'), 't3_sci_L_s42': ('t3_90', 't3'),
            't3_sci_R_s42': ('t3_90', 't3'), 't4_mug_neutral_s42': ('t45', 'tilt_trans'), 'hx_mug_s42': ('hx_reach', 'hx_ahead')}
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_c_stats.tex'), 'tabC:retest'):
        lab = cellplain(cells[0])
        pre_ = {'Original': ('orig', ''), 'Rerun 1': ('rep1', 'rep1_'), 'Rerun 2': ('rep2', 'rep2_')}.get(lab)
        if not pre_ or len(cells) != 9 or not ret:
            continue
        for j, cell_label in enumerate(order, 1):
            d = ret.get(cell_label, {})
            exp = f'{d.get(pre_[0])} ({d.get(pre_[0] + "_del")})'
            good = V.cell(rel, ln, j, cells[j], exp, f'Table C.8 {lab} {cell_label}', src='N45 retest (v1 Table 12)')
            f = C.fr.get(pre_[1] + cell_label) if C.fr else None
            if good and f and cell_label in spec:              # the same cell re-read from the per-cell summary
                kf, nf = spec[cell_label]
                n_ = f.get(nf)
                n_ = len(n_) if isinstance(n_, list) else n_
                V.check(exp == f'{f.get(kf)}/{n_} ({f.get("completed")}/{f.get("N")})', f'Table C.8 {lab} {cell_label} == fr_summary.json',
                        f'{rel}:{ln} Table C.8 {lab} {cell_label}: prints {exp}, fr_summary.json has {f.get(kf)}/{n_} ({f.get("completed")}/{f.get("N")})')

    # ---------------------------------------------------------------- Table D.4b (cone about the bearing), N45 t3_cone_h
    rel = 'sections/app_d_results.tex'
    dl = read(os.path.join(V2, 'sections', 'app_d_results.tex')).split('\n')
    cone = n45.get('t3_cone_h', {})
    at = [i for i, l in enumerate(dl) if 'Cone half-angle' in l]
    if at and cone:
        i = at[0]
        end = next(j for j in range(i, len(dl)) if '\\bottomrule' in dl[j])
        cur = None
        for j in range(i + 1, end):
            l = dl[j]
            first = split_amp(l)[0]
            for pat, k in [('pifive', 'pi05'), ('pifast', 'pi0fast'), ('Blind carry', 'scripted'), ('Uniform heading', 'uniform')]:
                if pat in first:
                    cur, todo = k, ['90', '75', '60', '45', '30']
            if cur is None or '\\%' not in l:
                continue
            for _ in range(len(re.findall(r'\\%', l))):
                ang = todo.pop(0)
                if cur == 'uniform':
                    val, src = pyround(100 * int(ang) / 180), 'half-angle / 180'
                else:
                    val, src = (cone[cur].get(ang) or cone[cur].get(int(ang)))['pct'], 'N45 t3_cone_h'
                V.text(rel, j + 1, l, f'{val} %', f'Table D.4b cone {ang} deg, {cur}', src=src)

    # ---------------------------------------------------------------- Table E.1 (humanoid), v1 App. E counts, plain Wilson
    rel = 'sections/app_e_humanoid.tex'
    for ln, raw, cells in table_rows(os.path.join(V2, 'sections', 'app_e_humanoid.tex'), 'tabE:g1'):
        if len(cells) != 5:
            continue
        m = re.match(r'(T\d[ab]?) ', cellplain(cells[0]))
        if not m or m.group(1) not in G1 or 'on the path' in cells[0]:
            continue
        k, n = G1[m.group(1)]
        lo, hi = wilson(k, n)
        V.cell(rel, ln, 2, cells[2], frac(k, n), f'Table E.1 {m.group(1)} count', src='v1 App. E (N45 heat_rows)')
        V.cell(rel, ln, 3, cells[3], f'{pyround(100 * k / n)} [{pyround(100 * lo)}, {pyround(100 * hi)}]', f'Table E.1 {m.group(1)} rate and plain Wilson interval',
               src='v1 App. E counts, Wilson interval recomputed', star=True)
    return V


# ------------------------------------------------------------------------------------------------ main pass
def iter_files(readme=False):
    for d in SRC_DIRS:
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.tex') and not fn.startswith('_'):
                yield os.path.join(d, fn)
    if readme:
        yield os.path.join(V2, 'supp', 'README.md')


def adj_key(rel, txt, s, a, b):
    return rel + ' :: ' + Verified.canon(txt) + ' :: ' + re.sub(r'\W+', ' ', s[max(0, a - 40):b + 40]).strip()


def main_pass(args, sources, V, adj):
    rows = []
    for path in iter_files(args.readme):
        rel = os.path.relpath(path, V2).replace('\\', '/')
        if args.file and args.file not in rel:
            continue
        lines = read(path).split('\n')
        tctx = table_context(lines)
        md_hdr = {}
        if path.endswith('.md'):                               # Markdown: a per cent sign is text, not the start of a LaTeX comment
            cleaned = [clean_line(expand_macros(re.sub(r'(?<!\\)%', r'\\%', l))) for l in lines]
            head = None                                        # a pipe table: its first line heads the columns of the rows below
            for i, l in enumerate(lines):
                if l.lstrip().startswith('|'):
                    if head is None:
                        head = cleaned[i].split('|')
                    else:
                        md_hdr[i] = head
                else:
                    head = None
        else:
            cleaned = [clean_line(expand_macros(l)) for l in lines]
        in_eq = False
        for ln, raw in enumerate(lines, 1):
            if re.search(r'\\begin\{(equation|align|gather|multline)\*?\}', raw):
                in_eq = True
            if in_eq:                                           # a displayed formula holds constants, not claims
                if re.search(r'\\end\{(equation|align|gather|multline)\*?\}', raw):
                    in_eq = False
                continue
            s = cleaned[ln - 1]
            if not s:
                continue
            is_row = '|' in s
            hdr, group, offset, rowlabel = tctx.get(ln - 1, ([], '', 0, ''))
            # prose: a sentence runs over the line break, so the neighbouring lines of the paragraph join the context
            prev = cleaned[ln - 2] if ln >= 2 and (ln - 2) not in tctx and not is_row else ''
            nxt = cleaned[ln] if ln < len(lines) and ln not in tctx and not is_row else ''
            ext = prev + ' ' + s + ' ' + nxt
            for kind, txt, a, b in tokenize(s):
                if kind == 'num':
                    val = float(txt.replace(',', ''))
                    if val == 0 and '.' not in txt:
                        continue
                ctx = s[max(0, a - 90):b + 90]
                a2 = a + len(prev) + 1
                cw = words(ext[max(0, a2 - 90):a2 + (b - a) + 90])
                col = offset + s[:a].count('|')
                if is_row:      # table row: the row label and the whole row are the context
                    cw |= words(s.split('|')[0]) | words(s)
                if (ln - 1) in tctx:
                    for h in hdr:
                        if col < len(h):
                            cw |= words(clean_line(expand_macros(h[col])))
                    if group:
                        cw |= words(clean_line(expand_macros(group)))
                    if rowlabel:
                        cw |= words(clean_line(expand_macros(rowlabel)))
                if (ln - 1) in md_hdr and col < len(md_hdr[ln - 1]):
                    cw |= words(md_hdr[ln - 1][col])
                key = adj_key(rel, txt, s, a, b)
                vsrc = V.cells.get((rel, ln), {}).get(col) or V.texts.get((rel, ln), {}).get(Verified.canon(txt))
                if vsrc:
                    st, best = 'FOUND', (99, 'struct', 'recomputed: ' + vsrc, '')
                else:
                    best = lookup(kind, txt, cw, sources)
                    st = classify(kind, txt, best)
                    if st != 'FOUND' and key in adj:
                        verdict = adj[key].get('verdict', '').lower()
                        st = {'wrong': 'WRONG', 'unsourced': 'UNSOURCED'}.get(verdict, 'ADJ')
                rows.append((rel, ln, kind, txt, st, best, ctx, key))
    return rows


def print_rows(rows, show, kind_filter, adj):
    cnt = Counter()
    wanted = {'open': ('weak', 'missing', 'wrong', 'unsourced')}.get(show, (show,))
    for rel, ln, kind, txt, st, best, ctx, key in rows:
        cnt[(st, kind)] += 1
        if show != 'all' and st.lower() not in wanted:
            continue
        if kind_filter and kind != kind_filter:
            continue
        src = f'{best[1]} ov={best[0]} "{best[2]}"' if best else '-'
        snippet = best[3][200:330].replace('\n', ' ') if best else ''
        print(f'{st:7s} {rel}:{ln} [{kind}] {txt!r}  <- {src}')
        print(f'        v2: …{ctx}…')
        if best and st not in ('FOUND',) and best[1] != 'struct':
            print(f'        src: …{snippet}…')
        if key in adj and st != 'FOUND':
            print(f'        adjudicated: {adj[key].get("verdict", "")}: {adj[key].get("note", "")}')
    print('\nSummary (status, kind): count')
    for (st, kind), c in sorted(cnt.items()):
        print(f'  {st:9s} {kind:6s} {c}')
    tot = Counter()
    for (st, _), c in cnt.items():
        tot[st] += c
    print('  totals:', dict(sorted(tot.items())))
    bysrc = Counter(best[1] for _, _, _, _, st, best, _, _ in rows if st == 'FOUND' and best)
    print('  FOUND by source:', dict(sorted(bysrc.items())))


# ------------------------------------------------------------------------------------------------ consistency
def plain(path):
    return ' '.join(clean_line(expand_macros(l)) for l in read(path).split('\n'))


def fig_text(name):
    try:
        out = subprocess.run(['pdftotext', '-layout', os.path.join(FIG_DIR, name), '-'], capture_output=True,
                             text=True, encoding='utf-8', errors='replace').stdout
    except Exception:
        out = ''
    return re.sub(r'\s+', ' ', out)


def table_numbers(env='table'):
    """{label: printed number} of every table (or figure), from the order of the floats: '3' in the main text, 'B.4' in an appendix.
    One number a float: right for the tables and for the appendix figures; a main-text float that holds two captions would be miscounted."""
    pat = r'\\begin\{table\*?\}|\\input\{tables/(\w+)\.tex\}' if env == 'table' else r'\\begin\{' + env + r'\*?\}()'
    main = read(os.path.join(V2, 'main.tex'))
    out = {}
    n_main = 0
    letter = None
    for m in re.finditer(r'\\appendix\b|\\input\{sections/(\w+)\.tex\}', main):
        if m.group(0).startswith('\\appendix'):
            letter = '@'
            continue
        if letter is not None:
            letter = chr(ord(letter) + 1)
        txt = read(os.path.join(V2, 'sections', m.group(1) + '.tex'))
        txt = '\n'.join(l for l in txt.split('\n') if not l.lstrip().startswith('%'))
        n = 0
        for t in re.finditer(pat, txt):
            if t.group(1):                                     # a generated table file holds one float
                lab = re.search(r'\\label\{([^}]+)\}', read(os.path.join(V2, 'tables', t.group(1) + '.tex')))
            else:
                lab = re.search(r'\\label\{([^}]+)\}', txt[t.end():txt.find('\\end{' + env, t.end())])
            if letter is None:
                n_main += 1
                num = str(n_main)
            else:
                n += 1
                num = f'{letter}.{n}'
            if lab:
                out[lab.group(1)] = num
    return out


WORDNUM = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
           'ten': 10, 'eleven': 11, 'twelve': 12, 'half': 0.5}


def consistency(C, V):
    issues = list(V.flags)
    ok = list(V.ok)

    def check(cond, msg_ok, msg_bad):
        (ok if cond else issues).append(msg_ok if cond else msg_bad)
        return cond

    tm = parse_tab_main()
    tc = parse_tab_counts()
    with open(FACTS_JSON, encoding='utf-8') as f:
        tf = json.load(f)['facts']
    val = lambda r, c: tm[r][c]['v']

    # 1. every k/n in the counts table prints round(100k/n) (Python half-even)
    for row, vals in tc.items():
        for col, v in vals.items():
            if col.startswith('_'):
                continue
            k, n, p, ci = v
            if p == 'n<8':
                check(n < 8, f'tabC:counts {row} {col}: n<8 for {k}/{n}', f'tabC:counts {row} {col}: n<8 printed but n={n}')
                continue
            if p is None:
                continue
            exp = pyround(100 * k / n)
            check(str(exp) == str(p), f'tabC:counts {row} {col}: {k}/{n} -> {p}',
                  f'tabC:counts {row} {col}: {k}/{n} = {100*k/n:.2f} % but printed {p}')

    # 2. Table 3 vs counts table vs table_facts
    for row, vals in tm.items():
        for col in ('Carry', 'SR', 'T1', 'T2', 'T3', 'T4', 'T5a', 'T6a', 'T6b'):
            v = vals[col]['v']
            if v in (None, '', '---'):
                continue
            if row in tc and col in tc[row]:
                k, n, p, ci = tc[row][col]
                check(v == p, f'Table 3 {row} {col} {v} == counts {k}/{n}',
                      f'Table 3 {row} {col} prints {v} but tabC:counts prints {k}/{n} -> {p}')
            tfk = f'tab_main:{row}:{"T6" if col == "T6a" else col}'
            if tfk in tf:
                tv = str(tf[tfk]['value'])
                check(v == tv, f'Table 3 {row} {col} == table_facts {tv}',
                      f'Table 3 {row} {col} prints {v} but table_facts says {tv}')
    if 'js' in tc and 'scripted' in tm:
        k, n, p, ci = tc['js']['T1']
        check(tm['scripted']['T1']['js'] == p, f'Table 3 control T1 cell, value after the slash == counts joint-space {k}/{n}',
              f'Table 3 control T1 cell prints {tm["scripted"]["T1"]["js"]} after the slash but tabC:counts joint-space row prints {p}')

    # 3. dimension scores = mean of exact sub-type rates, n>=8 rule (from the counts table as printed)
    dims = {'DimTraj': ('T1', 'T2'), 'DimOrient': ('T3', 'T4'), 'DimDyn': ('T6a', 'T6b')}
    for row, vals in tm.items():
        src = tc.get(row, {})
        for d, (a, b) in dims.items():
            v = vals[d]['v']
            if v in (None, '', '---'):
                continue
            if a in src and b in src:
                ka, na = src[a][:2]
                kb, nb = src[b][:2]
                if min(na, nb) < 8:
                    check(v == 'n<8', f'{row} {d} n<8', f'{row} {d} printed {v} but a member has n<8')
                else:
                    exp = pyround(50 * (ka / na + kb / nb))
                    check(v == str(exp), f'{row} {d} = {exp}',
                          f'{row} {d} printed {v}, mean of {ka}/{na} and {kb}/{nb} = {50*(ka/na+kb/nb):.2f}')

    # 4. App. E G1 table vs Table 3 G1 row
    e = plain(os.path.join(V2, 'sections', 'app_e_humanoid.tex'))
    for col, (k, n) in G1.items():
        kn = frac(k, n)
        check(kn in e and val('g1', col) == str(pyround(100 * k / n)), f'G1 {col} {kn} in App. E and Table 3',
              f'G1 {col}: App. E / Table 3 mismatch for {kn} (Table 3 {val("g1", col)})')
    m = re.search(r'Trajectory (\d+) ?\^? ?\*? ?, Orientation (\d+) ?\^? ?\*? ?, Speed and force (\d+) \(T5a\), Dynamics (\d+)', e)
    check(bool(m) and m.groups() == (val('g1', 'DimTraj'), val('g1', 'DimOrient'), val('g1', 'T5a'), val('g1', 'DimDyn')),
          'App. E dimension line matches Table 3', f'App. E dimension line {m.groups() if m else "not found"} vs Table 3 G1 row')
    if m:
        seg = e[m.start():m.end()]
        check(seg.count('*') == 2, 'App. E dimension line stars Trajectory and Orientation as Table 3 does',
              'App. E dimension line: Trajectory and Orientation should both carry the no-witness star (Table 3 G1 row)')

    # 5. headline numbers in abstract / intro / results / discussion vs Table 3 and the data
    secs = {n: plain(os.path.join(V2, 'sections', n + '.tex')) for n in
            ('abstract', 'intro', 'results', 'discussion', 'benchmark', 'definition', 'statements', 'app_a_metric_cards',
             'app_b_setup', 'app_c_stats', 'app_d_results', 'app_e_humanoid')}
    t2 = [int(val(r, 'T2')) for r in ('pi05', 'pi0fast', 'gr00t_droid')]
    rng = f'{min(t2)}–{max(t2)}%'
    for n in ('abstract', 'intro', 'results'):
        check(rng in secs[n], f'{n}: T2 headline {rng} matches Table 3', f'{n}: T2 headline range {rng} not found')
    k35 = C.kn([r for r in C.rows if r['role'] == 'prereg_serving_35s'], 'T2')
    eq = f'{min(t2)}–{pyround(100 * k35[0] / k35[1])}%'
    for n in ('abstract', 'intro'):
        check(eq in secs[n], f'{n}: T2 at equal episode length {eq} ({frac(*k35)} for GR00T-DROID at 35 s)',
              f'{n}: T2 range at equal episode length should read {eq} (GR00T-DROID at 35 s: {frac(*k35)})')
    check(frac(*k35) in secs['results'], f'results: 35 s rerun {frac(*k35)}', f'results: the 35 s rerun count {frac(*k35)} is not printed')
    # wording: pooled 6/79 -> 141/170, largest arm 30/32 (fr_summary.json, three prompt experiments)
    wd = wording_counts(C)
    if wd:
        lo, hi, top = (pyround(100 * wd['neutral'][0] / wd['neutral'][1]), pyround(100 * wd['spill'][0] / wd['spill'][1]),
                       pyround(100 * wd['arm3'][0] / wd['arm3'][1]))
        for n in ('abstract', 'intro', 'results'):
            check(f'from {lo}% to {hi}%' in secs[n], f'{n}: wording {lo}% -> {hi}% ({frac(*wd["neutral"])}, {frac(*wd["spill"])})',
                  f'{n}: wording headline should read "from {lo}% to {hi}%" ({frac(*wd["neutral"])} neutral, {frac(*wd["spill"])} spill clause)')
        for n in ('abstract', 'intro'):
            check(f'({top}% for' in secs[n], f'{n}: largest arm {top}% ({frac(*wd["arm3"])})',
                  f'{n}: the "do not spill the coffee" arm should read {top}% ({frac(*wd["arm3"])})')
        d0, d3 = wd['deliv0'], wd['deliv3']
        check(f'reaches {top}% and cuts delivery from {pyround(100*d0[0]/d0[1])}% to {pyround(100*d3[0]/d3[1])}%' in secs['results'],
              f'results: largest arm {top}%, delivery {frac(*d0)} -> {frac(*d3)}',
              f'results: the largest arm should read {top}% with delivery from {pyround(100*d0[0]/d0[1])}% to {pyround(100*d3[0]/d3[1])}%')
        check(frac(*wd['spill']) in secs['app_d_results'] and frac(*wd['neutral']) in secs['app_d_results'],
              'App. D.4 table prints the pooled wording counts', f'App. D.4 should print {frac(*wd["spill"])} and {frac(*wd["neutral"])}')
    r = secs['results']
    k3, n3 = C.kn(C.cr('pi05', 'T3'), 'T3')
    kc3, nc3 = C.kn(C.cr('scripted', 'T3'), 'T3')
    for label, pat in [
        (f'T3 pi0.5 {pyround(100*k3/n3)} / control {pyround(100*kc3/nc3)}',
         rf'{pyround(100*k3/n3)}% of carries and the person-blind control on {pyround(100*kc3/nc3)}%'),
        ('T6a pi0.5 reached and paused', rf'on {val("pi05", "T6a")}% of carries and pauses for it on 8%'),
        ('T6b no-walker reference 70%', rf"T6b's predicate fires on {val('mover', 'T6b')}% of"),
        ('F3 speeds 0.109 / 0.113, p 0.79', r'0\.109 m/s.*0\.113 m/s.*p = 0\.79'),
        ('T1 vs joint-space +8, p 0.169', r'\+8 points, p = 0\.169'),
        ('Holm 0.0003', r'p = 0\.0003'),
        ('hidden hand 81% against 83% visible', rf'\({val("mover", "T6a")}% against 83% visible\)'),
    ]:
        check(bool(re.search(pat, r)), f'results: {label}', f'results: {label} not as expected (pattern {pat})')
    check(pyround(100 * 7 / 88) == 8 and pyround(100 * 20 / 24) == 83, 'waits 7/88 = 8, visible hand 20/24 = 83', 'waits or visible-hand percentage mismatch')
    # witness rates: "at most a quarter" (results), "0-10% (25% for T6b)" (discussion)
    wit = {c: int(tm['wit'][c]['v']) for c in SUBS if tm['wit'][c]['v'].isdigit()}
    check(max(wit.values()) <= 25 and 'at most a quarter' in r.replace('  ', ' '), 'results: witness rate at most a quarter',
          f'results: "Its own rate is at most a quarter" vs witness row {wit}')
    others = [v for c, v in wit.items() if c != 'T6b']
    check(f'{min(others)}–{max(others)}% ({wit["T6b"]}% for T6b)' in secs['discussion'], 'discussion: witnesses read 0-10% (25% for T6b)',
          f'discussion: witness range should read {min(others)}–{max(others)}% ({wit["T6b"]}% for T6b)')
    # Carry / SR sentences of the policy-profile paragraph
    check(f'({val("pi0", "Carry")}% carried)' in r and f'({val("gr00t_droid", "Carry")}%; 90 s episodes)' in r,
          'results: carry of pi0 and GR00T-DROID as Table 3', f'results: "(39% carried)" / "(42%; 90 s episodes)" should match Table 3 Carry '
          f'{val("pi0", "Carry")} / {val("gr00t_droid", "Carry")}')
    check('deliver on about 60% of attempts' in r and all(55 <= int(val(p, 'SR')) <= 65 for p in ('pi05', 'pi0fast')),
          'results: pi0.5 and pi0-FAST deliver on about 60 % (Table 3 SR)', f'results: "about 60%" vs Table 3 SR {val("pi05", "SR")}, {val("pi0fast", "SR")}')
    check('under a third' not in r, 'results: no "under a third" carry claim', 'results: "under a third" is stale: Table 3 Carry is 39 and 42')
    top3 = lambda c: max(POLS, key=lambda p: int(val(p, c)) if val(p, c).isdigit() else -1)
    check(all(top3(c) == 'gr00t_droid' for c in ('T1', 'T2', 'T4')) and 'is highest on T1, T2 and T4' in r,
          'results: GR00T-DROID highest on T1, T2 and T4', 'results: "GR00T-DROID is highest on T1, T2 and T4" does not hold in Table 3')
    # stale references to marks and notes that Table 3 no longer has
    allraw = {os.path.relpath(p, V2).replace('\\', '/'): read(p) for p in iter_files()}
    for rel, t in allraw.items():
        if rel.startswith('tables/') or rel.endswith('app_c_stats.tex'):
            continue
        for pat, what in ((r'\\tU|\\tJ|\\circ\$ in Table|\\blacklozenge|\\bigcirc', 'a ring or diamond mark that Table 3 no longer prints'),):
            body = '\n'.join(l for l in t.split('\n') if not l.lstrip().startswith(('\\providecommand', '%')))
            check(not re.search(pat, body), f'{rel}: no reference to {what}', f'{rel}: refers to {what}')
    tmain = read(os.path.join(V2, 'tables', 'tab_main.tex'))
    body = tmain[tmain.index('\\begin{table}'):]
    check(not re.search(r'\\tW|\\tJ|\\tU|blacktriangle|blacklozenge|bigcirc', body), 'Table 3 prints no triangle, diamond or ring',
          'Table 3 still prints a triangle, diamond or ring mark')
    notes = sorted(set(re.findall(r'\^\{\\mathrm\{([a-z])\}\}', body)))
    check(notes == ['a', 'b', 'c'], 'Table 3 has the lettered notes a, b, c', f'Table 3 lettered notes are {notes}, expected a, b, c')
    for rel, t in allraw.items():
        for m_ in re.finditer(r'Table~\\ref\{tab:main\},? note ([a-z])', t):
            check(m_.group(1) in notes, f'{rel}: Table 3 note {m_.group(1)} exists', f'{rel}: refers to Table 3 note {m_.group(1)}, which does not exist')

    # 5b. the comparisons that give evidence in neither direction (ring marks of Table C.3) and those that could have
    #     shown a policy safer (Holm_0, the Holm-adjusted p of a policy with no violation, below 0.05). v2.2 wording:
    #     "uninformative" (abstract), "give evidence in neither direction; only three could have shown a policy safer"
    mc = parse_matched_c()
    n_unt = sum(1 for x in mc if x[4] == 'untested')
    n_all = len(mc)

    def cnum(cell):
        """a Bound or Holm_0 cell of Table C.3 as a number ('<0.001' reads as below it)"""
        t = cellplain(cell).replace(' ', '').replace('−', '-').replace('–', '-')
        try:
            return float(t[1:]) / 2 if t.startswith('<') else float(t)
        except ValueError:
            return None

    holm0 = {(x[0], x[1]): cnum(x[3][9]) for x in mc}
    bound = {(x[0], x[1]): cnum(x[3][8]) for x in mc}
    num_ok = all(v is not None for v in list(holm0.values()) + list(bound.values()))
    check(num_ok and len(holm0) == 12, 'Table C.3: every row prints a Bound and a Holm_0', 'Table C.3: a Bound or Holm_0 cell is not a number')
    if num_ok:
        for p_, s_, ln_, _, mark_ in mc:
            ring = holm0[(p_, s_)] >= 0.05 and bound[(p_, s_)] < 0      # could not have shown the policy safer, and does not exclude it
            check((mark_ == 'untested') == ring, f'Table C.3 {p_} {s_}: ring mark as its Holm_0 and Bound',
                  f'sections/app_c_stats.tex:{ln_} Table C.3 {p_} {s_}: ring mark is {mark_ == "untested"}, but Holm_0 {holm0[(p_, s_)]} at or '
                  f'above 0.05 with a negative Bound ({bound[(p_, s_)]}) is {ring}')
    n_could = sum(1 for v in holm0.values() if v is not None and v < 0.05)
    ab = secs['abstract']
    m = re.search(r'(\w+) of the (\w+) matched comparisons are uninformative', ab)
    check(bool(m) and WORDNUM.get(m.group(1)) == n_unt and WORDNUM.get(m.group(2)) == n_all,
          f'abstract: {n_unt} of {n_all} matched comparisons are uninformative (ring marks of Table C.3)',
          f'abstract: "{m.group(0) if m else "?"}" vs {n_unt} ring-marked rows of {n_all} in Table C.3')
    m = re.search(r'(\w+) of the (\w+) give evidence in neither direction', r)
    check(bool(m) and WORDNUM.get(m.group(1).lower()) == n_unt and WORDNUM.get(m.group(2)) == n_all,
          f'results: {n_unt} of the {n_all} give evidence in neither direction',
          f'results: "{m.group(0) if m else "?"}" vs {n_unt} ring-marked rows of {n_all} in Table C.3')
    m = re.search(r'only (\w+) could have shown a policy safer', r)
    check(bool(m) and WORDNUM.get(m.group(1)) == n_could, f'results: only {n_could} could have shown a policy safer (Table C.3, Holm_0 below 0.05)',
          f'results: "{m.group(0) if m else "?"}" vs {n_could} rows of Table C.3 with Holm_0 below 0.05')
    check(('Half of our matched comparisons give evidence in neither direction' in secs['discussion']) == (2 * n_unt == n_all),
          'discussion: half of the matched comparisons give evidence in neither direction',
          f'discussion: "Half of our matched comparisons give evidence in neither direction" vs {n_unt} of {n_all}')
    cst = secs['app_c_stats']
    m = re.search(r'safer than the Cartesian control; (\w+) give evidence in neither direction', cst)
    check(bool(m) and WORDNUM.get(m.group(1)) == n_unt, f'Table C.3 caption: {n_unt} give evidence in neither direction',
          f'Table C.3 caption: "{m.group(0) if m else "?"}" vs {n_unt} ring-marked rows')
    m = re.search(r'(\w+) rows could have produced a Holm-significant safer verdict', cst)
    check(bool(m) and WORDNUM.get(m.group(1).lower()) == n_could, f'App. C.3: {n_could} rows could have produced a Holm-significant safer verdict',
          f'App. C.3: "{m.group(0) if m else "?"}" vs {n_could} rows of Table C.3 with Holm_0 below 0.05')
    m = re.search(r'The other (\w+) rows, marked', cst)
    check(bool(m) and WORDNUM.get(m.group(1)) == n_unt, 'App. C.3: the other six rows', f'App. C.3 "the other ... rows" vs {n_unt} marked rows')
    n_worse = sum(1 for x in mc if x[4] == 'worse')
    bold = [(p, c) for p in POLS for c in SUBS if 'heatb' in tm[p][c]['macro']]
    check(len([b for b in bold if b[1] == 'T1']) == n_worse == 4 and len([b for b in bold if b[1] == 'T2']) == 3
          and "every policy's T1 and three policies' pre-registered T2" in r.replace('  ', ' '),
          "results: bold = every policy's T1 and three policies' pre-registered T2",
          f'results: the bold-cell sentence vs Table 3 bold cells {bold}')

    # 6. figure text vs paper (figure numbers shift; the files are named)
    f2 = fig_text('fig_main_t2.pdf')
    if f2:
        for p in POLS + ['scripted']:
            kn = frac(*C.kn(C.cr(p, 'T2', C.pre), 'T2'))
            check(kn in f2, f'fig_main_t2 has {kn}', f'fig_main_t2 lacks {kn} ({p}, pre-registered serving cell)')
        f4 = fig_text('fig_main_t4.pdf')
        for kn in ('3/32', '30/32', '5/32', '14/27', '1/31', '21/31', '16/23'):
            check(kn in f4, f'fig_main_t4 has {kn}', f'fig_main_t4 lacks {kn}')
        ft = fig_text('fig_teaser.pdf')
        for badge in ('43% vs 0%', '65% vs 0%'):               # the teaser is being rebuilt: only the stable badges
            check(badge in ft, f'teaser badge {badge}', f'teaser badge {badge} missing')
        check(re.search(r'68.94% vs 9%', ft) is not None, 'teaser T4 badge 68–94% vs 9% (21/31, 30/32 vs 3/32; the teaser is being rebuilt)',
              'teaser T4 badge changed')
        f1 = fig_text('fig_main_t1.pdf')
        for kn in ('18/80', '78/79', '68/68'):
            check(kn in f1, f'fig_main_t1 has {kn}', f'fig_main_t1 lacks {kn}')
        fs = fig_text('fig_t2_sweep.pdf')
        for kn in ('26/56', '32/56', '14/14', '43/58', '5/6', '0/24', '26/26', '33/34'):
            check(kn in fs, f'fig_t2_sweep has {kn}', f'fig_t2_sweep lacks {kn}')
        fc = fig_text('fig_t6_contact.pdf')
        a = secs['app_a_metric_cards']
        m = re.search(r"box's half-extent \((0\.\d+)–(0\.\d+) m", a)
        mf = re.search(r'contact distance[^(:]{0,12}\((0\.\d+) m\)', fc)
        if m and mf:
            check(float(m.group(1)) <= float(mf.group(1)) <= float(m.group(2)),
                  'G1 contact distance: fig_t6_contact lies in the range of App. A.6',
                  f'App. A T6a card gives the G1 contact distance as {m.group(1)}–{m.group(2)} m; fig_t6_contact draws it at {mf.group(1)} m')
        fth = fig_text('fig_t4_threshold.pdf')
        check('contact 19/32' in fth and 'contact 8/32' in fth, 'fig_t4_threshold: G1 contact 19/32, pi0.5 contact 8/32',
              'fig_t4_threshold contact counts changed')
    else:
        ok.append('figure texts skipped: pdftotext not available')

    # 6b. counts table intervals vs table_facts strings
    tfc = {k.split(':', 1)[1]: v['value'] for k, v in tf.items() if k.startswith('tab_counts:') and isinstance(v, dict)}
    raw = read(os.path.join(V2, 'tables', 'tab_counts.tex'))
    for key, v in tfc.items():
        if ':' not in key:
            continue
        row, col = key.split(':')[:2]
        sval = str(v)
        mk = re.match(r'(\d+/\d+) = (\d+)(?: \[(\d+), (\d+)\](\*?))?', sval)
        if not mk:
            continue
        kn, pcv, lo, hi, star = mk.groups()
        if lo is None:
            continue
        pat = re.escape(kn) + r'\\\\' + pcv + r'\\\\\{\[\}' + lo + r',\\,' + hi + r'\{\]\}' + (r'\*' if star else r'(?!\*)')
        check(re.search(pat, raw) is not None, f'tabC:counts {row} {col} {sval}',
              f'tabC:counts {row} {col}: expected "{sval}" (table_facts) not found')

    # 6c. Table B.1 rows, their sums and the totals quoted in the caption and Sec. 4.1
    b = read(os.path.join(V2, 'sections', 'app_b_setup.tex'))
    tot = [0, 0, 0]
    nrow = 0
    for ln, rawl, cells in table_rows(os.path.join(V2, 'sections', 'app_b_setup.tex'), 'tabB:policies'):
        if len(cells) != 6:
            continue
        nums = [cellplain(c) for c in cells[3:6]]
        m3 = [re.match(r'([\d,]+)(?: \((\d+)\))?$', x) for x in nums]
        if not all(m3):
            continue
        att, car, dl = [int(x.group(1).replace(',', '')) for x in m3]
        nrow += 1
        tot = [tot[0] + att, tot[1] + car, tot[2] + dl]
        check(m3[1].group(2) == str(pyround(100 * car / att)) and m3[2].group(2) == str(pyround(100 * dl / att)),
              f'Table B.1 row {nrow}: carried and delivered per cent of {att} attempted',
              f'Table B.1 row {nrow}: {car}/{att} = {100*car/att:.1f} %, {dl}/{att} = {100*dl/att:.1f} % but printed {m3[1].group(2)} and {m3[2].group(2)}')
    bcap = secs['app_b_setup']
    want = f'{tot[0]:,} attempted, {tot[1]:,} carried and {tot[2]:,} delivered'
    check(nrow == 5 and want in bcap, f'Table B.1: five rows total {want}', f'Table B.1: the rows total {want}; the caption prints otherwise')
    check(f'{tot[0]:,}' in secs['benchmark'], f'Sec. 4.1 prints {tot[0]:,}', f'Sec. 4.1 total differs from the Table B.1 sum {tot[0]:,}')
    tb = b[b.index('label{tabB:library}'):]
    tb = tb[tb.index('\\midrule'):tb.index('\\bottomrule')]
    rowsl = []
    for l in tb.split('\n'):
        cells = [c.strip() for c in l.rstrip('\\ ').split('&')]
        if len(cells) == 7:
            rowsl.append([0 if c in ('---', '') else int(c.replace(',', '')) for c in (cells[2], cells[3], cells[4], cells[6])])
    if rowsl:
        bodyl, total = rowsl[:-1], rowsl[-1]
        sums = [sum(x[i] for x in bodyl) for i in range(4)]
        check(sums == total, f'library column sums {total}', f'library column sums {sums} != printed {total}')
        check(f'has {sum(total[:3])} tasks' in bcap and f'delivers in {total[0]} of them, carries but rarely delivers in {total[1]} and cannot carry the payload in {total[2]}' in bcap,
              'App. B.5 task counts match the library table', f'App. B.5 task counts vs library totals {total}')
        check(f'{sum(total[:3])} tasks, of which' in secs['benchmark'] and f'can do {total[0]}' in secs['benchmark'],
              'Sec. 4.1 task counts match the library table', f'Sec. 4.1 task counts vs library totals {total}')

    # 6d. what each rate rests on: Table B.6 caption, Table 1 note and Sec. 3.3 vs the cells
    tt = plain(os.path.join(V2, 'tables', 'tab_tasks.tex'))
    goals = {p: {s: C.breadth(C.cr(p, s), s)[0] for s in SUBS if C.cr(p, s)} for p in POLS}
    one = lambda p, exc=(): all(g in ('1', '0+1') for s, g in goals[p].items() if s not in exc)
    check(one('pi0') and one('gr00t_droid') and one('pi0fast', ('T3', 'T4')) and goals['pi0fast']['T3'] == goals['pi0fast']['T4'] == '2'
          and 'rest on one goal' in tt and 'on one except T3 and T4 (two)' in tt,
          'Table B.6 caption: pi0 and GR00T-DROID one goal, pi0-FAST one except T3 and T4', f'Table B.6 caption on goals vs cells.csv {goals}')
    check(all(g in ('2', '3') for g in goals['pi05'].values()) and 'spans two or three goals' in tt,
          'Table B.6 caption: each pooled pi0.5 rate spans two or three goals', f'Table B.6 caption vs pi0.5 goals {goals["pi05"]}')
    sh = [C.breadth(C.cr('pi05', s), s)[2] for s in ('T1', 'T3', 'T4', 'T6a', 'T6b')]
    d = secs['definition']
    check(f'{min(sh)}–{max(sh)} %' in d and f'{100 - max(sh)}–{100 - min(sh)} %' in d,
          f'Sec. 3.3: pick-and-place {min(sh)}-{max(sh)} %, second goal {100 - max(sh)}-{100 - min(sh)} %',
          f'Sec. 3.3 shares should read {100 - max(sh)}–{100 - min(sh)} % and {min(sh)}–{max(sh)} %')

    # 6d2. Table C.1 caption: the rates that rest on 8-19 scored episodes, in every row of the table (v2.2 also names the
    #      G1's and the witness's; the tabletop T5a column is exposure, the G1's is a rate)
    thin = {}
    for p in POLS + ['scripted', 'js', 'g1', 'wit']:
        cols = ('T1', 'T2', 'T2pool', 'T3', 'T4') + (('T5a',) if p == 'g1' else ()) + ('T6a', 'T6b')
        got = [{'T2pool': 'pooled T2'}.get(c, c) for c in cols if c in tc.get(p, {}) and 8 <= tc[p][c][1] <= 19]
        if got:
            thin[p] = got
    names = {'pi05': "π0.5's", 'pi0': "π0's", 'pi0fast': "π0-FAST's", 'gr00t_droid': "GR00T-DROID's", 'scripted': "the Cartesian control's",
             'js': "the joint-space control's", 'g1': "the G1's", 'wit': "the witness's"}
    want = '; '.join(names[p] + ' ' + (' and '.join([', '.join(v[:-1]), v[-1]]) if len(v) > 1 else v[0]) for p, v in thin.items())
    capc = plain(os.path.join(V2, 'tables', 'tab_counts.tex'))
    check(f'Rates on 8–19 scored episodes: {want}.' in capc, f'Table C.1 caption lists the rates on 8-19 scored episodes ({want})',
          f'Table C.1 caption: the rates on 8–19 scored episodes are "{want}" by the table\'s own counts')

    # 6e. design-effect star threshold stated consistently
    s1 = re.search(r'star marks D\s*(≥|>)\s*1\.5', cst)
    s2 = re.search(r'design effect\s*(>|≥)\s*1\.5', plain(os.path.join(V2, 'tables', 'tab_counts.tex')))
    if s1 and s2:
        check(s1.group(1) == s2.group(1), 'star threshold consistent',
              f'App. C says "a star marks D {s1.group(1)} 1.5", Table C.1 caption says "design effect {s2.group(1)} 1.5"')

    # 6g. what the cell table is said to regenerate: main.tex, Sec. 4.2, App. B.4, statements vs supp/README.md
    rd = read(os.path.join(V2, 'supp', 'README.md'))
    check('its Carry and SR columns' in rd and 'cannot be summed from this file' in rd, 'README: Carry and SR of Table 3 summed from cells.csv; Table B.1 not',
          'README no longer says that Table 3 Carry/SR are summed from cells.csv and Table B.1 is not')
    check('Table 2' not in rd, 'README names the matrix Table 3', 'README still says "Table 2" for the matrix')
    # table numbers typed into the README against the order of the floats in the paper
    tn = table_numbers()
    rdf = ' '.join(rd.split())
    for lab, want, what in (('tab:main', '3', 'the matrix'), ('tab:taxonomy', '1', 'the taxonomy'), ('tabC:counts', 'C.1', 'the counts table'),
                            ('tabB:policies', 'B.1', 'the policy table with the all-cell totals')):
        check(tn.get(lab) == want and f'Table {want}' in rdf, f'README: Table {want} is {what} ({lab})',
              f'README calls {what} "Table {want}", but {lab} is Table {tn.get(lab)} in the paper')
    for pat, lab, what in ((r'Table 1, last column, and Table (\S+?)\*\* \(what each rate rests on\)', 'tabB:tasks', 'the table of what each rate rests on'),
                           (r'Table (\S+) adds the cells and the scored episodes', 'tabB:tasks', 'the table that adds cells and scored episodes'),
                           (r'robot-base frame of Table (\S+?) \(', 'tabB:surfaces', 'the table of the work surfaces (frame of person_x_m, person_y_m)'),
                           (r'matched comparisons with the control \(Table (\S+?)\)', 'tabC:matched', 'the table of matched comparisons'),
                           (r'the core suite of App\. (\S+?)\.', 'appB:seeds', 'the core suite')):
        mm = re.search(pat, rdf)
        if lab.startswith('tab'):
            check(bool(mm) and mm.group(1) == tn.get(lab), f'README: {what} is Table {tn.get(lab)}',
                  f'README: {what} is called "Table {mm.group(1) if mm else "?"}"; in the paper {lab} is Table {tn.get(lab)}')
    # (v2.2: the float of tab_tasks moved to the end of App. B, so the witnesses are B.4, the library B.5 and tab_tasks B.6)
    for lab, want in (('tabC:strata', 'C.2'), ('tabC:matched', 'C.3'), ('tabC:core', 'C.4'), ('tabC:prereg', 'C.5'), ('tabC:js', 'C.6'),
                      ('tabC:repl', 'C.7'), ('tabC:retest', 'C.8'), ('tabD:goals', 'D.1'), ('tabD:t2', 'D.3'), ('tabD:t3', 'D.4'),
                      ('tabD:t5', 'D.6'), ('tabB:surfaces', 'B.2'), ('tabB:instr', 'B.3'), ('tabB:witness', 'B.4'), ('tabB:library', 'B.5'),
                      ('tabB:tasks', 'B.6'), ('tabE:g1', 'E.1')):
        check(tn.get(lab) == want, f'table numbering: {lab} is Table {want} (as this checker names it)',
              f'table numbering changed: {lab} is now Table {tn.get(lab)}; the messages of this checker call it Table {want}')
    mt = plain(os.path.join(V2, 'main.tex'))
    for name, t in (('main.tex (appendix contents)', mt), ('App. B.4', bcap)):
        check('Carry and SR columns' in t, f'{name}: Carry and SR columns are among what cells.csv reproduces', f'{name}: the provenance sentence omits the Carry and SR columns')
    check('regenerates every tabletop number' not in secs['benchmark'], 'Sec. 4.2 does not claim every tabletop number', 'Sec. 4.2 overclaims: "regenerates every tabletop number"')
    check(f'table of {len(C.rows)} cells' in secs['benchmark'], f'Sec. 4.2: {len(C.rows)} cells in the release table', f'Sec. 4.2 cell count vs cells.csv rows {len(C.rows)}')

    # 6h. seeds, cells and surfaces repeated across files, from cells.csv
    nsc = len(C.sc)
    nseed = len([r for r in C.sc if r['seed'] not in ('42', '7')])
    for n in ('definition', 'statements', 'app_b_setup'):
        check(f'{nseed} of the {nsc} pooled cells' in secs[n], f'{n}: {nseed} of the {nsc} pooled cells use further seeds',
              f'{n}: should read "{nseed} of the {nsc} pooled cells" (cells.csv, role scored, seed not 42 or 7)')
    check(f'Of the {nsc} pooled cells, {nseed} use further seeds' in cst, f'App. C.1: {nseed} of {nsc}', f'App. C.1 seeds sentence vs {nseed} of {nsc}')
    # v2.2: these cells "hold fewer" episodes; not all of them stopped early (App. B.4 splits them three ways)
    short = len([r for r in C.rows if I(r['episodes']) < 8])
    check(f'{short} of the {len(C.rows)} released cells hold fewer' in bcap, f'App. B.4: {short} of {len(C.rows)} released cells hold fewer than eight episodes',
          f'App. B.4 should read "{short} of the {len(C.rows)} released cells hold fewer" (cells.csv, episodes below 8)')
    # the split: launched with six (run log; not in cells.csv), a payload log shorter than the link log (cells.csv: a scored
    # count above the episodes), and the rest, which stopped early; the three parts must add up to the cells that hold fewer
    over = [x for x in C.rows if any(I(x[s + '_scored']) > I(x['episodes']) for s in SUBS)]
    eps = sorted(I(x['episodes']) for x in over)
    m = re.search(r"(\w+) of GR00T-DROID's first cells were launched with six episodes.{0,80}?, (\w+) π0\.5 serving cells at the office desk ran eight "
                  r"but their payload log holds (\w+) to (\w+), and the other (\d+) stopped early", bcap)
    check(bool(m) and bool(over) and all(x['policy'] == 'pi05' and x['work_surface'] == 'office desk' and 'serving' in x['task'] for x in over)
          and WORDNUM.get(m.group(2)) == len(over) and (WORDNUM.get(m.group(3)), WORDNUM.get(m.group(4))) == (eps[0], eps[-1])
          and WORDNUM.get(m.group(1).lower(), -99) + len(over) + int(m.group(5)) == short,
          f'App. B.4: the cells that hold fewer split into {m.group(1).lower() if m else "?"} launched with six, {len(over)} with a shorter payload log '
          f'and {m.group(5) if m else "?"} that stopped early (sum {short})',
          f'App. B.4: the split of the {short} cells that hold fewer ("{m.group(0)[:60] if m else "?"} ...") does not add up, or the cells whose payload '
          f'log is shorter are not {len(over)} π0.5 office-desk serving cells with {eps[0] if eps else "?"} to {eps[-1] if eps else "?"} episodes (cells.csv)')
    # counts written as words (the token pass reads digits only)
    numword = {v: k for k, v in WORDNUM.items() if isinstance(v, int)}
    numword.update({16: 'sixteen', 22: 'twenty-two'})
    ssc = [r for r in C.sc if I(r['episodes']) < 8]
    want = f'{numword.get(len(ssc), len(ssc))} pooled cells, {len([r for r in ssc if r["policy"] == "gr00t_droid"])} of them GR00T-DROID\'s, hold fewer'
    check(want in cst.lower().replace("gr00t-droid's", "GR00T-DROID's"), f'App. C.1: {want}', f'App. C.1 should read "{want}" (cells.csv, role scored, fewer than 8 episodes)')
    jshort = [I(r['episodes']) for r in C.js_all if I(r['episodes']) < 8]
    want = (f'{numword.get(len(jshort), len(jshort))} of the {len(C.js_all)} cells stopped early with {min(jshort)}–{max(jshort)} episodes and count as run: '
            f'{C.tot(C.js_all, "episodes")} of {8 * len(C.js_all)} episodes, {C.tot(C.js, "episodes")} of {8 * len(C.js)} on the far side')
    check(want in cst[0].lower() + cst[1:].replace('Sixteen', 'sixteen'), f'App. C.4: {want}', f'App. C.4 should read "{want}" (cells.csv, role control_jointspace)')
    relit = [r for r in C.sc if r['policy'] == 'pi05' and r['environment'] not in ('scene default', 'industrial warehouse')]
    want = f'relight {len(relit)} of π0.5\'s T3 and T4 cells'
    check(want in bcap and len({r['environment'] for r in relit}) == 4 and 'Four further light maps' in bcap, f'App. B.2: four further light maps {want}',
          f'App. B.2 should read "{want}" with {len({r["environment"] for r in relit})} further light maps (cells.csv, environment)')
    surf = {p: len({r['work_surface'] for r in C.behind(p)} - {'island kitchen'}) for p in POLS}
    check(surf == {'pi05': 5, 'pi0': 5, 'pi0fast': 4, 'gr00t_droid': 3} and 'run at all five, π0-FAST at four and GR00T-DROID at three' in secs['benchmark'],
          'Sec. 4.1: surfaces per policy 5 / 5 / 4 / 3', f'Sec. 4.1 surfaces per policy vs cells.csv {surf}')
    for n in ('abstract', 'intro'):
        check(f'three to five' in secs[n], f'{n}: each policy at three to five work surfaces', f'{n}: "three to five" work surfaces missing')
    npp = len([r for r in C.sc if r['goal'] == PP])
    check(f'{pyround(100 * npp / nsc)} % of scored cells' in secs['benchmark'] and f'add {nsc - npp} cells' in secs['benchmark'],
          f'Sec. 4.1: {pyround(100 * npp / nsc)} % of scored cells are pick-and-place, {nsc - npp} others',
          f'Sec. 4.1 should read {pyround(100 * npp / nsc)} % and {nsc - npp} cells ({npp}/{nsc})')

    # 6i. witness counts repeated in App. A, App. B and the discussion
    a = secs['app_a_metric_cards']
    for s, phrase in (('T1', 'clears every 0.28 m keep-out ({u}) and delivers on {dk} of these {dn} carries'),
                      ('T2', '{u} in the band, {d} delivered'), ('T3', 'It reads {u} into the half-space as spawned, {d} delivered'),
                      ('T4', 'past 45° on {u} carries'), ('T6a', 'reaches the hand on {u} carries and delivers {d}'),
                      ('T6b', 'passed unslowed on {u}')):
        u = frac(*C.kn(C.W[s], s))
        dk, dn = C.tot(C.W[s], 'delivered'), C.tot(C.W[s], 'episodes')
        want = phrase.format(u=u, d=frac(dk, dn), dk=dk, dn=dn)
        check(want in a, f'App. A {s} witness: {want}', f'App. A {s} witness card should contain "{want}"')
    # v2.2: the baseline is the visible hand on the witness's own placement (dining table, mug), not all dining-table carries
    w6 = C.kn(C.W['T6a'], 'T6a')
    wobj = {x['object'] for x in C.W['T6a']}
    wsurf = {x['work_surface'] for x in C.W['T6a']}
    vis = C.kn([r for r in C.cr('pi05', 'T6a') if r['work_surface'] in wsurf and r['goal'] == PP and r['object'] in wobj], 'T6a')
    check(wobj == {'mug'} and wsurf == {'dining table'} and f'from {frac(*vis)} to {frac(*w6)} on the dining-table mug cells' in secs['discussion'],
          f'discussion: whole-arm stop {frac(*vis)} -> {frac(*w6)} on the dining-table mug cells',
          f'discussion: the whole-arm stop should read from {frac(*vis)} to {frac(*w6)} on the dining-table mug cells '
          f'(cells.csv: the witness ran {sorted(wobj)} at {sorted(wsurf)})')

    # 6j. T3 by side and the handover, results vs cells.csv
    pos = lambda r_: float(r_['person_y_m']) > 0
    for p, form in (('pi05', '{a} of {b} carries for a person on the side this yaw faces and {c} of {d} for'), ('scripted', 'The blind control reads {a}/{b} and {c}/{d}')):
        f_ = C.kn([x for x in C.cr(p, 'T3') if x['object'] == 'scissors' and pos(x)], 'T3')
        o_ = C.kn([x for x in C.cr(p, 'T3') if x['object'] == 'scissors' and not pos(x)], 'T3')
        want = form.format(a=f_[0], b=f_[1], c=o_[0], d=o_[1])
        check(want in r.replace('  ', ' '), f'results: T3 scissors by side, {p}: {frac(*f_)} and {frac(*o_)}', f'results: T3 by side for {p} should contain "{want}"')
    k4, n4 = C.kn(C.cr('pi05', 'T4'), 'T4')
    if C.fr:
        kd = sum((C.fr[x['label']].get('t45_delivered') or 0) for x in C.cr('pi05', 'T4'))
        check(f'{kd} of the {k4} tilted carries' in r, f'results: {kd} of the {k4} tilted carries are delivered',
              f'results: should read "{kd} of the {k4} tilted carries" (fr_summary t45_delivered over the scored T4 cells)')
        check(f'{pyround(100 * kd / k4)}% of the carries on which π0.5 tips a mug' in secs['intro'], f'intro: {pyround(100 * kd / k4)}% of tilted carries are delivered',
              f'intro: the share of tilted carries that are delivered should read {pyround(100 * kd / k4)}% ({kd}/{k4})')

    # 6k. revision v2.2: what the policy cameras show. The placements with no part of the bystander in the external frame
    #     are read from the brackets of Table B.2 ([0 %]); every count that the text hangs on them is summed from cells.csv
    app_b = os.path.join(V2, 'sections', 'app_b_setup.tex')
    outv = set()
    n_brackets = 0
    shares_tex = {}
    for ln_, raw_, cells_ in table_rows(app_b, 'tabB:surfaces'):
        if len(cells_) != 5:
            continue
        surf_ = re.sub(r'\s*\(probe\)', '', cellplain(cells_[0])).lower()
        for mm in re.finditer(r'\((-?[\d.]+), (-?[\d.]+)\) \[(\d+) %\]', cellplain(cells_[4])):
            n_brackets += 1
            shares_tex[(surf_, float(mm.group(1)), float(mm.group(2)))] = int(mm.group(3))
            if mm.group(3) == '0':
                outv.add((surf_, float(mm.group(1)), float(mm.group(2))))
    is_out = lambda x: x['person_x_m'] != '' and (x['work_surface'], float(x['person_x_m']), float(x['person_y_m'])) in outv
    check(n_brackets >= 9 and len(outv) == 2, f'Table B.2: {n_brackets} shares in brackets, two placements at 0 % ({sorted(outv)})',
          f'Table B.2: {n_brackets} bracketed shares read and {len(outv)} placements at [0 %]; the text speaks of two placements')
    behind = C.sc + C.pre
    n_out = len([x for x in behind if is_out(x)])
    split = lambda p_, s_: (C.kn([x for x in C.cr(p_, s_) if is_out(x)], s_), C.kn([x for x in C.cr(p_, s_) if not is_out(x)], s_), C.kn(C.cr(p_, s_), s_))
    t3o, t3i, t3a = split('pi05', 'T3')
    c3o, c3i, _ = split('scripted', 'T3')
    t2o, t2i, t2a = split('pi05', 'T2')
    want = (f"hold {n_out} of the {len(behind)} tabletop cells behind the rates, {t3o[1]} of π0.5's {t3a[1]} scored T3 carries and {t2o[1]} of its "
            f'{t2a[1]} pooled T2 episodes')
    check(want in bcap, f'App. B.2 (cameras): {want}', f'App. B.2 (what the cameras show) should read "{want}" (cells.csv, placements at [0 %] in Table B.2)')
    none_ = not any(is_out(x) and (x['role'].startswith('prereg') or I(x['T6a_scored']) or I(x['T6b_scored'])) for x in C.rows)
    check(none_ == ('they hold none of the pre-registered serving cell, T6a or T6b' in bcap),
          'App. B.2 (cameras): the two placements hold no pre-registered serving cell and no T6a or T6b count',
          f'App. B.2: "they hold none of the pre-registered serving cell, T6a or T6b" vs cells.csv (none: {none_})')
    surf_out = sorted({x[0] for x in outv})
    want = f"no policy camera shows it ({pyround(100 * t3o[1] / t3a[1]) if t3a[1] else '?'}% of π0.5's T3 carries)"
    check(len(surf_out) == 2 and 'at two of the five surfaces ' + want in secs['discussion'], f'discussion: at two of the five surfaces {want}',
          f'discussion should read "at two of the five surfaces {want}" ({frac(t3o[1], t3a[1])}; surfaces {surf_out})')
    pair_ = 'the ' + ' and the '.join(sorted(surf_out, key=lambda z: z != 'kitchen counter'))
    check(len(surf_out) == 2 and all(pair_ in secs[n_] for n_ in ('benchmark', 'app_b_setup', 'app_d_results')),
          f'Sec. 4.1, App. B.2 and App. D.3 name the two surfaces ({pair_})',
          f'the surfaces with [0 %] in Table B.2 are {surf_out}; Sec. 4.1, App. B.2 or App. D.3 does not say "{pair_}"')
    dres = secs['app_d_results']
    want = (f'π0.5 reads {frac(*t3o)} and the control {frac(*c3o)}; at the placements where the bystander is in the external frame, '
            f'{frac(*t3i)} against {frac(*c3i)}')
    check(want in dres, f'App. D.3 by camera view: {want}', f'App. D.3 should read "{want}" (cells.csv)')
    t2_surf = {x['work_surface'] for x in C.cr('pi05', 'T2') if is_out(x)}
    want = f'At the kitchen counter, where no camera shows the bystander ({frac(*t2o)};'
    check(t2_surf == {'kitchen counter'} and want in dres, f'App. D.2: {want}', f'App. D.2 should read "{want}" (cells.csv; surfaces {sorted(t2_surf)})')
    # the same facts in supp/README.md ("What the policy cameras show")
    fnum = lambda t: float(t.replace('−', '-').replace('–', '-'))
    shares_md = {(mm.group(1), fnum(mm.group(2)), fnum(mm.group(3))): int(mm.group(4))
                 for mm in re.finditer(r'\| ([a-z ]+?) \| \(([−–\-\d.]+), ([−–\-\d.]+)\) \| (\d+) %', rd)}
    check(len(shares_md) >= 9 and shares_md == shares_tex, f'README: the {len(shares_md)} shares in the external frame are those of Table B.2',
          f'README: shares in the external frame {sorted(shares_md.items())} differ from the brackets of Table B.2 {sorted(shares_tex.items())}')
    want = f'{n_out} of the {len(behind)} rows with `role` `scored` or `prereg_serving`'
    check(want in rdf, f'README (cameras): {want}', f'README (cameras) should read "{want}" (cells.csv)')
    want = (f"They hold {t3o[1]} of π0.5's {t3a[1]} scored T3 carries ({frac(*t3o)} against {frac(*t3i)} on the other placements; the control "
            f'{frac(*c3o)} against {frac(*c3i)}) and {t2o[1]} of its {t2a[1]} pooled T2 episodes ({frac(*t2o)})')
    check(want in rdf, f'README (cameras): {want}', f'README (cameras) should read "{want}" (cells.csv)')
    fn_ = table_numbers('figure')
    mfig = re.search(r'\(Fig\. (\S+?) of the paper\)', rdf)
    check(bool(mfig) and mfig.group(1) == fn_.get('figB:view'), f'README: the camera frames are Fig. {fn_.get("figB:view")} (figB:view)',
          f'README calls the figure of the camera frames "Fig. {mfig.group(1) if mfig else "?"}"; in the paper figB:view is Fig. {fn_.get("figB:view")}')
    mcam = [re.search(r'(\d\.\d+) m to its left and (\d\.\d+) m up', t_) for t_ in (bcap, rdf)]
    check(all(mcam) and mcam[0].groups() == mcam[1].groups(), 'README and App. B.2 give the same camera position',
          f'camera position: App. B.2 {mcam[0].groups() if mcam[0] else "?"} vs README {mcam[1].groups() if mcam[1] else "?"}')

    # 6l. revision v2.2: numbers that the prose now derives from the tables
    b5 = C.behind('pi05')
    dlv = [(C.tot([x for x in b5 if x['goal'] == g_], 'delivered'), C.tot([x for x in b5 if x['goal'] == g_], 'episodes'))
           for g_ in ('pour', 'put away in a drawer')]
    pcs = sorted(pyround(100 * k_ / n_) for k_, n_ in dlv)
    want = f'is rarely delivered ({pcs[0]}–{pcs[-1]} % of attempts'
    check(want in secs['definition'], f'Sec. 3.3: the second goal {want} (pour {frac(*dlv[0])}, drawer {frac(*dlv[1])})',
          f'Sec. 3.3 should read "{want}" (cells.csv: pour {frac(*dlv[0])}, drawer {frac(*dlv[1])}; Table D.1, last line)')
    t6 = [int(val(p_, 'T6a')) for p_ in POLS if val(p_, 'T6a').isdigit()]
    want = f'into the crossing hand on most carries ({min(t6)}–{max(t6)}%)' if len(t6) == 4 else '?'
    check(want in r, f'results: all four carry {want}', f'results should read "{want}" (Table 3, T6a column: {t6})')
    if C.fr:
        comp = {}
        for s_ in SUBS:
            f_ = {'T3': 't3_ok_done', 'T4': 't4_ok_done', 'T6b': 't6b_ok_done'}.get(s_)
            comp[s_] = (sum(C.fr[x['label']].get(f_) or 0 for x in C.W[s_]) if f_ else C.tot(C.W[s_], 'delivered'), C.tot(C.W[s_], 'episodes'))
        lo_ = min(SUBS, key=lambda s_: comp[s_][0] / comp[s_][1])
        hi_ = max(SUBS, key=lambda s_: comp[s_][0] / comp[s_][1])
        m = re.search(r'delivers without a violation on at least (\w+) attempts, from (\d+) of (\d+) \((T\w+)\) to (\d+) of (\d+) \((T\w+);', r)
        check(bool(m) and WORDNUM.get(m.group(1)) == min(c_[0] for c_ in comp.values())
              and (int(m.group(2)), int(m.group(3)), m.group(4)) == (comp[lo_][0], comp[lo_][1], lo_)
              and (int(m.group(5)), int(m.group(6)), m.group(7)) == (comp[hi_][0], comp[hi_][1], hi_),
              f'results: each witness delivers without a violation on at least {min(c_[0] for c_ in comp.values())} attempts, from {frac(*comp[lo_])} ({lo_}) '
              f'to {frac(*comp[hi_])} ({hi_})',
              f'results: "{m.group(0) if m else "?"}" vs the witnesses\' compliant deliveries {comp} (cells.csv, fr_summary.json; Table B.4, last column)')
        # the handover: scissors and fork carries with the hazardous end toward the receiving hand (fr_summary.json)
        ho = defaultdict(lambda: [0, 0, 0, 0, 0])
        for l_, v_ in C.fr.items():
            mm = re.fullmatch(r'(ho|how|hr)_(mug|sci|fork)_s\d+', l_)
            if mm and isinstance(v_, dict):
                for key_ in (('all',), ('mug',) if mm.group(2) == 'mug' else ('pointed',), (mm.group(1), mm.group(2) != 'mug')):
                    for i_, f_ in enumerate(('N', 'carried', 'completed', 'ho_n', 'ho_90')):
                        ho[key_][i_] += v_.get(f_) or 0
        al_, pt_ = ho[('all',)], ho[('pointed',)]
        byv = [frac(ho[(v_, True)][4], ho[(v_, True)][3]) for v_ in ('ho', 'hr', 'how')]   # reaching, parked away, withdrawing
        if al_[0]:
            want = f'it completes {al_[2]} of {al_[0]} attempts, with the hazardous end toward the receiving hand on {pt_[4]} of its {pt_[3]} scissors and fork carries'
            check(want in r, f'results: handover, {want}', f'results should read "{want}" (fr_summary.json, ho_/how_/hr_ cells)')
            want = (f'Of its {al_[1]} carries, {pt_[3]} are of scissors or a fork; on these the hazardous end faces the receiving hand on {pt_[4]} '
                    f'({pyround(100 * pt_[4] / pt_[3])} %; {byv[0]}, {byv[1]} and {byv[2]} by variant). The other {ho[("mug",)][1]} carry a mug')
            check(want in dres, f'App. D.3: handover, {want}', f'App. D.3 should read "{want}" (fr_summary.json, ho_/how_/hr_ cells)')
            want = f'on its {pt_[3]} scissors and fork carries the hazardous end faces the receiving hand on {pt_[4]} ({pyround(100 * pt_[4] / pt_[3])} %)'
            check(want in a, f'App. A.3: handover, {want}', f'App. A.3 should read "{want}" (fr_summary.json)')
    # tabletop T5a on the still-person envelope: the range quoted in Sec. 5.2 against the v_h = 0 row of the T5 table
    row0 = next((cells_ for ln_, raw_, cells_ in table_rows(os.path.join(V2, 'sections', 'app_d_results.tex'), 'tabD:t5')
                 if 'v_h=0' in raw_ and 'd_0=0.30' in raw_), None)
    fr0 = [re.fullmatch(r'(\d+)/(\d+)', cellplain(c_)) for c_ in (row0[1:6] if row0 else [])]
    if fr0 and all(fr0):
        p0 = [pyround(100 * int(x.group(1)) / int(x.group(2))) for x in fr0]
        want = f'the grey tabletop cells would read {min(p0)}–{max(p0)}%'
        check(want in r, f'results: on the still-person envelope {want}', f'results should read "{want}" (the v_h = 0 row of the T5 table: {[x.group(0) for x in fr0]})')
    else:
        issues.append('the v_h = 0 row of the T5 table (tabD:t5) was not found, so "0–1%" in Sec. 5.2 is unchecked')
    # light maps: the relit cells of Sec. 4.1 and the cells of the same placements under the surfaces' default maps
    relit3 = [x for x in C.sc if x['policy'] == 'pi05' and x['environment'] in ('industrial auto shop', 'outdoor courtyard', 'domestic lounge')
              and x['work_surface'] in ('kitchen counter', 'packing station')]
    pk_ = lambda x: tuple(x[c_] for c_ in PKEY if c_ not in ('environment', 'task'))
    keys_ = {pk_(x) for x in relit3}
    ref3 = [x for x in C.sc if x['policy'] == 'pi05' and x['environment'] in ('scene default', 'industrial warehouse')
            and x['task'] == 'pick-and-place, person at the table' and pk_(x) in keys_]
    want = (f'give π0.5 {frac(*C.kn(relit3, "T3"))} on T3 (default maps, same placement: {frac(*C.kn(ref3, "T3"))}) and {frac(*C.kn(relit3, "T4"))} on T4 '
            f'({frac(*C.kn(ref3, "T4"))})')
    check(want in secs['benchmark'], f'Sec. 4.1 light maps: {want}', f'Sec. 4.1 should read "{want}" (cells.csv: {len(relit3)} relit cells, {len(ref3)} default-map cells)')
    check(f'the {len(relit3)} under the first three maps at the kitchen counter and packing station' in bcap, f'App. B.2: {len(relit3)} cells under the first three maps',
          f'App. B.2 should read "the {len(relit3)} under the first three maps at the kitchen counter and packing station"')
    npp_ = len([x for x in C.sc if x['goal'] == PP])
    only_ = [p_ for p_ in POLS if all(x['goal'] == PP for x in C.sc if x['policy'] == p_)]
    want = f'Pick-and-place is the goal of {pyround(100 * npp_ / len(C.sc))}% of scored cells and the only one for π0 and GR00T-DROID'
    check(only_ == ['pi0', 'gr00t_droid'] and want in secs['discussion'], f'discussion: {want}', f'discussion should read "{want}" ({npp_}/{len(C.sc)}; only goal for {only_})')
    dyn_ = {x['work_surface'] for x in C.rows if I(x['T6a_scored']) or I(x['T6b_scored'])}
    check(('Dynamics is not scored at the packing station or the drawer kitchen' in secs['discussion']) == (not dyn_ & {'packing station', 'drawer kitchen'}),
          'discussion: Dynamics is not scored at the packing station or the drawer kitchen', f'discussion: Dynamics is scored at {sorted(dyn_)}')
    # episode lengths other than 35 s
    s20 = [x for x in C.rows if x['episode_length_s'] == '20']
    want = f'20 s for {numword.get(len(s20), len(s20))} π0 serving cells'
    check(all(x['policy'] == 'pi0' and 'serving' in x['task'] for x in s20) and want in secs['statements'], f'statements: {want}',
          f'statements should read "{want}" (cells.csv, episode_length_s = 20)')
    g14 = [x for x in C.sc if x['policy'] == 'gr00t_droid' and any(x[s_ + '_scored'] != '' for s_ in ('T1', 'T2', 'T3', 'T4'))]
    g35 = [x for x in g14 if x['episode_length_s'] != '90']
    want = f'the exception, a T3 cell, holds {C.tot(g35, "T3_scored")} of its {C.kn(C.cr("gr00t_droid", "T3"), "T3")[1]} scored T3 carries'
    check(len(g35) == 1 and want in cst, f'App. C.6: all but one of GR00T-DROID\'s T1–T4 cells ran 90 s; {want}',
          f'App. C.6 should read "{want}" (cells.csv: {len(g35)} of {len(g14)} T1–T4 cells not at 90 s)')
    # App. C.2: the centre of the interval and the relabelling counts
    g3 = C.matched('gr00t_droid', 'T3', C.cr('scripted', 'T3'))
    sgn_ = lambda x: ('+' if x >= 0 else '-') + str(abs(x))
    n45_ = load_n45().get('null_rel', {})
    if g3[0][1] and g3[1][1] and n45_:
        want = f"for GR00T-DROID's T3 it is {sgn_(pyround(100 * (g3[0][0] / g3[0][1] - g3[1][0] / g3[1][1])))} against {sgn_(n45_['gr00t_droid']['T3']['rd'])}"
        check(want in cst, f'App. C.2: pooled difference against the Mantel-Haenszel estimate, {want}',
              f'App. C.2 should read "{want}" (cells.csv {frac(*g3[0])} vs {frac(*g3[1])}; N45 null_rel)')
    nrel = {(p_, s_): C.relabellings(p_, s_, C.cr('scripted', s_)) for p_, s_, _, _, _ in mc}
    big = sorted(k_ for k_, v_ in nrel.items() if v_ > 20000)
    check(big == sorted([('pi05', 'T1'), ('pi0', 'T1'), ('pi0fast', 'T1'), ('pi05', 'T3')])
          and "4,000 draws for the T1 rows of π0.5, π0 and π0-FAST and for π0.5's T3 row" in cst,
          'App. C.2: the Monte Carlo rows of Table C.3 are those above 20,000 relabellings',
          f'App. C.2 names the T1 rows of π0.5, π0 and π0-FAST and π0.5\'s T3 row as Monte Carlo; above 20,000 relabellings are {big} (cells.csv)')
    bigj = sorted(p_ for p_ in POLS if C.relabellings(p_, 'T1', C.js) > 20000)
    check(bigj == sorted(['pi05', 'pi0', 'pi0fast']) and '20,000 for π0.5, π0 and π0-FAST in Table' in cst,
          'App. C.2: the Monte Carlo rows of Table C.6 are those above 20,000 relabellings',
          f'App. C.2 names π0.5, π0 and π0-FAST as the Monte Carlo rows of Table C.6; above 20,000 relabellings are {bigj} (cells.csv)')
    want = f"Enumerating π0-FAST's {nrel.get(('pi0fast', 'T1'), 0):,} T1 relabellings"
    check(want in cst, f'App. C.2: {want}', f'App. C.2 should read "{want}" (cells.csv, cells per shared placement)')

    # 8. counts of Holm families (prose claim vs enumeration)
    m = re.search(r'(\w+) families are Holm-corrected', cst)
    if m:
        listed = sum(1 for pat in (r'primary family', r'H1–H2', r'H3–H4', r'against the joint-space control form',
                                   r'P-D and P-E a') if re.search(pat, cst))
        num = WORDNUM.get(m.group(1).lower())
        check(num == listed, f'Holm families: {m.group(1).lower()} == {listed}',
              f'App. C says "{m.group(1)} families are Holm-corrected" but enumerates {listed}')
        mb = re.search(r'within each of (\w+) (?:pre-defined )?test families', secs['benchmark'])
        check(bool(mb) and WORDNUM.get(mb.group(1)) == num, 'Sec. 4.2 names the same number of Holm families as App. C',
              f'Sec. 4.2 says "{mb.group(0) if mb else "?"}" but App. C has {num}')
    return ok, issues


def wording_counts(C):
    """Pooled counts of the three prompt experiments for pi0.5, from fr_summary.json (None when it is absent)."""
    fr = C.fr
    if not fr:
        return None
    def arm(pred):
        ks = [k for k in fr if pred(k)]
        return (sum(fr[k].get('t45') or 0 for k in ks), sum(len(fr[k].get('tilt_trans') or []) for k in ks),
                sum(fr[k].get('completed') or 0 for k in ks), sum(fr[k].get('N') or 0 for k in ks))
    pd = lambda i: (lambda k: re.fullmatch(rf'pd_(din|off)_{i}_s\d+', k) is not None)
    pv = lambda c: (lambda k: re.fullmatch(rf'pv_(din|off)_{c}_s\d+', k) is not None)
    spill = [arm(pd(3)), arm(pd(5)), arm(pv('C')), arm(pv('D')), arm(pv('F')), arm(lambda k: k.startswith('hotchk_') and 'hot' in k[7:])]
    neutral = [arm(pd(0)), arm(pv('A')), arm(lambda k: k.startswith('hotchk_') and 'neu' in k[7:])]
    a3, a0 = arm(pd(3)), arm(pd(0))
    out = {'spill': (sum(x[0] for x in spill), sum(x[1] for x in spill)),
           'neutral': (sum(x[0] for x in neutral), sum(x[1] for x in neutral)),
           'arm3': a3[:2], 'deliv0': a0[2:], 'deliv3': a3[2:]}
    return out if out['spill'][1] and out['neutral'][1] and a3[1] and a0[3] and a3[3] else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--show', default='missing', choices=['found', 'weak', 'missing', 'open', 'adj', 'wrong', 'unsourced', 'all', 'none'])
    ap.add_argument('--file', default='')
    ap.add_argument('--kind', default='')
    ap.add_argument('--no-consistency', action='store_true')
    ap.add_argument('--no-extra', action='store_true', help='ignore the facts and adjudications of the extra directories')
    ap.add_argument('--extra-dir', action='append', default=None, help='an extra directory (repeatable); default: ' + ', '.join(EXTRA_DIRS))
    ap.add_argument('--readme', action='store_true', help='also read the tokens of supp/README.md')
    ap.add_argument('--dump', default='', help='write every token with its status to this JSON file')
    args = ap.parse_args()
    try:                                                       # the report holds π, ≥ and –; a GBK console cannot print them
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    extra = [] if args.no_extra else (args.extra_dir or EXTRA_DIRS)
    C = Cells()
    V = struct_verify(C)
    adj = load_adjudications(extra)
    if args.show != 'none' or args.dump:
        sources = load_sources(extra)
        rows = main_pass(args, sources, V, adj)
        if args.show != 'none':
            print_rows(rows, args.show, args.kind, adj)
        if args.dump:
            with open(args.dump, 'w', encoding='utf-8') as f:
                json.dump([{'file': r[0], 'line': r[1], 'kind': r[2], 'token': r[3], 'status': r[4],
                            'source': r[5][1] if r[5] else '', 'overlap': r[5][0] if r[5] else 0,
                            'src_ctx': r[5][3][200:330] if r[5] else '', 'ctx': r[6], 'key': r[7]} for r in rows],
                          f, ensure_ascii=False, indent=1)
    if not args.no_consistency:
        ok, issues = consistency(C, V)
        print(f'\nConsistency: {len(ok)} checks passed, {len(issues)} flagged')
        for i in issues:
            print('  FLAG', i)


if __name__ == '__main__':
    main()

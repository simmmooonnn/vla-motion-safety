#!/usr/bin/env python
"""Adversarial number check for paper v2.

Extracts every numeric claim token from docs/paper_v2/sections/*.tex and docs/paper_v2/tables/*.tex
(fractions k/n, percentages, p-values, decimals with units, intervals, signed differences, ranges, counts)
and looks each one up in the three fact sources:

  * _scratch/tmp/v2/facts.md            (curated facts sheet)
  * _scratch/tmp/v2/table_facts.json    (per-cell table provenance)
  * _scratch/tmp/v2/v1_fulltext.txt     (v1 PDF text, 122 pages)

A token is FOUND when the same token occurs in a source and the source context shares enough content words
with the v2 context; WEAK when it occurs only in an unrelated context; MISSING when it occurs nowhere.
MISSING and WEAK tokens must be adjudicated by hand (derived / rounding / wrong).

A second pass checks internal consistency: Table 2 vs the counts table vs the App. D heatmap vs App. E table,
percentages vs their k/n, dimension scores vs the exact sub-type rates, and the headline numbers in the
abstract / intro / Sec. 5 / figure text against Table 2.

Usage:  PYTHONIOENCODING=utf-8 python _scratch/check_v2_numbers.py [--show found|weak|missing|all]
                                                                  [--file SUBSTR] [--kind KIND] [--no-consistency]
Read-only: it writes nothing.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, 'docs', 'paper_v2')
SRC_DIRS = [os.path.join(V2, 'sections'), os.path.join(V2, 'tables')]
FACTS_MD = os.path.join(ROOT, '_scratch', 'tmp', 'v2', 'facts.md')
FACTS_JSON = os.path.join(ROOT, '_scratch', 'tmp', 'v2', 'table_facts.json')
V1_TXT = os.path.join(ROOT, '_scratch', 'tmp', 'v2', 'v1_fulltext.txt')
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


def clean_line(line):
    s = re.sub(r'(?<!\\)%.*$', '', line)                     # comments
    if re.match(r'\s*\\(providecommand|newcommand|providecolor|newenvironment|renewcommand)\b', s):
        return ''
    # layout commands whose numeric args are not claims
    for cmd, n in [('setlength', 2), ('renewcommand', 2), ('setcounter', 2), ('includegraphics', 1),
                   ('hspace', 1), ('vspace', 1), ('cmidrule', 1), ('addlinespace', 0), ('makebox', 0),
                   ('label', 1), ('ref', 1), ('citep', 1), ('citet', 1), ('cite', 1), ('input', 1),
                   ('cellcolor', 1), ('columncolor', 1), ('rowcolor', 1), ('multirow', 2), ('hangindent', 0),
                   ('heavyrulewidth', 0), ('linewidth', 0), ('nolinkurl', 1), ('texttt', 1), ('begin', 1),
                   ('end', 1), ('rule', 2), ('raisebox', 1), ('phantom', 1)]:
        s = remove_cmd_with_args(s, cmd, n)
    s = re.sub(r'\\multicolumn\{\d+\}\{[^}]*\}', ' ', s)
    s = re.sub(r'>\{[^}]*\}p\{[^}]*\}', ' ', s)
    s = re.sub(r'\bp\{[\d.]+cm\}', ' ', s)
    s = re.sub(r'\\\\\[[^\]]*\]', ' ', s)                   # \\[-1pt]
    s = re.sub(r'\[(?:-?\d+(?:\.\d+)?(?:pt|em|ex|cm|mm|in))\]', ' ', s)
    s = re.sub(r'-?\d+(?:\.\d+)?(?:pt|em|ex|cm(?=[^\w])|in\b|mm)\b', ' ', s) if 'tabcolsep' in s or 'width' in s else s
    s = re.sub(r'(?:black|gray|heatc|dtraj|dorient|dsf|ddyn|blue|red)!\d+', ' ', s)
    s = re.sub(r'\\numexpr[^\\]*\\relax', ' ', s)
    s = re.sub(r'trim=[\d ]+', ' ', s)
    # math and symbols
    s = s.replace('\\%', '%').replace('\\,', ' ').replace('~', ' ').replace('\\ ', ' ')
    s = s.replace('\\times', '×').replace('{\\times}', '×').replace('\\approx', '≈').replace('{\\approx}', '≈')
    s = s.replace('\\le', '≤').replace('\\geq', '≥').replace('\\ge', '≥').replace('{\\le}', '≤')
    s = s.replace('^{\\circ}', '°').replace('^\\circ', '°').replace('$^\\circ$', '°')
    s = s.replace('\\rightarrow', '→')
    s = re.sub(r'10\^\{(-?\d+)\}', r'10^\1', s)
    s = s.replace('$', '')
    s = s.replace('{[}', '[').replace('{]}', ']')
    s = s.replace('---', '—').replace('--', '–')
    s = re.sub(r'\\[A-Za-z]+\*?', ' ', s)                  # remaining command names
    s = s.replace('{', ' ').replace('}', ' ').replace('&', ' | ')
    s = re.sub(r'(?<=\d) +(?=\d{3}\b)', ',', s) if False else s
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


# identifiers that look like numbers but are not claims
NONCLAIM = [
    r'\bT[1-6][ab]?\b', r'\bT5[sc]\b', r'\bH[1-5]\b', r'\bP-?[1-3A-E]\b', r'\bF[1-4]\b',
    r'\bN1\.[67](?:-DROID|-3B)?\b', r'\bISO(?:/TS)? ?\d+(?:-\d)?(?:/-\d)?(?::\d{4})?\b', r'\b15066(?::2016)?\b',
    r'\b10218-[12](?:/-2)?(?::2025)?\b', r'\b13855\b', r'\b13482\b', r'\bclause \d\.\d\.\d\b', r'\b5\.5\.[45]\b',
    r'\bRT-2\b', r'\bHabitat 3\.0\b', r'\bRTX PRO 6000\b', r'\bv2\b', r'\bpi0\w*', r'\bpi05\w*', r'\bGR00T\b',
    r'\b67--101\b', r'π0(?:\.5)?(?:-FAST)?', r'\bG1\b', r'\(G1\)',
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
    ('pval', re.compile(r'\bp\s*(?:=|<|≤|≈)\s*(\d+(?:\.\d+)?(?:\s*×\s*10\^-?\d+)?)')),
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
    t = re.sub(r'\s*/\s*', '/', t)
    t = re.sub(r'(\d)\s+%', r'\1%', t)
    t = re.sub(r'\[\s*', '[', t)
    t = re.sub(r'\s*\]', ']', t)
    t = re.sub(r',\s+', ', ', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t


def load_sources():
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
    return {'facts': norm_src(facts.replace('\n', ' ')), 'tjson': norm_src(tj_txt.replace('\n', ' ')),
            'v1': norm_src(v1)}


KEYS = [
    ('POL:pi05', r'π0\.5|π_?\{?0\.5|pi0\.5|pi05|\\pifive'),
    ('POL:pi0fast', r'π0-FAST|pi0-FAST|π0 -FAST|\\pifast|pi0fast'),
    ('POL:pi0', r'π0(?![.\-\d]| -FAST)|\\pizero|pi0(?![.\-\dfa_])'),
    ('POL:groot', r'GR00T[- ]N1\.6-DROID|GR00T-DROID|\\grd|\\grfull|gr00t_droid'),
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
    if 'ID:T6' in w and ('ID:T6a' in w):
        pass
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
            v |= {f'{a}–{b}%', f'{a}-{b}%', f'{a}–{b} %', f'{a} to {b}%'}
        else:
            v |= {f'{a}%', f'{a} %', f'({a})', f'{a} per cent'}
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


def src_words(sname, src, pos):
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
                ctx = src[max(0, pos - 260):pos + 260]
                ov = len(ctx_words & src_words(sname, src, pos))
                cand = (ov, sname, var, ctx)
                if best is None or ov > best[0]:
                    best = cand
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


# ------------------------------------------------------------------------------------------------ main pass
def iter_files():
    for d in SRC_DIRS:
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.tex') and not fn.startswith('_'):
                yield os.path.join(d, fn)


def main_pass(args, sources):
    rows = []
    for path in iter_files():
        rel = os.path.relpath(path, V2).replace('\\', '/')
        if args.file and args.file not in rel:
            continue
        with open(path, encoding='utf-8') as f:
            lines = f.read().split('\n')
        for ln, raw in enumerate(lines, 1):
            s = clean_line(expand_macros(raw))
            if not s:
                continue
            is_row = '|' in s
            for kind, txt, a, b in tokenize(s):
                if kind == 'num':
                    val = float(txt.replace(',', ''))
                    if val == 0 and '.' not in txt:
                        continue
                ctx = s[max(0, a - 90):b + 90]
                cw = words(ctx)
                if is_row:      # table row: the row label and the whole row are the context
                    cw |= words(s.split('|')[0]) | words(s)
                best = lookup(kind, txt, cw, sources)
                st = classify(kind, txt, best)
                rows.append((rel, ln, kind, txt, st, best, ctx))
    return rows


def print_rows(rows, show, kind_filter):
    cnt = Counter()
    for rel, ln, kind, txt, st, best, ctx in rows:
        cnt[(st, kind)] += 1
        if show != 'all' and st.lower() != show:
            continue
        if kind_filter and kind != kind_filter:
            continue
        src = f'{best[1]} ov={best[0]} "{best[2]}"' if best else '-'
        snippet = best[3][200:330].replace('\n', ' ') if best else ''
        print(f'{st:7s} {rel}:{ln} [{kind}] {txt!r}  <- {src}')
        print(f'        v2: …{ctx}…')
        if best and st != 'FOUND':
            print(f'        src: …{snippet}…')
    print('\nSummary (status, kind): count')
    for (st, kind), c in sorted(cnt.items()):
        print(f'  {st:7s} {kind:6s} {c}')
    tot = Counter(st for (st, _), c in cnt.items() for _ in range(c))
    print('  totals:', dict(tot))


# ------------------------------------------------------------------------------------------------ consistency
def pyround(x):
    return int(round(x))


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def parse_tab_main():
    """Return {row: {col: value}} from tables/tab_main.tex."""
    cols = ['Carry', 'DimTraj', 'T1', 'T2', 'DimOrient', 'T3', 'T4', 'T5a', 'DimDyn', 'T6a', 'T6b']
    rows = {}
    for raw in read(os.path.join(V2, 'tables', 'tab_main.tex')).split('\n'):
        if '&' not in raw or raw.strip().startswith('%') or 'multicolumn' in raw and 'Trajectory' in raw:
            continue
        cells = [c.strip() for c in raw.rstrip('\\ ').split('&')]
        if len(cells) != 12:
            continue
        name = re.sub(r'\\rlap\{[^}]*\}|\\quad|\\textit|[{}$^]|\\mathrm', '', cells[0]).strip()
        name = {'\\pifive': 'pi05', '\\pizero': 'pi0', '\\pifast': 'pi0fast', '\\grfull': 'gr00t_droid',
                '\\gone': 'g1', 'Cartesian': 'scripted', 'joint-space\\dagger': 'js', 'joint-space': 'js',
                'Feasibility witness\\mathrmw': 'wit'}.get(name, name)
        if 'witness' in name.lower():
            name = 'wit'
        if name.startswith('joint'):
            name = 'js'
        vals = {}
        for c, cell in zip(cols, cells[1:]):
            m = re.search(r'\\(?:heat|ex|dimc)\{(\d+|---|\\nlow)\}', cell)
            if m:
                vals[c] = m.group(1)
            else:
                m2 = re.match(r'\s*(\d+|---|\\nlow)', cell)
                vals[c] = m2.group(1) if m2 else ''
        rows[name] = vals
    return rows


def parse_tab_counts():
    cols = ['Carry', 'T1', 'T2', 'T2pool', 'T3', 'T4', 'T5a', 'T6a', 'T6b']
    rows = {}
    for raw in read(os.path.join(V2, 'tables', 'tab_counts.tex')).split('\n'):
        if '&' not in raw or 'makecell' not in raw and 'Carry' not in raw:
            continue
        cells = [c.strip() for c in raw.rstrip('\\ ').split('&')]
        if len(cells) != 10:
            continue
        name = cells[0]
        key = None
        for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grfull', 'gr00t_droid'),
                       ('gone', 'g1'), ('Cartesian', 'scripted'), ('joint-space', 'js'), ('witness', 'wit')]:
            if pat in name:
                key = k
        if not key:
            continue
        vals = {}
        for c, cell in zip(cols, cells[1:]):
            m = re.search(r'(\d[\d,]*)/(\d[\d,]*)', cell)
            if m:
                k, n = int(m.group(1).replace(',', '')), int(m.group(2).replace(',', ''))
                pm = re.findall(r'\\\\\s*(?:\\textcolor\{black!50\}\{)?(\d+|\\nlow)', cell)
                vals[c] = (k, n, pm[0] if pm else None)
        rows[key] = vals
    return rows


def parse_heatmap():
    txt = read(os.path.join(V2, 'sections', 'app_d_results.tex'))
    body = txt[txt.index('\\begin{tabular}'):txt.index('\\end{tabular}')]
    body = body.replace('\n', ' ')
    cols = ['T1', 'T2', 'T2pool', 'T3', 'T4', 'T5a', 'T5b', 'T6a', 'T6b']
    rows = {}
    for chunk in body.split('\\\\'):
        if '\\dH' not in chunk and '\\dEx' not in chunk and '\\dNl' not in chunk:
            continue
        cells = [c.strip() for c in chunk.split('&')]
        name = cells[0]
        key = None
        for pat, k in [('pifive', 'pi05'), ('pizero', 'pi0'), ('pifast', 'pi0fast'), ('grfull', 'gr00t_droid'),
                       ('gone', 'g1'), ('Cartesian', 'scripted'), ('Joint-space', 'js'), ('witness', 'wit')]:
            if pat in name:
                key = k
        if not key:
            continue
        vals = {}
        for c, cell in zip(cols, cells[1:]):
            m = re.search(r'\\d(?:Ht|Hs|Ex)\{(\d+|exp\.)\}\{(\d+)/(\d+)\}', cell)
            m2 = re.search(r'\\dNl\{(\d+)/(\d+)\}', cell)
            if m:
                vals[c] = (int(m.group(2)), int(m.group(3)), m.group(1))
            elif m2:
                vals[c] = (int(m2.group(1)), int(m2.group(2)), 'n<8')
        rows[key] = vals
    return rows


def plain(path):
    return ' '.join(clean_line(l) for l in read(path).split('\n'))


def fig_text(name):
    try:
        out = subprocess.run(['pdftotext', '-layout', os.path.join(FIG_DIR, name), '-'], capture_output=True,
                             text=True, encoding='utf-8', errors='replace').stdout
    except Exception:
        out = ''
    return re.sub(r'\s+', ' ', out)


def consistency():
    issues = []
    ok = []

    def check(cond, msg_ok, msg_bad):
        (ok if cond else issues).append(msg_ok if cond else msg_bad)

    tm = parse_tab_main()
    tc = parse_tab_counts()
    hm = parse_heatmap()
    with open(FACTS_JSON, encoding='utf-8') as f:
        tf = json.load(f)['facts']

    # 1. every k/n in the counts table and heatmap prints round(100k/n) (Python half-even)
    for tabname, tab in (('tabC:counts', tc), ('figD:heatmap', hm)):
        for row, vals in tab.items():
            for col, (k, n, p) in vals.items():
                if p in (None, 'exp.', '\\nlow', 'n<8'):
                    if p in ('\\nlow', 'n<8'):
                        check(n < 8, f'{tabname} {row} {col}: n<8 for {k}/{n}', f'{tabname} {row} {col}: n<8 printed but n={n}')
                    continue
                exp = pyround(100 * k / n)
                check(str(exp) == str(p), f'{tabname} {row} {col}: {k}/{n} -> {p}',
                      f'{tabname} {row} {col}: {k}/{n} = {100*k/n:.2f} % but printed {p}')

    # 2. Table 2 vs counts table vs heatmap vs table_facts
    colmap = {'Carry': 'Carry', 'T1': 'T1', 'T2': 'T2', 'T3': 'T3', 'T4': 'T4', 'T5a': 'T5a', 'T6a': 'T6a', 'T6b': 'T6b'}
    for row, vals in tm.items():
        for col in colmap:
            v = vals.get(col)
            if v in (None, '', '---'):
                continue
            if row in tc and col in tc[row]:
                k, n, p = tc[row][col]
                pv = 'n<8' if v == '\\nlow' else v
                pc = 'n<8' if p == '\\nlow' else p
                check(pv == pc, f'Table 2 {row} {col} {v} == counts {k}/{n}',
                      f'Table 2 {row} {col} prints {v} but tabC:counts prints {k}/{n} -> {p}')
            hcol = {'T6a': 'T6a'}.get(col, col)
            if row in hm and hcol in hm[row] and col != 'Carry':
                k, n, p = hm[row][hcol]
                pv = 'n<8' if v == '\\nlow' else v
                check(pv == p, f'Table 2 {row} {col} == heatmap {k}/{n}',
                      f'Table 2 {row} {col} prints {v} but heatmap prints {p} ({k}/{n})')
            tfk = f'tab_main:{row}:{"T6" if col == "T6a" else col}'
            if tfk in tf:
                tv = str(tf[tfk]['value'])
                pv = 'n<8' if v == '\\nlow' else v
                check(pv == tv, f'Table 2 {row} {col} == table_facts {tv}',
                      f'Table 2 {row} {col} prints {v} but table_facts says {tv}')

    # 3. dimension scores = mean of exact sub-type rates, n>=8 rule
    dims = {'DimTraj': ('T1', 'T2'), 'DimOrient': ('T3', 'T4'), 'DimDyn': ('T6a', 'T6b')}
    for row, vals in tm.items():
        src = tc.get(row, {})
        for d, (a, b) in dims.items():
            v = vals.get(d)
            if v in (None, '', '---'):
                continue
            if a in src and b in src:
                ka, na, _ = src[a]
                kb, nb, _ = src[b]
                if min(na, nb) < 8:
                    check(v == '\\nlow', f'{row} {d} n<8', f'{row} {d} printed {v} but a member has n<8')
                else:
                    exp = pyround(50 * (ka / na + kb / nb))
                    check(v == str(exp), f'{row} {d} = {exp}',
                          f'{row} {d} printed {v}, mean of {ka}/{na} and {kb}/{nb} = {50*(ka/na+kb/nb):.2f}')

    # 4. App. E G1 table vs Table 2 G1 row
    e = plain(os.path.join(V2, 'sections', 'app_e_humanoid.tex'))
    for col, kn in [('T1', '11/30'), ('T2', '27/32'), ('T3', '14/27'), ('T4', '0/17'), ('T5a', '22/22'),
                    ('T6a', '21/24'), ('T6b', '17/18')]:
        k, n = map(int, kn.split('/'))
        check(kn in e and tm['g1'][col] == str(pyround(100 * k / n)), f'G1 {col} {kn} in App. E and Table 2',
              f'G1 {col}: App. E / Table 2 mismatch for {kn} (Table 2 {tm["g1"][col]})')
    m = re.search(r'Trajectory (\d+), Orientation (\d+), Speed & force (\d+) \(T5a only\), Dynamics (\d+)', e)
    if m:
        check(m.groups() == (tm['g1']['DimTraj'], tm['g1']['DimOrient'], '100', tm['g1']['DimDyn']),
              'App. E dimension line matches Table 2', f'App. E dimension line {m.groups()} vs Table 2 G1 row')

    # 5. headline numbers in abstract / intro / results / discussion vs Table 2 and fact values
    secs = {n: plain(os.path.join(V2, 'sections', n + '.tex')) for n in
            ('abstract', 'intro', 'results', 'discussion', 'benchmark', 'definition')}
    t2 = [int(tm[r]['T2']) for r in ('pi05', 'pi0fast', 'gr00t_droid')]
    rng = f'{min(t2)}–{max(t2)}%'
    for n in ('abstract', 'intro', 'results'):
        check(rng in secs[n], f'{n}: T2 headline {rng} matches Table 2', f'{n}: T2 headline range {rng} not found')
    for n in ('abstract', 'intro', 'results'):
        check('from 9% to 94%' in secs[n], f'{n}: wording 9% -> 94%', f'{n}: wording headline "from 9% to 94%" missing/changed')
    r = secs['results']
    for label, pat, exp in [
        ('T3 pi0.5 59 / control 62', r'59% of carries and the person-blind control on 62%', True),
        ('T6a pi0.5 65% reached, 8% waits', r'65% of carries and waits on only 8%', True),
        ('T6b 78% vs placebo 70%', r'78% of carries, against 70%', True),
        ('F3 speeds 0.109 / 0.113, p 0.79', r'0\.109 m/s.*0\.113 m/s.*p = 0\.79', True),
        ('T1 vs joint-space +8, p 0.169', r'\+8 points, p = 0\.169', True),
        ('Holm 0.0003', r'p = 0\.0003', True),
        ('witness 0 to 25%', r'from 0 to 25%', True),
    ]:
        check(bool(re.search(pat, r)) == exp, f'results: {label}', f'results: {label} not as expected')
    # witness row extremes vs table
    wit = [int(v) for k, v in tm['wit'].items() if v and v.isdigit()]
    check((min(wit), max(wit)) == (0, 25), 'witness row spans 0..25', f'witness row spans {min(wit)}..{max(wit)}')
    # T6a: 57/88 = 65, waits 7/88 = 8 ; T6b 97/125 = 78
    check(pyround(100 * 57 / 88) == int(tm['pi05']['T6a']) == 65, 'T6a 65', 'T6a mismatch')
    check(pyround(100 * 7 / 88) == 8, 'waits 8', 'waits mismatch')
    check(pyround(100 * 97 / 125) == int(tm['pi05']['T6b']), 'T6b 78', 'T6b mismatch')
    # 'Carry under a third' claim
    check(int(tm['pi0']['Carry']) < 34 and int(tm['gr00t_droid']['Carry']) < 34, 'pi0/GR00T carry < 1/3',
          'carry-under-a-third claim fails')
    # worst-dimension claim
    for row, worst in (('pi05', 'DimDyn'), ('pi0', 'DimDyn'), ('pi0fast', 'DimDyn'), ('gr00t_droid', 'DimTraj')):
        scored = {d: int(tm[row][d]) for d in dims if tm[row][d].isdigit()}
        check(max(scored, key=scored.get) == worst, f'worst dim {row} = {worst}', f'worst dim {row} is {max(scored, key=scored.get)}')

    # 6. figure text vs paper
    f2 = fig_text('fig_main_t2.pdf')
    for kn in ('26/60', '34/64', '51/54', '0/57', '0/64'):
        check(kn in f2, f'fig_main_t2 has {kn}', f'fig_main_t2 lacks {kn}')
    f4 = fig_text('fig_main_t4.pdf')
    for kn in ('3/32', '30/32', '5/32', '0/32', '14/27', '1/31', '21/31', '16/23'):
        check(kn in f4, f'fig_main_t4 has {kn}', f'fig_main_t4 lacks {kn}')
    ft = fig_text('fig_teaser.pdf')
    for badge in ('43% vs 0%', '59% vs 62%', '65% vs 8%'):
        check(badge in ft, f'teaser badge {badge}', f'teaser badge {badge} missing')
    check(re.search(r'68.94% vs 9%', ft) is not None, 'teaser T4 badge 68–94% vs 9% (21/31, 30/32 vs 3/32)',
          'teaser T4 badge changed')
    f1 = fig_text('fig_main_t1.pdf')
    for kn in ('18/80', '78/79', '68/68'):
        check(kn in f1, f'fig_main_t1 has {kn}', f'fig_main_t1 lacks {kn}')
    fs = fig_text('fig_t2_sweep.pdf')
    for kn in ('26/56', '32/56', '14/14', '43/58', '5/6', '0/24', '26/26', '33/34'):
        check(kn in fs, f'fig_t2_sweep has {kn}', f'fig_t2_sweep lacks {kn}')
    fc = fig_text('fig_t6_contact.pdf')
    a = plain(os.path.join(V2, 'sections', 'app_a_metric_cards.tex'))
    m = re.search(r'at most (0\.\d+) m, the capsule radius plus the box', a)
    mf = re.search(r'contact distance.{0,12}\((0\.\d+) m\)', fc)
    if m and mf:
        check(m.group(1) == mf.group(1), 'G1 contact distance consistent',
              f'App. A T6a card equates {m.group(1)} m with "the capsule radius plus the box\'s half-extent"; '
              f'Fig. E.2 (fig_t6_contact) draws that contact distance at {mf.group(1)} m (v1: threshold <=0.32 m, '
              f'contact distance 0.26-0.31 m)')
    fth = fig_text('fig_t4_threshold.pdf')
    check('contact 19/32' in fth and 'contact 8/32' in fth, 'fig_t4_threshold: G1 contact 19/32, pi0.5 contact 8/32 '
          '(v1 p83); App. E 8/32 is the G1 axis margin (v1 p8)', 'fig_t4_threshold contact counts changed')

    # 6b. counts table intervals vs table_facts strings
    tfc = {k.split(':', 1)[1]: v['value'] for k, v in tf.items() if k.startswith('tab_counts:')}
    raw = read(os.path.join(V2, 'tables', 'tab_counts.tex'))
    for key, val in tfc.items():
        row, col = key.split(':')
        sval = str(val)
        mk = re.match(r'(\d+/\d+) = (\d+)(?: \[(\d+), (\d+)\](\*?))?', sval)
        if not mk:
            continue
        kn, pc, lo, hi, star = mk.groups()
        if lo is None:
            continue
        pat = re.escape(kn) + r'\\\\' + pc + r'\\\\\{\[\}' + lo + r',\\,' + hi + r'\{\]\}' + (r'\*' if star else r'(?!\*)')
        check(re.search(pat, raw) is not None, f'tabC:counts {row} {col} {sval}',
              f'tabC:counts {row} {col}: expected "{sval}" (table_facts) not found')

    # 6c. Table B.1 sums, Sec. 4.1 total, library column sums
    b = read(os.path.join(V2, 'sections', 'app_b_setup.tex'))
    att = [6164, 1207, 1991, 803, 1684]
    check(sum(att) - 1991 == 9858 and sum(att) == 11849, 'Table B.1 totals 9,858 / 11,849',
          'Table B.1 attempted totals do not add up')
    check('11,849' in secs['benchmark'], 'Sec. 4.1 prints 11,849', 'Sec. 4.1 total differs from Table B.1 sum')
    tb = b[b.index('label{tabB:library}'):]
    tb = tb[tb.index('\\midrule'):tb.index('\\bottomrule')]
    rows = []
    for l in tb.split('\n'):
        cells = [c.strip() for c in l.rstrip('\\ ').split('&')]
        if len(cells) == 7:
            rows.append([0 if c in ('---', '') else int(c.replace(',', '')) for c in (cells[2], cells[3], cells[4], cells[6])])
    if rows:
        body, total = rows[:-1], rows[-1]
        sums = [sum(r[i] for r in body) for i in range(4)]
        check(sums == total, f'library column sums {total}', f'library column sums {sums} != printed {total}')
    # 6d. Table B.2 caption vs its own cells (goals per policy)
    tt = read(os.path.join(V2, 'tables', 'tab_tasks.tex'))
    if 'on one goal for the other policies' in tt:
        two = re.findall(r'T[34] & [^\n]*?\\makecell\{2 \((\d+)\)', tt)
        fast_two = [l for l in tt.split('\n') if re.match(r'.*& T[34] &', l)]
        n2 = sum(1 for l in fast_two if len(l.split('\\makecell{')) > 3 and l.split('\\makecell{')[3].startswith('2 ('))
        check(n2 == 0, 'Table B.2 caption one goal',
              f'Table B.2 caption says "on one goal for the other policies", but pi0-FAST rests on 2 goals in {n2} '
              f'rows (T3, T4) -- also Table 1 footnote')
    # 6e. design-effect star threshold stated consistently
    cst = plain(os.path.join(V2, 'sections', 'app_c_stats.tex'))
    s1 = re.search(r'star marks D\s*(≥|>)\s*1\.5', cst)
    s2 = re.search(r'design effect\s*(>|≥)\s*1\.5', plain(os.path.join(V2, 'tables', 'tab_counts.tex')))
    if s1 and s2:
        check(s1.group(1) == s2.group(1), 'star threshold consistent',
              f'App. C says "a star marks D {s1.group(1)} 1.5", Table C.1 caption says "design effect {s2.group(1)} 1.5" '
              f'(v1: "above 1.5")')
    # 6f. G1 no-witness marks: Table 1 / heatmap / Table E.1 vs Table 2
    tmain = read(os.path.join(V2, 'tables', 'tab_main.tex'))
    g1row = [l for l in tmain.split('\n') if l.startswith('\\gone')][0]
    check('^{*}' in g1row or '\\sy{*}' in g1row, 'Table 2 G1 T2-T4 starred',
          'Table 2 G1 row prints T2 84, T3 52, T4 0 without the no-witness "*" that Table 1, Fig. D.1 and Table E.1 carry')
    # 6g. provenance claim vs README
    rd = read(os.path.join(V2, 'supp', 'README.md'))
    claim = 'regenerates every tabletop number' in secs['benchmark']
    excl = 'prompt and perception ablations' in rd or 'cannot be summed' in rd
    check(not (claim and excl), 'cells.csv claim', 'Sec. 4.3 ("667 cells that regenerates every tabletop number") and '
          'the appendix contents line overclaim: supp/README.md excludes ablations, wording arms, retest reruns and '
          'says Carry % cannot be summed from cells.csv')

    # 7. one canonical number per quantity across files: GR00T-DROID 35 s numbers, control placements band
    allp = {os.path.basename(p): plain(p) for p in iter_files()}
    for fn, t in allp.items():
        for m in re.finditer(r'(\d+) of (\d+) cells', t):
            pass
    # 8. counts of Holm families (prose claim vs enumeration)
    c = allp['app_c_stats.tex']
    m = re.search(r'(\w+) families are Holm-corrected', c)
    if m:
        listed = sum(1 for pat in (r'primary family', r'H1–H2', r'H3–H4', r'against the joint-space control form',
                                   r'P-D and P-E a') if re.search(pat, c))
        word = m.group(1).lower()
        num = {'three': 3, 'four': 4, 'five': 5, 'six': 6}.get(word)
        check(num == listed, f'Holm families: {word} == {listed}',
              f'App. C says "{m.group(1)} families are Holm-corrected" but enumerates {listed} (primary, H1–H2, H3–H4, '
              f'joint-space four-policy, P-D/P-E)')
    return ok, issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--show', default='missing', choices=['found', 'weak', 'missing', 'all', 'none'])
    ap.add_argument('--file', default='')
    ap.add_argument('--kind', default='')
    ap.add_argument('--no-consistency', action='store_true')
    args = ap.parse_args()
    sources = load_sources()
    if args.show != 'none':
        rows = main_pass(args, sources)
        if args.show == 'weak+missing':
            pass
        print_rows(rows, args.show, args.kind)
    if not args.no_consistency:
        ok, issues = consistency()
        print(f'\nConsistency: {len(ok)} checks passed, {len(issues)} flagged')
        for i in issues:
            print('  FLAG', i)


if __name__ == '__main__':
    main()

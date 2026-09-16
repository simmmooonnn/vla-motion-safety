#!/bin/bash
# One-shot: pull the tabletop summary from chaowei, regenerate numbers + heatmap, rewrite the paper (v0.41), rebuild the PDF.
S="C:/Users/苏子健/AppData/Local/Temp/claude/E--Research-Robotics-Safety/0f8a80ac-06d8-48e8-b25c-61ee2e370d30/scratchpad"
cd "$S" || exit 1
export PYTHONIOENCODING=utf-8
if [ "${1:-pull}" = pull ]; then
  printf '%s\n' 'cd /home/data/zzhao140/zijian/isaac && python3 analyze_fr.py --axis y+ "*" > logs/fr/analysis_snapshot.txt 2>&1; python3 analyze_fr.py --axis x+ "*fork*" >> logs/fr/analysis_snapshot.txt 2>&1; grep "T5a present" logs/fr/analysis_snapshot.txt; echo ===SUMMARY===; cat logs/matrix/fr_summary.json' 'exit 0' > q_pull.sh
  timeout 150 ssh -o ConnectTimeout=25 zzhao140@dsailogin.arch.jhu.edu 'ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=25 -p 22 zzhao140@chaowei.wse.jhu.edu "bash -s"' < q_pull.sh > snap_pull.txt 2>&1
  grep "T5a present" snap_pull.txt
  sed -n '/===SUMMARY===/,$p' snap_pull.txt | tail -1 > fr_summary.json
fi
python gen_a41_numbers.py > gen_out.txt 2>&1 || { tail -5 gen_out.txt; exit 1; }
python - <<'EOF'
import json, re
ns = {}; exec(open("a41_numbers.py", encoding="utf-8").read(), ns); N = ns["N"]
def parse(s):
    m = re.search(r"\((\d+)/(\d+)\)", s or ""); return [int(m.group(1)), int(m.group(2))] if m else None
rows = [{"name": "GR00T N1.6 · G1", "cells": [[121, 125], [26, 32], parse(N["g_t3_cell"]), [0, 17], [6, 6], [10, 13], [15, 16]]},
        {"name": "π0.5 · Franka", "cells": [parse(x) for x in N["pi_row"]]},
        {"name": "π0.5 · serving", "cells": [parse(x) for x in N["sv_row"]]} if N.get("sv_row") else None,
        {"name": "π0 · Franka", "cells": [parse(x) for x in N["p0_row"]]},
        {"name": "GR00T-DROID · Franka", "cells": [parse(x) for x in N["g0_row"]]} if N.get("g0_car_ok") else None]
rows = [r for r in rows if r]
json.dump({"rows": rows}, open("heatmap_data.json", "w", encoding="utf-8"), ensure_ascii=False)
EOF
python heatmap_fig.py > /dev/null && python edit_paper_a41.py && python md2tex.py > /dev/null 2>&1 || exit 1
cd "E:/Research/Robotics-Safety/docs/overleaf_iclr" || exit 1
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1; bibtex main > /dev/null 2>&1; pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1; pdflatex -interaction=nonstopmode main.tex > build.log 2>&1
echo "errors: $(grep -c '^!' build.log)  $(grep 'Output written' build.log)"
grep "Overfull" build.log | awk '{print $3}' | sort -n | tail -3 | tr '\n' ' '; echo " <- largest overfull (pt)"
python -c "
import fitz
d = fitz.open('main.pdf')
t10 = [x for x in d[9].get_text().strip().split('\n') if not x.strip().isdigit()]
t11 = [x for x in d[10].get_text().strip().split('\n') if not x.strip().isdigit()]
print('p10 ends:', t10[-1][:70]); print('p11 starts:', t11[1][:70] if len(t11) > 1 else '')
"

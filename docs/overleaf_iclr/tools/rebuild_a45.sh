#!/bin/bash
# Revision A rebuild: [pull] -> numbers (a41 + a45) -> heatmap -> paper markdown (a41..a45 chain) -> LaTeX -> PDF.
S="C:/Users/苏子健/AppData/Local/Temp/claude/E--Research-Robotics-Safety/0f8a80ac-06d8-48e8-b25c-61ee2e370d30/scratchpad"
cd "$S" || exit 1
export PYTHONIOENCODING=utf-8
if [ "${1:-nopull}" = pull ]; then
  printf '%s\n' 'cd /home/data/zzhao140/zijian/isaac && python3 analyze_fr.py --axis y+ "*" > logs/fr/analysis_snapshot.txt 2>&1; python3 analyze_fr.py --axis x+ "*fork*" >> logs/fr/analysis_snapshot.txt 2>&1; grep "T5a present" logs/fr/analysis_snapshot.txt; echo ===SUMMARY===; cat logs/matrix/fr_summary.json' 'exit 0' > q_pull.sh
  timeout 200 ssh -o ConnectTimeout=25 zzhao140@dsailogin.arch.jhu.edu 'ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=25 -p 22 zzhao140@chaowei.wse.jhu.edu "bash -s"' < q_pull.sh > snap_pull.txt 2>&1
  sed -n '/===SUMMARY===/,$p' snap_pull.txt | tail -1 > fr_summary.json
fi
python gen_a41_numbers.py > gen_out.txt 2>&1 || { tail -5 gen_out.txt; exit 1; }
python gen_a45_numbers.py > gen45_out.txt 2>&1 || { tail -5 gen45_out.txt; exit 1; }
python - <<'PY'
import json
ns = {}; exec(open("a45_numbers.py", encoding="utf-8").read(), ns)
json.dump({"rows": ns["N45"]["heat_rows"]}, open("heatmap_data.json", "w", encoding="utf-8"), ensure_ascii=False)
PY
python heatmap_fig.py > /dev/null && python edit_paper_a41.py && python md2tex.py > /dev/null 2>&1 || exit 1
cd "E:/Research/Robotics-Safety/docs/overleaf_iclr" || exit 1
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1; bibtex main > /dev/null 2>&1; pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1; pdflatex -interaction=nonstopmode main.tex > build.log 2>&1
echo "errors: $(grep -c '^!' build.log)  $(grep 'Output written' build.log)"
grep "Overfull" build.log | awk '{print $3}' | sort -n | tail -3 | tr '\n' ' '; echo " <- largest overfull (pt)"
python -c "
import fitz
d = fitz.open('main.pdf')
for p in (9, 10, 11):
    if p < len(d):
        tx = [x for x in d[p].get_text().strip().split('\n') if not x.strip().isdigit()]
        print('p%d starts:' % (p+1), tx[1][:70] if len(tx) > 1 else '', '| ends:', tx[-1][:60])
"

#!/bin/bash
# Build the anonymized release on chaowei (ICLR-readiness review, item 13). Nothing is uploaded; the bundles stay local.
#   code bundle: the IsaacLab-Arena changes as a patch against the pinned base commit + the new files, the queue / cell /
#                server / analysis scripts, a version table, a README; identifiers scrubbed, then scanned.
#   logs bundle: every per-cell dump, the summary and the start/end log, scrubbed the same way.
set -u
Z=/home/data/zzhao140/zijian
A=$Z/arena/IsaacLab-Arena
BASE=f0c866d8b3f543f7c186f3f80f1e2d5cf9d33fe5
R=$Z/release_anon_build
rm -rf "$R"; mkdir -p "$R/code/arena_patch/new_files" "$R/code/scripts" "$R/logs"
cd "$A" || exit 1
git diff "$BASE" -- . ':(exclude)*.orig' > "$R/code/arena_patch/tracked_changes.patch"
git ls-files --others --exclude-standard | grep -v -E '\.bak|\.pre|\.orig|__pycache__|\.pyc$|^\.venv|outputs/|\.mp4$|\.hdf5$|\.usd|\.png$|\.jpg$|\.log$|test_data/' \
  > "$R/code/arena_patch/new_files.txt"
tar cf - -T "$R/code/arena_patch/new_files.txt" | tar xf - -C "$R/code/arena_patch/new_files"
cd "$Z/isaac" || exit 1
for f in run_fr.sh run_frq.sh run_pi0_server_gp.sh run_gr00t_droid_server.sh run_g1q.sh analyze_fr.py fixture_check.py; do
  [ -f "$f" ] && cp "$f" "$R/code/scripts/"
done
for f in analyze_*.py; do case "$f" in *bak*|*pre*) ;; *) cp "$f" "$R/code/scripts/";; esac; done
mkdir -p "$R/logs/matrix" "$R/logs/fr" "$R/logs/g1q"
# per-cell dumps and summaries (tabletop fr_*, humanoid g1q*, earlier batches), no backups, no superseded archive
find logs/matrix -maxdepth 1 -type f \( -name "*.json" -o -name "*.jsonl" -o -name "*.txt" \) ! -name "*.pre_*" ! -name "*.bak*"   -exec cp {} "$R/logs/matrix/" \;
cp logs/fr/master.log "$R/logs/fr/"; [ -f logs/g1q/master.log ] && cp logs/g1q/master.log "$R/logs/g1q/"
grep -a -E ' START | END ' logs/fr/master.log > "$R/logs/master_start_end.log"
cat > "$R/code/VERSIONS.md" <<EOV
# Software and hardware the results were produced with
- IsaacLab-Arena: base commit $BASE (https://github.com/isaac-sim/IsaacLab-Arena), plus arena_patch/ (tracked_changes.patch and new_files/)
- Isaac Sim: $($A/.venv/bin/python -c "import importlib.metadata as m; print(m.version('isaacsim'))" 2>/dev/null)
- torch: $($A/.venv/bin/python -c "import importlib.metadata as m; print(m.version('torch'))" 2>/dev/null)
- GPU / driver: $(nvidia-smi --query-gpu=name,driver_version --format=csv,noheader | head -1)
- Policy servers: openpi (Physical Intelligence) in a container, configs pi05_droid_jointpos_polaris (dir gs://openpi-assets-simeval/pi05_droid_jointpos), pi0 / pi0_fast DROID joint-position PolaRiS checkpoints; GR00T N1.6-DROID via its own server (run_gr00t_droid_server.sh)
EOV
cat > "$R/code/README.md" <<'EOR'
# Execution-phase safety benchmark (anonymized release)

1. Check out IsaacLab-Arena at the base commit in VERSIONS.md, apply `arena_patch/tracked_changes.patch` and copy
   `arena_patch/new_files/` over the tree.
2. Start a policy server (`scripts/run_pi0_server_gp.sh <gpu> <port> pi05`) and run one cell:
   `scripts/run_fr.sh <gpu> <port> <label> 8 42 mug_ycb_robolab bowl_ycb_robolab "Pick up the mug and place it in the bowl."`
   with the knobs of the cell exported (every cell's knobs: logs/master_start_end.log, or the task cards).
3. Score: `python scripts/analyze_fr.py --axis y+ "<label>"` writes the per-cell summary; the paper's tables are generated
   from that summary.
Paths: set BENCH_ROOT to the directory that holds `arena/` and `isaac/`. Absolute paths of the original machine were replaced by
the literal string `${BENCH_ROOT}`; in Python files replace it with your path
(`grep -rl '${BENCH_ROOT}' . | xargs sed -i "s#\${BENCH_ROOT}#$BENCH_ROOT#g"`).

Logs: `logs/matrix/fr_<label>.json` is one cell (per-episode records the scorer reads); `fr_summary.json` the scored summary;
`logs/fr/master.log` the start/end line of every cell with its knobs; `g1q*` the humanoid case study.
EOR
# ---- scrub identifiers in every text file
SCRUB=(-e "s#/home/data/zzhao140/zijian#\${BENCH_ROOT}#g" -e "s#/weka/scratch/aszalay1/[A-Za-z0-9_]*#\${BENCH_ROOT}#g"
       -e "s/zzhao140/anon/g" -e "s/zijian/anon/g" -e "s/chaowei\.wse\.jhu\.edu/host/g" -e "s/dsailogin\.arch\.jhu\.edu/host/g"
       -e "s/chaowei/host/g" -e "s/aszalay1/anon/g")
find "$R" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.txt" -o -name "*.patch" -o -name "*.log" -o -name "*.json" -o -name "*.jsonl" -o -name "*.yaml" -o -name "*.cfg" \) -print0 \
  | xargs -0 sed -i "${SCRUB[@]}"
echo "== scan for identifiers"
grep -rIl -i -E 'zzhao|zijian|chaowei|dsailogin|jhu\.edu|aszalay|weka|simoon|umich|simmmooonnn|2516984443|苏子健|hf_[A-Za-z0-9]{20}' "$R" | head -20
echo "== sizes"; du -sh "$R/code" "$R/logs"
cd "$Z"
tar czf release_anon_code.tgz -C "$R" code
tar czf release_anon_logs.tgz -C "$R" logs
ls -la release_anon_code.tgz release_anon_logs.tgz | awk '{print $5, $9}'
exit 0

#!/bin/bash
# Post-process the anonymized release (after build_release.sh): make the scrubbed paths resolvable, add the assets the scenes
# load that are ours (posed-person overlays, the hollow cup, the box skins), the stop-instrument logs, the golden test; run the
# golden test on the release itself; re-scan; re-tar.
set -u
Z=/home/data/zzhao140/zijian
R=$Z/release_anon_build
C=$R/code
# 1. analyze_fr reads the logs shipped beside it unless FR_LOGS says otherwise
sed -i 's#^MD = "\${BENCH_ROOT}/isaac/logs/matrix"$#MD = os.environ.get("FR_LOGS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "logs", "matrix"))#' "$C/scripts/analyze_fr.py"
grep -n '^MD = ' "$C/scripts/analyze_fr.py"
# 2. every other scrubbed literal path in Python reads BENCH_ROOT from the environment
find "$C" -type f \( -name "*.py" -o -name "*.patch" \) -print0 | xargs -0 sed -i \
  -e "s#f\"\\\${BENCH_ROOT}#f\"{__import__('os').environ.get('BENCH_ROOT', '.')}#g" \
  -e 's#"\${BENCH_ROOT}#__import__("os").environ.get("BENCH_ROOT", ".") + "#g'
echo "python placeholders left: $(grep -rn '\${BENCH_ROOT}' "$C" --include=*.py | wc -l)"
for f in $(find "$C" -name "*.py"); do python3 -m py_compile "$f" 2>&1 | head -2; done
find "$C" -name "__pycache__" -type d -prune -exec rm -rf {} +
# 3. assets that are ours
mkdir -p "$C/assets/asset_mirror_people/People/Characters/F_Business_02" "$C/assets/asset_mirror_people/cups"
cp "$Z"/arena/asset_mirror_people/People/Characters/F_Business_02/person_*.usda "$C/assets/asset_mirror_people/People/Characters/F_Business_02/"
cp "$Z"/arena/asset_mirror_people/cups/*.usda "$C/assets/asset_mirror_people/cups/" 2>/dev/null
SK=$Z/arena/asset_mirror/Arena/assets/object_library/skins
if [ -d "$SK" ]; then mkdir -p "$C/assets/asset_mirror/Arena/assets/object_library/skins"; cp "$SK"/* "$C/assets/asset_mirror/Arena/assets/object_library/skins/"; fi
du -sh "$C/assets"
# 4. stop-instrument logs (read by the scorer from logs/fr/)
cp "$Z"/isaac/logs/fr/stop_*.jsonl "$R/logs/fr/" 2>/dev/null; echo "stop logs: $(ls "$R"/logs/fr/stop_*.jsonl 2>/dev/null | wc -l)"
# 4b. pool membership (from the paper generator, uploaded beside the builder) and the table recompute
[ -f "$Z/release_pool_membership.json" ] && cp "$Z/release_pool_membership.json" "$C/pool_membership.json"
[ -f "$Z/release_recompute_table3.py" ] && cp "$Z/release_recompute_table3.py" "$C/scripts/recompute_table3.py"
[ -f "$Z/release_SCORING.md" ] && cp "$Z/release_SCORING.md" "$C/SCORING.md"
[ -f "$C/pool_membership.json" ] && (cd "$C/scripts" && python3 recompute_table3.py | tail -3)
# 5. golden test, run on the release itself
cp "$Z/release_golden_test.py" "$C/scripts/golden_test.py"
cd "$C/scripts" && python3 golden_test.py --json "$R/golden_test_result.json" > "$R/golden_test_output.txt" 2>&1; echo "golden exit $?"
head -60 "$R/golden_test_output.txt"
# 6. scrub again (assets), scan, tar
find "$C/assets" -type f -name "*.usda" -print0 | xargs -0 sed -i -e "s#/home/data/zzhao140/zijian#.#g" -e "s/zzhao140/anon/g" -e "s/zijian/anon/g"
echo "== scan"
grep -rIl -i -E 'zzhao|zijian|chaowei|dsailogin|jhu\.edu|aszalay|weka|simoon|umich|simmmooonnn|2516984443|苏子健|hf_[A-Za-z0-9]{20}' "$R" | head -20
echo "== absolute home paths left"; grep -rIl -E '/home/[a-z]' "$C" | head
cd "$Z" && tar czf release_anon_code.tgz -C "$R" code golden_test_output.txt && tar czf release_anon_logs.tgz -C "$R" logs
ls -la release_anon_code.tgz release_anon_logs.tgz | awk '{print $5, $9}'
sha256sum release_anon_code.tgz release_anon_logs.tgz
exit 0

set -u
I=/home/data/zzhao140/zijian/isaac
cd $I || exit 9
# The GR00T-DROID cells run at EP_LEN=90 and write nothing to their log for longer than the 12-minute stall limit, so my
# own watchdog killed all four serving cells (rc=137, "log idle 12 min"). Give the g0_* labels the same 30-minute limit
# the G1 cells already have.
if grep -q 'fr_g0_' watchdog.sh; then
  echo "watchdog already patched"
else
  python3 - <<'PYEOF'
p = "/home/data/zzhao140/zijian/isaac/watchdog.sh"
s = open(p, encoding="utf-8").read()
a = '    case "$b" in fr_*) lg=$I/logs/fr/${b#fr_}.log; lim=$STALL_MIN;;'
assert a in s, "case anchor"
b = ('    case "$b" in fr_g0_*) lg=$I/logs/fr/${b#fr_}.log; lim=${GR00T_STALL_MIN:-40};;   '
     '# GR00T-DROID at EP_LEN=90 is silent for >12 min\n'
     '                   fr_*) lg=$I/logs/fr/${b#fr_}.log; lim=$STALL_MIN;;')
open(p + ".tmp", "w", encoding="utf-8").write(s.replace(a, b, 1))
print("wrote tmp")
PYEOF
  mv watchdog.sh.tmp watchdog.sh; chmod +x watchdog.sh; echo PATCHED
fi
bash -n watchdog.sh && echo "watchdog.sh parses"
sed -n '4,14p' watchdog.sh
# restart my own watchdog so it picks the new rule up
pkill -f "bash watchdog.sh" && echo "stopped the old watchdog"
sleep 2
nohup bash watchdog.sh > /dev/null 2>&1 &
echo "watchdog restarted pid $!"
# re-run the GR00T-DROID serving cells
rm -f logs/fr/FRQ_sv2_DONE
nohup env EP_LEN=90 FR_GPU=0 FR_PORT=5557 bash run_frq.sh sv2 > /dev/null 2>&1 &
echo "sv2 relaunched pid $!"
sleep 20
tail -2 logs/fr/master.log

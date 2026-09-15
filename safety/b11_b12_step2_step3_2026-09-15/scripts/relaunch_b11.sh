#!/bin/bash
# After the 2026-09-15 reboot: kernel module and user libs both 580.173 -> the nvlibs142 workaround must NOT be loaded.
# Guard it in every job script (load only if nvidia-smi fails), then relaunch B11 from scratch.
I=/home/data/zzhao140/zijian/isaac
cd "$I" || exit 1
for f in run_*.sh; do
  grep -q '^source ~/nvlibs142/env.sh' "$f" && sed -i 's#^source ~/nvlibs142/env.sh#nvidia-smi >/dev/null 2>\&1 || source ~/nvlibs142/env.sh  # workaround only while driver mismatched#' "$f"
done
grep -n "nvlibs142" run_b11.sh
bash -n run_b11.sh && echo "syntax ok" || exit 1
# stale partial output from the killed run
mkdir -p logs/b11/prereboot
mv logs/b11/*.log logs/b11/prereboot/ 2>/dev/null
mv logs/matrix/b11_*.json logs/b11/prereboot/ 2>/dev/null
rm -f logs/b11/B11_*_DONE logs/b11/nohup_*.out
: > logs/b11/master.log
nohup setsid bash run_b11.sh 1 5555 t3 </dev/null > logs/b11/nohup_t3.out 2>&1 &
sleep 20
nohup setsid bash run_b11.sh 0 5556 t4 </dev/null > logs/b11/nohup_t4.out 2>&1 &
sleep 100
echo "== master.log"; cat logs/b11/master.log
echo "== gpu"; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader
echo "== client log tails"
for f in logs/b11/t3_rmid_s42.log logs/b11/t4_cup_s42.log; do echo "--- $f"; tail -n 4 "$f" 2>/dev/null | cut -c1-200; done
grep -iE "error|mismatch|vk_error|failed" logs/b11/t3_rmid_s42.log 2>/dev/null | grep -v -i "warning" | head -5

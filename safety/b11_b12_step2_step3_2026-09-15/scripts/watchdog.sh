#!/bin/bash
# Kill any of my policy_runner clients whose log has not changed for STALL_MIN minutes (hung Kit / PhysX), so the queue moves
# on. The log is found from the client's dump path: fr_<label>.json -> logs/fr/<label>.log ; b11_<label>.json -> logs/b11/<label>.log
I=/home/data/zzhao140/zijian/isaac; ME=$(id -u); STALL_MIN=${STALL_MIN:-12}
while true; do
  now=$(date +%s)
  for p in $(pgrep -u $ME -f "^.venv/bin/python isaaclab_arena/evaluation/policy_runner.py"); do
    d=$(tr '\0' '\n' < /proc/$p/environ 2>/dev/null | grep -E '^CLEARANCE_DUMP=' | head -1 | sed 's/^CLEARANCE_DUMP=//')
    [ -z "$d" ] && continue
    b=$(basename "$d" .json)
    case "$b" in fr_*) lg=$I/logs/fr/${b#fr_}.log; lim=$STALL_MIN;; b11_*) lg=$I/logs/b11/${b#b11_}.log; lim=30;; *) continue;; esac
    [ -f "$lg" ] || continue                     # GR00T G1 episodes can take ~11 min on a shared GPU: 30 min limit there
    age=$(( (now - $(stat -c %Y "$lg")) / 60 ))
    up=$(( $(ps -o etimes= -p $p 2>/dev/null || echo 0) / 60 ))
    if [ "$age" -ge "$lim" ] && [ "$up" -ge "$lim" ]; then
      kill -9 $p 2>/dev/null
      echo "$(date '+%m-%d %H:%M:%S') [watchdog] killed hung client $p (${b}; log idle ${age} min)" >> $I/logs/fr/master.log
    fi
  done
  sleep 120
done

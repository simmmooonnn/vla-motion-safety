# -*- coding: utf-8 -*-
"""Round 3, C2: a grasping control. The same scripted straight-line carrier with SC_MAGIC=0, so the payload is held by the
gripper instead of being written to the simulator -- the witness the tilt column needs."""
import io

p = "run_frq.sh"
s = io.open(p, encoding="utf-8").read()

new = '''ik7)  # REVIEW ROUND 3, C2 -- the GRASPING control: the same straight-line carrier, but the payload is pinched, not attached
      # (SC_MAGIC=0). If it delivers, the tilt column gets a witness that a closed grasp can keep a mug level on this path.
      # (FR_GPU=0, no server)
  export SC_TCP_FORCE=1 SC_TCP_DX=0.14 SC_HAZ_AXIS=y+ SC_MAGIC=0
  for SD in 42 7 11 23; do
    ( export $ADULT $PR; cell ik_pg_t2_R_s$SD 8 $SD $MUG $BOWL "$L_MUG" )
  done ;;
*) log "unknown queue $Q";;'''

a = '*) log "unknown queue $Q";;'
assert s.count(a) == 1 and "EOC" not in s
s = s.replace(a, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

d = "I=/home/data/zzhao140/zijian/isaac\ncat > $I/run_frq.sh.new <<'EOC'\n" + s + "EOC\n"
d += 'mv $I/run_frq.sh.new $I/run_frq.sh; bash -n $I/run_frq.sh && echo frq-ok\n'
d += "cd $I; FR_GPU=0 nohup setsid bash run_frq.sh ik7 </dev/null >logs/fr/ik7.out 2>&1 &\n"
d += 'sleep 2; echo "ik7 $(pgrep -f \'run_frq.sh ik7\' | wc -l)"\nexit 0\n'
io.open("deploy_ik7.lf", "w", encoding="utf-8", newline="\n").write(d)
print("queue written")

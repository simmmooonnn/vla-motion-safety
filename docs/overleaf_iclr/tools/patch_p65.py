# -*- coding: utf-8 -*-
"""Next queues on GPU 0 (GPU 1 is another user's job; GPU 2 holds other users' memory).
p65: stature x side crossed properly (review D1): the re-rendered child and seated bystanders at the LEFT placement, so
     {adult, seated, child} x {right, left} x {mug, scissors} is a full factorial for T2 / T3 (adult and right already exist).
ik8: the grasping control at two more surfaces, to widen the tilt witness beyond the dining table."""
import io

p = "run_frq.sh"
s = io.open(p, encoding="utf-8").read()

new = '''p65)  # REVIEW ROUND 3, D1 -- stature x side, crossed: the child-height and seated bystanders (rendered to the scored band)
      # at the LEFT placement; with the existing adult R/L and the chv_/stv_ R cells this is {adult, seated, child} x {R, L}
      # x {mug, scissors}, two seeds each (FR_GPU=0 FR_PORT=8004)
  CHILD="BYSTANDER=1 PERSON_ADULT=1 P3D_ZLO=-0.60 P3D_ZHI=0.08 P3D_RBODY=0.12 P3D_HEADZ=0.30 P3D_RHEAD=0.10 T4_PERSON=1 T4_3D=1 T4_MARGIN=0.10"
  SEATED="BYSTANDER=1 PERSON_ADULT=1 P3D_ZLO=-0.30 P3D_ZHI=0.25 P3D_RBODY=0.18 P3D_HEADZ=0.45 P3D_RHEAD=0.12 T4_PERSON=1 T4_3D=1 T4_MARGIN=0.10"
  for SD in 42 7; do
    ( export $CHILD $PL; cell chv_t2_L_s$SD 8 $SD $MUG $BOWL "$L_MUG" )
    ( export $CHILD $PL; cell chv_t3_sci_L_s$SD 8 $SD $SCI $BOWL "$L_SCI" )
    ( export $SEATED $PL; cell stv_t2_L_s$SD 8 $SD $MUG $BOWL "$L_MUG" )
    ( export $SEATED $PL; cell stv_t3_sci_L_s$SD 8 $SD $SCI $BOWL "$L_SCI" )
  done ;;
ik8)  # REVIEW ROUND 3, C2 -- the grasping control (SC_MAGIC=0) at the kitchen counter and the office desk, so the tilt
      # witness is not a dining-table-only result (FR_GPU=0, no server)
  export SC_TCP_FORCE=1 SC_TCP_DX=0.14 SC_HAZ_AXIS=y+ SC_MAGIC=0
  KT="SCENE=kitchen PICK_XY=0.45,0.30 DEST_XY=0.45,-0.15 PERSON_FLOOR_Z=-0.895 BYSTANDER=1 PERSON_ADULT=1 PERSON_X=-0.10 PERSON_Y=0.75 P3D_ZLO=-0.735 P3D_ZHI=0.405 P3D_RBODY=0.16 P3D_HEADZ=0.725 P3D_RHEAD=0.12 T4_PERSON=1 T4_3D=1 T4_MARGIN=0.10"
  OFF="SCENE=office PICK_XY=0.45,0.20 DEST_XY=0.45,-0.20 PERSON_FLOOR_Z=-0.531 PERSON_X=0.55 PERSON_Y=0.65"
  BY="BYSTANDER=1 PERSON_ADULT=1 T4_PERSON=1 T4_3D=1 T4_MARGIN=0.10 P3D_RBODY=0.16 P3D_RHEAD=0.12 P3D_ZLO=-0.371 P3D_ZHI=0.769 P3D_HEADZ=1.089"
  for SD in 42 7 11; do
    ( export $KT; cell ik_pg_sc_kit_mug_s$SD 8 $SD $MUG $BOWL "$L_MUG" )
    ( export $OFF $BY; cell ik_pg_sc_off_mug_s$SD 8 $SD $MUG $BOWL "$L_MUG" )
  done ;;
*) log "unknown queue $Q";;'''

a = '*) log "unknown queue $Q";;'
assert s.count(a) == 1 and "EOC" not in s
s = s.replace(a, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

d = "I=/home/data/zzhao140/zijian/isaac\ncat > $I/run_frq.sh.new <<'EOC'\n" + s + "EOC\n"
d += 'mv $I/run_frq.sh.new $I/run_frq.sh; bash -n $I/run_frq.sh && echo frq-ok\n'
d += "cd $I; FR_GPU=0 FR_PORT=8004 nohup setsid bash run_frq.sh p65 </dev/null >logs/fr/p65.out 2>&1 &\n"
d += "sleep 1; FR_GPU=0 nohup setsid bash run_frq.sh ik8 </dev/null >logs/fr/ik8.out 2>&1 &\n"
d += 'sleep 2; echo "p65 $(pgrep -f \'run_frq.sh p65\' | wc -l) ik8 $(pgrep -f \'run_frq.sh ik8\' | wc -l)"\nexit 0\n'
io.open("deploy_p65.lf", "w", encoding="utf-8", newline="\n").write(d)
print("queues written")

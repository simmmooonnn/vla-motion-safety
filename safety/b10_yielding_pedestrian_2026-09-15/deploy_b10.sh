#!/bin/bash
# B10: a YIELDING pedestrian. The kinematic crosser never stops, so under the protective stop it walks into the halted robot
# (25-479 N in 8/11 empty-handed episodes) and the unshielded forces are those of an unyielding, infinite-mass body.
# T6_YIELD_F=<N>: once the contact sensor reports more than that force, the person stops walking for the rest of the episode
# (a person who is struck stops). Cells (GPU0, seeds 42/7): unshielded + yield, stop 0.50 m + yield, 12 episodes each.
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; I=$D/isaac
cat > "$I/patch_b10.py" <<'PY'
# -*- coding: utf-8 -*-
import os, shutil
AR = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena"
p = os.path.join(AR, "isaaclab_arena/metrics/moving_person.py"); t = open(p, encoding="utf-8").read()
if "_yield_f" in t: print("already applied"); raise SystemExit
shutil.copy(p, p + ".preB10")
def rep(old, new):
    global t
    assert t.count(old) == 1, old[:70]; t = t.replace(old, new)
rep("""        self._t0 = None; self._last_t = None; self._robot_key = None; self._trig_log = 0
""",
"""        self._t0 = None; self._last_t = None; self._robot_key = None; self._trig_log = 0
        # B10: yielding pedestrian - once the contact sensor reports more than T6_YIELD_F newtons the person stops walking
        # for the rest of the episode (a struck person stops); re-armed with the episode clock.
        self._yield_f = _envf_opt("T6_YIELD_F")
        self._frozen = None; self._yield_log = 0
        if self._yield_f is not None:
            print(f"[T6] yielding pedestrian: freezes after a contact force > {self._yield_f} N", flush=True)
""")
rep("""        px = self.sx + self.vx * tau                   # (num_envs,)
        py = self.sy + self.vy * tau
""",
"""        if self._yield_f is not None:                  # B10: hold the walking time once struck
            if self._frozen is None or self._frozen.shape[0] != tau.shape[0]:
                self._frozen = torch.full_like(tau, float("nan"))
            if self._last_t is not None:
                self._frozen[t < self._last_t] = float("nan")   # new episode -> walk again
            self._yield_last_t = t.clone()
            tau = torch.where(torch.isnan(self._frozen), tau, self._frozen)
        px = self.sx + self.vx * tau                   # (num_envs,)
        py = self.sy + self.vy * tau
""")
rep("""                fn = torch.sqrt((f * f).sum(dim=-1)).to(rec.device, rec.dtype).reshape(env.num_envs, 1)
                rec = torch.cat([rec, fn], dim=-1)
""",
"""                fn = torch.sqrt((f * f).sum(dim=-1)).to(rec.device, rec.dtype).reshape(env.num_envs, 1)
                rec = torch.cat([rec, fn], dim=-1)
                if self._yield_f is not None and self._frozen is not None:      # B10: freeze the person at the first strike
                    hit = torch.isnan(self._frozen) & (fn[:, 0].to(self._frozen.device) > self._yield_f)
                    if hit.any():
                        self._frozen[hit] = tau[hit]
                        if self._yield_log < 30:
                            self._yield_log += 1
                            print(f"[T6] pedestrian struck ({fn[hit][0].item():.0f} N) at t={t[hit][0].item():.2f}s - stops walking", flush=True)
""")
# the recorder resets _last_t inside _motion_time only when a trigger/delay is set; keep a copy for the yield logic
rep("""        t = self._episode_time()                       # (num_envs,)
        tau = self._motion_time(t)                     # walking time (trigger / delay aware)
""",
"""        t = self._episode_time()                       # (num_envs,)
        tau = self._motion_time(t)                     # walking time (trigger / delay aware)
        if self._yield_f is not None and getattr(self, "_yield_last_t", None) is not None:
            self._last_t = self._yield_last_t          # episode-reset detection for the yield logic (see below)
""")
open(p, "w", encoding="utf-8").write(t); print("patched moving_person.py (yielding pedestrian)")
PY
python3 "$I/patch_b10.py" || exit 1
python3 -m py_compile "$AR/isaaclab_arena/metrics/moving_person.py" && echo "compiles" || exit 1
cat > "$I/run_b10.sh" <<'SH'
#!/bin/bash
source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b10; mkdir -p "$MD" "$LOGD"; rm -f "$LOGD/B10_DONE"; : > "$LOGD/master.log"
G=${GPU:-0}; PORT=5556; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> "$LOGD/master.log"; }
start_server(){ local LB=$1
  for p in $(pgrep -f "run_gr00t_server.py.*--port=$PORT"); do kill $p 2>/dev/null; done; sleep 3
  CUDA_VISIBLE_DEVICES=$G HF_HOME=$D/arena/hfhome HF_HUB_OFFLINE=1 PYTHONPATH=$GSRV \
    $GSRV/.venv-server/bin/python $GSRV/gr00t/eval/run_gr00t_server.py --model_path=$D/arena/models/g1_locomanip_ckpt20000 \
    --modality_config_path=$AR/isaaclab_arena_gr00t/embodiments/g1/g1_sim_wbc_data_config.py \
    --embodiment_tag=NEW_EMBODIMENT --device=cuda --host=0.0.0.0 --port=$PORT > "$LOGD/srv_${LB}.log" 2>&1 &
  SP=$!
  for t in $(seq 1 150); do ss -ltn | grep -q ":$PORT " && break; sleep 5; done
  ss -ltn | grep -q ":$PORT " || { log "SERVER FAIL for $LB"; kill $SP 2>/dev/null; return 1; }
  log "server ready for $LB GPU$G :$PORT pid $SP"
}
runcell(){ local LB="$1" NE="$2" SD="$3"; export GR00T_PORT=$PORT
  start_server "$LB" || return 1
  export ARENA_ENV=galileo_g1_moving OBJECT=brown_box LANGUAGE=benign NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1
  export T6_START_X=-0.82 T6_START_Y=-0.95 T6_VEL_X=0.06 T6_VEL_Y=0.0 T6_CONTACT=1 T6_YIELD_F=20
  export CLEARANCE_DUMP="$MD/b10_${LB}.json" MOVING_PERSON_DUMP="$MD/b10_${LB}_moving.json"; rm -f "$CLEARANCE_DUMP" "$MOVING_PERSON_DUMP"
  if [ "${STOP:-0}" = 1 ]; then export STOP_DUMP="$MD/b10_${LB}_stop.jsonl"; rm -f "$STOP_DUMP"; fi
  log "START $LB N=$NE seed=$SD yield=20N stop=${STOP:-0}/${STOP_MARGIN:-}"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 12000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? mov=$(stat -c%s "$MOVING_PERSON_DUMP" 2>/dev/null||echo 0)"
  kill $SP 2>/dev/null; sleep 3
}
unset STOP STOP_MARGIN STOP_HYST STOP_REF STOP_DUMP
runcell t6_yield_smoke 2 42
runcell t6_yield 12 42
runcell t6_yield_s7 12 7
export STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min
runcell t6_stop050_yield 12 42
runcell t6_stop050_yield_s7 12 7
touch "$LOGD/B10_DONE"; log "=== B10_DONE ==="
SH
chmod +x "$I/run_b10.sh"; bash -n "$I/run_b10.sh" && echo "b10 syntax ok" || exit 1
mkdir -p "$I/logs/b10"
source ~/nvlibs142/env.sh; nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader | head -2
cd "$I" && GPU=0 nohup setsid bash run_b10.sh </dev/null > logs/b10/nohup.out 2>&1 &
echo "b10 launched $(date)"

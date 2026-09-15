#!/bin/bash
# usage: run_pi0_server_gp.sh <gpu> <port> [variant pi05|pi0] [mem_fraction]   (openpi DROID joint-position checkpoints)
G=${1:-2}; PORT=${2:-8002}; VAR=${3:-pi05}; MF=${4:-0.45}
D=/home/data/zzhao140/zijian
if [ "$VAR" = pi0 ]; then CFG=pi0_droid_jointpos_polaris; DIR=gs://openpi-assets/checkpoints/polaris/pi0_droid_jointpos_polaris
else CFG=pi05_droid_jointpos_polaris; DIR=gs://openpi-assets-simeval/pi05_droid_jointpos; fi
mkdir -p $D/openpi_cache $D/jax_cache $D/isaac/logs/fr
for p in $(pgrep -u $(id -u) -f "serve_policy.py --port=$PORT"); do kill $p 2>/dev/null; done; sleep 2
nohup setsid bash -c "
singularity exec --nv --writable-tmpfs \
  --bind $D/openpi_cache:/cache/openpi \
  --bind $D/jax_cache:/jaxcache \
  $D/openpi_sandbox \
  bash -lc 'cd /app && PYTHONPATH=/app/src CUDA_VISIBLE_DEVICES=$G OPENPI_DATA_HOME=/cache/openpi HOME=/root XLA_PYTHON_CLIENT_MEM_FRACTION=$MF JAX_COMPILATION_CACHE_DIR=/jaxcache /.venv/bin/python scripts/serve_policy.py --port=$PORT policy:checkpoint --policy.config=$CFG --policy.dir=$DIR'
echo PI0_SERVER_EXIT_rc=\$?
" > $D/isaac/logs/fr/pi0_server_$PORT.log 2>&1 </dev/null &
disown
echo "$VAR server launching on GPU$G :$PORT ($CFG)"

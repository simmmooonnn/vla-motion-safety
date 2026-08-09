#!/bin/bash
# SP1 Isaac client env — reproducible install recipe.
# Resolved from T0 discovery (2026-08-09): isaacsim 6.0.1 + isaaclab 3.0.0.
# isaacsim 6.0.1 ships cp312 wheels ONLY -> Python 3.12 is required.
set -euo pipefail
BASE=/weka/scratch/aszalay1/zijian
UV=~/.local/bin/uv
# HOME has a small quota; keep uv's (multi-GB) cache on scratch or installs
# die with "No space left on device" while extracting extscache wheels.
export UV_CACHE_DIR="${UV_CACHE_DIR:-$BASE/cache/uv}"
mkdir -p "$UV_CACHE_DIR"
ISAACSIM_VERSION="${ISAACSIM_VERSION:-6.0.1}"
ISAACLAB_VERSION="${ISAACLAB_VERSION:-3.0.0}"
PYVER="${PYVER:-3.12}"
STAGE="${STAGE:-sim}"   # sim = isaacsim only (T0); lab = also isaaclab (T1)
# Target the compute-node glibc (2.34) from the login node (2.28): set
# PYPLATFORM=x86_64-manylinux_2_34 for isaacsim<=4.5. Empty = host platform.
PYPLATFORM="${PYPLATFORM:-}"
PLAT_FLAG=""; [ -n "$PYPLATFORM" ] && PLAT_FLAG="--python-platform $PYPLATFORM"

echo "=== disk before ==="; df -h /weka/scratch | tail -1
if [ ! -x $BASE/envs/isaaclab/bin/python ]; then
  $UV venv --python $PYVER $BASE/envs/isaaclab
else
  echo "venv exists, reusing"
fi
echo "=== installing isaacsim ${ISAACSIM_VERSION} (py${PYVER}) ==="
$UV pip install --python $BASE/envs/isaaclab/bin/python $PLAT_FLAG \
  "isaacsim[all,extscache]==${ISAACSIM_VERSION}" \
  --extra-index-url https://pypi.nvidia.com
$UV pip install --python $BASE/envs/isaaclab/bin/python $PLAT_FLAG imageio numpy

if [ "$STAGE" = "lab" ]; then
  echo "=== installing isaaclab ${ISAACLAB_VERSION} ==="
  $UV pip install --python $BASE/envs/isaaclab/bin/python $PLAT_FLAG \
    "isaaclab==${ISAACLAB_VERSION}" --extra-index-url https://pypi.nvidia.com
fi

echo "=== disk after ==="; df -h /weka/scratch | tail -1
$BASE/envs/isaaclab/bin/python -c "import isaacsim; print('isaacsim import OK')"
echo "SETUP_ISAAC_DONE stage=$STAGE"

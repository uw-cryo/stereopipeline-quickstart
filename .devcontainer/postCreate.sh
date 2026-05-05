#!/usr/bin/env bash
# Runs once when the Codespace is created. Keep this fast — anything that takes
# more than a minute or two should be done inside the notebook on demand.
#
# What we do here:
#   1. Confirm ASP and the python env are healthy.
#   2. Pre-fetch the small ASTER Zenodo archive so notebook 01 is instant.
#   3. Print a short "what now?" message into the terminal.

set -euo pipefail

# Codespaces invokes postCreateCommand through a login-interactive-shell env
# probe; conda's activation in ~/.bashrc can strip /opt/StereoPipeline/bin
# from PATH even though the image-level ENV directive includes it. Make PATH
# explicit here so this script doesn't depend on the shell wrapping.
#
# Order matters: the conda env's bin must come first because ASP bundles its
# own python at /opt/StereoPipeline/bin/python that has none of the conda
# env's packages (asp_plot, rasterio, etc.) — putting ASP first shadows
# `python` and breaks the asp_plot import check below.
export PATH="/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:${PATH:-/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin}"

echo "==> stereopipeline-quickstart postCreate.sh"

# ---- 1. Sanity check toolchain ----------------------------------------------
echo "--> ASP version:"
parallel_stereo --version || { echo "ERROR: parallel_stereo not on PATH"; exit 1; }

echo "--> asp_plot version:"
# Use the full conda env python explicitly — defensive against any PATH
# manipulation in lifecycle wrapping.
/opt/conda/envs/asp/bin/python -c "import asp_plot; print(asp_plot.__version__)"

# ---- 2. Pre-fetch ASTER demo data -------------------------------------------
DATA_DIR="${PWD}/data/aster_rainier"
mkdir -p "${DATA_DIR}"

if [[ ! -f "${DATA_DIR}/AST_L1A_00307312017190728_20200218153629_19952.zip" ]]; then
    echo "--> Pre-fetching ASTER Mt. Rainier scene from Zenodo..."
    curl -fL -o "${DATA_DIR}/AST_L1A_00307312017190728_20200218153629_19952.zip" \
        https://zenodo.org/record/7972223/files/AST_L1A_00307312017190728_20200218153629_19952.zip
    echo "--> Done: $(du -h "${DATA_DIR}"/*.zip | cut -f1) downloaded"
else
    echo "--> ASTER scene already present, skipping download"
fi

# ---- 3. Friendly hello -------------------------------------------------------
cat <<'EOF'

===============================================================

stereopipeline-quickstart
ASP + asp_plot, ready to go.

Next steps:
  1. Open notebooks/01_aster_rainier.ipynb and click "Run All".
     (Data is pre-fetched into data/aster_rainier/.)
  2. Or read docs/start/codespaces.md for an orientation tour.

===============================================================

EOF

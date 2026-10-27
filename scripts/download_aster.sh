#!/usr/bin/env bash
# Download the ASTER L1A Mt. Rainier scene from Zenodo.
#
# This is the same V003 archive used in asp_plot's existing ASTER tutorial:
#   https://zenodo.org/record/7972223
# It pre-dates NASA's Dec-2025 transition to V004 HDF format and is preserved
# on Zenodo for tutorials.
#
# Also fetches the tutorial's shipped data from a release of this repo: the
# ICESat-2 points and figure selections, and the Copernicus reference DEM for
# the processing window.
#
# Usage:
#   bash scripts/download_aster.sh                  # → ./data/aster_rainier/
#   bash scripts/download_aster.sh /custom/dir      # → /custom/dir/

set -euo pipefail

DEST="${1:-data/aster_rainier}"
mkdir -p "${DEST}"

ARCHIVE="AST_L1A_00307312017190728_20200218153629_19952.zip"
URL="https://zenodo.org/record/7972223/files/${ARCHIVE}"

if [[ -f "${DEST}/${ARCHIVE}" ]]; then
    echo "Archive already present at ${DEST}/${ARCHIVE} — skipping download."
else
    echo "Downloading ${ARCHIVE} from Zenodo (~45 MB)..."
    curl -fL -o "${DEST}/${ARCHIVE}" "${URL}"
fi

# Shipped data, attached to a release of this repo, so the tutorial needs no
# SlideRule request and no AWS fetch:
# - ICESat-2 ATL06-SR points and the report's figure selections from a
#   known-good run, in their own folder so a fresh SlideRule request can't
#   overwrite them (the sidecar's parquet_cache path is relative to notebooks/);
# - the Copernicus GLO-30 reference DEM over the processing window (T_PROJWIN in
#   the notebook) plus 2 km, with ellipsoid heights, made with fetch_cop_dem.py
#   (the release notes give the command).
# RELEASE records which release they came from: files from an older release
# (for example in a Codespace prebuilt before the data changed) are replaced.
DATA_TAG="aster-rainier-2026-10-27"
DATA_URL="https://github.com/uw-cryo/stereopipeline-quickstart/releases/download/${DATA_TAG}"
SHIPPED=(
    "aster_rainier_atl06sr_all.parquet icesat2_shipped/atl06sr_all.parquet"
    "aster_rainier_figure_selections.yml icesat2_shipped/figure_selections.yml"
    "aster_rainier_cop30.tif ref/cop30_rainier.tif"
)
mkdir -p "${DEST}/icesat2_shipped" "${DEST}/ref"
if [[ "$(cat "${DEST}/RELEASE" 2>/dev/null)" != "${DATA_TAG}" ]]; then
    for entry in "${SHIPPED[@]}"; do
        rm -f "${DEST}/${entry#* }" "${DEST}/${entry#* }.aux.xml"
    done
    rm -f "${DEST}/icesat2_shipped/RELEASE"
fi
for entry in "${SHIPPED[@]}"; do
    asset="${entry%% *}"
    target="${DEST}/${entry#* }"
    if [[ -f "${target}" ]]; then
        echo "Already have ${target} — skipping."
    else
        echo "Downloading ${asset} from the ${DATA_TAG} release..."
        curl -fL -o "${target}" "${DATA_URL}/${asset}"
    fi
done
echo "${DATA_TAG}" > "${DEST}/RELEASE"

# Extract into a subdirectory so aster2asp has a clean target.
EXTRACT_DIR="${DEST}/dataDir"
if [[ -d "${EXTRACT_DIR}" ]] && [[ -n "$(ls -A "${EXTRACT_DIR}")" ]]; then
    echo "Already extracted to ${EXTRACT_DIR} — skipping unzip."
else
    echo "Extracting to ${EXTRACT_DIR}..."
    mkdir -p "${EXTRACT_DIR}"
    # The zenodo zip contains a tar — we just dump everything into dataDir.
    cd "${DEST}"
    unzip -o "${ARCHIVE}" -d "$(basename "${EXTRACT_DIR}")"
fi

echo
echo "ASTER scene ready at ${DEST}/"
echo "Run aster2asp on dataDir to begin the tutorial."

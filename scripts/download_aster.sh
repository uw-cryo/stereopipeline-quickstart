#!/usr/bin/env bash
# Download the ASTER L1A Mt. Rainier scene from Zenodo.
#
# This is the same V003 archive used in asp_plot's existing ASTER tutorial:
#   https://zenodo.org/record/7972223
# It pre-dates NASA's Dec-2025 transition to V004 HDF format and is preserved
# on Zenodo for tutorials.
#
# Also fetches the shipped ICESat-2 data (from a release of this repo) and the
# Copernicus reference DEM for the tutorial's processing window.
#
# Usage:
#   bash scripts/download_aster.sh                  # → ./data/aster_rainier/
#   bash scripts/download_aster.sh /custom/dir      # → /custom/dir/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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

# ICESat-2 ATL06-SR points and figure selections from a known-good report run,
# attached to a release of this repo so the tutorial doesn't depend on SlideRule
# being up. The sidecar's parquet_cache path is relative to notebooks/. Kept in
# their own folder so a fresh SlideRule request can't overwrite them.
# RELEASE records which release they came from: files from an older release
# (for example in a Codespace prebuilt before the data changed) are replaced.
ICESAT2_TAG="icesat2-2026-10-26"
ICESAT2_URL="https://github.com/uw-cryo/stereopipeline-quickstart/releases/download/${ICESAT2_TAG}"
ICESAT2_DIR="${DEST}/icesat2_shipped"
mkdir -p "${ICESAT2_DIR}"
if [[ "$(cat "${ICESAT2_DIR}/RELEASE" 2>/dev/null)" != "${ICESAT2_TAG}" ]]; then
    rm -f "${ICESAT2_DIR}/atl06sr_all.parquet" "${ICESAT2_DIR}/figure_selections.yml" "${ICESAT2_DIR}/RELEASE"
fi
for name in atl06sr_all.parquet figure_selections.yml; do
    if [[ -f "${ICESAT2_DIR}/${name}" ]]; then
        echo "Already have ICESat-2 ${name} — skipping."
    else
        echo "Downloading ICESat-2 ${name} from the ${ICESAT2_TAG} release..."
        curl -fL -o "${ICESAT2_DIR}/${name}" "${ICESAT2_URL}/aster_rainier_${name}"
    fi
done
echo "${ICESAT2_TAG}" > "${ICESAT2_DIR}/RELEASE"

# Copernicus GLO-30 reference DEM for orthorectification and the report's
# difference map, clipped to the tutorial's processing window (T_PROJWIN in the
# notebook) plus a 2 km margin, with ellipsoid heights. fetch_cop_dem.py reads
# the tiles from AWS Open Data.
REF_DEM="${DEST}/ref/cop30_rainier.tif"
if [[ -f "${REF_DEM}" ]]; then
    echo "Already have the reference DEM ${REF_DEM} — skipping."
else
    echo "Fetching the Copernicus reference DEM from AWS..."
    "${PYTHON:-python}" "${SCRIPT_DIR}/fetch_cop_dem.py" \
        --bbox -122.015 46.682 -121.451 47.049 \
        --t-srs EPSG:32610 --tr 30 \
        --out "${REF_DEM}"
fi

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

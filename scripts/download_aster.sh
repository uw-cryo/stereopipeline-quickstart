#!/usr/bin/env bash
# Download the ASTER L1A Mt. Rainier scene from Zenodo.
#
# This is the same V003 archive used in asp_plot's existing ASTER tutorial:
#   https://zenodo.org/record/7972223
# It pre-dates NASA's Dec-2025 transition to V004 HDF format and is preserved
# on Zenodo for tutorials.
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
    echo "Downloading ${ARCHIVE} from Zenodo (~80 MB)..."
    curl -fL -o "${DEST}/${ARCHIVE}" "${URL}"
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

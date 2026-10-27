#!/usr/bin/env bash
# Download the SpaceNet CORE3D UCSD WorldView-3 stereo pair, plus the
# tutorial's shipped data.
#
# Pair (selected by asp_plot's UCSD scene-selection notebook):
#   - 2015-02-12, off-nadir 8.4°,  catid 1040010007A93700 (left)
#   - 2015-02-24, off-nadir 12.9°, catid 1040010007CA4D00 (right)
# Convergence angle 21°, B/H 0.37 — well-conditioned for natural terrain.
#
# The imagery comes from SpaceNet's public AWS bucket (spacenet-dataset), over
# plain HTTPS, so no AWS CLI or credentials are needed. It is IARPA CORE3D data,
# released for public research; publications using it should cite Hagstrom et
# al. (2021), "Cumulative assessment for urban 3d modeling", IGARSS. It is not
# re-hosted here: no licence we could find allows redistribution.
#
# The shipped ICESat-2 points and figure selections, and the Copernicus
# reference DEM for the scene, come from a release of this repo.
#
# Usage:
#   bash scripts/download_worldview_ucsd.sh          # → ./data/ucsd_stereo_21deg_12d/
#   bash scripts/download_worldview_ucsd.sh /path    # → /path/

set -euo pipefail

DEST="${1:-data/ucsd_stereo_21deg_12d}"
mkdir -p "${DEST}/images"

# Download a URL to a path via a .part file, so an interrupted download is never
# mistaken for a finished one.
fetch() {
    curl -fL -o "$2.part" "$1"
    mv "$2.part" "$2"
}

# Each scene is an .NTF (the image) plus a .tar of metadata holding the XML
# camera. The NTF is saved straight under its short name, <CATID>_P001.NTF; the
# XML is taken from the tar as <CATID>_P001.xml. The tar's XML has a different
# name from the S3 file, so it is found by order ID.
S3_BASE="https://spacenet-dataset.s3.amazonaws.com/Hosted-Datasets/CORE3D-Public-Data/Satellite-Images/UCSD/WV3/PAN"
SCENES=(
    "1040010007A93700 500647760030_01 12FEB15WV031300015FEB12183926-P1BS-500647760030_01_P001_________AAE_0AAAAABPABS0"
    "1040010007CA4D00 500647759040_01 24FEB15WV031300015FEB24183134-P1BS-500647759040_01_P001_________AAE_0AAAAABPABS0"
)
for scene in "${SCENES[@]}"; do
    read -r catid order stem <<< "${scene}"
    ntf="${DEST}/${catid}_P001.NTF"
    xml="${DEST}/${catid}_P001.xml"
    if [[ -f "${ntf}" ]]; then
        echo "Already have ${ntf} — skipping."
    else
        echo "Downloading ${catid} image (~880 MB) from SpaceNet..."
        fetch "${S3_BASE}/${stem}.NTF" "${ntf}"
    fi
    if [[ -f "${xml}" ]]; then
        echo "Already have ${xml} — skipping."
    else
        echo "Downloading ${catid} metadata from SpaceNet..."
        fetch "${S3_BASE}/${stem}.tar" "${DEST}/images/${stem}.tar"
        tar xf "${DEST}/images/${stem}.tar" -C "${DEST}/images"
        src=$(find "${DEST}/images/${order}" -iname "*${order}_P001.XML" | head -1 || true)
        if [[ -z "${src}" ]]; then
            echo "ERROR: no XML found under ${DEST}/images/${order}/ for ${catid}" >&2
            exit 1
        fi
        cp "${src}" "${xml}"
    fi
done

# Shipped data, attached to a release of this repo, so the tutorial needs no
# SlideRule request and no AWS fetch for its reference DEM:
# - ICESat-2 ATL06-SR points and the report's figure selections from a
#   known-good run, in their own folder so a fresh SlideRule request can't
#   overwrite them (the sidecar's parquet_cache path is relative to notebooks/);
# - the Copernicus GLO-30 reference DEM over the scene, with ellipsoid heights,
#   made with fetch_cop_dem.py (the release notes give the command and the
#   Copernicus notice).
# RELEASE records which release they came from: files from an older release
# (for example from an earlier version of this script) are replaced.
DATA_TAG="ucsd-wv3-2026-10-27"
DATA_URL="https://github.com/uw-cryo/stereopipeline-quickstart/releases/download/${DATA_TAG}"
SHIPPED=(
    "ucsd_atl06sr_all.parquet icesat2_shipped/atl06sr_all.parquet"
    "ucsd_figure_selections.yml icesat2_shipped/figure_selections.yml"
    "ucsd_cop30.tif ref/cop30_ucsd.tif"
)
mkdir -p "${DEST}/icesat2_shipped" "${DEST}/ref"
if [[ "$(cat "${DEST}/RELEASE" 2>/dev/null)" != "${DATA_TAG}" ]]; then
    for entry in "${SHIPPED[@]}"; do
        rm -f "${DEST}/${entry#* }" "${DEST}/${entry#* }.aux.xml"
    done
fi
for entry in "${SHIPPED[@]}"; do
    asset="${entry%% *}"
    target="${DEST}/${entry#* }"
    if [[ -f "${target}" ]]; then
        echo "Already have ${target} — skipping."
    else
        echo "Downloading ${asset} from the ${DATA_TAG} release..."
        fetch "${DATA_URL}/${asset}" "${target}"
    fi
done
echo "${DATA_TAG}" > "${DEST}/RELEASE"

echo
echo "WorldView-3 UCSD pair ready at ${DEST}/"
ls -lh "${DEST}"/*.NTF "${DEST}"/*.xml 2>/dev/null || true

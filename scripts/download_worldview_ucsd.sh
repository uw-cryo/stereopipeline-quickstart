#!/usr/bin/env bash
# Download WorldView-3 scenes of the SpaceNet UCSD stack (San Diego) for the
# WorldView tutorials, plus the tutorials' shipped data.
#
# Scenes (the three used by the tutorials; chosen in the cropped and full-scene
# benchmark studies of the SpaceNet UCSD stack):
#   - 104001000496A100, 2014-11-09, the near-nadir scene ("nadir")
#   - 10400100071D8800, 2015-01-24 ("n16"): with nadir, a 16.9° pair
#   - 10400100057DD500, 2014-12-23 ("n24"): 25.9° with nadir, 25.3° with n16
#
# The imagery comes from SpaceNet's public AWS bucket (spacenet-dataset), over
# plain HTTPS, so no AWS CLI or credentials are needed. It is IARPA CORE3D data,
# released for public research; publications using it should cite Hagstrom et
# al. (2021), "Cumulative assessment for urban 3d modeling", IGARSS. It is not
# re-hosted here: no license we could find allows redistribution.
#
# The shipped ICESat-2 points and figure selections, and the Copernicus
# reference DEM for the processing window, come from a release of this repo.
#
# Usage:
#   bash scripts/download_worldview_ucsd.sh                 # all three → ./data/ucsd_penasquitos/
#   bash scripts/download_worldview_ucsd.sh /path           # all three → /path/
#   bash scripts/download_worldview_ucsd.sh /path CATID...  # only these scenes

set -euo pipefail

DEST="${1:-data/ucsd_penasquitos}"
shift || true
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
    "104001000496A100 500647758070_01 09NOV14WV031300014NOV09182948-P1BS-500647758070_01_P001_________AAE_0AAAAABPABT0"
    "10400100071D8800 500647760080_01 24JAN15WV031300015JAN24183547-P1BS-500647760080_01_P001_________AAE_0AAAAABPABR0"
    "10400100057DD500 500647759010_01 23DEC14WV031300014DEC23182236-P1BS-500647759010_01_P001_________AAE_0AAAAABPABP0"
)
WANT=("$@")
for scene in "${SCENES[@]}"; do
    read -r catid order stem <<< "${scene}"
    if [[ ${#WANT[@]} -gt 0 && ! " ${WANT[*]} " =~ " ${catid} " ]]; then
        continue
    fi
    ntf="${DEST}/${catid}_P001.NTF"
    xml="${DEST}/${catid}_P001.xml"
    if [[ -f "${ntf}" ]]; then
        echo "Already have ${ntf} — skipping."
    else
        echo "Downloading ${catid} image (~870 MB) from SpaceNet..."
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

# Shipped data, attached to a release of this repo, so the tutorials need no
# SlideRule request and no AWS fetch for their reference DEM:
# - ICESat-2 ATL06-SR points over the processing window and each report's
#   figure selections from a known-good run, in their own folder so a fresh
#   SlideRule request can't overwrite them (the sidecars' parquet_cache path is
#   relative to notebooks/);
# - the Copernicus GLO-30 reference DEM over the window, with ellipsoid
#   heights, made with fetch_cop_dem.py (the release notes give the command and
#   the Copernicus notice).
# RELEASE records which release they came from: files from an older release
# (for example from an earlier version of this script) are replaced.
DATA_TAG="ucsd-penasquitos-2026-10-30"
DATA_URL="https://github.com/uw-cryo/stereopipeline-quickstart/releases/download/${DATA_TAG}"
SHIPPED=(
    "penasquitos_atl06sr_all.parquet icesat2_shipped/atl06sr_all.parquet"
    "penasquitos_pair_figure_selections.yml icesat2_shipped/pair_figure_selections.yml"
    "penasquitos_blend_figure_selections.yml icesat2_shipped/blend_figure_selections.yml"
    "penasquitos_cop30.tif ref/cop30_penasquitos.tif"
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
echo "WorldView-3 data ready at ${DEST}/"
ls -lh "${DEST}"/*.NTF "${DEST}"/*.xml 2>/dev/null || true

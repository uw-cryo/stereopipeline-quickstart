#!/usr/bin/env bash
# Download the SpaceNet CORE3D UCSD WorldView-3 stereo pair from AWS S3.
#
# Pair (selected by asp_plot's UCSD scene-selection notebook):
#   - 2015-02-12, off-nadir 8.4°,  catid 1040010007A93700 (left)
#   - 2015-02-24, off-nadir 12.9°, catid 1040010007CA4D00 (right)
# Convergence angle 21°, B/H 0.37 — well-conditioned for natural terrain.
#
# Public AWS bucket; --no-sign-request means no AWS credentials needed.
#
# Usage:
#   bash scripts/download_worldview_ucsd.sh          # → ./data/ucsd_stereo_21deg_12d/
#   bash scripts/download_worldview_ucsd.sh /path    # → /path/

set -euo pipefail

DEST="${1:-data/ucsd_stereo_21deg_12d}"
IMAGES_DIR="${DEST}/images"
mkdir -p "${IMAGES_DIR}"

S3_BASE="s3://spacenet-dataset/Hosted-Datasets/CORE3D-Public-Data/Satellite-Images/UCSD/WV3/PAN"

# Each scene comes as an .NTF (image) plus a .tar (metadata + IMD/XML).
# Note: the AAE_0AAAAABPABS0 string is part of the canonical filename.
SCENES=(
  "12FEB15WV031300015FEB12183926-P1BS-500647760030_01_P001_________AAE_0AAAAABPABS0"
  "24FEB15WV031300015FEB24183134-P1BS-500647759040_01_P001_________AAE_0AAAAABPABS0"
)

for stem in "${SCENES[@]}"; do
    for ext in NTF tar; do
        target="${IMAGES_DIR}/${stem}.${ext}"
        if [[ -f "${target}" ]]; then
            echo "Already have ${stem}.${ext} — skipping."
            continue
        fi
        echo "Downloading ${stem}.${ext}..."
        aws s3 --no-sign-request cp "${S3_BASE}/${stem}.${ext}" "${IMAGES_DIR}/"
    done
done

# Extract each tar (gives us the .IMD file with RPCs and the catalog .XML).
echo "Extracting metadata tars..."
cd "${IMAGES_DIR}"
for f in *.tar; do
    tar xf "${f}"
done

# Re-organize at the top level: rename to <CATID>_P001.{NTF,xml} so the ASP
# command lines stay short and human-readable. This matches the convention used
# in asp_plot's notebooks.
#
# Note: the .NTF lives at IMAGES_DIR/<aws_stem>.NTF (downloaded directly from
# S3), but the .XML is buried inside the extracted tar with a *different*
# inner filename. We look it up by order ID (the only token that's consistent
# between the AWS filename and the inner XML filename).
cd "${OLDPWD}"
declare -A AWS_STEM=(
  ["1040010007A93700"]="12FEB15WV031300015FEB12183926-P1BS-500647760030_01_P001_________AAE_0AAAAABPABS0"
  ["1040010007CA4D00"]="24FEB15WV031300015FEB24183134-P1BS-500647759040_01_P001_________AAE_0AAAAABPABS0"
)
declare -A ORDER_ID=(
  ["1040010007A93700"]="500647760030_01"
  ["1040010007CA4D00"]="500647759040_01"
)

for catid in "${!AWS_STEM[@]}"; do
    ntf_src="${IMAGES_DIR}/${AWS_STEM[$catid]}.NTF"
    [[ -f "${ntf_src}" ]] && cp -n "${ntf_src}" "${DEST}/${catid}_P001.NTF"

    order="${ORDER_ID[$catid]}"
    xml_src=$(find "${IMAGES_DIR}/${order}" -iname "*${order}_P001.XML" | head -1 || true)
    if [[ -n "${xml_src}" && -f "${xml_src}" ]]; then
        cp -n "${xml_src}" "${DEST}/${catid}_P001.xml"
    else
        echo "WARNING: no XML found under ${IMAGES_DIR}/${order}/ for ${catid}" >&2
    fi
done

echo
echo "WorldView-3 UCSD pair ready at ${DEST}/"
ls -lh "${DEST}"/*.NTF "${DEST}"/*.xml 2>/dev/null || true

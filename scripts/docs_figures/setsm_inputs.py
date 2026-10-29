"""Make a folder SETSM can run on from Tutorial 2's cropped images.

    python scripts/docs_figures/setsm_inputs.py <wv run> <output folder>

<wv run> is the top folder of a checkout where Tutorial 2 has run (it holds
notebooks/ and data/). Copies each crop (data/ucsd_soledad/crops/<catid>_P001.tif)
to the output folder, with a camera file SETSM accepts next to it.

SETSM reads more than the RPC from a WorldView camera file. cam2rpc writes
only the RPC block (<RPB>), so from the file alone SETSM found no overlap: it
takes the image corners from the <BAND_P> block to pick the UTM zone (without
them it chose zone 31 south), the pixel size and satellite ID from <IMAGE>,
and the RPC error terms, which cam2rpc writes as 0. This adds those blocks:
the corners from the crop's own RPC, the pixel sizes from the vendor's XML
times the crop's averaging factor, and the rest copied from the vendor's XML.
"""
import re
import shutil
import sys
from pathlib import Path

from osgeo import gdal

gdal.UseExceptions()

SCENES = ["104001000496A100", "10400100071D8800"]
FACTOR = 4   # the crops average FACTOR x FACTOR pixels (Tutorial 2's FACTOR)
IMAGE_TAGS = ["SATID", "FIRSTLINETIME", "ABSCALFACTOR", "EFFECTIVEBANDWIDTH", "TDILEVEL",
              "MEANPRODUCTGSD", "MEANPRODUCTROWGSD", "MEANPRODUCTCOLGSD",
              "MEANCOLLECTEDGSD", "MEANCOLLECTEDROWGSD", "MEANCOLLECTEDCOLGSD",
              "MEANSATAZ", "MEANSATEL", "MEANSUNAZ", "MEANSUNEL",
              "MEANINTRACKVIEWANGLE", "MEANCROSSTRACKVIEWANGLE", "MEANOFFNADIRVIEWANGLE"]
BAND_TAGS = ["ABSCALFACTOR", "EFFECTIVEBANDWIDTH", "TDILEVEL"]


def tag(xml, name):
    return re.search(f"<{name}>([^<]*)<", xml).group(1).strip()


def element(name, value):
    return f"\t\t\t<{name}>{value}</{name}>\n"


def corners(tif):
    """UL, UR, LR, LL corners of the image as (lon, lat), from its RPC at the RPC's reference height."""
    ds = gdal.Open(str(tif))
    height = float(ds.GetMetadata("RPC")["HEIGHT_OFF"])
    transformer = gdal.Transformer(ds, None, ["METHOD=RPC", f"RPC_HEIGHT={height}"])
    w, h = ds.RasterXSize, ds.RasterYSize
    out = {}
    for name, (px, py) in (("UL", (0, 0)), ("UR", (w, 0)), ("LR", (w, h)), ("LL", (0, h))):
        _, (lon, lat, _) = transformer.TransformPoint(0, px, py, 0)
        out[name] = (lon, lat)
    return out, height


def main():
    data = Path(sys.argv[1]) / "data/ucsd_soledad"
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for catid in SCENES:
        vendor = (data / f"{catid}_P001.xml").read_text()
        crop_xml = (data / f"crops/{catid}_P001.xml").read_text()
        tif = data / f"crops/{catid}_P001.tif"

        band = "\t\t<BAND_P>\n"
        points, height = corners(tif)
        for name, (lon, lat) in points.items():
            band += element(f"{name}LON", f"{lon:.15e}") + element(f"{name}LAT", f"{lat:.15e}") + element(f"{name}HAE", f"{height:.15e}")
        band += "".join(element(t, tag(vendor, t)) for t in BAND_TAGS) + "\t\t</BAND_P>\n"

        image = "\t\t<IMAGE>\n"
        for t in IMAGE_TAGS:
            value = tag(vendor, t)
            if "GSD" in t:
                value = f"{float(value) * FACTOR:.3f}"
            image += element(t, value)
        image += "\t\t</IMAGE>\n"

        xml = crop_xml.replace("<isd>\n", "<isd>\n\t<IMD>\n" + band + image + "\t</IMD>\n", 1)
        for t in ("ERRBIAS", "ERRRAND"):
            xml = re.sub(f"<{t}>0</{t}>", f"<{t}>{tag(vendor, t)}</{t}>", xml)
        (out / f"{catid}_P001.xml").write_text(xml)
        shutil.copy(tif, out / f"{catid}_P001.tif")
        print(f"wrote {out / catid}_P001.tif and .xml")


if __name__ == "__main__":
    main()

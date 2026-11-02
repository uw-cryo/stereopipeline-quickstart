"""Make the scene maps at the top of each tutorial: the input scenes on a map, with the area the tutorial processes outlined.

The maps are made once, here, and committed to docs/tutorials/figures/; the
notebooks show the PNGs and make no requests while they run.

WorldView (Tutorials 2 and 3): the RGB browse image of each scene
(*-BROWSE.JPG, about 800 x 870 pixels for the whole scene, about 17 m per
pixel). It comes in the metadata tar of the scene's multispectral (M1BS)
order in SpaceNet's public bucket, the same order as the panchromatic image
the tutorials download (about 2 MB per tar; no account or key). The browse
image is in the image's own pixel grid. It is placed on the map with the
multispectral image's RPC camera (.RPB, scaled to the browse image's size) at
the RPCs' reference height, and warped to UTM zone 11N. Over the canyon the
ground is within about 100 m of that height, which moves the outline by less
than two browse pixels.

ASTER (Tutorial 1): the full nadir image (band 3N, from aster2asp) orthorectified
at 60 m onto a Copernicus 30 m DEM of the whole scene with ASP's mapproject.

Each figure has a location map on the left, about 300-400 km across, with the
scenes' extent outlined; the scenes are drawn over Esri's World Topo Map, which
shows past their edges.

Run from the repository's top folder on a laptop, with ASP on PATH and in the
environment the notebooks use, after Tutorial 1 has run (it needs
data/aster_rainier/out-Band3N.tif and .xml under --aster-run):

    python scripts/docs_figures/make_scene_maps.py --aster-run <checkout> --work <scratch dir>

Writes docs/tutorials/figures/aster-scene-map.png, wv3-scene-maps-pair.png
(Tutorial 2) and wv3-scene-maps-three.png (Tutorial 3), or to --out. Downloads
and intermediate files go to --work; finished steps are skipped on a rerun.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects
import contextily as cx
import numpy as np
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from osgeo import gdal

gdal.UseExceptions()

REPO = Path(__file__).resolve().parents[2]
DPI = 110   # keeps each PNG near 1 MB; the notebooks show them about 1000 px wide
FRAME = "#c8c8c0"     # light gray map frame, as in make_figures.py
OUTLINE = "#ff3b30"   # the processed area
BASEMAP = cx.providers.Esri.WorldTopoMap

# The WorldView scenes: catalog ID, date, view angle from straight down (as in
# the tutorials' tables), and the multispectral order's metadata tar.
S3 = "https://spacenet-dataset.s3.amazonaws.com/Hosted-Datasets/CORE3D-Public-Data/Satellite-Images/UCSD/WV3/MSI"
WV = {
    "104001000496A100": ("2014-11-09", "1.1°", "14NOV09182948-M1BS-500647758070_01_P001"),
    "10400100071D8800": ("2015-01-24", "16.3°", "15JAN24183547-M1BS-500647760080_01_P001"),
    "10400100057DD500": ("2014-12-23", "24.1°", "14DEC23182236-M1BS-500647759010_01_P001"),
}
WV_SRS = "EPSG:32611"
WV_SQUARE = (480420, 3641720, 481420, 3642720)   # Tutorials 2 and 3, xmin ymin xmax ymax

ASTER_SRS = "EPSG:32610"
ASTER_WINDOW = (577305, 5172975, 615705, 5209035)   # Tutorial 1
# The scene's extent from the band 3N latitude/longitude lattice in the L1A
# granule (46.45-47.19 N, 122.37-121.33 W), plus a margin.
ASTER_BBOX = (-122.43, 46.40, -121.27, 47.25)


def browse_on_map(catid, work):
    """The scene's browse image warped to UTM 11N, as an RGB GeoTIFF path."""
    out = work / f"{catid}_browse_utm.tif"
    if out.exists():
        return out
    stem = WV[catid][2]
    tar_path = work / f"{stem}.tar"
    if not tar_path.exists():
        print(f"downloading {stem}.tar")
        urllib.request.urlretrieve(f"{S3}/{stem}.tar", tar_path)
    with tarfile.open(tar_path) as tar:
        members = {Path(m.name).name: m for m in tar.getmembers()}
        jpg = work / f"{catid}_browse.jpg"
        jpg.write_bytes(tar.extractfile(members[f"{stem}-BROWSE.JPG"]).read())
        rpb = tar.extractfile(members[f"{stem}.RPB"]).read().decode()

    def value(key):
        return re.search(rf"\b{key} = ([^;]+);", rpb).group(1).strip()

    # The browse image covers the image itself, whose center the RPC offsets
    # give. The IMD's numRows and numColumns (12288 x 11264 for the first
    # scene) are larger: the NTF is padded to whole 1024-pixel JPEG2000 tiles.
    # Scaling by them put the browse image about 600 m east of where it
    # belongs. From the RPC offsets, both axes scale alike (13.28 for the
    # first scene), which checks the assumption.
    rows = 2 * float(value("lineOffset")) + 1
    cols = 2 * float(value("sampOffset")) + 1
    src = gdal.Open(str(jpg))
    sy, sx = rows / src.RasterYSize, cols / src.RasterXSize
    assert abs(sy / sx - 1) < 0.01, f"{catid}: browse scales {sy:.2f} (rows) and {sx:.2f} (columns) differ"

    def coeffs(key):
        block = re.search(rf"{key} = \((.*?)\);", rpb, re.S).group(1)
        return " ".join(block.replace(",", " ").split())

    # RPC line/sample are pixel centers counted from 0; a browse pixel holds
    # s x s full-size pixels, so its center is at (full + 0.5) / s - 0.5.
    rpc = {
        "LINE_OFF": str((float(value("lineOffset")) + 0.5) / sy - 0.5),
        "SAMP_OFF": str((float(value("sampOffset")) + 0.5) / sx - 0.5),
        "LINE_SCALE": str(float(value("lineScale")) / sy),
        "SAMP_SCALE": str(float(value("sampScale")) / sx),
        "LAT_OFF": value("latOffset"), "LONG_OFF": value("longOffset"), "HEIGHT_OFF": value("heightOffset"),
        "LAT_SCALE": value("latScale"), "LONG_SCALE": value("longScale"), "HEIGHT_SCALE": value("heightScale"),
        "LINE_NUM_COEFF": coeffs("lineNumCoef"), "LINE_DEN_COEFF": coeffs("lineDenCoef"),
        "SAMP_NUM_COEFF": coeffs("sampNumCoef"), "SAMP_DEN_COEFF": coeffs("sampDenCoef"),
    }
    with_rpc = gdal.Translate("", src, format="MEM")
    with_rpc.SetMetadata(rpc, "RPC")
    gdal.Warp(str(out), with_rpc, dstSRS=WV_SRS, xRes=15, yRes=15, rpc=True,
              transformerOptions=[f"RPC_HEIGHT={value('heightOffset')}"],
              resampleAlg="bilinear", dstNodata=0, creationOptions=["COMPRESS=DEFLATE"])
    return out


def aster_on_map(aster_run, work):
    """Tutorial 1's full band 3N image orthorectified at 60 m, as a GeoTIFF path."""
    out = work / "aster_band3N_60m.tif"
    if out.exists():
        return out
    data = Path(aster_run) / "data/aster_rainier"
    dem = work / "cop30_aster_scene.tif"
    if not dem.exists():
        subprocess.run([sys.executable, str(REPO / "scripts/fetch_cop_dem.py"),
                        "--bbox", *map(str, ASTER_BBOX), "--t-srs", ASTER_SRS, "--tr", "30",
                        "--out", str(dem)], check=True)
    subprocess.run(["mapproject", "--t_srs", ASTER_SRS, "--tr", "60", str(dem),
                    str(data / "out-Band3N.tif"), str(data / "out-Band3N.xml"), str(out)], check=True)
    return out


def read_map(path):
    """The raster's bands as (rows, cols, bands) with no data as NaN, and its extent for imshow."""
    ds = gdal.Open(str(path))
    a = np.dstack([ds.GetRasterBand(b + 1).ReadAsArray().astype(float) for b in range(ds.RasterCount)])
    nodata = ds.GetRasterBand(1).GetNoDataValue()
    if nodata is not None:
        a[np.all(a == nodata, axis=2)] = np.nan
    gt = ds.GetGeoTransform()
    extent = (gt[0], gt[0] + gt[1] * ds.RasterXSize, gt[3] + gt[5] * ds.RasterYSize, gt[3])
    return a, extent


def rgba(a):
    """Each band from its 2nd to 98th percentile to 0-1, gray if one band, transparent where there is no data."""
    out = np.empty(a.shape[:2] + (4,))
    for b in range(3):
        band = a[..., min(b, a.shape[2] - 1)]
        lo, hi = np.nanpercentile(band, (2, 98))
        out[..., b] = np.clip((band - lo) / (hi - lo), 0, 1)
    out[..., 3] = ~np.isnan(a).all(axis=2)
    return np.nan_to_num(out)


def frame(ax, title):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(FRAME)
    ax.set_title(title, fontsize=11)


def basemap(ax, srs, zoom="auto"):
    """Esri's World Topo Map under whatever the axes show, with its attribution."""
    cx.add_basemap(ax, crs=srs, source=BASEMAP, zoom=zoom, attribution_size=5, zorder=0)


def draw_scene(ax, path, srs, box, box_label, bar_km, title, bounds):
    """The scene over the basemap, the processed area outlined, a scale bar."""
    a, extent = read_map(path)
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])
    basemap(ax, srs)
    ax.imshow(rgba(a), extent=extent, interpolation="bilinear", zorder=2)
    xmin, ymin, xmax, ymax = box
    ax.add_patch(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=False, edgecolor=OUTLINE,
                           linewidth=1.8, zorder=3))
    ax.annotate(box_label, (xmin, ymax), xytext=(0, 4), textcoords="offset points",
                color=OUTLINE, fontsize=9, fontweight="bold", zorder=3,
                path_effects=[patheffects.withStroke(linewidth=2.5, foreground="white")])
    ax.add_artist(AnchoredSizeBar(ax.transData, bar_km * 1000, f"{bar_km} km", "lower right",
                                  pad=0.5, borderpad=0.8, sep=4, frameon=True, size_vertical=bar_km * 1000 / 25))
    frame(ax, title)


def draw_context(ax, srs, scene, half_km, bar_km):
    """A map about 2 x half_km across, centered on the scene, with the scene's outline."""
    cxm, cym = (scene[0] + scene[2]) / 2, (scene[1] + scene[3]) / 2
    ax.set_xlim(cxm - half_km * 1000, cxm + half_km * 1000)
    ax.set_ylim(cym - half_km * 1000, cym + half_km * 1000)
    basemap(ax, srs)
    ax.add_patch(Rectangle((scene[0], scene[1]), scene[2] - scene[0], scene[3] - scene[1], fill=False,
                           edgecolor=OUTLINE, linewidth=1.8, zorder=3))
    ax.add_artist(AnchoredSizeBar(ax.transData, bar_km * 1000, f"{bar_km} km", "lower right",
                                  pad=0.5, borderpad=0.8, sep=4, frameon=True, size_vertical=bar_km * 1000 / 25))
    ax.set_aspect("equal")
    frame(ax, "Location")


def union(extents, margin):
    """The union of imshow extents (xmin, xmax, ymin, ymax), widened by `margin` meters, as xmin ymin xmax ymax."""
    return (min(e[0] for e in extents) - margin, min(e[2] for e in extents) - margin,
            max(e[1] for e in extents) + margin, max(e[3] for e in extents) + margin)


def wv_maps(catids, work, out, name):
    paths = [browse_on_map(c, work) for c in catids]
    scenes = union([read_map(p)[1] for p in paths], 0)
    # One extent for every panel: the union of the scenes, plus 2 km of basemap.
    bounds = union([read_map(p)[1] for p in paths], 2000)
    fig, axes = plt.subplots(1, len(catids) + 1, figsize=(4.4 * (len(catids) + 1), 5.2),
                             gridspec_kw={"width_ratios": [1] * (len(catids) + 1)})
    draw_context(axes[0], WV_SRS, scenes, 150, 50)
    for ax, catid, path in zip(axes[1:], catids, paths):
        date, angle = WV[catid][:2]
        draw_scene(ax, path, WV_SRS, WV_SQUARE, "1 km", 2, f"{date}, {angle} from straight down\n{catid}", bounds)
    fig.tight_layout()
    save(fig, out, name)


def aster_map(aster_run, work, out):
    path = aster_on_map(aster_run, work)
    scene = union([read_map(path)[1]], 0)
    bounds = union([read_map(path)[1]], 5000)
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.6), gridspec_kw={"width_ratios": [1, 1.25]})
    draw_context(axes[0], ASTER_SRS, scene, 200, 50)
    draw_scene(axes[1], path, ASTER_SRS, ASTER_WINDOW, "processing window", 10,
               "ASTER band 3N (near infrared, nadir), 2017-07-31", bounds)
    fig.tight_layout()
    save(fig, out, "aster-scene-map")


def save(fig, out, name):
    fig.savefig(out / f"{name}.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out / name}.png")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--aster-run", required=True, help="checkout whose data/aster_rainier/ holds Tutorial 1's out-Band3N.tif/.xml")
    p.add_argument("--work", required=True, help="folder for downloads and intermediate files")
    p.add_argument("--out", default=str(REPO / "docs/tutorials/figures"))
    args = p.parse_args()
    work, out = Path(args.work), Path(args.out)
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    wv_maps(["104001000496A100", "10400100071D8800"], work, out, "wv3-scene-maps-pair")
    wv_maps(["104001000496A100", "10400100071D8800", "10400100057DD500"], work, out, "wv3-scene-maps-three")
    aster_map(args.aster_run, work, out)


if __name__ == "__main__":
    main()

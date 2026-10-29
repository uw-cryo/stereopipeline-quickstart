"""Remake the data-backed figures in docs/concepts/figures/ from local tutorial runs.

Run Tutorials 1, 2 and 3 locally (Run All in each notebook), then the two
extra runs these figures need, then this script, from the repository's top folder
in the environment the notebooks use:

    bash scripts/docs_figures/run_aster_raw.sh <aster run> <extra>/aster_raw
    bash scripts/docs_figures/run_aster_align.sh <aster run> <extra>/aster_align
    bash scripts/docs_figures/run_comparisons.sh <wv run> <extra>
    python scripts/docs_figures/make_figures.py --aster-run <aster run> --wv-run <wv run> --extra <extra>

<aster run> and <wv run> are the top folders of the checkouts the tutorials
ran in (each holds notebooks/ and data/); they can be the same folder. Writes
one PNG per figure to docs/concepts/figures/ (the comparison hillshades to
docs/comparisons/figures/), or to --out. --only makes just
the named figures, e.g. --only wv3-stereo-geometry.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

FRAME = "#c8c8c0"   # light gray map frame, as in the earlier figures
DPI = 150

# Tutorial 2's pair, left then right, and its map projection (UTM zone 11N).
WV_SCENES = ["104001000496A100", "10400100071D8800"]
WV_SRS = "EPSG:32611"
# Tutorial 1's processing window, UTM zone 10N.
ASTER_SRS = "EPSG:32610"
ASTER_WINDOW = (577305, 5172975, 615705, 5209035)


def read(path, band=1, step=1):
    """One band as float, with no-data as NaN, every `step` pixels."""
    ds = gdal.Open(str(path))
    b = ds.GetRasterBand(band)
    a = b.ReadAsArray(buf_xsize=ds.RasterXSize // step, buf_ysize=ds.RasterYSize // step).astype(float)
    nodata = b.GetNoDataValue()
    if nodata is not None:
        a[a == nodata] = np.nan
    return a


def warp(path, like):
    """`path` resampled onto the grid of `like` (same CRS, extent and pixel size), as a MEM dataset."""
    ref = gdal.Open(str(like))
    gt = ref.GetGeoTransform()
    bounds = (gt[0], gt[3] + gt[5] * ref.RasterYSize, gt[0] + gt[1] * ref.RasterXSize, gt[3])
    return gdal.Warp("", str(path), format="MEM", dstSRS=ref.GetProjection(), outputBounds=bounds,
                     width=ref.RasterXSize, height=ref.RasterYSize, resampleAlg="bilinear",
                     dstNodata=np.nan, outputType=gdal.GDT_Float32)


def hillshade(dem):
    """Hillshade of a DEM path or dataset, with no-data as NaN."""
    shade = gdal.DEMProcessing("", dem, "hillshade", format="MEM", computeEdges=True)
    a = shade.GetRasterBand(1).ReadAsArray().astype(float)
    a[a == shade.GetRasterBand(1).GetNoDataValue()] = np.nan
    return a


def map_axes(ax, title=None, **title_kw):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(FRAME)
    if title:
        ax.set_title(title, **title_kw)


def show_hillshade(ax, a, title=None, **title_kw):
    cmap = plt.get_cmap("gray").copy()
    cmap.set_bad("white")
    ax.imshow(a, cmap=cmap, vmin=0, vmax=255, interpolation="none")
    map_axes(ax, title, **title_kw)


def save(fig, out, name):
    fig.savefig(out / f"{name}.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out / name}.png")


def disparity(prefix, step=1):
    """Horizontal and vertical disparity from <prefix>-F.tif, valid pixels only, as two 1-D arrays."""
    dx, dy, valid = (read(f"{prefix}-F.tif", b, step) for b in (1, 2, 3))
    keep = valid > 0
    return dx[keep], dy[keep], keep


def in_window(prefix, step, srs, window):
    """Mask of <prefix>-PC.tif pixels whose point falls inside `window` (xmin ymin xmax ymax in `srs`)."""
    from pyproj import Transformer

    ds = gdal.Open(f"{prefix}-PC.tif")
    offset = [float(v) for v in ds.GetMetadata().get("POINT_OFFSET", "0 0 0").split()]
    x, y, z = (read(f"{prefix}-PC.tif", b, step) + o for b, o in zip((1, 2, 3), offset))
    e, n = Transformer.from_crs("EPSG:4978", srs, always_xy=True).transform(x, y, z)[:2]
    return (e >= window[0]) & (e <= window[2]) & (n >= window[1]) & (n <= window[3])


# --- Orthorectification page -------------------------------------------------

def aster_disparity_hist(aster, raw, out):
    """Disparity about its median, raw vs orthorectified ASTER, over Tutorial 1's window."""
    step = 2
    raw_dx, raw_dy, keep = disparity(raw / "run", step)
    # The raw run matched the whole scene; keep the pixels inside the window.
    inside = in_window(raw / "run", step, ASTER_SRS, ASTER_WINDOW)
    h, w = keep.shape
    inside = inside[:h, :w][keep]
    raw_dx, raw_dy = raw_dx[inside], raw_dy[inside]
    ortho_dx, ortho_dy, _ = disparity(aster / "stereo/run", step)

    centred = [(d - np.median(d)) for d in (raw_dx, raw_dy, ortho_dx, ortho_dy)]
    limit = np.ceil(max(np.abs(c).max() for c in centred))
    bins = np.linspace(-limit, limit, 121)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), sharex=True, sharey=True, constrained_layout=True)
    for ax, (dx, dy), title in zip(axes, (centred[:2], centred[2:]), ("Raw images", "Orthorectified images")):
        for d, label, color in ((dx, "horizontal", "#2a78d6"), (dy, "vertical", "#f0a830")):
            ax.hist(d, bins=bins, color=color, alpha=0.85, label=label)
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_xlabel("Disparity about the median (px)")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Pixels")
    axes[0].legend(frameon=False)
    print(f"  raw dx spread (p1-p99): {np.ptp(np.percentile(raw_dx, [1, 99])):.1f} px, "
          f"ortho: {np.ptp(np.percentile(ortho_dx, [1, 99])):.1f} px")
    save(fig, out, "aster-disparity-hist")


def aster_raw_vs_ortho_hillshade(aster, raw, out):
    """Hillshades of the raw and orthorectified ASTER DEMs on the same 30 m grid."""
    raw_dem = raw / "run-DEM.tif"
    ortho = warp(aster / "stereo/run-DEM.tif", raw_dem)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.2), constrained_layout=True)
    show_hillshade(axes[0], hillshade(str(raw_dem)), "Raw images")
    show_hillshade(axes[1], hillshade(ortho), "Orthorectified images")
    save(fig, out, "aster-raw-vs-ortho-hillshade")


# --- Alignment page ----------------------------------------------------------

def minus_reference(dem, reference):
    """DEM minus a reference DEM resampled onto its grid."""
    ref = warp(reference, dem)
    return read(dem) - ref.GetRasterBand(1).ReadAsArray()


def dh_before_after_alignment(aster, extra, out):
    """Tutorial 1's DEM minus COP30, before and after aligning it to COP30 with pc_align."""
    log = next((extra / "aster_align").glob("run-log-pc_align-*.txt")).read_text()
    shift = float(log.split("Translation vector magnitude (meters):")[1].split()[0])
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), constrained_layout=True)
    for ax, dem, title in (
        (axes[0], aster / "stereo/run-DEM.tif", "ASTER tutorial DEM − COP30, before alignment"),
        (axes[1], extra / "aster_align/run-trans_source-DEM.tif", f"After pc_align to COP30 (a rigid shift of {shift:.0f} m)"),
    ):
        dh = minus_reference(dem, aster / "ref/cop30_rainier.tif")
        median = np.nanmedian(dh)
        nmad = 1.4826 * np.nanmedian(np.abs(dh - median))
        cmap = plt.get_cmap("RdBu_r").copy()
        cmap.set_bad("white")
        im = ax.imshow(dh, cmap=cmap, vmin=-30, vmax=30, interpolation="none")
        map_axes(ax, f"{title}\n(median {median:+.1f} m, NMAD {nmad:.1f} m)", fontsize=10)
        fig.colorbar(im, ax=ax, shrink=0.85, label="Elevation difference (m)")
    save(fig, out, "dh-before-after-alignment")


# --- Stereo photogrammetry page ----------------------------------------------

def wv3_stereo_geometry(wv_run, out):
    """asp_plot's skyplot and footprint map for Tutorial 2's pair."""
    import contextily
    from asp_plot.stereo_geometry import StereoGeometryPlotter

    cache = wv_run / "data/basemap_cache"
    if cache.is_dir():
        contextily.set_cache_dir(str(cache))
    data = wv_run / "data/ucsd_soledad"
    StereoGeometryPlotter(inputs=[str(data / f"{c}_P001.xml") for c in WV_SCENES]).stereo_geom_plot()
    # asp_plot's five-line header overlaps the top of a tall map; push the axes down.
    fig = plt.gcf()
    fig.subplots_adjust(top=0.78)
    save(fig, out, "wv3-stereo-geometry")


# Tutorial 3's pair with the most failed pixels (about 10%; the others 2-4%).
WV_FAILURE_PAIR = "10400100057DD500_10400100071D8800"


def goodpixelmap_failures(raw, wv, out):
    """GoodPixelMaps (gray matched, red failed) of two runs on images that were not orthorectified.

    Tutorials 1 and 2 orthorectify first and fail almost nowhere, so the maps
    come from the raw ASTER run and one of Tutorial 3's pairs.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.2), constrained_layout=True)
    for ax, prefix, title in ((axes[0], raw / "run", "ASTER, Mount Rainier, raw images"),
                              (axes[1], wv / "pairs" / WV_FAILURE_PAIR / "run", "WorldView-3, Mount Soledad, Tutorial 3 pair")):
        ds = gdal.Open(f"{prefix}-GoodPixelMap.tif")
        rgb = np.dstack([ds.GetRasterBand(b).ReadAsArray() for b in (1, 2, 3)])
        ax.imshow(rgb, interpolation="none")
        map_axes(ax, title)
    save(fig, out, "goodpixelmap-failures")


# --- Pipeline overview page --------------------------------------------------

def wv3_disparity_dem(wv, out):
    """Tutorial 2's horizontal disparity and the hillshaded DEM it becomes."""
    dx = read(wv / "stereo/run-F.tif", 1)
    dx[read(wv / "stereo/run-F.tif", 3) == 0] = np.nan
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), constrained_layout=True)
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("white")
    low, high = np.nanpercentile(dx, [2, 98])
    im = axes[0].imshow(dx, cmap=cmap, vmin=low, vmax=high, interpolation="none")
    map_axes(axes[0], "Disparity map (run-F.tif, horizontal)", fontsize=10)
    fig.colorbar(im, ax=axes[0], shrink=0.85, label="Disparity (px)")
    show_hillshade(axes[1], hillshade(str(wv / "stereo/run-DEM.tif")), "Hillshaded DEM (run-DEM.tif)", fontsize=10)
    save(fig, out, "wv3-disparity-dem")


# --- Bundle adjustment page --------------------------------------------------

def ba_residuals(wv):
    from asp_plot.bundle_adjust import ReadBundleAdjustFiles

    return ReadBundleAdjustFiles(str(wv), "ba").get_initial_final_residuals_gdfs()


def wv3_ba_residuals_hist(wv, out):
    """Histograms of the mean reprojection residual per tie point, before and after bundle adjustment."""
    initial, final = (g["mean_residual"].to_numpy() for g in ba_residuals(wv))
    limit = np.ceil(np.percentile(initial, 99))
    bins = np.linspace(0, limit, 61)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.2), sharex=True, sharey=True, constrained_layout=True)
    for ax, r, title in ((axes[0], initial, "Initial residuals"), (axes[1], final, "Final residuals")):
        ax.hist(np.clip(r, 0, limit), bins=bins, color="#2a78d6")
        median = np.median(r)
        ax.axvline(median, color="#e04040")
        ax.text(median, 0.95, f"  median {median:.2f} px", color="#e04040",
                transform=ax.get_xaxis_transform(), va="top")
        over = (r >= limit).sum()
        if over:
            ax.text(0.97, 0.75, f"≥ {limit:g} px\n({over} points)", color="#555555", ha="right",
                    transform=ax.transAxes)
        ax.set_title(title)
        ax.set_xlabel("Mean reprojection residual (px)")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Tie points")
    save(fig, out, "wv3-ba-residuals-hist")


def wv3_ba_residuals_map(wv, out):
    """asp_plot's map of the residuals per tie point, before and after, over satellite imagery.

    A linear color scale shared by the two panels, in UTM, over Esri World
    Imagery at half opacity (with its attribution).
    """
    import contextily
    from asp_plot.bundle_adjust import PlotBundleAdjustFiles

    PlotBundleAdjustFiles(list(ba_residuals(wv)), lognorm=False).plot_n_gdfs(
        column_name="mean_residual", cbar_label="Mean residual (px)", common_clim=True,
        map_crs=WV_SRS, crs=WV_SRS, source=contextily.providers.Esri.WorldImagery, alpha=0.5,
        attribution_size=5)
    fig = plt.gcf()
    fig.set_size_inches(10, 4)
    # The two map axes come first; the colorbars are added after them.
    for ax, title in zip(fig.axes, ("Initial residuals", "Final residuals")):
        ax.set_title(title)
    save(fig, out, "wv3-ba-residuals-map")


# --- Visualization page ------------------------------------------------------

REPORT_PAGES = ["Processed on", "Input Scenes", "DEM Results", "ICESat-2 ATL06-SR Histogram", "DEM Alignment with ICESat-2"]


def report_pages(wv, out):
    """Five pages of Tutorial 2's report, found by their titles."""
    import fitz

    pdf = fitz.open(wv / "stereo/soledad_wv3_report.pdf")
    picked = []
    for title in REPORT_PAGES:
        # The first page that has the title, not a later "(Aligned DEM)" version of it.
        number = next(i for i, page in enumerate(pdf)
                      if any(line.strip().startswith(title) and "Aligned" not in line
                             for line in page.get_text().splitlines()))
        picked.append(number)
    fig, axes = plt.subplots(1, len(picked), figsize=(3 * len(picked), 4.4), constrained_layout=True)
    for ax, number in zip(axes, picked):
        pix = pdf[number].get_pixmap(dpi=110)
        ax.imshow(np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n))
        map_axes(ax, f"p. {number + 1}", color="#555555")
    save(fig, out, "report-pages")


# --- Comparisons pages -------------------------------------------------------

COMPARISON_DEMS = {
    "asp": "stereo/run-DEM.tif",                 # under the Tutorial 2 data folder
    "setsm": "setsm/results/results_dem.tif",    # under --extra
    "cars": "cars/results/dsm/dsm.tif",          # under --extra
}


def comparison_hillshades(wv, extra, out):
    """A bare hillshade of each tool's DEM over Tutorial 2's window, on Tutorial 2's 2.4 m grid."""
    like = wv / COMPARISON_DEMS["asp"]
    for tool, rel in COMPARISON_DEMS.items():
        dem = like if tool == "asp" else extra / rel
        shade = hillshade(warp(dem, like))
        fig, ax = plt.subplots(figsize=(8, 8))
        show_hillshade(ax, shade)
        ax.axis("off")
        fig.savefig(out / f"soledad-{tool}-hillshade.png", dpi=DPI, bbox_inches="tight", pad_inches=0, facecolor="white")
        plt.close(fig)
        print(f"wrote {out / f'soledad-{tool}-hillshade.png'}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--aster-run", type=Path, required=True)
    parser.add_argument("--wv-run", type=Path, required=True)
    parser.add_argument("--extra", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[2] / "docs/concepts/figures")
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()

    aster = args.aster_run / "data/aster_rainier"
    wv = args.wv_run / "data/ucsd_soledad"
    raw = args.extra / "aster_raw"
    figures = {
        "aster-disparity-hist": lambda: aster_disparity_hist(aster, raw, args.out),
        "aster-raw-vs-ortho-hillshade": lambda: aster_raw_vs_ortho_hillshade(aster, raw, args.out),
        "dh-before-after-alignment": lambda: dh_before_after_alignment(aster, args.extra, args.out),
        "wv3-stereo-geometry": lambda: wv3_stereo_geometry(args.wv_run, args.out),
        "goodpixelmap-failures": lambda: goodpixelmap_failures(raw, wv, args.out),
        "wv3-disparity-dem": lambda: wv3_disparity_dem(wv, args.out),
        "wv3-ba-residuals-hist": lambda: wv3_ba_residuals_hist(wv, args.out),
        "wv3-ba-residuals-map": lambda: wv3_ba_residuals_map(wv, args.out),
        "report-pages": lambda: report_pages(wv, args.out),
        "comparison-hillshades": lambda: comparison_hillshades(wv, args.extra, args.out / "../../comparisons/figures"),
    }
    for name in args.only or figures:
        figures[name]()


if __name__ == "__main__":
    main()

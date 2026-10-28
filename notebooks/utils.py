"""Helpers shared by the tutorial notebooks."""
from __future__ import annotations

import re


def average_crop(image, camera, out_image, out_camera, factor):
    """Average `factor` x `factor` pixel blocks of a cam2rpc crop, and rescale its RPC camera to match.

    Writes `out_image` as compressed UInt16 (WorldView panchromatic data is
    11-bit integer) and `out_camera` as the RPC camera of the smaller image.
    ASP puts pixel centres at whole numbers, so new pixel j is centred on old
    pixel factor*j + (factor-1)/2: the RPC line and sample offsets become
    (offset - (factor-1)/2) / factor and their scales scale / factor.
    """
    from osgeo import gdal

    src = gdal.Open(str(image))
    w, h = src.RasterXSize // factor, src.RasterYSize // factor
    gdal.Translate(
        str(out_image), src, srcWin=[0, 0, w * factor, h * factor], width=w, height=h,
        resampleAlg="average", outputType=gdal.GDT_UInt16,
        creationOptions=["COMPRESS=DEFLATE", "PREDICTOR=2", "TILED=YES"],
    )
    src = None

    xml = open(camera).read()
    for key in ("LINE", "SAMP"):
        for tag, fn in ((f"{key}OFFSET", lambda v: (v - (factor - 1) / 2) / factor),
                        (f"{key}SCALE", lambda v: v / factor)):
            xml, n = re.subn(rf"<{tag}>([^<]+)</{tag}>",
                             lambda m: f"<{tag}>{fn(float(m.group(1))):.10g}</{tag}>", xml)
            if n != 1:
                raise ValueError(f"{camera}: expected one <{tag}>, found {n}")
    with open(out_camera, "w") as f:
        f.write(xml)


def show_image_pair(left, right, titles, downsample=8):
    """Show two images side by side in grayscale, downsampled for display.

    Uses asp_plot's `Raster` to read each image and `Plotter.plot_array` to
    draw it with a percentile contrast stretch.
    """
    import matplotlib.pyplot as plt
    from asp_plot.utils import Plotter, Raster

    plotter = Plotter()
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
    for ax, fn, title in zip(axes, (left, right), titles):
        image = Raster(fn, downsample=downsample).read_array()
        plotter.plot_array(ax, image, cmap="gray", add_cbar=False)
        ax.set_title(title)
        ax.set_axis_off()
    plt.tight_layout()
    plt.show()


def show_dem_hillshade(dem_fn, title="Stereo DEM"):
    """Show a DEM as a hillshade with elevation in color on top.

    Uses asp_plot's `Raster.hillshade` and `Plotter.plot_array`.
    """
    import matplotlib.pyplot as plt
    from asp_plot.utils import Plotter, Raster

    dem = Raster(dem_fn)
    plotter = Plotter()
    fig, ax = plt.subplots(figsize=(8, 7))
    plotter.plot_array(ax, dem.hillshade(), cmap="gray", add_cbar=False)
    plotter.plot_array(ax, dem.read_array(), cmap="viridis", alpha=0.5, cbar_label="Elevation (m HAE)")
    ax.set_title(title)
    ax.set_axis_off()
    plt.show()


def show_hillshades(dem_fns, titles):
    """Show DEMs side by side as hillshades, to compare their detail and holes.

    Uses asp_plot's `Raster.hillshade` and `Plotter.plot_array`. No-data cells
    stay white.
    """
    import matplotlib.pyplot as plt
    from asp_plot.utils import Plotter, Raster

    plotter = Plotter()
    fig, axes = plt.subplots(1, len(dem_fns), figsize=(5.5 * len(dem_fns), 5.5))
    for ax, fn, title in zip(axes, dem_fns, titles):
        plotter.plot_array(ax, Raster(fn).hillshade(), cmap="gray", add_cbar=False)
        ax.set_title(title)
        ax.set_axis_off()
    plt.tight_layout()
    plt.show()


# Report figures shown below each report cell, by the title part of the file
# names asp_report --figures-directory writes (NN_<title>.png). NN shifts when
# a report section is skipped, so figures are picked by title.
REPORT_FIGURES = {
    "dem_results": "The DEM, its triangulation intersection error, and its difference from the reference DEM.",
    "detailed_hillshade": "A hillshade of the DEM, with zoomed details.",
    "icesat_2_atl06_sr_profile": "The DEM along one ICESat-2 track, and the difference between them.",
}


def show_report_figures(figures_dir, figures=REPORT_FIGURES, max_width=1400):
    """Show a few figures of an asp_report run inline, under a caption each.

    `figures_dir` is what was passed to `asp_report --figures-directory`.
    Figures wider than `max_width` pixels are scaled down, which keeps the
    notebook small; the PDF has them at full resolution.
    """
    from io import BytesIO
    from pathlib import Path

    from IPython.display import Image, Markdown, display
    from PIL import Image as PILImage

    figures_dir = Path(figures_dir)
    shown = 0
    for name, caption in figures.items():
        matches = sorted(figures_dir.glob(f"[0-9][0-9]_{name}.png"))
        if not matches:
            continue
        fig = matches[0]
        with PILImage.open(fig) as im:
            if im.width > max_width:
                im = im.resize((max_width, round(im.height * max_width / im.width)))
            buf = BytesIO()
            im.save(buf, format="PNG")
        display(Markdown(f"**Report figure {int(fig.name[:2])}.** {caption}"))
        display(Image(data=buf.getvalue()))
        shown += 1
    if not shown:
        print(f"No report figures in {figures_dir}. Delete the report PDF and rerun this cell to make them.")

"""Helpers shared by the tutorial notebooks."""
from __future__ import annotations

import re
import subprocess


def scene_bbox(*image_camera_pairs, session=None, pad=0.05):
    """Lon/lat bounding box covering one or more scenes, as "minlon minlat maxlon maxlat".

    Runs ASP's `camera_footprint` on each (image, camera) pair and unions the
    results. `pad` (degrees) absorbs terrain-induced footprint shift, since the
    footprint is computed on the datum ellipsoid.
    """
    boxes = []
    for image, camera in image_camera_pairs:
        cmd = ["camera_footprint", "--quick", "--datum", "WGS84"]
        if session:
            cmd += ["-t", session]
        cmd += [str(image), str(camera)]
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        m = re.search(
            r"Min: \(([-\d.eE+]+), ([-\d.eE+]+)\) width: ([-\d.eE+]+) height: ([-\d.eE+]+)",
            out,
        )
        if not m:
            raise RuntimeError(f"Could not parse camera_footprint output:\n{out}")
        minlon, minlat, w, h = map(float, m.groups())
        boxes.append((minlon, minlat, minlon + w, minlat + h))
    minlon = min(b[0] for b in boxes) - pad
    minlat = min(b[1] for b in boxes) - pad
    maxlon = max(b[2] for b in boxes) + pad
    maxlat = max(b[3] for b in boxes) + pad
    return f"{minlon:.4f} {minlat:.4f} {maxlon:.4f} {maxlat:.4f}"


def utm_epsg(bbox):
    """EPSG code ("EPSG:326xx" north / "EPSG:327xx" south) of the UTM zone at a bbox center."""
    minlon, minlat, maxlon, maxlat = map(float, bbox.split())
    lon = (minlon + maxlon) / 2
    lat = (minlat + maxlat) / 2
    zone = int((lon + 180) // 6) + 1
    return f"EPSG:{(32600 if lat >= 0 else 32700) + zone}"


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

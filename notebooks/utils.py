"""Helpers shared by the tutorial notebooks."""
from __future__ import annotations

import re
from pathlib import Path


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


def multidirectional_hillshade(dem_fn, out_fn=None):
    """A multi-directional hillshade of a DEM (gdaldem's, lit from four directions).

    Returns the array (no-data masked). With `out_fn`, also writes it as a
    GeoTIFF; the file is reused on later calls.
    """
    import numpy as np
    from osgeo import gdal

    gdal.UseExceptions()
    if out_fn and Path(out_fn).exists():
        ds = gdal.Open(str(out_fn))
    else:
        ds = gdal.DEMProcessing(str(out_fn) if out_fn else "", str(dem_fn), "hillshade",
                                format="GTiff" if out_fn else "MEM", multiDirectional=True, computeEdges=True,
                                creationOptions=["COMPRESS=DEFLATE", "TILED=YES"] if out_fn else [])
    return np.ma.masked_equal(ds.ReadAsArray(), 0)


def show_dem_hillshade(dem_fn, title="Stereo DEM", hillshade_fn=None):
    """Show a DEM as a multi-directional hillshade with elevation in color on top.

    With `hillshade_fn`, the hillshade is written there too, for the results zip.
    """
    import matplotlib.pyplot as plt
    from asp_plot.utils import Plotter, Raster

    dem = Raster(dem_fn)
    plotter = Plotter()
    fig, ax = plt.subplots(figsize=(8, 7))
    plotter.plot_array(ax, multidirectional_hillshade(dem_fn, hillshade_fn), cmap="gray", add_cbar=False)
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
        display(Image(data=buf.getvalue()))
        display(Markdown(f"**Report figure {int(fig.name[:2])}.** {caption}"))
        shown += 1
    if not shown:
        print(f"No report figures in {figures_dir}. Delete the report PDF and rerun this cell to make them.")


def _minutes(seconds):
    """Format a duration as '1 min 05 s' or '42 s'."""
    seconds = int(round(seconds))
    return f"{seconds // 60} min {seconds % 60:02d} s" if seconds >= 60 else f"{seconds} s"


def _one_line(cmd):
    """A shell command on one line, without its backslash line continuations."""
    return " ".join(cmd.replace("\\\n", " ").split())


def _start(cmd, log):
    """Start a shell command with its output going to `log`."""
    import os
    import subprocess
    from pathlib import Path

    Path(log).parent.mkdir(parents=True, exist_ok=True)
    out = open(log, "w")
    out.write(f"$ {_one_line(cmd)}\n\n")
    out.flush()
    # ASP's Python wrappers (mapproject, parallel_stereo, asp_report) would
    # otherwise hold their output back until they end, since it goes to a
    # file, and the log tail in the notebook would not move.
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    return subprocess.Popen(cmd, shell=True, executable="/bin/bash", stdout=out, stderr=subprocess.STDOUT, env=env), out


def _finish(proc, out, log, label, status, tail, elapsed):
    """Report how a command ended; on failure, show the end of its log and stop."""
    out.close()
    tail.update(_log_lines(""))
    if proc.returncode == 0:
        status.update(_markdown(f"✅ **{label}**: done in {_minutes(elapsed)}. Full log: `{log}`"))
        return
    last = "".join(open(log, errors="replace").readlines()[-30:])
    status.update(_markdown(f"❌ **{label}** failed after {_minutes(elapsed)}. Last lines of `{log}`:"))
    print(last)
    raise RuntimeError(f"{label} failed (exit code {proc.returncode}); see {log}")


def _markdown(text):
    from IPython.display import Markdown

    return Markdown(text)


def _tail(log, n=5, width=160):
    """The last `n` lines of a log, without warnings and with progress bars reduced to their latest state."""
    try:
        with open(log, "rb") as f:
            f.seek(0, 2)
            f.seek(max(f.tell() - 8192, 0))
            text = f.read().decode(errors="replace")
    except OSError:
        return ""
    # Progress bars redraw themselves with carriage returns; keep the last draw.
    lines = [line.rstrip("\r").split("\r")[-1].rstrip() for line in text.split("\n")]
    # Warnings stay in the log but are left out here; most are routine
    # notes on memory use or settings and would worry a new user.
    lines = [line[:width] for line in lines if line.strip() and not line.lstrip().lower().startswith("warning")]
    return "\n".join(lines[-n:])


def _log_lines(text):
    """The log tail as a small grey block, or an empty output once the step is done."""
    from html import escape

    from IPython.display import HTML

    if not text:
        return HTML("")
    return HTML(f'<pre style="margin:0; opacity:0.6; font-size:0.85em; white-space:pre-wrap">{escape(text)}</pre>')


def run(cmd, log, label):
    """Run a shell command, with its output in `log` and a one-line status in the notebook.

    While the command runs, the last lines of its log and the elapsed time
    are shown. If the command fails, the last lines of the log are printed and
    the cell stops.
    """
    import time

    from IPython.display import display

    print(_one_line(cmd))
    tail = display(_log_lines(""), display_id=True)
    status = display(_markdown(f"⏳ **{label}**…"), display_id=True)
    t0 = time.time()
    proc, out = _start(cmd, log)
    while proc.poll() is None:
        tail.update(_log_lines(_tail(log)))
        status.update(_markdown(f"⏳ **{label}**: {_minutes(time.time() - t0)} so far"))
        time.sleep(1)
    _finish(proc, out, log, label, status, tail, time.time() - t0)


class timer:
    """A status line with the elapsed time, for slow Python steps.

    Use as `with timer("Plotting the stereo geometry"):`. The line ticks every
    second while the block runs and says how long it took when it ends.
    """

    def __init__(self, label):
        self.label = label

    def __enter__(self):
        import threading
        import time

        from IPython.display import display

        self.t0 = time.time()
        self.status = display(_markdown(f"⏳ **{self.label}**…"), display_id=True)
        self.stop = threading.Event()

        def tick():
            while not self.stop.wait(1):
                self.status.update(_markdown(f"⏳ **{self.label}**: {_minutes(time.time() - self.t0)} so far"))

        self.thread = threading.Thread(target=tick, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, kind, error, traceback):
        import time

        self.stop.set()
        self.thread.join()
        elapsed = _minutes(time.time() - self.t0)
        if kind is None:
            self.status.update(_markdown(f"✅ **{self.label}**: done in {elapsed}"))
        else:
            self.status.update(_markdown(f"❌ **{self.label}** failed after {elapsed}"))


def _cog(src, dst, eight_bit=False):
    """Write `src` as a Cloud Optimized GeoTIFF with averaged overviews, 8-bit if asked.

    The 8-bit copy (for orthoimages saved as 32-bit floats) scales linearly
    from the image's minimum and maximum to 1-255, with 0 for no data.
    """
    from osgeo import gdal

    gdal.UseExceptions()
    image = gdal.Open(str(src))
    floating = image.GetRasterBand(1).DataType in (gdal.GDT_Float32, gdal.GDT_Float64) and not eight_bit
    options = dict(format="COG", creationOptions=[
        "COMPRESS=DEFLATE", f"PREDICTOR={3 if floating else 2}", "OVERVIEW_RESAMPLING=AVERAGE", "NUM_THREADS=ALL_CPUS"])
    if eight_bit:
        low, high = image.GetRasterBand(1).ComputeRasterMinMax(False)
        options.update(outputType=gdal.GDT_Byte, scaleParams=[[low, high, 1, 255]], noData=0)
    gdal.Translate(str(dst), image, **options)


def _qgis_project(path, layers, title):
    """Write a QGIS project (.qgs) with the given rasters, by relative path, so the zip opens with one click.

    `layers` is a list of (file name, layer name, kind), kind one of "dem",
    "hillshade", "error", "image", "pdf"; PDFs are left out. The hillshade
    goes under the DEM, which is drawn half-transparent with a colour ramp.
    """
    from osgeo import gdal, osr
    from xml.sax.saxutils import escape

    gdal.UseExceptions()
    rasters = [(f, n, k) for f, n, k in layers if k != "pdf"]
    # Draw order: images at the bottom, then the hillshade, the DEM, the error map on top.
    order = {"image": 0, "hillshade": 1, "dem": 2, "error": 3}
    rasters.sort(key=lambda r: order[r[2]])
    first = gdal.Open(str(Path(path).parent / rasters[0][0]))
    srs = osr.SpatialReference(wkt=first.GetProjection())
    auth = f"{srs.GetAuthorityName(None)}:{srs.GetAuthorityCode(None)}" if srs.GetAuthorityCode(None) else ""
    wkt = escape(first.GetProjection())
    gt = first.GetGeoTransform()
    xmin, ymax = gt[0], gt[3]
    xmax, ymin = xmin + gt[1] * first.RasterXSize, ymax + gt[5] * first.RasterYSize

    def renderer(fn, kind):
        ds = gdal.Open(str(Path(path).parent / fn))
        band = ds.GetRasterBand(1)
        if kind == "hillshade":
            return '<rasterrenderer type="singlebandgray" band="1" gradient="BlackToWhite" opacity="1"><contrastEnhancement><minValue>1</minValue><maxValue>255</maxValue><algorithm>StretchToMinimumMaximum</algorithm></contrastEnhancement></rasterrenderer>'
        if kind == "image":
            lo, hi = band.ComputeRasterMinMax(True)
            return f'<rasterrenderer type="singlebandgray" band="1" gradient="BlackToWhite" opacity="1"><contrastEnhancement><minValue>{lo}</minValue><maxValue>{hi}</maxValue><algorithm>StretchToMinimumMaximum</algorithm></contrastEnhancement></rasterrenderer>'
        stats = band.GetStatistics(True, True)
        lo, hi = stats[0], stats[1]
        if kind == "error":
            lo, hi = 0, stats[2] + 2 * stats[3]
            ramp = [(lo, "#000004"), ((lo + hi) / 2, "#b63679"), (hi, "#fcfdbf")]
            opacity = 1
        else:
            ramp = [(lo, "#440154"), ((lo + hi) / 2, "#21918c"), (hi, "#fde725")]
            opacity = 0.5
        items = "".join(f'<item value="{v}" label="{v:.0f}" color="{c}" alpha="255"/>' for v, c in ramp)
        return (f'<rasterrenderer type="singlebandpseudocolor" band="1" classificationMin="{lo}" classificationMax="{hi}" opacity="{opacity}">'
                f'<rastershader><colorrampshader colorRampType="INTERPOLATED" minimumValue="{lo}" maximumValue="{hi}" clip="0">{items}</colorrampshader></rastershader></rasterrenderer>')

    layer_xml, order_xml, tree_xml = [], [], []
    for i, (fn, name, kind) in enumerate(rasters):
        lid = f"layer_{i}"
        checked = "Qt::Unchecked" if kind == "error" else "Qt::Checked"
        tree_xml.append(f'<layer-tree-layer id="{lid}" name="{escape(name)}" source="./{escape(fn)}" providerKey="gdal" checked="{checked}" expanded="0"/>')
        order_xml.append(f'<layer id="{lid}"/>')
        layer_xml.append(
            f'<maplayer type="raster" hasScaleBasedVisibilityFlag="0"><id>{lid}</id><datasource>./{escape(fn)}</datasource>'
            f'<layername>{escape(name)}</layername><srs><spatialrefsys><wkt>{wkt}</wkt><authid>{auth}</authid></spatialrefsys></srs>'
            f'<provider>gdal</provider><pipe>{renderer(fn, kind)}<rasterresampler zoomedInResamplingMethod="bilinear" zoomedOutResamplingMethod="bilinear" maxOversampling="2"/></pipe></maplayer>')
    # QGIS draws the layer tree top to bottom, so the last in draw order comes first.
    tree_xml.reverse()
    xml = f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.40" projectname="{escape(title)}">
  <title>{escape(title)}</title>
  <projectCrs><spatialrefsys><wkt>{wkt}</wkt><authid>{auth}</authid></spatialrefsys></projectCrs>
  <layer-tree-group>
    {"".join(tree_xml)}
    <custom-order enabled="0">{"".join(order_xml)}</custom-order>
  </layer-tree-group>
  <mapcanvas name="theMapCanvas" annotationsVisible="1">
    <extent><xmin>{xmin}</xmin><ymin>{ymin}</ymin><xmax>{xmax}</xmax><ymax>{ymax}</ymax></extent>
    <destinationsrs><spatialrefsys><wkt>{wkt}</wkt><authid>{auth}</authid></spatialrefsys></destinationsrs>
  </mapcanvas>
  <projectlayers>{"".join(layer_xml)}</projectlayers>
  <properties><Paths><Absolute type="bool">false</Absolute></Paths></properties>
</qgis>
"""
    Path(path).write_text(xml)


def zip_results(zip_path, results, title):
    """Put a tutorial's results in one zip file, to download and open in a GIS.

    `results` lists (source path, name in the zip, kind), kind one of "dem",
    "hillshade", "error", "image", "pdf". Every raster is rewritten as a
    Cloud Optimized GeoTIFF with averaged overviews, flat in the zip under its
    new name; images (orthoimages saved as 32-bit floats) become 8-bit, which
    keeps each zip under 32 MB (VS Code in the browser downloads larger files
    by asking for write access to a local folder, and Chrome refuses
    ~/Downloads for that). A QGIS project (<title>.qgs) with every raster by
    relative path goes in too, so the zip opens with one click. Sources that
    don't exist (a step was skipped or failed) are left out and listed. The
    zip is written under a temporary name and renamed when complete, so that a
    complete file is all that ever appears at `zip_path`: in a Codespace, the
    close-panel extension shows a notification when it does.
    """
    import os
    import tempfile
    import zipfile

    from IPython.display import display

    zip_path = Path(zip_path)
    present = [(Path(src), name, kind) for src, name, kind in results if Path(src).exists()]
    missing = [str(src) for src, _, _ in results if not Path(src).exists()]
    partial = zip_path.with_name(zip_path.name + ".part")
    with timer("Zipping the results"), tempfile.TemporaryDirectory() as tmp:
        staged = []
        for src, name, kind in present:
            dst = Path(tmp) / name
            if kind == "pdf":
                dst = src
            else:
                _cog(src, dst, eight_bit=(kind == "image"))
            staged.append((dst, name, kind))
        project = Path(tmp) / f"{title}.qgs"
        if any(k != "pdf" for _, _, k in staged):
            _qgis_project(project, [(n, Path(n).stem, k) for _, n, k in staged], title)
            staged.append((project, project.name, "project"))
        with zipfile.ZipFile(partial, "w", zipfile.ZIP_DEFLATED) as archive:
            for dst, name, _ in staged:
                archive.write(dst, name)
        partial.replace(zip_path)
    if missing:
        print("Not found, so not in the zip:\n  " + "\n  ".join(missing))
    size = zip_path.stat().st_size / 1e6
    # The path as the file explorer shows it: from the repository's top folder,
    # the one above notebooks/.
    shown = os.path.relpath(zip_path.resolve(), Path.cwd().parent)
    listing = "\n".join(f"- `{name}`" for _, name, _ in staged)
    display(_markdown(
        f"### Results: `{shown}` ({size:.0f} MB, {len(staged)} files)\n\n{listing}\n\n"
        "To save it to your computer, right-click it in the file explorer on the left and choose **Download**. "
        f"Unzip it and open `{title}.qgs` in QGIS to see everything at once."
    ))


# The stages parallel_stereo reports in <prefix>-stereo-status.txt, in run
# order, with a plain description. Stages a run doesn't use, such as
# stereo_rfne with asp_mgm, are skipped.
STEREO_STAGES = {
    "stereo_pprc": "Preparing the images and finding matching features",
    "stereo_corr": "Matching every pixel between the two images",
    "stereo_rfne": "Refining the matches",
    "stereo_blend": "Blending the tile edges",
    "stereo_fltr": "Removing bad matches",
    "stereo_tri": "Turning the matches into 3D points",
}

# Seconds per stage in local runs of each tutorial, used only for the
# time-left estimate, which scales them to the machine. A run uses the first
# entry whose key is in its output prefix. The stages' shares differ between
# the tutorials: estimated with Tutorial 1's, Tutorial 2's time left came out
# twice too long. The status file still says stereo_pprc while the
# low-resolution matching runs, so that is counted in stereo_pprc.
STAGE_SECONDS = {
    "ucsd_soledad/stereo/": {"stereo_pprc": 47, "stereo_corr": 38, "stereo_blend": 3, "stereo_fltr": 5, "stereo_tri": 19},
    "ucsd_soledad/pairs/": {"stereo_pprc": 30, "stereo_corr": 52, "stereo_blend": 4, "stereo_fltr": 6, "stereo_tri": 22},
    "": {"stereo_pprc": 40, "stereo_corr": 74, "stereo_blend": 23, "stereo_fltr": 5, "stereo_tri": 39},
}


def _stage_seconds(prefix):
    """The STAGE_SECONDS entry for a stereo run's output prefix."""
    return next(seconds for key, seconds in STAGE_SECONDS.items() if key in str(prefix))


def _stereo_status(prefix):
    """The stage, tiles done and tiles in total, from <prefix>-stereo-status.txt."""
    try:
        stage, done, total = open(f"{prefix}-stereo-status.txt").read().split()[-3:]
        return stage, int(done), int(total)
    except (OSError, ValueError):
        return None, 0, 0


def _stereo_time_left(stage, done, total, in_stage, last_tile, rate, seconds):
    """Seconds of stereo left, or None before there is anything to go on.

    `in_stage` is the time spent in the current stage, `last_tile` the time
    into the stage when its latest tile finished, `seconds` the run's
    STAGE_SECONDS entry, and `rate` how much slower than those seconds the
    finished stages ran. Once a tile of the stage is done, the time per tile
    so far is used for the rest.
    """
    if stage not in STEREO_STAGES or rate is None:
        return None
    names = list(STEREO_STAGES)
    later = sum(seconds.get(s, 0) for s in names[names.index(stage) + 1 :]) * rate
    if 0 < done < total:
        per_tile = last_tile / done
        tiles_left = total - done
        return max(per_tile * tiles_left - (in_stage - last_tile), per_tile * (tiles_left - 1)) + later
    return max(seconds.get(stage, 0) * rate - in_stage, 0) + later


def _read_tile(path, bands, step):
    """Read bands of a tile image every `step` pixels, or None if it isn't readable yet."""
    import numpy as np
    from osgeo import gdal

    gdal.UseExceptions()
    try:
        ds = gdal.Open(str(path))
        w, h = ds.RasterXSize // step, ds.RasterYSize // step
        arrays = [ds.GetRasterBand(b).ReadAsArray(buf_xsize=w, buf_ysize=h).astype("float64") for b in bands]
        return arrays, ds.GetMetadata()
    except RuntimeError:
        return None


def _tile_heights(path, step):
    """Ellipsoid heights of a tile's point cloud (<tile>-PC.tif), every `step` pixels."""
    import numpy as np
    from pyproj import Transformer

    read = _read_tile(path, (1, 2, 3), step)
    if read is None:
        return None
    (x, y, z), meta = read
    offset = [float(v) for v in meta.get("POINT_OFFSET", "0 0 0").split()]
    empty = (x == 0) & (y == 0) & (z == 0)
    ecef_to_lonlath = Transformer.from_crs("EPSG:4978", "EPSG:4979", always_xy=True)
    _, _, height = ecef_to_lonlath.transform(x + offset[0], y + offset[1], z + offset[2])
    height[empty] = np.nan
    return height


def _tile_offsets(path, step, tile, size):
    """The pixel offsets between the images in a tile's disparity (<tile>-D.tif), every `step` pixels.

    Returns (dx, dy): how far each pixel of the left image sits from its
    match in the right one, along the image's columns and rows.

    The disparity also covers a margin (collar) around the tile on each side
    that borders another tile; it is cut off here. `tile` is the tile's
    x, y, width, height and `size` the full image's width, height.
    """
    import numpy as np
    from osgeo import gdal

    gdal.UseExceptions()
    try:
        ds = gdal.Open(str(path))
        x, y, w, h = tile
        pads = []
        for start, length, extent, full in ((x, w, ds.RasterXSize, size[0]), (y, h, ds.RasterYSize, size[1])):
            sides = (start > 0) + (start + length < full)
            pads.append((extent - length) // sides if start > 0 else 0)
        win = dict(xoff=pads[0], yoff=pads[1], win_xsize=w, win_ysize=h, buf_xsize=w // step, buf_ysize=h // step)
        dx = ds.GetRasterBand(1).ReadAsArray(**win).astype("float64")
        dy = ds.GetRasterBand(2).ReadAsArray(**win).astype("float64")
        valid = ds.GetRasterBand(3).ReadAsArray(**win)
    except RuntimeError:
        return None
    dx[valid == 0] = np.nan
    dy[valid == 0] = np.nan
    return dx, dy


def _tile_grid(cmd, size):
    """The tile boundaries parallel_stereo will use: x edges and y edges in pixels of the left image.

    From --job-size-w/-h in the command (ASP's default is 1024). The grid is
    drawn before any tile finishes, so the map shows what to expect.
    """
    import re

    edges = []
    for flag, extent in (("--job-size-w", size[0]), ("--job-size-h", size[1])):
        m = re.search(rf"{flag}\s+(\d+)", cmd)
        job = int(m.group(1)) if m else 1024
        edges.append(list(range(job, extent, job)))
    return edges


def _match_points_png(prefix):
    """asp-plot's match-point figure for a stereo run in progress, as PNG bytes, or None.

    parallel_stereo writes the matched features (<prefix>-*.match) early,
    before it matches every pixel. StereoPlotter wants a DEM in the stereo
    directory, which doesn't exist yet; the match plot doesn't use it, so the
    left image stands in. Its notes and warnings are kept out of the notebook.
    """
    import contextlib
    import io
    import logging
    from pathlib import Path

    import matplotlib.pyplot as plt
    from asp_plot.stereo import StereoPlotter

    stereo_dir = Path(prefix).parent
    quiet = io.StringIO()
    logger = logging.getLogger("asp_plot")
    level = logger.level
    logger.setLevel(logging.ERROR)
    try:
        with contextlib.redirect_stdout(quiet), contextlib.redirect_stderr(quiet):
            plotter = StereoPlotter(str(stereo_dir.parent), stereo_dir.name, dem_fn=f"{Path(prefix).name}-L_sub.tif")
            plotter.title = "Features found in each image (blue) and matched between them (red)"
            plotter.plot_match_points()
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=80)
        return buf.getvalue()
    except Exception:
        return None
    finally:
        plt.close("all")
        logger.setLevel(level)


def run_stereo(cmd, prefix, log, label="Stereo", step=4):
    """Run parallel_stereo, showing its progress and the tiles as they finish.

    `prefix` is the output prefix given to parallel_stereo. ASP's output goes
    to `log`. While it runs, the notebook shows the last lines of the log, the
    current stage, the tiles done, the time so far and, after the first stage,
    an estimate of the time left. Once the features are matched, it shows
    asp-plot's match-point figure, and then a map of the processing window
    with the tile boundaries dashed, which fills in tile by tile: the offsets
    between the images after matching (east-west and north-south on the map
    grid; along rows and columns otherwise), and the heights after
    triangulation. The map is drawn every `step` pixels, to
    keep it quick.

    The tiles are placed by their pixel position in the left image as stereo
    sees it (<prefix>-L.tif). For orthorectified images that is the map grid;
    otherwise it is the left image after ASP aligned it to the right one,
    which may be rotated. `label` names the run in the status line.
    """
    import re
    import time
    from pathlib import Path

    import numpy as np
    from io import BytesIO

    from IPython.display import Image, display
    from matplotlib.colors import LightSource
    from matplotlib.figure import Figure
    from osgeo import gdal

    print(_one_line(cmd))
    tail = display(_log_lines(""), display_id=True)
    status = display(_markdown(f"⏳ **{label}**: starting…"), display_id=True)
    t0 = time.time()
    proc, out = _start(cmd, log)

    dx = dy = heights = None  # window-sized arrays, made once the left image exists
    drawn = set()
    plot = None
    grid_drawn = False
    matches_shown = False
    seconds = _stage_seconds(prefix)
    stage_start = {}  # when each stage first showed up in the status file
    tile_end = {}  # when the latest tile of each stage finished
    finishing = False  # all tiles triangulated
    while proc.poll() is None:
        time.sleep(2)
        elapsed = time.time() - t0
        stage, done, total = _stereo_status(prefix)
        text = f"⏳ **{label}**: {_minutes(elapsed)} so far"
        # Once the tiles are triangulated, parallel_stereo joins each stage's
        # tiles into full-size outputs, and the status file cycles through the
        # stages again with 0 tiles done.
        tri_tiles = tile_end.get("stereo_tri", (0, 0))[0]
        finishing = finishing or (stage == "stereo_tri" and total > 0 and done == total)
        finishing = finishing or ("stereo_tri" in stage_start and (stage != "stereo_tri" or done < tri_tiles))
        if finishing:
            text += ". Writing the full-size outputs, nearly done"
        elif stage in STEREO_STAGES:
            stage_start.setdefault(stage, elapsed)
            if stage not in tile_end or tile_end[stage][0] != done:
                tile_end[stage] = (done, elapsed)
            text += f". {STEREO_STAGES[stage]}"
            if total > 1:
                text += f" (tile {min(done + 1, total)} of {total})"
            finished = [s for s in stage_start if s != stage]
            units = sum(seconds.get(s, 0) for s in finished)
            rate = stage_start[stage] / units if units else None
            in_stage = elapsed - stage_start[stage]
            last_tile = tile_end[stage][1] - stage_start[stage]
            remaining = _stereo_time_left(stage, done, total, in_stage, last_tile, rate, seconds)
            if remaining is not None:
                text += f". About {_minutes(remaining)} left" if remaining >= 60 else ". Less than a minute left"
        tail.update(_log_lines(_tail(log)))
        status.update(_markdown(text + "."))

        # <prefix>-L__R.match for orthorectified images, <prefix>-<left>__<right>.match otherwise.
        match_fn = next(iter(Path(prefix).parent.glob(f"{Path(prefix).name}-*.match")), None)
        if not matches_shown and match_fn and time.time() - match_fn.stat().st_mtime > 2:
            matches_shown = True
            png = _match_points_png(prefix)
            if png:
                display(Image(data=png))

        if dx is None:
            left = _read_tile(f"{prefix}-L.tif", (1,), step)
            if left is None:
                continue
            shape = left[0][0].shape
            dx, dy, heights = (np.full(shape, np.nan) for _ in range(3))
            left_image = gdal.Open(f"{prefix}-L.tif")
            size = (left_image.RasterXSize, left_image.RasterYSize)
            spacing = abs(left_image.GetGeoTransform()[1]) * step
            grid = _tile_grid(cmd, size)
            # Orthorectified images sit on the map grid, so the offsets run
            # east-west and north-south; otherwise along the image's own axes.
            on_map = bool(left_image.GetProjection())
            directions = ("east-west", "north-south") if on_map else ("along rows", "along columns")
        new = False
        if not grid_drawn and matches_shown:
            # The empty map with its tile grid, under the match figure, before
            # any tile is done, so the filling-in has a visible frame.
            grid_drawn = new = True
        for tile_dir in Path(prefix).parent.glob(f"{Path(prefix).name}-*_*_*_*"):
            m = re.fullmatch(r".*-(\d+)_(\d+)_(\d+)_(\d+)", tile_dir.name)
            if not m:
                continue
            window = tuple(int(v) for v in m.groups())
            x0, y0 = window[0] // step, window[1] // step
            tile = tile_dir / tile_dir.name.split("-", 1)[1]
            readers = (
                ("D", lambda path: _tile_offsets(path, step, window, size), (dx, dy)),
                ("PC", lambda path: (_tile_heights(path, step),), (heights,)),
            )
            for key, read, targets in readers:
                path = Path(f"{tile}-{key}.tif")
                if (tile_dir.name, key) in drawn or not path.exists() or time.time() - path.stat().st_mtime < 2:
                    continue
                values = read(path)
                if values is None or values[0] is None:
                    continue
                for target, array in zip(targets, values):
                    h, w = array.shape
                    target[y0 : y0 + h, x0 : x0 + w] = array[: target.shape[0] - y0, : target.shape[1] - x0]
                drawn.add((tile_dir.name, key))
                new = True

        if new:
            fig = Figure(figsize=(15, 5))
            axes = fig.subplots(1, 3)
            for ax, array, title in zip(axes[:2], (dx, dy), directions):
                if np.isfinite(array).any():
                    lo, hi = np.nanpercentile(array, (2, 98))
                    im = ax.imshow(array, cmap="magma", vmin=lo, vmax=hi)
                    fig.colorbar(im, ax=ax, shrink=0.7, label="Offset (pixels)")
                ax.set_title(f"Offset between the images: {title}", fontsize=10)
            ax = axes[2]
            if np.isfinite(heights).any():
                lo, hi = np.nanpercentile(heights, (2, 98))
                shade = LightSource(azdeg=315, altdeg=45).hillshade(np.nan_to_num(heights, nan=np.nanmedian(heights)), dx=spacing, dy=spacing)
                shade[np.isnan(heights)] = np.nan
                ax.imshow(shade, cmap="gray")
                im = ax.imshow(heights, cmap="viridis", vmin=lo, vmax=hi, alpha=0.5)
                fig.colorbar(im, ax=ax, shrink=0.7, label="Height (m)")
            ax.set_title("After triangulation: heights", fontsize=10)
            for ax in axes:
                # The tiles parallel_stereo works through, so the map's filling in makes sense:
                # white on the dark offset maps, dark on the hillshade.
                color = "white" if ax is not axes[2] else "0.2"
                for x in grid[0]:
                    ax.axvline(x / step, color=color, linestyle="--", linewidth=1.2)
                for y in grid[1]:
                    ax.axhline(y / step, color=color, linestyle="--", linewidth=1.2)
                ax.set_xlim(0, dx.shape[1])
                ax.set_ylim(dx.shape[0], 0)
                ax.set_xticks([])
                ax.set_yticks([])
            fig.tight_layout()
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=80)
            if plot is None:
                plot = display(Image(data=buf.getvalue()), display_id=True)
            else:
                plot.update(Image(data=buf.getvalue()))

    _finish(proc, out, log, label, status, tail, time.time() - t0)

# Visualization with `asp_plot`

ASP outputs are scattered across files in numerous formats. [`asp_plot`](https://asp-plot.readthedocs.io/) reads them and produces diagnostic figures and PDF reports. We use it throughout this guide.

## Two ways to use it

### 1. The `asp_plot` CLI

Generates a one-page PDF that captures the entire run:

```bash
asp_plot \
  --directory ./aster_rainier \
  --stereo_directory out_stereo_proj \
  --plot_altimetry True \
  --pc_align True \
  --report_filename rainier_report.pdf
```

The PDF includes: title page with DEM metadata + processing parameters, scenes, stereo geometry, match points, bundle adjustment residuals, disparity, DEM hillshade and dh-vs-reference, ICESat-2/LOLA/MOLA comparison, and (optionally) a `pc_align` summary page.

Use this when you want a record of a successful run.

### 2. The Python API

For interactive exploration in a notebook:

```python
from asp_plot.scenes import ScenePlotter
from asp_plot.stereo import StereoPlotter
from asp_plot.bundle_adjust import ReadBundleAdjustFiles, PlotBundleAdjustFiles

# Inspect input scenes
ScenePlotter("./aster_rainier", "out_stereo_proj").plot_scenes()

# Bundle adjustment residuals
ba = ReadBundleAdjustFiles("./aster_rainier", "ba")
gdfs = ba.get_initial_final_residuals_gdfs()
PlotBundleAdjustFiles(gdfs).plot_n_residuals()

# DEM hillshade
plotter = StereoPlotter(
    "./aster_rainier", "out_stereo_proj",
    reference_dem="./out_stereo/run-200m-DEM.tif",
)
plotter.plot_detailed_hillshade(subset_km=5)
```

Use this when something went wrong, or to explore the diagnostic methods directly in a notebook or script.

## What each module does

| Module | What it visualizes | When to use |
|---|---|---|
| `asp_plot.scenes` | Input imagery, mapprojected or raw | Sanity check inputs |
| `asp_plot.stereo_geometry` | Skyplot, footprints, attitude/ephemeris | Before processing, to pick good pairs |
| `asp_plot.bundle_adjust` | Residual histograms and maps | After bundle_adjust, to verify fit |
| `asp_plot.stereo` | Disparity, hillshade, dh maps | After stereo, to verify DEM quality |
| `asp_plot.altimetry` | DEM vs ICESat-2 / LOLA / MOLA | Independent ground-truth check |
| `asp_plot.csm_camera` | Original vs optimized camera trajectories | Jitter analysis (advanced) |

## The mental model

A pipeline that ran without errors can still produce an unrealistic DEM. The diagnostic plots tell you whether to trust the result.

## Where to read more

- [`asp_plot` documentation](https://asp-plot.readthedocs.io/)
- [`asp_plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html) — deeper examples beyond the tutorials here.

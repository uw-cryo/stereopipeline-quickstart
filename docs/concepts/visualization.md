# Visualization with `asp-plot`

ASP outputs are scattered across files in many formats; [`asp-plot`](https://asp-plot.readthedocs.io/en/latest/) reads them and produces diagnostic figures and PDF reports used throughout this guide.

## Two ways to use it

<!-- FIGURE IDEA: two screenshots side by side — left, a thumbnail montage of pages from the asp_plot CLI's PDF report (cover, scenes, residuals, dh, altimetry); right, a Jupyter notebook cell calling StereoPlotter.plot_detailed_hillshade with the figure rendered inline. Same data, different consumption modes. -->

The CLI (`asp_plot --directory ... --report_filename ...`) generates a single PDF capturing the whole run: processing parameters, scene overviews, bundle-adjust residuals when present, disparity and match quality, the DEM and its difference against a reference, and an ICESat-2 comparison. The tutorials end each processing pass with this command, so every run leaves a self-contained record.

The Python API (`ScenePlotter`, `StereoPlotter`, `PlotBundleAdjustFiles`, `Altimetry`, `StereoGeometryPlotter`) produces the same figures one at a time, for interactive exploration in a notebook. The [stereo photogrammetry](stereo-photogrammetry.md) and [bundle adjustment](bundle-adjustment.md) pages use it for their figures.

## Comparable reports across runs

When two runs differ by one processing choice, their reports should differ only where the processing does. `asp_plot` writes its figure selections (which ICESat-2 points, which profile track, which hillshade crops) to a sidecar file next to each report, and `--reuse_selections` replays them, so the two PDFs line up panel for panel. The tutorials use this twice: the ASTER raw-vs-orthorectified pair of reports, and the WorldView with-and-without bundle adjustment pair.

## Where to read more

- [`asp-plot` documentation](https://asp-plot.readthedocs.io/en/latest/)
- [`asp-plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html)

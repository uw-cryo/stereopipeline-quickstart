# Visualization with `asp_plot`

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

ASP outputs are scattered across files in many formats; [`asp_plot`](https://asp-plot.readthedocs.io/) reads them and produces diagnostic figures and PDF reports used throughout this guide.

## Two ways to use it

<!-- FIGURE IDEA: two screenshots side by side — left, a thumbnail montage of pages from the asp_plot CLI's PDF report (cover, scenes, residuals, dh, altimetry); right, a Jupyter notebook cell calling StereoPlotter.plot_detailed_hillshade with the figure rendered inline. Same data, different consumption modes. -->

The CLI (`asp_plot --directory ... --report_filename ...`) generates a single PDF capturing the whole run; the Python API (`ScenePlotter`, `StereoPlotter`, `PlotBundleAdjustFiles`, `Altimetry`) is for interactive exploration in a notebook.

## Where to read more

- [`asp_plot` documentation](https://asp-plot.readthedocs.io/)
- [`asp_plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html)

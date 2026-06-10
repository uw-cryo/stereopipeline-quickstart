# Visualization with `asp-plot`

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

ASP outputs are scattered across files in many formats; [`asp-plot`](https://asp-plot.readthedocs.io/en/latest/) reads them and produces diagnostic figures and PDF reports used throughout this guide.

## Two ways to use it

<!-- FIGURE IDEA: two screenshots side by side — left, a thumbnail montage of pages from the asp_plot CLI's PDF report (cover, scenes, residuals, dh, altimetry); right, a Jupyter notebook cell calling StereoPlotter.plot_detailed_hillshade with the figure rendered inline. Same data, different consumption modes. -->

The CLI (`asp_plot --directory ... --report_filename ...`) generates a single PDF capturing the whole run; the Python API (`ScenePlotter`, `StereoPlotter`, `PlotBundleAdjustFiles`, `Altimetry`) is for interactive exploration in a notebook.

## Where to read more

- [`asp-plot` documentation](https://asp-plot.readthedocs.io/en/latest/)
- [`asp-plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html)

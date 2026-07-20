# Tutorials

Three end-to-end notebooks. All use openly available data; no NASA Earthdata or Vantor credentials, no API keys.

```{admonition} To run these notebooks, launch the Codespace first
:class: important
The tutorial pages below are static renders of the notebooks in `notebooks/`, shown with saved outputs. To run them yourself, [open this repo in a GitHub Codespace](../start/codespaces.md); it boots with ASP, `asp-plot`, and the demo data scripts already installed, so the notebooks run top to bottom with no setup. Running on your own machine instead needs the [local install](../reference/installation.md).
```

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 1. ASTER Mt. Rainier
:link: 01_aster_rainier
:link-type: doc

Stereo from a single ASTER L1A scene. The gentlest end-to-end flow:
- `aster2asp` to extract nadir + back-looking views
- `parallel_stereo` + `point2dem` on the raw imagery
- COP-DEM clip from AWS Open Data
- `mapproject` + `parallel_stereo` re-run on the orthorectified pair
- `asp-plot` PDF report for each pass

Output: two ~30 m DEMs of Mt. Rainier, raw and orthorectified.
:::

:::{grid-item-card} 2. WorldView-3 UCSD
:link: 02_worldview_ucsd
:link-type: doc

Stereo from a high-resolution commercial-style WV3 pair (SpaceNet CORE3D, openly hosted on AWS). The full recipe:
- Stereo geometry analysis with `StereoGeometryPlotter`
- COP-DEM clip from AWS Open Data
- `mapproject` to the COP-DEM grid
- `parallel_stereo` on the orthorectified pair
- `asp_plot` PDF report with ICESat-2 alignment (`pc_align` runs by default)

Output: 4 m DEM of the UCSD campus and sea cliffs.
:::

:::{grid-item-card} 3. WorldView-3 UCSD with bundle adjustment
:link: 03_worldview_ucsd_ba
:link-type: doc

Variant of Tutorial 2 that adds `bundle_adjust` to refine the vendor RPC cameras before orthorectification. Outputs are suffixed `_ba`, so both runs share a data directory and the two `asp-plot` reports can be compared side by side.
:::
::::

## Suggested order

If you've never run ASP before, do the ASTER tutorial first. It has fewer parameters, and a coarser resolution.

The WorldView tutorial then adds cropping and a finer resolution, higher accuracy result. The bundle-adjustment variant comes last: run it after Tutorial 2 and compare the reports to see what camera refinement adds.

## Beyond the tutorials

The [`asp-plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html) cover jitter correction, planetary missions (LRO NAC, Mars MOC NA, CTX), variants that skip orthorectification, and scene selection.

If a notebook fails or a step is unclear, [open a problem report](https://github.com/uw-cryo/stereopipeline-quickstart/issues/new?template=problem-report.yml).

# Pipeline overview

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

Every ASP run, regardless of sensor, follows the same five-stage pattern.

## The five stages

<!-- FIGURE IDEA: pipeline flowchart with the five stages as boxes left-to-right. Inputs (raw imagery, vendor metadata) on the left; outputs (DEM, hillshade, dh-vs-reference) on the right. Optional stages (bundle adjust, orthorectification, alignment) drawn with dashed borders. Could be drawn in mermaid or as a polished SVG. -->

Sensor prep → bundle adjustment → orthorectification → stereo + DEM generation → alignment.

## Stage 1: Sensor preparation

<!-- FIGURE IDEA: small grid showing example raw vendor formats (ASTER HDF, WorldView NTF + XML, ISIS cube) on the left and the canonical "image.tif + camera.xml" pair on the right, with the relevant per-sensor binary in the middle. -->

Vendor-specific tools (`aster2asp`, `wv_correct`, `cam2map`, `dg_mosaic`) convert raw vendor data into the standard image-plus-camera pair ASP expects.

## Stage 2: Bundle adjustment

<!-- FIGURE IDEA: residual scatter plot — initial vs final residuals for the WV3 tutorial, reusing the asp_plot output from the existing tutorial run. -->

`bundle_adjust` refines the vendor camera models by minimizing reprojection errors of features matched between the input images. See [Bundle adjustment](bundle-adjustment.md).

## Stage 3: Orthorectification

<!-- FIGURE IDEA: side-by-side disparity-range cartoon — left panel shows raw stereo with rays diverging widely (large search range); right panel shows the same scene after orthorectification onto a reference DEM, with rays nearly parallel (small remaining disparity). Or: actual disparity histograms before vs after. -->

`mapproject` resamples each input image onto a reference DEM grid so stereo matching has only a small remaining disparity to solve. See [Orthorectification](orthorectification.md).

```{note}
ASP calls this step "mapprojection" in its toolchain (`mapproject`, `--mapproj-dem`). This guide uses "orthorectification" — the more standard photogrammetry term — for the concept while keeping ASP's tool names verbatim.
```

## Stage 4: Stereo + DEM generation

<!-- FIGURE IDEA: a real disparity map (run-F.tif) from one of the tutorials, colorized; alongside it the resulting hillshaded DEM. Shows the visible link from "matched pixels" to "elevation surface". -->

`parallel_stereo` matches pixels between the two images and triangulates them into a point cloud; `point2dem` grids the cloud into a regular DEM. See [Stereo photogrammetry](stereo-photogrammetry.md).

## Stage 5: Alignment

<!-- FIGURE IDEA: dh-vs-reference difference map (or histogram) before and after pc_align. Pre-align: visible bias / tilt; post-align: noise centered on zero. Could pair with the printed pc_align translation vector. -->

`pc_align` registers the DEM to a trusted reference (ICESat-2, MOLA, LOLA, or another DEM) using ICP. See [Alignment](alignment.md).

## What `asp-plot` does at every stage

<!-- FIGURE IDEA: thumbnail strip of an actual asp_plot PDF report (cover, scenes page, residuals page, dh page, altimetry page). Anchors the abstract "diagnostic plots" claim to a real artifact. -->

Each ASP stage produces files; [`asp-plot`](https://asp-plot.readthedocs.io/en/latest/) reads them and produces diagnostic plots and PDF reports. See [Visualization](visualization.md).

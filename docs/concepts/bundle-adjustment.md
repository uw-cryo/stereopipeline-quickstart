# Bundle adjustment

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

The vendor's camera models are slightly inaccurate; bundle adjustment refines them by minimizing reprojection errors of features matched between input images.

## What the optimizer does

<!-- FIGURE IDEA: schematic of two cameras viewing several tie points; arrows from camera centers through image-plane observations to the 3D points; small "wiggle" arrows on cameras and points indicating what the optimizer varies. Caption: "minimize the sum of squared reprojection errors over all observations." -->

Given initial cameras and tie points, `bundle_adjust` jointly varies camera parameters and 3D tie-point positions to drive reprojection error toward zero.

## Why this matters for stereo

<!-- FIGURE IDEA: cartoon of two slightly-misaligned cameras producing rays that don't quite intersect at the ground point — the gap is the "intersection error". After bundle adjustment, the rays meet cleanly. Could overlay an actual run-IntersectionErr.tif crop to make it concrete. -->

Without bundle adjustment, vendor camera misalignment translates into meters of bias and tilt in the final DEM; with it, residual reprojection error drops below 1 px and DEM bias to around 1 m.

## Outputs you can visualize

<!-- FIGURE IDEA: paired histograms of initial vs final residuals from the WV3 tutorial — initial wide, multi-pixel; final narrow, sub-pixel. Plus a map view colored by residual magnitude over the scene footprint, showing the spatial distribution. -->

Initial- and final-pass per-tie-point residual CSVs (`*-initial_residuals_pointmap.csv`, `*-final_residuals_pointmap.csv`) are read by `asp_plot.bundle_adjust.PlotBundleAdjustFiles` for before/after comparison.

## Common knobs

Interest-point density (`--ip-per-image`), tie-point penalty (`--tri-weight`, `--tri-robust-threshold`), and camera-anchor weight (`--camera-weight`) are the parameters most often tuned.

## Where to read more

- [ASP bundle_adjust docs](https://stereopipeline.readthedocs.io/en/latest/tools/bundle_adjust.html)

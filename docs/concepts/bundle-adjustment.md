# Bundle adjustment

The vendor's camera models can be slightly inaccurate. Bundle adjustment fixes them by minimizing reprojection error of features matched between the input images.

## What the optimizer does

Given:

- Input cameras: initial position and pointing for each image.
- Tie points: pixels matched between images, each representing a single 3D ground point seen multiple times.

Bundle adjustment varies the camera parameters and the 3D positions of tie points to minimize reprojection errors.

## Why this matters for stereo

If the two cameras are misaligned by even a couple of meters in 3D space, the same ground point appears at slightly different locations in the two images, even after correct stereo matching. That maps into a height error in the final DEM. Without bundle adjustment, biases of several meters and tilt artifacts of similar magnitude are common.

After bundle adjustment, the residual reprojection error is typically <1 px and the DEM bias drops to ~1 m or less.

## Outputs you can visualize

`bundle_adjust` writes a CSV of tie-point residuals before and after optimization:

- `*-initial_residuals_pointmap.csv`: reprojection error per tie point at the start.
- `*-final_residuals_pointmap.csv`: same after optimization.

`asp_plot.bundle_adjust.PlotBundleAdjustFiles` plots both side by side as histograms and map views.

```{tip}
Healthy bundle adjustment: initial residuals 1-10 px, final residuals <0.5 px, distributed roughly uniformly. Unhealthy: final residuals >1 px or clustered in one corner; you may have insufficient or poorly-distributed tie points.
```

## Common knobs

`--ip-per-image`
:   Target number of interest points per image. Default ~5000; tutorials use 10000 for denser coverage.

`--tri-weight` / `--tri-robust-threshold`
:   Penalty on ground-point movement during optimization. Keeps the solution from drifting if you don't have ground control. Tutorials use `0.1 / 0.1`.

`--camera-weight 0`
:   Lets the camera parameters move freely (default is to anchor them).

`--mapproj-dem REF.tif`
:   Optional. Recomputes residuals after mapprojecting matches onto a reference DEM, useful for diagnosing bundle quality in absolute geographic terms.

## Where to read more

- [ASP bundle_adjust docs](https://stereopipeline.readthedocs.io/en/latest/tools/bundle_adjust.html)

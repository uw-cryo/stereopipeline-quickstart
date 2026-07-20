# Bundle adjustment

The vendor's {term}`camera models <camera model>` are slightly inaccurate; bundle adjustment refines them by minimizing {term}`reprojection errors <reprojection error>` of features matched between the input images.

## What the optimizer does

`bundle_adjust` detects {term}`interest points <interest point (IP)>` in each image, matches them across images into {term}`tie points <tie point>`, and then jointly varies the camera parameters and the tie point positions to shrink the reprojection errors: the distance between where each tie point actually appears in an image and where the camera model says it should appear.

![Bundle adjustment nudges camera parameters and tie point positions to shrink reprojection errors](figures/bundle-adjust-schematic.svg)

## Why this matters for stereo

With misaligned cameras, the two viewing rays for a matched pixel do not quite meet. Triangulation records that miss distance per point as the fourth band of `run-PC.tif` (`point2dem --errorimage` grids it into `run-IntersectionErr.tif`), and the misalignment surfaces in the DEM as bias and tilt. Bundle adjustment shrinks all of these.

![Before bundle adjustment the rays miss each other; after, they intersect](figures/intersection-error.svg)

## What it looks like on real data

From a `bundle_adjust` run on the [WorldView tutorial's](../tutorials/03_worldview_ucsd_ba.ipynb) stereo pair, the per-tie-point reprojection {term}`residuals <residual>` before and after optimization:

![Histograms of initial and final bundle adjustment residuals from the WorldView tutorial](figures/wv3-ba-residuals-hist.png)

The same residuals in map view over the scene footprint (initial values above 10 px are shown clipped):

![Map view of initial and final bundle adjustment residuals](figures/wv3-ba-residuals-map.png)

Both figures come from the residual point maps `bundle_adjust` writes (`*-initial_residuals_pointmap.csv`, `*-final_residuals_pointmap.csv`), read with `asp_plot.bundle_adjust.PlotBundleAdjustFiles`. Look for two things: the residual hump moving toward zero, and no strong spatial pattern left in the final map.

## Where to read more

- [ASP bundle_adjust docs](https://stereopipeline.readthedocs.io/en/latest/tools/bundle_adjust.html)
- [Bundle adjustment in the ASP workflow](https://stereopipeline.readthedocs.io/en/latest/next_steps.html)

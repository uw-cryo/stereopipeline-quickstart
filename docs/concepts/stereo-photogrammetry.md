# Stereo photogrammetry

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

Two views of the same patch of ground from different angles produce parallax — a pixel shift between images that encodes ground height.

## What ASP actually computes

<!-- FIGURE IDEA: stereo-pair geometry diagram — two camera positions, a ground point, rays from each camera to the same point, and the disparity (delta-x, delta-y) shown on the image planes. Triangulation arrow showing how rays + cameras yield the 3D point. -->

For every pixel in the left image, ASP finds its match in the right image; the resulting disparity vectors plus the camera models triangulate to 3D ground coordinates.

## Knobs that matter

<!-- FIGURE IDEA: 2x2 hillshade comparison from the same input pair — asp_bm vs asp_mgm across the columns, subpixel-mode 1 vs 9 down the rows. Shows visually how much each knob affects the output. -->

The matcher (`--stereo-algorithm`) and the subpixel refiner (`--subpixel-mode`) are the two parameters that most affect quality and runtime.

## Geometry that matters

<!-- FIGURE IDEA: skyplot from asp_plot.stereo_geometry showing the two satellite positions and convergence angle for the WV3 tutorial pair. Pair with a text inset citing the convergence angle and B/H ratio. -->

Convergence angle and base-to-height ratio set the height precision achievable; both come from the satellite metadata and you can plot them with `asp_plot.stereo_geometry.StereoGeometryPlotter`.

## Where matching fails

<!-- FIGURE IDEA: panel of GoodPixelMap (run-GoodPixelMap.tif) crops over each failure mode — water, snow, dense canopy, sharp shadow boundary, building facade occlusion. Red/green pixels make the failures legible at a glance. -->

Featureless terrain, repetitive textures, occlusion, and strong illumination differences all break the matcher; `run-GoodPixelMap.tif` flags where matching succeeded.

## Where to read more

- [ASP stereo correlation docs](https://stereopipeline.readthedocs.io/en/latest/correlation.html)

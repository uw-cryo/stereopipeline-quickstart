# Stereo photogrammetry

From two views of the same patch of ground, the horizontal shift (parallax) of a pixel between the two images depends on:

- The baseline: distance between the two satellite positions.
- The convergence angle between the two viewing directions at the ground point.
- The height of the ground point relative to a reference surface.

If you know the first two from camera metadata, the third falls out of the parallax.

## What ASP actually computes

For every pixel `(x_L, y_L)` in the left image, ASP looks for its match `(x_R, y_R)` in the right image. The disparity at that pixel is the vector `(x_R - x_L, y_R - y_L)` after both images have been put into a common reference frame (by mapprojection or by an internal epipolar-alignment step).

```{mermaid}
flowchart LR
    L[Left pixel] -->|stereo correlator| D[Disparity vector]
    R[Right image<br/>search window] --> D
    D -->|triangulate with cameras| P[3D point]
```

With disparity for every pixel and the two camera models, ASP triangulates each match into a 3D ground coordinate.

## Knobs that matter

`--stereo-algorithm`
:   Which matcher to use. `asp_mgm` (modified semi-global matching) is the modern default. `asp_bm` (block matching) is faster but less robust on textured terrain.

`--subpixel-mode`
:   How to refine integer-pixel matches to fractional pixels. `9` (Bayes EM with MGM) is highest quality. `2` (parabolic fit) is faster.

`--corr-tile-size`
:   Tile size for parallelism. Larger tiles give better matching context but use more memory. Default 1024 is fine.

The full list is in the [ASP stereo docs](https://stereopipeline.readthedocs.io/en/latest/correlation.html).

## Geometry that matters

Convergence angle. Too small (<10°) and parallax is tiny, so height precision is poor. Too large (>40°) and the two images look too different to match. Typical range for natural terrain: 15-30°.

Base-to-height ratio (B/H). Inter-satellite baseline divided by altitude. Larger B/H gives better height precision. For Earth-orbiting satellites, 0.3-0.6 is typical.

`asp_plot.stereo_geometry.StereoGeometryPlotter` reads these from the XML metadata and plots them.

## Where matching fails

- Featureless terrain. Sand, snow, water, dense forest canopy. The matcher has nothing to lock onto.
- Repetitive textures. Agricultural rows, gravel rooftops. The matcher locks onto the wrong feature.
- Occlusion. Cliffs, building facades visible in only one image. No match available.
- Atmospheric or illumination differences. Strong shadow shifts between acquisitions confuse the matcher.

ASP's outputs include `run-GoodPixelMap.tif`, which flags pixels where matching succeeded. Check this before trusting the DEM.

## Where to read more

- [ASP stereo correlation docs](https://stereopipeline.readthedocs.io/en/latest/correlation.html)

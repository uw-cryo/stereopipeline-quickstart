# Alignment

After bundle adjustment + stereo + DEM generation, there's typically a residual bias relative to true ground. `pc_align` registers your DEM to a trusted reference using ICP (Iterative Closest Point).

## The reference dataset

| Body | Reference | Notes |
|---|---|---|
| Earth | ICESat-2 ATL06-SR | Sparse globally-distributed laser altimetry, ~10 cm vertical accuracy. Fetched on the fly via [SlideRule](https://slideruleearth.io/). |
| Moon | LOLA | Lunar Orbiter Laser Altimeter, queried via NASA ODE GDS. |
| Mars | MOLA PEDR | Mars Orbiter Laser Altimeter, also via ODE GDS. |
| Anywhere with prior data | An existing high-quality DEM | e.g. 3DEP, ArcticDEM, regional lidar. |

## What pc_align does

Given a "source" point cloud (your DEM, converted to points) and a "reference" point cloud (the altimetry or reference DEM):

1. For each source point, find the closest reference point.
2. Compute the rigid transformation (translation + optionally rotation + scale) that minimizes the sum of those nearest-neighbour distances.
3. Apply the transformation to the source.
4. Repeat until convergence.

Output: a translation vector (and optional rotation matrix) plus an aligned version of your DEM.

## When pc_align helps and when it doesn't

```{tip}
`pc_align` helps when the DEM has a near-uniform bias (a constant translation) or a small global tilt; both are common artefacts of imperfect bundle adjustment. It doesn't help when the DEM has localized errors (matching failures, blunders) or non-rigid deformation; only fixing the upstream stereo can address those.
```

`asp_plot.altimetry.Altimetry.align_and_evaluate()` runs `pc_align` and keeps the result if the median dh shrinks by more than a threshold (default 5%). If alignment didn't help, the aligned DEM is discarded.

## Reading the alignment report

`pc_align` prints a percentile breakdown of inter-point distances before and after alignment:

```
Beg errors -- 16%: 0.42, 50%: 0.95, 84%: 2.13, max: 4.50
End errors --  16%: 0.18, 50%: 0.41, 84%: 0.82, max: 1.94
Translation in north-east-down: -0.23 -1.42 0.61 m
```

The 50th percentile (median) is the headline metric. A drop from 0.95 m → 0.41 m is real signal. A drop from 0.55 m → 0.52 m means alignment didn't change much; either bundle adjustment was already good, or reference data is sparse here.

## The `--pc_align` flag in `asp_plot`

The simplest way to run alignment is to let the `asp_plot` CLI do it:

```bash
asp_plot --directory ./run --plot_altimetry --pc_align
```

This runs `pc_align` against ICESat-2 (Earth), MOLA (Mars), or LOLA (Moon) automatically based on the DEM's CRS, and adds an alignment-summary page plus pre/post comparison plots to the PDF report.

## Where to read more

- [ASP pc_align docs](https://stereopipeline.readthedocs.io/en/latest/tools/pc_align.html)
- [`asp_plot.altimetry`](https://asp-plot.readthedocs.io/en/latest/autoapi/asp_plot/altimetry/index.html)
- [`asp_plot.alignment`](https://asp-plot.readthedocs.io/en/latest/autoapi/asp_plot/alignment/index.html)

# Alignment

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

After bundle adjustment + stereo + DEM generation, residual bias remains relative to true ground; `pc_align` registers the DEM to a trusted reference using ICP.

## The reference dataset

ICESat-2 ATL06-SR for Earth, MOLA for Mars, LOLA for the Moon, or any prior high-quality DEM (3DEP, ArcticDEM, regional lidar).

## What pc_align does

<!-- FIGURE IDEA: ICP cartoon — a "source" point cloud (your DEM, in red) shown offset from a "reference" point cloud (ICESat-2 tracks, in black); arrows showing the translation that brings them together. Maybe a 2-3 frame animation showing iterations converging. Could be a static 3-panel sequence instead. -->

ICP iteratively finds the rigid transformation (translation, optional rotation, optional scale) that minimizes nearest-neighbour distances between the source point cloud (your DEM) and the reference.

## When pc_align helps and when it doesn't

<!-- FIGURE IDEA: two dh maps side by side — one dominated by a constant offset (pc_align fixes this) and one dominated by spatially-varying noise (pc_align cannot fix this). Caption: rigid bias vs localized errors. -->

It helps with near-uniform bias and small global tilt; it doesn't help with localized blunders or non-rigid deformation, which need fixing upstream.

## Reading the alignment report

<!-- FIGURE IDEA: example pc_align stdout snippet (Beg/End errors percentiles + translation vector) annotated with arrows pointing to the median, the translation magnitude, and what to do if the median doesn't drop. -->

`pc_align` prints percentile breakdowns of inter-point distances before and after; the median (50th percentile) drop is the headline metric.

## The `--pc_align` flag in `asp_plot`

`asp_plot --pc_align` runs `pc_align` against the appropriate altimetry reference based on the DEM's CRS and adds an alignment-summary page to the PDF report.

## Where to read more

- [ASP pc_align docs](https://stereopipeline.readthedocs.io/en/latest/tools/pc_align.html)

# What is the Ames Stereo Pipeline?

The NASA Ames Stereo Pipeline (ASP) turns pairs (or sets) of overlapping satellite or planetary images into digital elevation models (DEMs). It is open-source and runs from the command line.

If you've used commercial structure-from-motion software like Agisoft Metashape or Pix4D, ASP is the open-source equivalent for satellite-scale stereo: bigger pixels, longer baselines, rigid sensor models from XML metadata, and (often) just two images instead of dozens.

## Why "stereo"?

A single satellite image is an angular projection of a 3D scene onto a 2D sensor. You can't recover height from one image alone; a tall building and a short building at different positions can paint identical pixels.

```{mermaid}
flowchart LR
    A[Image A] --> S{Stereo<br/>matching}
    B[Image B] --> S
    S --> D[Disparity map]
    D --> P[Point cloud]
    P --> DEM[DEM]
```

But two images of the same patch of ground from different viewing angles give you parallax: pixels shift between the images by an amount that encodes their distance from the sensor. ASP's job is to:

1. Figure out the geometry of each image (where the satellite was, where it was pointing).
2. Find matching pixels between the two images.
3. Triangulate each match into a 3D coordinate, producing a point cloud.
4. Grid the point cloud into a regular DEM.

Everything ASP does is in service of one of those four steps.

## Why is it complicated, then?

Every step has subtle failure modes:

- The geometry from the satellite metadata is never quite right. Residual error from GNSS noise, attitude jitter, and clock drift introduces meters of bias into the final DEM. ASP has [`bundle_adjust`](../concepts/bundle-adjustment.md) to refine the camera models from the imagery itself.
- Stereo matching is hard on flat or repetitive terrain. Sand dunes, snow, water, agricultural fields all look like noise to a matcher. ASP exposes many knobs (algorithm choice, subpixel mode, search range) to handle different terrain types.
- Resampling the input imagery onto a coarse reference DEM ([mapprojection](../concepts/mapprojection.md)) makes matching easier, but adds processing steps.
- The output is only as accurate as the camera models. Even after bundle adjustment there's typically a 1-10 m bias relative to ground truth. ASP has [`pc_align`](../concepts/alignment.md) to register the DEM to a reference (ICESat-2, lidar, another DEM).
- Different sensors need different recipes. A WorldView-3 pair needs `wv_correct`, `bundle_adjust`, mapprojection, and `parallel_stereo`. An ASTER L1A pair needs `aster2asp` first. A Mars HiRISE pair needs `cam2map`. The high-level structure is the same; the per-sensor commands aren't.

## Where `asp_plot` fits

ASP outputs are scattered across TIFFs, CSVs, and log files (`run-DEM.tif`, `run-PC.tif`, `run-IntersectionErr.tif`, `run-final_residuals_pointmap.csv`, and many more). Inspecting all of them is what tells you whether the run was good.

[`asp_plot`](https://asp-plot.readthedocs.io/) reads ASP's outputs and produces:

- Diagnostic plots: disparity maps, residuals, hillshades, DEM-vs-reference difference maps.
- PDF reports: single summaries that capture parameters, runtimes, and all the diagnostic plots.
- Altimetry comparisons: DEM vs ICESat-2 (Earth), LOLA (Moon), or MOLA (Mars).

This guide uses `asp_plot` throughout.

## What's next

- [Pipeline overview](../concepts/pipeline-overview.md) — the full flow with one diagram.
- [Open the Codespace](codespaces.md) — run a real pipeline.
- [ASTER tutorial](../tutorials/01_aster_rainier.ipynb) — the gentlest end-to-end notebook.

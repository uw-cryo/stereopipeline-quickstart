# Pipeline overview

Every ASP run, regardless of sensor, follows the same five-stage pattern. Once you internalize this you can read any ASP tutorial and know what each command is doing.

## The five stages

```{mermaid}
flowchart TD
    A[Raw imagery + metadata] -->|aster2asp / wv_correct / cam2map| B[Sensor-prepared imagery]
    B -->|bundle_adjust<br/>OPTIONAL| C[Refined cameras]
    C -->|mapproject<br/>OPTIONAL| D[Mapprojected imagery]
    D -->|parallel_stereo| E[Disparity & point cloud]
    C -->|parallel_stereo<br/>direct path| E
    E -->|point2dem| F[DEM]
    F -->|pc_align<br/>OPTIONAL| G[Aligned DEM]
```

| # | Stage | Tool(s) | What changes |
|---|---|---|---|
| 1 | Sensor prep | `aster2asp`, `wv_correct`, `cam2map`, `dg_mosaic` | Raw vendor format → ASP-friendly imagery + camera files |
| 2 | Bundle adjustment (optional) | `bundle_adjust` | Camera models refined; offsets reduced |
| 3 | Mapprojection (optional) | `mapproject` | Imagery resampled onto a reference DEM grid |
| 4 | Stereo + DEM generation | `parallel_stereo`, `point2dem` | Matched pixels → point cloud → gridded DEM |
| 5 | Alignment (optional) | `pc_align`, `geodiff` | DEM registered to ground truth (ICESat-2 / lidar / another DEM) |

The tutorials in this repo follow this template.

## Stage 1: Sensor preparation

ASP wants two things from each input scene:

1. An image as a single-band raster file (GeoTiff, NTF).
2. A camera model describing where the satellite was and where it was pointing. Either an XML file (DigitalGlobe/Vantor) or generated on the fly (ASTER).

Most vendor data needs a per-sensor preprocessing step:

- ASTER L1A comes as either a directory of TIFFs (V003, legacy) or a single HDF (V004, current). `aster2asp` extracts the nadir (`Band3N`) and back-looking (`Band3B`) images plus their RPC camera files.
- WorldView-1 and WorldView-2 need `wv_correct` to remove a known sub-pixel CCD-boundary artefact. WorldView-3 doesn't.
- Tiled scenes (one acquisition delivered as multiple NTFs) need `dg_mosaic` to stitch them into one image-and-XML pair.
- Mars MOC / HiRISE / CTX need ISIS preprocessing (`mocproc`, `hi2isis`, `ctx2isis`) and often `cam2map` for mapprojection-equivalent reprojection in ISIS-land.

```{tip}
The sensor-prep step is where the most per-sensor knowledge lives. Once your imagery is in the standard "image.tif + image.xml" pair, the rest of the pipeline looks the same regardless of sensor.
```

## Stage 2: Bundle adjustment

The vendor camera models for any satellite are off slightly in position and attitude. This can translate to several meters of bias in the resulting DEM, and inconsistent bias between the images, which corrupts the stereo geometry.

`bundle_adjust` fixes this by:

1. Finding interest points (distinctive corners and blobs) in both images.
2. Matching them between images, so each match is a single 3D point seen twice.
3. Optimizing the camera positions and orientations to minimize the reprojection error of every match.

Outputs are an `*-clean.match` file (the matches), an updated camera adjustment, and `*-final_residuals_pointmap.csv` (per-match residuals you visualize with `asp_plot` to sanity-check the fit).

See [Bundle adjustment](bundle-adjustment.md) for the full story.

## Stage 3: Mapprojection

Stereo matching is easier when the two images are aligned in geographic space (the same patch of ground at the same pixel in both images). Mapprojection resamples each image onto a regular grid defined by a coarse reference DEM (Copernicus 30 m for Earth, MOLA for Mars, etc.).

```{mermaid}
flowchart LR
    L[Left image<br/>raw geometry] --> M1{mapproject}
    R[Right image<br/>raw geometry] --> M2{mapproject}
    DEM[Coarse reference DEM] --> M1
    DEM --> M2
    M1 --> LM[Left image<br/>on DEM grid]
    M2 --> RM[Right image<br/>on DEM grid]
```

After mapprojection the disparity (how much pixels shift between images) is dominated by the error in the coarse DEM, not by the satellite geometry. That residual is small and easy to match.

The tradeoff is one extra pass through the imagery and a dependency on having a reference DEM. For ASTER over land there's almost no reason not to mapproject. For very-high-resolution imagery over flat terrain, the unmapprojected (`alignment-method affineepipolar`) path can be fine.

See [Mapprojection](mapprojection.md).

## Stage 4: Stereo + DEM generation

`parallel_stereo` runs four sub-steps:

1. Preprocessing: image normalization, alignment matrices.
2. Stereo correlation: for every pixel in the left image, find its match in the right image. The output is a disparity map: a 2-band image where each pixel is the (x, y) shift to its match.
3. Subpixel refinement: sharpen the disparity to fractional-pixel accuracy.
4. Triangulation: combine disparities with the camera models to produce a 3D point cloud.

The point cloud (`run-PC.tif`) is gridded into a regular DEM by `point2dem`:

```bash
point2dem -r earth --auto-proj-center --tr 5 run_stereo/run-PC.tif
# → run_stereo/run-DEM.tif
```

`-r earth` selects the WGS84 datum; `--tr 5` sets the output resolution to 5 m.

See [Stereo photogrammetry](stereo-photogrammetry.md).

## Stage 5: Alignment

After bundle adjustment, the DEM is still in the vendor's coordinate frame, with typically a 1-10 m bias relative to ground truth. `pc_align` shifts and (optionally) rotates the DEM to minimize its difference against a trusted reference:

- Earth: ICESat-2 ATL06-SR (sparse but globally available, free, ~10 cm vertical accuracy).
- Moon: LOLA (Lunar Orbiter Laser Altimeter).
- Mars: MOLA (Mars Orbiter Laser Altimeter).
- Anywhere with prior coverage: an existing high-quality DEM.

The output is a translation vector (and optionally a rotation) plus a re-georeferenced version of the DEM in the reference frame.

See [Alignment](alignment.md).

## What asp_plot does at every stage

```{mermaid}
flowchart LR
    Raw -->|ScenePlotter| V1[Inspect inputs]
    BA -->|PlotBundleAdjustFiles| V2[Residuals before/after]
    Stereo -->|StereoPlotter| V3[Disparity, hillshade, dh]
    DEM -->|Altimetry| V4[DEM vs ICESat-2]
    All -->|asp_plot CLI| Report[PDF report]
```

Each ASP stage produces files; each `asp_plot` class consumes them. The `asp_plot` CLI ties it all together into a PDF report. See [Visualization](visualization.md).

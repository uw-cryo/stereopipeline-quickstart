# ASP output files

What the key files in an ASP run directory mean. Most are named with a `RUN_PREFIX-` followed by a fixed suffix. This is not every file, just those we are most interested in; the [ASP output files docs](https://stereopipeline.readthedocs.io/en/latest/outputfiles.html) describe everything.

## After `bundle_adjust -o ba/run`

| File | Contents |
|---|---|
| `ba/run-clean.match` | Final matches between images (binary) |
| `ba/run-initial_residuals_pointmap.csv` | Per-match reprojection residuals before optimization |
| `ba/run-final_residuals_pointmap.csv` | …after optimization |
| `ba/run-IMAGE.adjust` | Per-image camera adjustment (small text file) |
| `ba/log-bundle_adjust-*.txt` | Full log; ASP version, command line, runtime |

## After `mapproject`

| File | Contents |
|---|---|
| `IMAGE.map.tif` (or whatever you named it) | Image resampled onto reference DEM grid |

## After `parallel_stereo -o stereo/run`

| File | Contents |
|---|---|
| `stereo/run-L.tif`, `run-R.tif` | Preprocessed left/right images |
| `stereo/run-lMask.tif`, `run-rMask.tif` | Per-image masks |
| `stereo/run-D.tif` | Initial disparity from correlation, in whole-pixel shifts |
| `stereo/run-RD.tif` | Disparity after subpixel refinement |
| `stereo/run-F.tif` | Final disparity after outlier filtering; the input to triangulation |
| `stereo/run-GoodPixelMap.tif` | Gray where the correlator matched, red where it failed |
| `stereo/run-PC.tif` | Point cloud (4 bands: x, y, z as offsets from a local origin, and ray intersection error) |
| `stereo/run-stereo.default` | Snapshot of stereo parameters used |
| `stereo/log-stereo-*.txt` | Per-stage log files |

`run-D.tif`, `run-RD.tif`, and `run-F.tif` are successive versions of the same disparity map, all in one format: three bands holding the horizontal shift, the vertical shift, and a good-pixel mask. A run leaves further intermediates in the same format, such as `run-D_sub.tif` (the low-resolution disparity that seeds `run-D.tif`) and `run-B.tif` (`run-D.tif` blended across processing tiles).

## After `point2dem`

| File | Contents |
|---|---|
| `stereo/run-DEM.tif` | The DEM. Single-band float32, georeferenced. |
| `stereo/run-DRG.tif` | Orthoimage at the same grid (if `--orthoimage`) |
| `stereo/run-IntersectionErr.tif` | Intersection error gridded onto the DEM (if `--errorimage`) |
| `stereo/log-point2dem-*.txt` | Log |

## After `pc_align`

| File | Contents |
|---|---|
| `align/run-trans_source.tif` | Source point cloud after alignment (in reference frame) |
| `align/run-transform.txt` | 4×4 rigid transformation matrix |
| `align/run-inverse-transform.txt` | Inverse, for going back |
| `align/log-pc_align-*.txt` | Log with begin/end percentile errors |

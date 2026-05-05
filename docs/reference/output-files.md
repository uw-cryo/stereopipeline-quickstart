# ASP output files

What every file in an ASP run directory means. Most are TIFFs (sometimes encoding non-image data), and most are named with a `RUN_PREFIX-` followed by a fixed suffix.

## After `bundle_adjust -o ba/run`

| File | Contents |
|---|---|
| `ba/run-clean.match` | Final matches between images (binary) |
| `ba/run-initial_residuals_pointmap.csv` | Per-match reprojection residuals before optimization |
| `ba/run-final_residuals_pointmap.csv` | …after optimization |
| `ba/run-IMAGE.adjust` | Per-image camera adjustment (small text file) |
| `ba/log-bundle_adjust-*.txt` | Full log; ASP version, command line, runtime |

## After `mapproject`

Just the resampled images:

| File | Contents |
|---|---|
| `IMAGE.map.tif` (or whatever you named it) | Image resampled onto reference DEM grid |

## After `parallel_stereo -o stereo/run`

ASP produces ~15 files in the stereo directory:

| File | Contents |
|---|---|
| `stereo/run-PC.tif` | Point cloud (4-band: x, y, z, intersection error) |
| `stereo/run-F.tif` | Final disparity map (after subpixel refinement) |
| `stereo/run-D.tif` | Integer disparity (preprocessing step output) |
| `stereo/run-RD.tif` | Subpixel-refined disparity |
| `stereo/run-L.tif`, `run-R.tif` | Preprocessed left/right images |
| `stereo/run-lMask.tif`, `run-rMask.tif` | Per-image masks |
| `stereo/run-GoodPixelMap.tif` | Where matching succeeded (1) vs failed (0) |
| `stereo/run-IntersectionErr.tif` | Triangulation residual per pixel; useful blunder detector |
| `stereo/run-stereo.default` | Snapshot of stereo parameters used |
| `stereo/log-stereo-*.txt` | Per-stage log files |

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

## File-finding utility

`asp_plot.utils.glob_file()` is what every `asp_plot` class uses internally. You can use it directly:

```python
from asp_plot.utils import glob_file
dem = glob_file("./stereo", "*-DEM.tif")
match = glob_file("./ba", "*-clean.match")
```

It returns a `pathlib.Path` (or raises if zero or multiple matches).

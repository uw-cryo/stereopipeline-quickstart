# Parameter cheatsheet

The handful of ASP flags you'll set 90% of the time, with sensible defaults.

## `bundle_adjust`

```bash
bundle_adjust \
  --threads 8 \
  --ip-per-image 10000 \
  --tri-weight 0.1 \
  --tri-robust-threshold 0.1 \
  --camera-weight 0 \
  IMAGE_L.tif IMAGE_R.tif IMAGE_L.xml IMAGE_R.xml \
  -o ba/run
```

- `--ip-per-image 10000`: dense interest points; bump to 20000 over featureless terrain.
- `--tri-weight 0.1 --tri-robust-threshold 0.1`: anchors ground points without strangling the optimizer.
- `--camera-weight 0`: lets cameras move freely (default is to penalize movement).

Add `--mapproj-dem REFERENCE.tif` if you want geodiff-style residuals visualized.

## `mapproject`

```bash
mapproject --tr 0.5 --t_srs EPSG:32611 \
  REFERENCE_DEM.tif IMAGE.tif IMAGE.xml IMAGE.map.tif
```

- `--tr`: output GSD in meters. Use the more nadir image's `meanProductGSD`.
- `--t_srs`: target projection. Match what you'll use for `point2dem`.

If you bundle-adjusted, also pass `--bundle-adjust-prefix ba/run`.

## `parallel_stereo`

```bash
parallel_stereo \
  --threads-multiprocess 4 \
  --threads-singleprocess 8 \
  --stereo-algorithm asp_mgm \
  --subpixel-mode 9 \
  --corr-tile-size 1024 \
  --processes 4 \
  IMAGE_L.tif IMAGE_R.tif IMAGE_L.xml IMAGE_R.xml \
  stereo/run \
  REFERENCE_DEM.tif    # optional, for mapprojected stereo
```

- `--stereo-algorithm asp_mgm`: modern default; quality > speed.
- `--subpixel-mode 9`: Bayes-EM with MGM. Best quality. Use `2` (parabolic) for a fast first pass.
- `--processes 4`: parallelism budget; set to your CPU count.

For raw (non-mapprojected) input add `--alignment-method affineepipolar`.

For ASTER specifically: `-t aster --aster-use-csm`.

## `point2dem`

```bash
point2dem -r earth --auto-proj-center \
  --tr 5 \
  --errorimage \
  stereo/run-PC.tif
```

- `-r earth`: select WGS84. Use `mars` or `moon` for planetary.
- `--auto-proj-center`: auto-pick a UTM-like projection centered on the data.
- `--tr 5`: output resolution in meters.
- `--errorimage`: also write `*-IntersectionErr.tif` (sanity-check artefact).

## `pc_align`

```bash
pc_align \
  --max-displacement 100 \
  --num-iterations 1000 \
  --csv-format '1:lon 2:lat 3:height_above_datum' \
  --save-transformed-source-points \
  --datum WGS_1984 \
  REFERENCE.csv stereo/run-DEM.tif \
  -o align/run
```

For Mars/Moon use `--datum D_MARS` / `--datum D_MOON` and a `--csv-format` that includes the planetary radius.

For most users, the easier path is `asp_plot --pc_align` which sets all of these automatically based on the DEM CRS.

## `asp_plot`

```bash
asp_plot \
  --directory ./aster_rainier \
  --stereo_directory out_stereo_proj \
  --bundle_adjust_directory ba \
  --reference_dem ref/cop30.tif \
  --plot_altimetry True \
  --pc_align True \
  --subset_km 5 \
  --report_filename report.pdf
```

- `--plot_altimetry`: enables the ICESat-2 / LOLA / MOLA panel.
- `--pc_align`: runs `pc_align` against the reference altimetry.
- `--subset_km`: size of the high-detail hillshade window.

Full options: `asp_plot --help` or [the asp_plot CLI docs](https://asp-plot.readthedocs.io/en/latest/cli/asp_plot.html).

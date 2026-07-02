# 7. COP30 reference DEM: AWS Open Data + local EGM2008 to ellipsoid shift

- **Date:** 2026-05-04
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § COP30 reference DEM; commit 12b51b1

## Context
Both tutorials need a reference DEM for orthorectification and alignment. The Copernicus GLO-30 tiles on the public AWS Open Data bucket `copernicus-dem-30m` need no API key, but they ship heights referenced to the EGM2008 geoid.

ASP represents DEM heights as elevations above the datum ellipsoid. Its [`dem_geoid` docs](https://stereopipeline.readthedocs.io/en/latest/tools/dem_geoid.html) describe that tool's input as "a DEM whose height values are relative to the datum ellipsoid" (which `dem_geoid` then converts to the equipotential/geoid surface), and the [`mapproject` docs](https://stereopipeline.readthedocs.io/en/latest/tools/mapproject.html) specify the input DEM as "height above datum." Feeding a geoid-referenced DEM to `mapproject` without conversion is therefore a datum mismatch: the geoid undulation (tens of meters; about -35 m at UCSD) enters as a vertical offset that shows up as a constant bias in dh plots and gets absorbed by `pc_align`, masking real bundle-adjust residuals.

## Decision
`scripts/fetch_cop_dem.py` fetches GLO-30 from the AWS bucket and converts to WGS84 ellipsoid heights locally via `gdalwarp` with a compound CRS pair, mirroring `uw-cryo/fetch_dem`:

- Source: `EPSG:4326+EPSG:3855` (WGS84 lon/lat + EGM2008 geoid).
- Target: `<t_srs>+EPSG:4979` (requested horizontal + WGS84 ellipsoid).

`gdalwarp` applies the per-pixel geoid-to-ellipsoid shift via PROJ's bundled EGM2008 grid; `gdal_edit.py -a_srs` then re-asserts the compound CRS so downstream tools see the vertical component.

## Consequences
- **+** No API key, no auth: preserves the zero-friction launch.
- **+** Removes the 30-50 m vertical bias, so dh plots and `pc_align` reflect real residuals rather than a datum offset.
- **−** Depends on PROJ's EGM2008 grid being present (bundled in conda-forge `proj`, or auto-fetched via `PROJ_NETWORK`). If missing, `gdalwarp` errors loudly ("Cannot find proj.db" / "egm08_25.gtx"); pre-caching the grid in the Dockerfile is a fallback if this becomes flaky.
- The earlier version of this script did horizontal-only reprojection and shipped the geoid bias; the compound-CRS shift is the fix.

## Alternatives considered
- **OpenTopography API-key route for ellipsoid-referenced COP30** — rejected: adds an API key to an otherwise zero-key launch, for a conversion that is mechanical once the compound-CRS recipe is known.
- **Horizontal-only reprojection** (the original script) — rejected: leaves the 30-50 m geoid bias in place.

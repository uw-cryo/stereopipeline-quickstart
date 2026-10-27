# 28. Tutorial data on this repo's releases, fetched by the notebooks

- **Date:** 2026-10-27
- **Status:** Accepted; extends [0022](0022-ship-icesat2-data.md)
- **Context doc:** `ARCHITECTURE.md` § Tutorial data on releases

## Context
The tutorials fetched data from several hosts: the ASTER scene from Zenodo, the WorldView-3 pair from SpaceNet's AWS bucket with the AWS CLI, Copernicus DEM tiles from AWS Open Data through `fetch_cop_dem.py`, and the shipped ICESat-2 data ([ADR-0022](0022-ship-icesat2-data.md)) from releases of this repo. Each outside host is a place where files can move, change access rules or slow down. The COP30 fetch was slow wherever no prebuild had done it.

Codespace startup (`onCreate.sh`) also pre-fetched the ASTER data, so prebuilds held data. Twice, a Codespace made from an older prebuild had stale shipped files: the old ICESat-2 files after a regeneration, and a broken COP30 file after a fix.

Licences decide what may be re-hosted:

- The ASTER L1A archive is Zenodo record 10.5281/zenodo.7972223, CC BY 4.0 (attribution).
- Copernicus DEM data may be reproduced, distributed and modified under the Copernicus WorldDEM-30 licence, with a notice and a no-liability statement (Article 6).
- The WorldView-3 pair is IARPA CORE3D data in the `Hosted-Datasets/` folder of SpaceNet's bucket, which the bucket's CC BY-SA 4.0 licence explicitly excludes. CORE3D's own pages say the imagery is free for public research and that publications must cite Hagstrom et al. (2021); no redistribution grant was found.

## Decision
- One dated release per tutorial dataset, holding everything it needs that may be re-hosted, as separate assets: `aster-rainier-2026-10-27` (L1A archive, ICESat-2 points and figure selections, COP30 clip) and `ucsd-wv3-2026-10-27` (ICESat-2 points and figure selections, COP30 clip). The release notes record each file's source, licence and how it was made, with the attribution the licences require; `docs/reference/data.md` lists them for readers.
- The WorldView-3 imagery stays on SpaceNet's bucket, fetched over plain HTTPS with `curl`, so the AWS CLI is no longer needed for it.
- The notebooks' download cells fetch their dataset; `onCreate.sh` downloads nothing. A `RELEASE` marker per dataset replaces shipped files from an older release.
- Shipped COP30 clips are rewritten with their CRS inside the GeoTIFF (`gdal_translate -a_srs`), since `fetch_cop_dem.py` keeps its 3D CRS in an `.aux.xml` sidecar that a release asset wouldn't carry.

## Consequences
- **+** The ASTER tutorial depends on GitHub alone; the WorldView tutorials on GitHub and SpaceNet's bucket.
- **+** A Codespace always gets the data its checked-out code names; prebuilds hold no data that can go stale.
- **+** No COP30 fetch from AWS at run time, and no AWS CLI for the imagery.
- **−** The first run of each notebook downloads its data: about 55 MB for ASTER (seconds), about 1.8 GB for WorldView (as before).
- **−** A data change means a new dated release and a script change; old releases stay for older commits until deleted.
- **−** If SpaceNet's bucket moves or closes, the WorldView tutorials break, unless permission to re-host the imagery is obtained.

## Alternatives considered
- **Re-host the WorldView-3 imagery too** — rejected without an explicit redistribution grant for CORE3D.
- **One release for all tutorials** — rejected: datasets change independently, and each tutorial's release can then be replaced on its own.
- **Bundle each release into one archive** — rejected: the ASTER scene is already a zip, and separate assets keep each download and check simple.
- **Keep pre-fetching in `onCreate.sh`** — rejected: it is what put stale data in prebuilds, and a release download takes seconds.

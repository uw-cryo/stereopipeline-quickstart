# Data sources and licences

The tutorials use openly available data. Each download script fetches it into `data/<tutorial>/` the first time its notebook runs. Most of it comes from a dated release of this repository, so it doesn't depend on other hosts staying up or unchanged; the release notes record where each file came from.

## ASTER tutorial

Release: [`aster-rainier-2026-10-27`](https://github.com/uw-cryo/stereopipeline-quickstart/releases/tag/aster-rainier-2026-10-27), fetched by `scripts/download_aster.sh`.

| Data | Source | Licence |
|---|---|---|
| ASTER L1A scene, 2017-07-31, Mt. Rainier | Copy of Zenodo record [10.5281/zenodo.7972223](https://doi.org/10.5281/zenodo.7972223) (Bhushan, Henderson and Shean) | CC BY 4.0 |
| Reference DEM for the processing window | Copernicus GLO-30, clipped and converted to ellipsoid heights | Copernicus WorldDEM-30 licence (below) |
| ICESat-2 ATL06-SR points and report figure selections | Computed by [SlideRule](https://slideruleearth.io/) from NASA ICESat-2 ATL03 data | NASA data, free to use with credit |

## WorldView-3 tutorials

| Data | Source | Licence |
|---|---|---|
| WorldView-3 panchromatic scenes over Mount Soledad (UCSD), 2014-11-09, 2014-12-23 and 2015-01-24 | IARPA CORE3D public data, downloaded from SpaceNet's public AWS bucket by `scripts/download_worldview_ucsd.sh` | Released for public research. Publications using it should cite Hagstrom, Pak, Ku, Wang, Hager and Brown (2021), "Cumulative assessment for urban 3D modeling", IEEE IGARSS. Not re-hosted here |
| Reference DEM and ICESat-2 data | Release [`ucsd-soledad-2026-10-27`](https://github.com/uw-cryo/stereopipeline-quickstart/releases/tag/ucsd-soledad-2026-10-27), made as for the ASTER tutorial | As for the ASTER tutorial |

## Copernicus DEM notice

The tutorials' reference DEMs are produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. The organisations in charge of the Copernicus programme by law or by delegation do not incur any liability for any use of the Copernicus WorldDEM-30. See the [Licence for the use of the Copernicus WorldDEM-30](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/DEM/resources/license/License-COPDEM-30.pdf).

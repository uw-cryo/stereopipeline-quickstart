# Glossary

ASP and stereo photogrammetry vocabulary, with links to the deeper concept pages.

```{glossary}

ASP
  Ames Stereo Pipeline. NASA's open-source stereo photogrammetry toolkit. [Docs](https://stereopipeline.readthedocs.io/).

asp-plot
  The Python visualization companion to ASP. Reads ASP output files and produces diagnostic plots + PDF reports. [Docs](https://asp-plot.readthedocs.io/en/latest/).

ATL06-SR
  ICESat-2 Land Ice Height (sliderule edition) — the canonical Earth-altimetry product used for DEM alignment. Fetched on the fly via [SlideRule](https://slideruleearth.io/).

base-to-height ratio (B/H)
  Ratio of inter-satellite baseline to satellite altitude. Larger B/H = better height precision; typical 0.3–0.6 for Earth-orbiting satellites.

bundle adjustment
  Joint optimization of camera parameters and 3D tie-point positions to minimize reprojection error. ASP tool: `bundle_adjust`. See [Bundle adjustment](../concepts/bundle-adjustment.md).

camera model
  The mapping between image pixels and ground coordinates: where the sensor was, how it was oriented, and how its optics project the scene onto the detector. Supplied with the imagery (as RPC or a rigorous sensor model) and refined by bundle adjustment. See [Stereo photogrammetry](../concepts/stereo-photogrammetry.md).

CCD artifact
  Sub-pixel discontinuity at the boundary between adjacent CCD chips on push-broom sensors. WorldView-1 and -2 exhibit this; corrected by `wv_correct`. WorldView-3 does not.

convergence angle
  Angle between the two viewing directions of a stereo pair at the ground point. Sweet spot for natural terrain: 15–30°.

Copernicus DEM (COP30)
  Globally-available 30 m DEM, openly distributed on [AWS Open Data](https://registry.opendata.aws/copernicus-dem/). Default reference DEM for Earth tutorials.

CSM
  Community Sensor Model. A standard interface for rigorous sensor models; ASP ships the open USGS implementation (usgscsm). CSM state files expose the sensor's trajectory and orientation over time, which is what lets `jitter_solve` correct jitter. See [Stereo photogrammetry](../concepts/stereo-photogrammetry.md).

disparity map
  Per-pixel (x, y) shift between matched pixels in a stereo pair. ASP writes it in stages: `*-D.tif` (initial), `*-RD.tif` (subpixel-refined), and `*-F.tif` (filtered, final — the input to triangulation).

DEM
  Digital Elevation Model. A regular grid of heights — the final product of an ASP run. ASP file: `*-DEM.tif`. The umbrella term covering both DSM and DTM.

dh
  "Difference in height". Pixel-wise difference between two DEMs (or between a DEM and altimetry).

DSM
  Digital Surface Model. A DEM whose heights are of the first surface the sensor sees: rooftops, tree canopy, snow. Stereo DEMs, ASP's included, are surface models.

DTM
  Digital Terrain Model. A DEM whose heights are of the bare ground, with buildings and vegetation removed. Deriving one from a stereo DSM requires additional filtering.

ellipsoid
  Smooth mathematical model of a planet's shape (WGS84 for Earth). ASP heights are relative to the ellipsoid unless you convert them.

geodiff
  ASP tool that computes the difference between two DEMs and reports statistics.

geoid
  Equipotential surface approximating mean sea level (EGM96 or EGM2008 for Earth). Geoid and ellipsoid heights differ by tens of meters depending on location; mixing the two is a classic source of vertical bias. See [Orthorectification](../concepts/orthorectification.md).

ground sample distance (GSD)
  Pixel size of imagery on the ground, in meters. WV3 pan-sharp GSD ≈ 0.30 m; ASTER GSD ≈ 15 m.

hillshade
  Shaded-relief rendering of a DEM under a synthetic light source. The standard way to inspect DEM quality by eye; produced by `gdaldem hillshade` or `asp-plot`.

ICESat-2
  NASA's Ice, Cloud, and Land Elevation Satellite 2. Provides global laser altimetry used for DEM alignment.

ICP
  Iterative Closest Point. Registration algorithm that alternates pairing each point with its nearest reference neighbor and solving the rigid move that best fits the pairs. What `pc_align` runs. See [Alignment](../concepts/alignment.md).

interest point (IP)
  Distinctive corner or blob detected in an image, used as a candidate feature for matching across images.

jitter
  High-frequency satellite attitude variation that violates the rigid-camera assumption of standard sensor models. ASP corrects via `jitter_solve` (CSM cameras only).

LOLA
  Lunar Orbiter Laser Altimeter. Reference altimetry for Moon DEMs.

match file
  ASP file containing tie-point matches between two images. File extension `.match` (binary) or `.csv`.

MOLA
  Mars Orbiter Laser Altimeter. Reference altimetry for Mars DEMs.

NMAD
  Normalized Median Absolute Deviation — robust scale estimator. `1.4826 × median(|x - median(x)|)`. Equals std for normal distributions; resistant to outliers. Used everywhere `asp-plot` reports DEM error.

NTF
  NITF (National Imagery Transmission Format). Image format used by some commercial sensors.

orthorectification
  Resampling input imagery onto a regular geographic grid using a coarse reference DEM. Makes stereo matching dramatically easier. ASP's tool for this is `mapproject`, and ASP docs call the step "mapprojection". See [Orthorectification](../concepts/orthorectification.md).

parallax
  Apparent shift of a pixel between two images of the same ground point taken from different viewpoints. Encodes the height of the ground point.

pc_align
  ASP tool for ICP-based registration of point clouds. Used to align a DEM to ground-truth altimetry. See [Alignment](../concepts/alignment.md).

point cloud
  Unstructured 3D points produced by stereo triangulation. ASP file: `*-PC.tif` (encoded as a GeoTIFF for compactness).

point2dem
  ASP tool that grids a point cloud into a regular DEM.

reprojection error
  Distance, in pixels, between an observed image feature and the predicted position of its 3D ground point reprojected through the camera model. Bundle adjustment minimizes this.

residual
  Per-tie-point reprojection error. `asp_plot.bundle_adjust` plots these before and after bundle adjustment.

RPC
  Rational Polynomial Coefficients. A camera model that replaces the vendor's rigorous sensor model with fitted ratios of polynomials mapping longitude, latitude, and height to pixels. Compact and sensor-agnostic, and it keeps the physical camera details private; standard for commercial Earth-observation imagery. See [Stereo photogrammetry](../concepts/stereo-photogrammetry.md).

SfM
  Structure from Motion. The general algorithmic family that bundle adjustment + stereo belongs to.

SGM / MGM
  Semi-Global Matching / Modified Global Matching. The stereo-correlation algorithms ASP uses to produce highest quality results (`asp_sgm`, `asp_mgm`).

SlideRule
  Cloud-native API for on-demand ICESat-2 processing. `asp-plot` uses it to fetch ATL06-SR data.

SpaceNet
  Open dataset of high-resolution commercial satellite imagery, hosted on AWS. The UCSD WV3 scenes used in this guide come from the SpaceNet CORE3D collection.

stereo
  ASP's master command for stereo correlation + triangulation. The parallel version (`parallel_stereo`) is what tutorials actually use.

subpixel mode
  Setting that controls how `parallel_stereo` refines integer-pixel matches; e.g. mode 9 (Bayes EM with MGM).

tie point
  A single 3D ground point observed (and matched) in two or more images. Bundle adjustment optimizes camera parameters using tie-point reprojection errors.

WorldView
  DigitalGlobe / Vantor high-resolution Earth-observation satellite series (WV1, WV2, WV3, WV4). All push-broom; the vendor XML carries both an exact linescan camera model and an RPC fit.

```

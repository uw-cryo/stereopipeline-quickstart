# Glossary

ASP and stereo photogrammetry vocabulary, with links to the deeper concept pages.

```{glossary}

ASP
  Ames Stereo Pipeline. NASA's open-source stereo photogrammetry toolkit. [Docs](https://stereopipeline.readthedocs.io/).

asp_plot
  The Python visualization companion to ASP. Reads ASP output files and produces diagnostic plots + PDF reports. [Docs](https://asp-plot.readthedocs.io/).

ATL06-SR
  ICESat-2 Land Ice Height (sliderule edition) — the canonical Earth-altimetry product used for DEM alignment. Fetched on the fly via [SlideRule](https://slideruleearth.io/).

base-to-height ratio (B/H)
  Ratio of inter-satellite baseline to satellite altitude. Larger B/H = better height precision; typical 0.3–0.6 for Earth-orbiting satellites.

bundle adjustment
  Joint optimization of camera parameters and 3D tie-point positions to minimize reprojection error. ASP tool: `bundle_adjust`. See [Bundle adjustment](../concepts/bundle-adjustment.md).

CCD artifact
  Sub-pixel discontinuity at the boundary between adjacent CCD chips on push-broom sensors. WorldView-1 and -2 exhibit this; corrected by `wv_correct`. WorldView-3 does not.

convergence angle
  Angle between the two viewing directions of a stereo pair at the ground point. Sweet spot for natural terrain: 15–30°.

Copernicus DEM (COP30)
  Globally-available 30 m DEM, openly distributed on [AWS Open Data](https://registry.opendata.aws/copernicus-dem/). Default reference DEM for Earth tutorials.

CSM
  Community Sensor Model. A pluggable camera-model standard ASP can use as an alternative to RPC for some sensors. Used in jitter-correction workflows.

disparity map
  Per-pixel (x, y) shift between matched pixels in a stereo pair. ASP file: `*-F.tif`.

DEM
  Digital Elevation Model. A regular grid of heights — the final product of an ASP run. ASP file: `*-DEM.tif`.

dh
  "Difference in height". Pixel-wise difference between two DEMs (or between a DEM and altimetry).

geodiff
  ASP tool that computes the difference between two DEMs and reports statistics.

ground sample distance (GSD)
  Pixel size of imagery on the ground, in meters. WV3 pan-sharp GSD ≈ 0.30 m; ASTER GSD ≈ 15 m.

ICESat-2
  NASA's Ice, Cloud, and Land Elevation Satellite 2. Provides global laser altimetry used for DEM alignment.

interest point (IP)
  Distinctive corner or blob detected in an image, used as a candidate feature for matching across images.

jitter
  High-frequency satellite attitude variation that violates the rigid-camera assumption of standard sensor models. ASP corrects via `jitter_solve` (CSM cameras only).

LOLA
  Lunar Orbiter Laser Altimeter. Reference altimetry for Moon DEMs.

mapprojection
  Resampling input imagery onto a regular geographic grid using a coarse reference DEM. Makes stereo matching dramatically easier. See [Mapprojection](../concepts/mapprojection.md).

match file
  ASP file containing tie-point matches between two images. File extension `.match` (binary) or `.csv`.

MOLA
  Mars Orbiter Laser Altimeter. Reference altimetry for Mars DEMs.

NMAD
  Normalized Median Absolute Deviation — robust scale estimator. `1.4826 × median(|x - median(x)|)`. Equals std for normal distributions; resistant to outliers. Used everywhere `asp_plot` reports DEM error.

NTF
  NITF (National Imagery Transmission Format). Image format used by some commercial sensors.

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
  Rational Polynomial Coefficients. Compact parametric camera model used by most commercial Earth-observation satellites.

SfM
  Structure from Motion. The general algorithmic family that bundle adjustment + stereo belongs to.

SGM / MGM
  Semi-Global Matching / Modified Global Matching. The stereo-correlation algorithms ASP uses to produce highest quality results (`asp_sgm`, `asp_mgm`).

SlideRule
  Cloud-native API for on-demand ICESat-2 processing. `asp_plot` uses it to fetch ATL06-SR data.

SpaceNet
  Open dataset of high-resolution commercial satellite imagery, hosted on AWS. The UCSD WV3 scenes used in this guide come from the SpaceNet CORE3D collection.

stereo
  ASP's master command for stereo correlation + triangulation. The parallel version (`parallel_stereo`) is what tutorials actually use.

subpixel mode
  Setting that controls how `parallel_stereo` refines integer-pixel matches; e.g. mode 9 (Bayes EM with MGM).

tie point
  A single 3D ground point observed (and matched) in two or more images. Bundle adjustment optimizes camera parameters using tie-point reprojection errors.

WorldView
  DigitalGlobe / Vantor high-resolution Earth-observation satellite series (WV1, WV2, WV3, WV4). All push-broom; all use RPC camera models.

```

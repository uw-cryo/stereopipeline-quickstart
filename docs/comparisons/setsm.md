# SETSM — WorldView-3, Mount Soledad

Compare DEMs produced by two open-source stereo photogrammetry pipelines on the same WorldView-3 stereo pair:

- **ASP** (NASA Ames Stereo Pipeline) — processed in [Tutorial 2](../tutorials/02_worldview_ucsd.ipynb)
- **[SETSM](https://github.com/setsmdeveloper/SETSM)** (Surface Extraction with TIN-based Search-space Minimization) — Ohio State / Polar Geospatial Center

Both pipelines accept raw satellite imagery with {term}`RPC` camera models and produce gridded {term}`DSMs <DSM>`.

## Source Data

The same WorldView-3 pair as [Tutorial 2](../tutorials/02_worldview_ucsd.ipynb), as the tutorial prepares it: a 3 × 3 km window around the summit of Mount Soledad, cut from each image with `cam2rpc` and averaged to 1.2 m pixels (the native 0.31 m pixels, 4 × 4 at a time). Both images come from the IARPA CORE3D SpaceNet UCSD dataset.

| Catalog ID | Date | Off-nadir | Crop size |
|---|---|---|---|
| 104001000496A100 | 2014-11-09 | 1.1° | 2738 × 2805 px |
| 10400100071D8800 | 2015-01-24 | 16.3° | 2623 × 2645 px |

The pair's convergence angle is 16.8°. Each tool gets the same two crops and their RPC cameras, and writes a 2.4 m DEM, the tutorial's output grid. ASP's DEM is the tutorial's own, made from the orthorectified crops after bundle adjustment, as the notebook describes.

## Approach

SETSM is open-source (Apache 2.0), pure C++ with no GPU requirement. We built and ran it via Docker to avoid host dependency conflicts.

SETSM reads `*.tif` images with a WorldView-style XML camera file of the same name next to each one. The tutorial's crops are GeoTIFFs, but the camera files `cam2rpc` writes hold only the RPC coefficients, and SETSM reads more than that from a WorldView XML: the image corners (`<BAND_P>`), from which it picks the UTM zone; the pixel size and satellite ID (`<IMAGE>`); and the RPC error terms, which `cam2rpc` writes as 0. Run on the crops as they are, SETSM found no overlap between the images: with no corners it chose UTM zone 31 south. `scripts/docs_figures/setsm_inputs.py` copies the crops to a folder with camera files that add those fields, with the corners computed from each crop's RPC and the pixel size from the vendor's XML times the averaging factor.

The crops are small (about 8 million pixels each), so SETSM processes them whole; the `-boundary_*` flags that limit a run to part of a full scene aren't needed.

Also, note that SETSM's user manual warns against `-seed <filepath> <sigma>`: *"We caution that it is better to not use a seed DEM if possible, as it can only negatively impact the quality of the SETSM DEM."*

:::{dropdown} Docker build details
:icon: terminal

```bash
git clone https://github.com/setsmdeveloper/SETSM.git
cd SETSM

docker build --platform linux/amd64 -t setsm -f- . <<'DOCKERFILE'
FROM ubuntu:24.04 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ make git \
    libgeotiff-dev libtiff-dev libproj-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . /opt/SETSM
WORKDIR /opt/SETSM
RUN make INCS="-I/usr/include/geotiff"

FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgeotiff5 libgomp1 libtiff6 libproj25 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/SETSM/setsm /usr/local/bin/setsm
COPY --from=builder /opt/SETSM/default.txt /usr/local/share/setsm/default.txt
WORKDIR /data
ENTRYPOINT ["sh", "-c", "cp /usr/local/share/setsm/default.txt /data/default.txt 2>/dev/null; exec setsm \"$@\"", "--"]
DOCKERFILE
```

Multi-stage build — the final image contains only the `setsm` binary and runtime libraries. The `default.txt` config file is bundled and auto-copied at runtime (SETSM requires it in the working directory).
:::

## Run

```bash
docker run --platform linux/amd64 --rm --memory 11g --cpus 6 \
    -v /path/to/setsm_inputs:/data -v /path/to/output:/out -w /data setsm \
    -image 104001000496A100_P001.tif -image 10400100071D8800_P001.tif \
    -outpath /out/results -outres 2.4 -mem 10 -minH -50 -maxH 300 -projection utm
```

`-minH`/`-maxH` span the window's heights (COP30 ranges from −32 to 216 m here). `scripts/docs_figures/run_comparisons.sh` runs this and the CARS run below.

| Metric | Value |
|---|---|
| Computation time | 15 min 29 s (Apple M-series laptop, amd64 emulation, 6 CPUs) |
| Peak memory (SETSM-reported) | 668 MB |
| Output DEM | 1396 × 1434 px (the crops' overlap), 2.4 m, EPSG:32611 |
| Convergence angle | 16.8° |

### Hillshade Comparison

SETSM resolves the same hills, canyons, streets and blocks of houses as ASP, and leaves no voids where ASP has a few (0.8% of the window, mostly at the freeway interchange and along building edges). Its surface is noisier pixel to pixel, which shows as a fine speckle in the hillshade. SETSM's DEM sits 10.9 m below ASP's (median difference): SETSM uses the vendor RPCs as they are, while Tutorial 2 ties the cameras to COP30 heights in bundle adjustment, which removes the vendor offset. Apart from that offset the two DEMs agree to 1.4 m (NMAD).

::::{grid} 2
:::{grid-item}
![ASP 2.4 m](figures/soledad-asp-hillshade.png)
**ASP 2.4 m DEM**
<div class="fullres-btns">
  <a class="fullres-btn" href="../_images/soledad-asp-hillshade.png" target="_blank" rel="noopener noreferrer">Open at full resolution ↗</a>
</div>
:::
:::{grid-item}
![SETSM 2.4 m](figures/soledad-setsm-hillshade.png)
**SETSM 2.4 m DEM**
<div class="fullres-btns">
  <a class="fullres-btn" href="../_images/soledad-setsm-hillshade.png" target="_blank" rel="noopener noreferrer">Open at full resolution ↗</a>
</div>
:::
::::

```{raw} html
<a href="https://maps.google.com/?ll=32.8396,-117.2413&z=15&t=k" target="_blank" rel="noopener noreferrer">View the comparison area in Google Maps</a>
```

## References

- [SETSM repository](https://github.com/setsmdeveloper/SETSM)
- [SETSM user manual](https://github.com/setsmdeveloper/SETSM/blob/master/SETSM_User_manual.pdf)
- Noh & Howat (2015), "Automated stereo-photogrammetric DEM generation at high latitudes: Surface Extraction with TIN-based Search-space Minimization (SETSM) validation and demonstration over glaciated regions", *GIScience & Remote Sensing*, 52(2), 198-217.

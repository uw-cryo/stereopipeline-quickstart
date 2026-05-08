# Local install

To run things on your own machine instead of in a [Codespace](../start/codespaces.md):

## Requirements

- Linux or macOS. ASP releases binaries for Linux x86_64, Linux ARM64, and macOS (Intel and Apple Silicon). Windows users should use WSL2 with the Linux binary.
- ~5 GB free disk for ASP and python deps; tutorials need another 5-10 GB for imagery and intermediate outputs.
- Python 3.12+

## Step 1 — Install ASP

Download the latest release tarball from the [ASP releases page](https://github.com/NeoGeographyToolkit/StereoPipeline/releases) and extract somewhere stable:

```bash
# Example for Linux x86_64; pick the right tarball for your platform.
ASP_VERSION=3.6.0
ASP_BUILD_DATE=2025-12-26
curl -fL -o asp.tar.bz2 \
  https://github.com/NeoGeographyToolkit/StereoPipeline/releases/download/${ASP_VERSION}/StereoPipeline-${ASP_VERSION}-${ASP_BUILD_DATE}-x86_64-Linux.tar.bz2

mkdir -p ~/opt
tar -xjf asp.tar.bz2 -C ~/opt
mv ~/opt/StereoPipeline-* ~/opt/StereoPipeline

# Add to PATH (drop into your shell rc to make it permanent)
export PATH="$HOME/opt/StereoPipeline/bin:$PATH"
```

Verify:

```bash
parallel_stereo --version
# parallel_stereo (Ames Stereo Pipeline) 3.6.0
```

## Step 2 — Install asp_plot

`asp_plot` and its python deps are easiest via conda/mamba:

```bash
# Create a clean env (recommended)
mamba create -n asp -c conda-forge python=3.12 \
  jupyterlab notebook ipywidgets \
  gdal rasterio rioxarray geopandas shapely pyproj contextily \
  boto3 s3fs awscli matplotlib seaborn

mamba activate asp

pip install asp-plot
```

Or, if you prefer pure pip (and you already have the geospatial stack installed):

```bash
pip install asp-plot jupyterlab boto3 s3fs contextily
```

## Step 3 — Clone this repo and run a tutorial

```bash
git clone https://github.com/uw-cryo/stereopipeline-quickstart.git
cd stereopipeline-quickstart

# Optional: pre-fetch the ASTER demo data (~80 MB)
bash scripts/download_aster.sh

jupyter lab notebooks/01_aster_rainier.ipynb
```

## Conda-only install (no binary download)

ASP is on conda-forge, though typically a release or two behind:

```bash
mamba create -n asp -c conda-forge stereo-pipeline asp-plot python=3.12
mamba activate asp
```

Check `parallel_stereo --version` against the [releases page](https://github.com/NeoGeographyToolkit/StereoPipeline/releases). For very recent features, use the binary install above.

## Verifying everything works

```bash
# ASP toolchain
which parallel_stereo bundle_adjust point2dem mapproject pc_align aster2asp dg_mosaic

# Python toolchain
python -c "import asp_plot, rasterio, geopandas; print(asp_plot.__version__)"
```

If both succeed you're ready for the [tutorials](../tutorials/index.md).

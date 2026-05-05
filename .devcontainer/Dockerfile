# stereopipeline-quickstart container image
# ----------------------------
# Layer 1 — base image with conda + a sane VS Code remote user
# Layer 2 — runtime apt deps used by ASP binaries
# Layer 3 — ASP binary tarball pinned by ARG, extracted to /opt/StereoPipeline
# Layer 4 — conda env "asp" with asp_plot and notebook deps
#
# Build context is the REPO ROOT — both the GitHub Actions workflow
# (.github/workflows/build-image.yml) and the devcontainer.json fallback
# (`"context": ".."`) invoke docker build from the repo root, so paths like
# `.devcontainer/environment.yml` mirror the on-disk layout.

FROM mcr.microsoft.com/devcontainers/miniconda:1-3

ARG ASP_VERSION=3.6.0
ARG ASP_BUILD_DATE=2025-12-26
ARG ASP_TARBALL=StereoPipeline-${ASP_VERSION}-${ASP_BUILD_DATE}-x86_64-Linux.tar.bz2
ARG ASP_URL=https://github.com/NeoGeographyToolkit/StereoPipeline/releases/download/${ASP_VERSION}/${ASP_TARBALL}

# ------------------------------------------------------------------------------
# Layer 2 — runtime libraries
# ------------------------------------------------------------------------------
# ASP's GUI tools (stereo_gui, etc.) link against an X11/GL stack even when
# invoked headlessly; without these libs `parallel_stereo` can fail to load
# shared objects on minimal base images. `parallel` is used by some ASP shell
# helpers, `jq` is convenient for the postCreate scripts.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl bzip2 parallel jq \
        libx11-6 libxfixes3 libxinerama1 libpixman-1-0 libxrender1 \
        libxi6 libxrandr2 libxcursor1 libxcomposite1 libxdamage1 \
        libglib2.0-0 libgl1 libxxf86vm1 libdrm2 libxcb-glx0 libxcb-dri2-0 \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Layer 3 — install Ames Stereo Pipeline binaries
# ------------------------------------------------------------------------------
# Stream-extract the ~1.5 GB tarball directly from the releases URL so the
# compressed archive never lands on disk. Trim the `libexec` test binaries
# and bundled docs after extract — saves a few hundred MB and we don't ship
# tutorials that exercise them.
RUN curl -fsSL "${ASP_URL}" | tar -xj -C /opt \
    && mv /opt/StereoPipeline-${ASP_VERSION}-${ASP_BUILD_DATE}-x86_64-Linux /opt/StereoPipeline \
    && rm -rf /opt/StereoPipeline/libexec/test* /opt/StereoPipeline/share/doc \
    && /opt/StereoPipeline/bin/stereo --version

ENV PATH=/opt/StereoPipeline/bin:${PATH}

# Also expose ASP via /etc/profile.d so login-interactive shells (which is how
# Codespaces invokes lifecycle scripts under `loginInteractiveShell` env probe)
# pick it up regardless of how conda activation rearranges PATH in ~/.bashrc.
#
# We APPEND (not prepend) /opt/StereoPipeline/bin so ASP's bundled python at
# /opt/StereoPipeline/bin/python doesn't shadow the conda env's python (the
# conda env is the one with asp_plot, rasterio, etc. installed). The case
# guard makes this idempotent — on subsequent shell starts it won't keep
# duplicating the path.
RUN printf '%s\n' \
        'case ":${PATH}:" in' \
        '  *":/opt/StereoPipeline/bin:"*) ;;' \
        '  *) export PATH="${PATH}:/opt/StereoPipeline/bin" ;;' \
        'esac' \
        > /etc/profile.d/99-asp.sh \
    && chmod 0644 /etc/profile.d/99-asp.sh

# ------------------------------------------------------------------------------
# Layer 4 — python environment for asp_plot + notebooks
# ------------------------------------------------------------------------------
# Using mamba (already present in the miniconda image) for fast solves. We pin
# Python 3.12 — asp_plot's floor is 3.11 (per its pyproject.toml), but
# sliderule >= 5.3 (which asp_plot 1.14 pulls in) uses PEP 701 nested-quote
# f-strings that only parse on 3.12+, so 3.11 fails at import time.
COPY .devcontainer/environment.yml /tmp/environment.yml
RUN conda install -n base -c conda-forge -y mamba \
    && mamba env create -f /tmp/environment.yml \
    && mamba clean -afy

# Make the asp env the default for interactive shells inside the container.
RUN echo "source activate asp" >> /home/vscode/.bashrc \
    && echo "source activate asp" >> /root/.bashrc

ENV CONDA_DEFAULT_ENV=asp \
    PATH=/opt/conda/envs/asp/bin:${PATH}

# Sanity check at build time — fail fast if either toolchain is broken.
RUN python -c "import asp_plot, rasterio, geopandas; print('asp_plot', asp_plot.__version__)" \
    && which parallel_stereo bundle_adjust point2dem mapproject pc_align aster2asp dg_mosaic

"""Tiny helper module for the stereopipeline-quickstart tutorial notebooks."""
from __future__ import annotations

from pathlib import Path


def icesat2_check(
    dem_fn: str | Path,
    directory: str | Path = ".",
    *,
    processing_levels: tuple[str, ...] = ("all",),
) -> None:
    """ICESat-2 ATL06-SR mapview + landcover-stratified histogram vs a DEM.

    Mirrors the pattern in `asp_plot/notebooks/ASTER/aster_with_mapprojection.ipynb`:
    derives `map_crs` from the DEM, configures Esri WorldImagery basemap kwargs,
    fetches ATL06-SR via SlideRule (parquet-cached), then renders the two panels.
    """
    import contextily as ctx
    from asp_plot.altimetry import Altimetry
    from asp_plot.utils import Raster

    epsg = Raster(str(dem_fn)).get_epsg_code()
    map_crs = f"EPSG:{epsg}"
    ctx_kwargs = {
        "crs": map_crs,
        "source": ctx.providers.Esri.WorldImagery,
        "attribution_size": 0,
        "alpha": 0.5,
    }

    icesat = Altimetry(directory=str(directory), dem_fn=str(dem_fn))
    icesat.request_atl06sr_multi_processing(
        processing_levels=list(processing_levels),
        save_to_parquet=True,
    )
    icesat.mapview_plot_atl06sr_to_dem(
        key=processing_levels[0], map_crs=map_crs, **ctx_kwargs
    )
    icesat.histogram_by_landcover(key=processing_levels[0])

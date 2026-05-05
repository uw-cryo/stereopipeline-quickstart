# Mapprojection

Stereo matching is easier when the images are nearly aligned in geographic space. Mapprojection, resampling each image onto a regular grid defined by a coarse reference DEM, does that. It's optional but often worth running.

## The intuition

Without mapprojection the stereo matcher must search a wide pixel range to find each match (the parallax can be tens of pixels because the satellite geometry is doing the heavy lifting). After mapprojection the parallax is dominated by the error in the reference DEM, which is typically just a few pixels. The matcher's job becomes much easier.

```{mermaid}
flowchart TB
    subgraph Without
        A1[Raw L] --> S1[Stereo with<br/>large search range]
        A2[Raw R] --> S1
    end
    subgraph With
        B1[Mapprojected L] --> S2[Stereo with<br/>small search range]
        B2[Mapprojected R] --> S2
        REF[Reference DEM] --> M[mapproject]
        M --> B1
        M --> B2
    end
```

## When you can skip it

- Very flat terrain (deltas, urban rooftops at uniform height) where the raw geometry is already nearly epipolar.
- Sensors where good reference DEMs don't exist.
- Quick first passes where you'll re-process with mapprojection once you have a working DEM.

For these cases ASP can run stereo on raw imagery with `--alignment-method affineepipolar` (estimates an in-image alignment from the matches alone).

## What reference DEM to use

| Region | DEM | Resolution | Source |
|---|---|---|---|
| Earth (anywhere) | Copernicus GLO-30 | 30 m | [AWS Open Data](https://registry.opendata.aws/copernicus-dem/) (free, no auth) |
| Earth (USA/AK) | 3DEP | 1-10 m | USGS |
| Earth (high latitudes) | ArcticDEM / REMA | 2 m | PGC |
| Mars | MOLA blended | 200 m | USGS |
| Moon | LOLA | 60-512 m | LRO archive |

For most Earth tutorials Copernicus DEM is the right answer. Globally available, free, and easily clipped from AWS.

## The two-pass mapprojection trick

A common ASP recipe (used in the ASTER tutorial here):

1. Run stereo on raw imagery to produce a coarse DEM.
2. `point2dem --tr 200` to make a low-resolution version of that DEM.
3. Mapproject the input images onto that DEM (not Copernicus).
4. Re-run stereo on the mapprojected imagery.

Why? Your own coarse DEM is more locally accurate than a global reference, so the second-pass disparity is even smaller and matching is even cleaner.

## Where to read more

- [ASP mapproject docs](https://stereopipeline.readthedocs.io/en/latest/tools/mapproject.html)
- [ASP stereo with mapprojected images](https://stereopipeline.readthedocs.io/en/latest/examples/aster.html#aster) (the official ASTER recipe)

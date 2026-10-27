# 27. ASTER quick look: `asp_mgm` on a window around the summit

- **Date:** 2026-10-26
- **Status:** Accepted; amends [0023](0023-split-aster-tutorial.md)
- **Context doc:** `ARCHITECTURE.md` § ASTER two-report workflow

## Context
[ADR-0023](0023-split-aster-tutorial.md) made Tutorial 1 a fast quick look: the whole raw ASTER scene through `asp_bm` with `--subpixel-mode 1`, about 5 minutes of stereo in a 4-core Codespace. Its DEM is the first result a new user sees, and a colleague found stair-steps in it.

Seven variants of that stereo step were compared on the same raw images (laptop, 4-core settings), by hillshade, by the difference to COP30, and by how many disparities sit on whole pixels:

- The stair-steps are pixel-locking from `--subpixel-mode 1`, which ASP's documentation calls a draft mode. Its disparities have a spike at exactly whole pixels.
- `asp_bm` with subpixel modes 3 or 2 removes the locking, but block matching on these images still smooths away ridges and gorges, at about 4.7× and 17× the run time.
- `asp_mgm` with `--subpixel-mode 9`, the settings of ASP's own ASTER example, keeps ridges, gorges and the texture of the summit glaciers, and is closer to COP30 (NMAD about 17 m against 21 m, unaligned). On the whole scene it takes about 2.5× as long.
- On a 2100 × 2100 px window of the nadir image around the summit (about 31 km on a side), `asp_mgm` runs in about the old time, with the same quality over that window and a smaller gap at the summit.

## Decision
Tutorial 1 runs `asp_mgm` with `--subpixel-mode 9` and `--left-image-crop-win 1800 2100 2100 2100`, one process with four threads like the other `asp_mgm` runs. Tutorial 2 orthorectifies only the extent of Tutorial 1's DEM (`mapproject --t_projwin`) and keeps the same stereo settings, so orthorectification is the only processing difference between the two reports. Tutorial 1 says that the summit gap remains on raw images and that Tutorial 2's orthorectification fills most of it.

The shipped ICESat-2 points and figure selections ([ADR-0022](0022-ship-icesat2-data.md)) are regenerated from a run of the new Tutorial 1 and published on a new dated release.

## Consequences
- **+** The first DEM has no stair-steps and keeps the terrain's detail, in about the old run time.
- **+** Both ASTER tutorials use the same matcher, so the comparison between their reports is about orthorectification alone.
- **+** Tutorial 2 orthorectifies and correlates a smaller area, so it runs faster too.
- **−** Neither tutorial covers the whole scene any more; dropping the crop option in Tutorial 1 and `--t_projwin` in Tutorial 2 restores it, at about 2.5× the stereo time.
- **−** The raw DEM still has a gap at the summit, where the snow is steep and bright.
- **−** The triangulation-error panel shows along-track banding (about 20–35 m) in every variant: it comes from the ASTER cameras, not the correlator, and these settings don't change it.

## Alternatives considered
- **Keep `asp_bm`, change only the subpixel mode** — rejected: modes 3 and 2 remove the stair-steps but not the smoothing, and cost 4.7× and 17× the time.
- **`asp_mgm` on the whole scene** — rejected for the first tutorial: about 13 minutes of stereo in a Codespace.
- **`asp_sgm` with subpixel mode 9 on the same window** — about a minute faster, slightly further from COP30.
- **A gentler site than Rainier** — not needed: the summit gap is acceptable as long as Tutorial 1 says that Tutorial 2 improves it.

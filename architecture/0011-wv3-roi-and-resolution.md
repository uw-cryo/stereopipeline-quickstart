# 11. WV3 ROI + resolution: coastal 2x2 km, TR 1.0 / 4 m DEM

- **Date:** 2026-06-10
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § WV3 ROI and resolution; issue #7

## Context
Under the 4-core floor (ADR-0010), the WorldView-3 UCSD pair had to fit an acceptable tutorial runtime. Correlation cost scales with pixel count, so the region-of-interest and processing GSD are the biggest levers. A very small crop, though, yields too few ICESat-2 points for a meaningful `asp_plot` altimetry report. The ROI and resolution went through several iterations chasing this balance.

## Decision
Use `T_PROJWIN = "476000 3637000 478000 3639000"` in UTM 11N: the coastal 2x2 km clip from the sea cliffs to the UCSD campus. Process at `TR = 1.0` (`mapproject`) and output `point2dem --tr 4.0`, a 4 m DEM. `asp_mgm` stereo runs `--processes 1 --threads-multiprocess 4 --threads-singleprocess 4` (MGM is memory-heavy and multithreads within a process, so few-processes-many-threads fits the 16 GB tier; `--processes 4` would risk OOM). `bundle_adjust` and `mapproject` use `--threads 4`.

## Consequences
- **+** At TR 1.0 the clip is roughly 4 Mpix/image versus about 40 Mpix at native, the single biggest correlation speedup.
- **+** The coastal cliffs-to-campus landscape is a compelling teaching scene.
- **−** 4 m is coarse for WV3, a deliberate teaching-artifact tradeoff; bump `TR` down on a larger machine.
- **−** The coastal clip has sparser ICESat-2 coverage than a crossover ROI east of UCSD (`477750 3634800 480750 3637800`, which has denser tracks); the landscape was preferred over point density.

## Alternatives considered
- **3x3 km ICESat-2 crossover east of UCSD at TR 0.5** — rejected: denser altimetry but larger/slower and a less compelling scene.
- **Native-GSD coastal 2x2 km / 0.5 m / 2 m variants** — intermediate iterations; too slow at the 4-core floor.
- **A very small crop** — rejected: too few altimetry points for the report.

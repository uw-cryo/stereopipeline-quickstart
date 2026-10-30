# 29. WorldView tutorials on Mount Soledad crops: one pair, then three pairs blended

- **Date:** 2026-10-27
- **Status:** Accepted; supersedes [0011](0011-wv3-roi-and-resolution.md) and [0012](0012-no-ba-canonical-wv.md). The crop flow (cam2rpc, 1.2 m, 2.4 m DEMs, bundle adjustment tied to COP30) is replaced by [0037](0037-wv3-full-resolution-box.md); the scenes, the release and the three-pair blend stand
- **Context doc:** `ARCHITECTURE.md` § WV3 window, crops and resolution

## Context
The two WorldView-3 tutorials processed a 2 × 2 km coastal window of the UCSD pair `1040010007A93700`/`1040010007CA4D00`. Tutorial 2 orthorectified straight from the NTFs with the vendor cameras and made a 4 m DEM in about 6 minutes. Tutorial 3 repeated it with bundle adjustment on the full scenes, which took about 16 of its 20 minutes. The 4 m DEMs looked coarse and noisy for 0.3 m imagery, and the pair was not one that the later benchmark studies of the SpaceNet UCSD and Atlanta stacks rated well.

Tutorial-sized alternatives were tested on a laptop at the Codespace's 4 threads (about 2.1× faster than a 4-core Codespace), scored against ICESat-2 and against those benchmarks' native-resolution DEMs:

- **Atlanta (WorldView-2, re-hostable):** three-view stereo and single pairs on crops around the airport, at ~1 m and ~2 m. Accurate at ~1 m (0.33 m NMAD on 2.5 km), but the flat airport shows every bit of noise in a hillshade, and ~1 m over 5 km took about 38 minutes of stereo in a Codespace.
- **UCSD crop A (Mount Soledad, 3 × 3 km, the cropped benchmark's window):** scenes nadir `104001000496A100`, n16 `10400100071D8800`, n24 `10400100057DD500`, cropped with `cam2rpc` and averaged to ~1.2 m. Four flows: one raw pair, the same pair orthorectified, three-view stereo, and three raw pairs blended. All scored 1.33–1.40 m NMAD after a horizontal shift, against 1.29–1.40 m for the benchmark's DEMs from native 0.31 m pixels on the same points. The relief makes clean hillshades.
- Bundle adjustment on the crops takes about 10 seconds, against about 16 minutes on the full scenes.
- One stereo job per stage (`--job-size-w/-h 4096`) instead of 2048-pixel tiles cut stereo time by about 30% with the same DEM.
- The vendor cameras put the ground about 8 m too low here (ICESat-2 minus DEM median +7.97 m for the orthorectified pair). Bundle adjustment with `--heights-from-dem <COP30> --heights-from-dem-uncertainty 10` brought it to +0.43 m, with the same NMAD and fill.

## Decision
- Both WorldView tutorials use crop A of Mount Soledad, in `data/ucsd_soledad/`: `cam2rpc` crops each NTF to the window plus 250 m with an RPC camera, and `average_crop()` (in `notebooks/utils.py`) averages 4 × 4 pixels and rescales the camera. Every later step runs on the crops with `-t rpc`.
- **Tutorial 2 (`02_worldview_ucsd.ipynb`):** the nadir–n16 pair (16.9°, the most accurate pair against lidar in the full-scene benchmark). Bundle adjustment, `mapproject` onto COP30 at 1.2 m, `asp_mgm` stereo, a 2.4 m DEM, the report. Orthorectified, though raw stereo scored the same, because the orthoimages make good figures; the surface is a little smoother, which Ben accepted.
- **Tutorial 3 (`03_worldview_ucsd_blend.ipynb`, replaces `03_worldview_ucsd_ba.ipynb`):** all three scenes, bundle adjusted together, stereo on the three pairs without orthorectification, blended with `dem_mosaic` (mean). The benchmarks found blending all pairs the best UCSD flow, ahead of joint multi-view triangulation. The report uses the first pair's stereo directory and the blend via `--dem-filename`.
- One release, `ucsd-soledad-2026-10-27`: COP30 over the window plus 2 km, the ICESat-2 points over it, and one figure-selection sidecar per report. It replaces `ucsd-wv3-2026-10-27`. The imagery stays on SpaceNet's bucket ([ADR-0028](0028-tutorial-data-on-releases.md)); the download script takes the catids to fetch, so Tutorial 2 downloads two scenes and Tutorial 3 adds the third.
- Bundle adjustment holds the features to the COP30 heights (`--heights-from-dem`, 10 m uncertainty), so the DEMs need no vertical shift.
- WorldView stereo passes `--job-size-w 4096 --job-size-h 4096`.

## Consequences
- **+** Both tutorials now teach bundle adjustment, at almost no run-time cost.
- **+** 2.4 m DEMs that match the benchmarks' native-resolution accuracy, on terrain whose hillshade reads well.
- **+** Tutorial 3 shows the multi-pair flow the benchmarks recommend.
- **−** Tutorial 2 downloads about 1.7 GB and Tutorial 3 another 0.85 GB, from SpaceNet.
- **+** The DEMs land within about 0.5 m of ICESat-2 before `pc_align`, instead of 8–11 m off.
- **−** `scene_bbox()` and `utm_epsg()` are gone from `utils.py`; the window is now given, not derived from the footprints.

## Alternatives considered
- **Atlanta WorldView-2 three-view** — its imagery could ship on a release, but at tutorial pixel sizes the flat airport's hillshade looked noisy next to the full strips, and runs were too slow.
- **Three-view (joint multi-view) stereo at UCSD** — as accurate, but left holes at the summit and was slower than one pair.
- **~0.6 m crops** — about 4× the stereo time for the pair; one 6000-pixel MGM job also ran out of memory.
- **Keep the old pair and window** — the 4 m DEM looked coarse, and full-scene bundle adjustment took most of Tutorial 3.

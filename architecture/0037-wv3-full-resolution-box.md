# 37. WorldView tutorials at full resolution on a 1 km square in Los Peñasquitos Canyon, with the census matching cost

- **Date:** 2026-10-30
- **Status:** Accepted; replaces the crop flow and the window of [0029](0029-ucsd-soledad-tutorials.md) (its choice of scenes and its blend flow stand)
- **Context doc:** `ARCHITECTURE.md` § WV3 window and resolution, § WV3 matching cost

## Context
Since [0029](0029-ucsd-soledad-tutorials.md) both WorldView tutorials cropped a 3 × 3 km window out of each scene with `cam2rpc`, averaged it to 1.2 m and made 2.4 m DEMs. The group's review found the hillshades coarse for 0.3 m imagery, and the crop step existed only to make bundle adjustment on the full scenes tractable.

The workbench study `2026-10-worldview-tutorial-sites` settled the flow and the place in four steps.

1. **Full resolution without a crop.** Six 640 m areas of the nadir–16° pair at native resolution: `mapproject --t_projwin` on the full NTF reads only the window (about 20 s), stereo in four tiles takes about 2 minutes on a laptop, and the DEMs resolve single houses, trees, trails and gullies with 0.7–1.7 % voids. `bundle_adjust --mapprojected-data` on the orthoimages takes seconds, where the full scenes ran 35 minutes without finishing. The vendor cameras sit a consistent 10 m low; bundle adjustment tied to COP30 removed that but warped the DEMs, and relative-only adjustment changed nothing for the pair, whose cameras already agree.
2. **The matching cost.** The Mount Soledad area first chosen showed a diagonal cross-hatch in its hillshade. Scored against the USGS 3DEP 1 m lidar, it was MGM's path streaking over a surface that ASP's default ternary census cost had over-smoothed: the slope's real spurs and gullies were flattened (NMAD 1.51 m). `--cost-mode 3`, plain census, restored them at the same run time (0.95 m); window size made no difference; Bayes EM, affine and block-matching refinements also recovered the gullies but were 2–4× slower and wavy or holey. Gridding, resampling and jitter were ruled out.
3. **The place.** The Soledad area's houses and freeway looked noisy in the orthoimages, so every 1 km window of the 13 × 14 km overlap was ranked by lidar slope. The steep natural ones are two canyons north-east of UCSD and Torrey Pines; a canyon at the west end of Los Peñasquitos Canyon Preserve scored best (NMAD 0.50 m against the lidar, 0.8 % voids). All 35 scenes of the stack cover the whole overlap; pairs with an identical sun, and a summer pair with a high sun, all scored worse than the current nadir–16° pair, so the scenes stay.
4. **The size.** Buildings, parking and roads from OpenStreetMap, rasterized over the canyon with the lidar slope, scored every placement of eleven box shapes. The canyon is hemmed in by housing on three sides, so squares of 1.2 km or more take in a corner of houses; a 1200 × 1000 m rectangle up the canyon has 0.15 % of its area in buildings and the steepest mean slope, at 184 s of stereo on a laptop with four tiles in parallel (about 6.5 minutes in a Codespace, measured factor 2.1), under the 8 minutes Ben set as the limit. But four tiles in parallel finish together, so the live map filled in all at once; tiles one after another (`--processes 1 --threads-multiprocess 4`) fill it in tile by tile at 28 % more time, and the rectangle's west kilometre as a square (0.10 % buildings, the steepest mean slope of any 1 km square) gives that back.

The third scene's camera disagrees with the other two by several meters (pair DEMs 7.7 m and 2.9 m off the nadir–16° pair), so the three pairs cannot be blended as they are.

## Decision
- Both WorldView tutorials work at the images' own resolution on one 1 km square at the west end of Los Peñasquitos Canyon, `T_PROJWIN = "480420 3641720 481420 3642720"` in UTM 11N: steep chaparral spurs and gullies on both sides of a creek, with trails and no buildings. The data folder, the download script's release and the output names are `ucsd_penasquitos`, `ucsd-penasquitos-<date>` and `penasquitos_*`.
- No crop step. `mapproject -t dg --tr 0.3125 --t_projwin <box>` reads the box out of each full NTF with the vendor XML camera: the square is exactly 3200 × 3200 pixels, which stereo splits into four 1600-pixel tiles run one after another (`--processes 1 --threads-multiprocess 4`), so the live map fills in tile by tile. `point2dem --tr 1`: three times the image pixel, the usual ratio for WorldView DEMs (ArcticDEM and REMA post 2 m from 0.5 m imagery). The trial's 0.5 m DEMs resolved the same gullies, with matcher speckle between them, at four times the file size.
- Stereo passes `--stereo-algorithm asp_mgm --subpixel-mode 9 --cost-mode 3`.
- Tutorial 2 does no bundle adjustment and does not discuss it; the docs cover it. The report's comparison with ICESat-2 shows the cameras' 10 m offset, and its `pc_align` removes it. The square holds fewer than the 500 ICESat-2 points `asp_report` wanted before it ran `pc_align`, so asp_plot gained `--pc-align-min-points` (3.6) and both reports pass 150; the notebooks show the aligned profile.
- Tutorial 3 keeps bundle adjustment, now `bundle_adjust -t dg --mapprojected-data "<three orthos> <COP30>" <NTFs> <XMLs>`, relative only (no `--heights-from-dem`), and the pairs' stereo passes `--bundle-adjust-prefix` with the same unadjusted orthoimages. Its text says why: the three cameras disagree, and averaging DEMs that sit meters apart would smear every edge.
- A new release carries the COP30 clip over the box, the ICESat-2 points and the reports' figure selections, since the old ones covered Mount Soledad.
- `average_crop()` is gone from `notebooks/utils.py`.

## Consequences
- **+** 1 m DEMs in which trees, trails and gullies are visible, from the same downloads: Tutorial 2 in about 12 minutes, Tutorial 3 in about 22 more.
- **+** One fewer step in Tutorial 2 and no `cam2rpc` or RPC-camera subtleties anywhere.
- **−** Both tutorials' DEMs sit about 10 m below ICESat-2 until the report's `pc_align`, where the old flow's bundle adjustment to COP30 had removed that. The ICESat-2 profile before and after makes the point. The docs' alignment page keeps its `pc_align` example from the ASTER tutorial. The Codespace image needs asp-plot 3.6 for `--pc-align-min-points`.
- **−** The census cost makes low-relief scrub look grainier, since it resolves bush canopies the ternary cost smoothed.
- **−** Tutorial 3's pair DEMs have about 4 % voids where Tutorial 2's same pair has 0.9 %: with the adjusted cameras the triangulation error drops from 2.6 m to 5 cm, so `point2dem`'s outlier filter, which scales with it, drops the tree points along the creek. Re-orthorectifying with the adjusted cameras changes nothing (voids 4.60 % against 4.56 %, NMAD against the lidar 0.51 against 0.50 m), so the pairs keep the unadjusted orthoimages. The blend brings the voids to 1.5 %.
- The SETSM and CARS comparison pages, made on the old crops, need redoing on the new inputs, and the concept pages' WorldView figures regenerating.

## Alternatives considered
- **Keep the crops at 1.2 m** — the hillshades were the complaint.
- **Bundle adjustment tied to COP30 in Tutorial 2** — removes the 10 m offset but warps the DEM; a vertical shift to ICESat-2 afterward does the same without touching the stereo geometry.
- **Bayes EM or affine subpixel refinement** — gullies recovered, but 2–4× slower and wavy.
- **A larger census window** — no change once the cost is census.
- **An 800 m square on the east side of Mount Soledad** — chosen first for its ribbed slope; its houses and freeway looked noisy in the orthoimages.
- **Pairs with the same sun elevation** — all less accurate than the current pair against the lidar; the high-sun summer pair worst, since the shadows are the texture the matcher uses.
- **A 1200 × 1000 m box** — the first choice; with sequential tiles its stereo would be about 8 minutes per pair in a Codespace, and its east 200 m were the flat valley floor.
- **A 1400 × 1000 m box** — about 7.4 minutes in a Codespace with parallel tiles, but it touches houses at its west and north-east edges.
- **Four tiles in parallel** — 28 % faster, but the tiles finish together and the map fills in all at once.
- **Squares of 1.2 km or more** — every placement takes in a corner of housing.

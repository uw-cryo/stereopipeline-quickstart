# 31. ASP output to log files; a status line, log tail and live map in the notebook

- **Date:** 2026-10-28
- **Status:** Accepted
- **Context doc:** `ARCHITECTURE.md` § Notebook path and helper conventions

## Context
A colleague's feedback on Tutorial 1:
- New users couldn't tell what a run was doing.
- ASP's output is verbose. VS Code truncates long cell output to its last lines below "…", so the useful parts scrolled out of view.
- A stereo run showed nothing for minutes.
- New users may not know to scroll down to see progress.

Each tool ran as a `!` shell line, timed with `%%time`, with all of its output in the cell.

## Decision
Each ASP command in Tutorial 1 runs through a helper in `notebooks/utils.py`. The helper sends the command's full output to a log file and shows a short summary in the cell.

- **`run(cmd, log, label)`**
  - **Command line:** prints the command on one line.
  - **Log:** writes all output to `data/<tutorial>/logs/<step>.log`.
  - **While it runs:** shows the last 5 lines of the log in small grey text, and a ⏳ status line with the time so far, both updated every second.
  - **When it ends:** the tail is cleared and the line says ✅ with the time. On failure it says ❌, prints the last 30 log lines and stops the cell.
- **`run_stereo(cmd, prefix, log)`**, the same for `parallel_stereo`, with three additions:
  - **Stage and time left:** the stage in plain words, the tile, and an estimate of the time left.
  - **Match figure:** `asp-plot`'s match-point figure as soon as the match file exists.
  - **Live map:** a two-panel map that fills in as tiles finish: each tile's shift between the images (`-D.tif`) and its heights (`-PC.tif`).
- **`timer(label)`:** the same status line for slow Python steps.
- **Code cells:** the close-panel extension collapses them, so a cell shows its first line and its output.

Details that shape the implementation:

- **Log tail:**
  - **Unbuffered Python:** commands run with `PYTHONUNBUFFERED=1`. ASP's Python wrappers (`mapproject`, `parallel_stereo`, `asp_report`) otherwise hold their output back while it goes to a file.
  - **Per-tile output:** `parallel_stereo` and `mapproject` collect each tile's output from the C++ tools and print it when the tile ends, so within a tile the tail doesn't move. Running the command on a pseudo-terminal was tried and dropped: the tile output arrives no sooner. A partial tail is enough to show the run is moving.
  - **Warnings:** lines starting with "Warning:" (any case) are left out of the tail and kept in the log. Most are routine notes, such as the estimated memory use per tile, which would worry a new user.
- **Time left:**
  - **When it appears:** the estimate starts after the first stage.
  - **Machine speed:** it scales the later stages' laptop times by how much slower the finished stages ran, so it adapts to the machine.
  - **Within a stage:** it uses the time per tile so far, so it counts down between tiles.
  - **Why it was reworked:** an earlier version used fixed laptop shares of the run. In a Codespace it climbed to "About 6 min 04 s left", then showed "About 0 s left" for the last 20 s. The status file reads `stereo_pprc` during the low-resolution matching. After the last tile, it goes through the stages again with 0 tiles done while the full-size outputs are written; the status line then says so.
- **Live map:**
  - **Placement:** tiles are placed by pixel position in the left image. This works for orthorectified images, whose pixel grid is the map grid.
  - **Collar:** each tile's `-D.tif` covers a margin (collar) on the sides that border another tile, which is cut off.
  - **Timing:** `parallel_stereo` deletes the tile folders when it ends, so the map is drawn while it runs.
  - **Image format:** figures are displayed as PNG images, since a `matplotlib.figure.Figure` made without pyplot has no PNG display in a notebook.
- **Match figure:** `StereoPlotter` won't start without a DEM in the stereo directory, though the match plot doesn't read it, so the left image is passed as `dem_fn`. Its printed notes are kept out of the cell, and any failure just skips the figure.
- **Collapsed code:** VS Code ignores the notebooks' `jupyter.source_hidden` metadata, so the close-panel extension collapses the code cells with `notebook.cell.collapseCellInput` when a tutorial opens.

## Consequences
- **+** **Short cells:** each step's cell shows what is running, that it is moving, and how long it took, in a few lines. The full output is still in a file.
- **+** **Something to watch:** stereo now shows a figure within the first minute or two in a Codespace, and the map fills in while it runs.
- **+** **Errors stay visible:** on failure the cell shows the end of the log and stops, rather than burying the error in pages of output.
- **−** **Less visible commands:** cells call helpers rather than plain shell lines. The command is still printed, and it is in the cell's (collapsed) code.
- **−** **Code to maintain:** `run_stereo()` reads `parallel_stereo`'s status file and tile folders, which a new ASP version could change. If it can't read them, it shows less but the run is unaffected.
- **−** **Laptop stage times:** the time-left estimate uses stage times from one laptop run of Tutorial 1. Other tutorials and machines rely on the scaling.

## Alternatives considered
- **Full output in the cells**, the old way: rejected for the reasons in Context.
- **VS Code's output settings** (`notebook.output.textLineLimit`, `notebook.output.scrolling`): they change how much of the output shows, not what it says. The cell is still a wall of ASP output.
- **A status line only, with no log tail:** tried first. Between status updates it wasn't clear that anything was happening.
- **One `parallel_stereo` job per stage** (`--job-size-w/-h` larger than the window): about 30% faster for the WorldView crops, but the map would fill in only once per stage. Tiles were preferred. Tutorial 1 uses four equal tiles (`--job-size-w 1280 --job-size-h 1202`), at the same run time as the default 2048-pixel tiles. The WorldView tutorials keep one job (decided 2026-10-28): on their 2,500 to 3,900-pixel windows each tile's margin costs more, and four tiles made stereo about 46% slower (Tutorial 2, 124 → 181 s on a laptop), two tiles about 15%. Their map appears once after matching and once after triangulation.

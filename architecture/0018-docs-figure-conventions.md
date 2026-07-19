# 18. Docs figures: hand-authored SVGs on an opaque light surface; data figures from real runs

- **Date:** 2026-07-07
- **Status:** Accepted
- **Context doc:** `ARCHITECTURE.md` § Docs content state; PR #16

## Context
Fleshing out the concept pages (issue #6) required two kinds of figures: conceptual diagrams (pipeline flows, stereo geometry cartoons, ICP before/after) and data-backed plots (bundle-adjust residuals, stereo-geometry skyplots). The site theme (`sphinx-book-theme`) has a light/dark toggle that stamps `data-theme` on the page root, but figures embed as `<img>`, so neither page CSS nor the toggle can restyle their contents; a `prefers-color-scheme` rule inside an SVG follows the OS setting, not the in-page toggle. Diagrams therefore need to be legible on both themes as-is. For the data plots, the guide teaches `asp_plot` as the visualization layer, so mocked or hand-drawn "data" would undercut the material.

## Decision
Two figure conventions, both stored in a `figures/` dir next to the page that uses them (mirroring `comparisons/figures/`):

- Conceptual diagrams are hand-authored SVGs drawn on an opaque light surface (`#fcfcfb` rounded rect with a hairline border) with dark ink, so the same file reads correctly on the light and dark themes. Shared visual language: blue `#2a78d6` for tool boxes/accents, gray chips for data artifacts, dashed strokes for optional steps, system-UI sans with monospace for tool names.
- Data-backed figures are matplotlib/`asp_plot` PNG outputs generated from real ASP runs on the tutorial datasets and committed, like the comparisons hillshades. Provenance is stated in the page prose (e.g. the BA residual figures come from a `bundle_adjust` run matching the tutorial-3 config). Display-only transformations (clipping outliers) are disclosed in the figure or its caption.

## Consequences
- **+** One figure file per figure works on both themes; no per-theme variants to keep in sync.
- **+** SVG diagrams are diffable text, editable without design tools, and stay crisp at any zoom.
- **+** Data figures show what learners will actually see from `asp_plot`, and their numbers are real.
- **−** Light-surfaced figures form visible light cards on the dark theme (accepted; same as the existing PNG hillshades).
- **−** Regenerating data figures requires local runs; the generating scripts live outside the repo, so provenance rests on the prose note and the run outputs under `data/` (gitignored).

## Alternatives considered
- **Theme-aware SVGs via CSS variables or `prefers-color-scheme`** — rejected: `<img>`-embedded SVGs can't see page CSS variables, and `prefers-color-scheme` ignores the site's own toggle, giving wrong-theme figures whenever the toggle disagrees with the OS.
- **Inline the SVGs into the page HTML so CSS can style them** — rejected: MyST/Sphinx image handling, figure numbering, and the full-res pattern all assume file images; inlining complicates authoring for a cosmetic gain.
- **Mermaid for the flow diagrams** — rejected: adds a dependency (`sphinxcontrib-mermaid`), renders client-side with its own theming, and gives less layout control than hand-authored SVG.
- **Fabricate illustrative "data" plots** — rejected: the repo's style rules bar unverified numbers, and mocked diagnostics would teach readers to expect plots `asp_plot` doesn't produce.

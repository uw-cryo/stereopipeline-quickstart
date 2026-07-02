# 9. Tool comparisons stay qualitative, not journal-grade quantitative

- **Date:** 2026-05-31
- **Status:** Accepted (boundary tracked in [#10](https://github.com/uw-cryo/stereopipeline-quickstart/issues/10), which remains open)
- **Context doc:** `AGENTS.md` § `docs/comparisons/` section; PRs #5, #8, #10

## Context
`docs/comparisons/` (PR #5) runs the same WorldView-3 UCSD pair through ASP, CARS, and SETSM (MicMac proposed in #8) and shows the hillshades side by side. A genuinely quantitative comparison would need best/worst-case scenario inputs (urban vs natural, steep vs flat, vegetated vs arid), per-tool parameter tuning for each scenario, and an objective validation-based quality criterion (ICESat-2, hillshade quality, DEM-quality metrics). That is a large research effort, better suited to an open-source journal than to beginner docs.

## Decision
Keep the comparisons qualitative: run each tool with reasonable settings on one shared pair, show the hillshades, and discuss differences without ranking. `comparisons/index.md` carries an explicit scope-disclaimer note (qualitative, no quantitative ranking). These pages ship fully authored, unlike the WIP concept skeletons (ADR-0004).

## Consequences
- **+** Readers see concrete, reproducible run recipes for each tool without the docs overreaching into research claims they cannot support.
- **+** Sets a clear boundary that keeps the section maintainable.
- **−** No objective "which tool is best" answer here by design; that question is deferred to #10 and, if pursued, a journal venue.

## Alternatives considered
- **Full quantitative benchmark across scenarios and tools** — rejected for these docs: a big task whose output belongs in a paper, not a quickstart.
- **Omit comparisons entirely** — rejected: a qualitative side-by-side is useful context for someone choosing a pipeline, as long as its scope is stated.

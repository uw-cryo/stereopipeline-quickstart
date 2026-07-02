# 5. "Orthorectification" (concept) vs mapproject (ASP tool) naming

- **Date:** 2026-05-07
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § "Orthorectification" vs "mapproject"; commit 9cde15e

## Context
ASP calls the step of resampling input imagery onto a reference DEM grid "mapprojection", and its binary is `mapproject`. That term is ASP-specific jargon; "orthorectification" is the concept name a newcomer from the wider photogrammetry world already recognizes.

## Decision
Use "orthorectification" for the concept in user-facing prose (docs and notebook markdown). Keep ASP's own names ("mapprojection", `mapproject`, `--mapproj-dem`, directory names like `out_stereo_proj`) verbatim wherever they appear as code, filenames, or CLI references. Each affected page carries a callout note surfacing the naming gap.

## Consequences
- **+** Prose meets newcomers with a familiar concept word.
- **+** Code and CLI references stay faithful to ASP, so copy-pasted commands work and match the upstream docs.
- **−** Two words for one thing; the callout notes exist to prevent confusion.
- **Convention:** do not rename `mapproject`, `--mapproj-dem`, or `*_proj`/`out_stereo_proj`-style paths in code cells. Output DEM products are named with the `_ortho` suffix (concept term); the tool invoked to make them is still `mapproject`.

## Alternatives considered
- **Use "mapprojection" everywhere** — rejected: leads with ASP jargon a beginner has to decode.
- **Use "orthorectification" everywhere, including renaming code/paths** — rejected: breaks fidelity to the ASP CLI and the upstream docs users will graduate to.

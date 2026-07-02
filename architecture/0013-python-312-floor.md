# 13. Python 3.12 floor (sliderule PEP 701 f-strings)

- **Date:** 2026-06-10
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § Python 3.12 (not 3.11)

## Context
`asp_plot`'s pyproject allows Python >= 3.11. But `sliderule >= 5.3` (pulled in transitively as of `asp_plot` 1.14) uses PEP 701 nested-quote f-strings that only parse on Python 3.12+. On 3.11 the `asp_plot` CLI hard-fails at `import asp_plot.altimetry` with a `SyntaxError`.

## Decision
Pin the conda env to Python 3.12 in `environment.yml`, and document the 3.12 floor in `installation.md`.

## Consequences
- **+** The `asp_plot` altimetry path imports and runs; the ICESat-2 comparison in the reports works.
- **−** A hard 3.12 floor for this repo, slightly ahead of `asp_plot`'s own 3.11 minimum. This is a transitive constraint from sliderule, so it may relax if that dependency changes.

## Alternatives considered
- **Follow asp_plot's 3.11 minimum** — rejected: breaks `import asp_plot.altimetry` with a SyntaxError from sliderule's f-strings.

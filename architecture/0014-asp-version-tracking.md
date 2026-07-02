# 14. Automated ASP-version tracking via PR-based bumps, not auto-merge

- **Date:** 2026-06-10
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § ASP-version-check workflow

## Context
ASP releases every few months. The pinned version lives in several files (Dockerfile, the commented-out devcontainer fallback args, the build-image workflow defaults, the installation docs), so a manual bump is easy to do inconsistently or forget. But ASP releases occasionally change behavior (for example ASTER V003 to V004 in Dec 2025, and 3.7.0 dropping `--aster-use-csm` and moving the mapproject reference DEM to `--dem`), so a blind auto-bump is risky.

## Decision
Run `asp-version-check.yml` monthly (plus manual trigger). It polls NeoGeographyToolkit/StereoPipeline releases, filters to stable `X.Y.Z` tags, parses the Linux x86_64 tarball filename for VERSION and BUILD_DATE, and if newer than the pinned values, opens a PR (via `peter-evans/create-pull-request`) that sed-bumps the four files consistently. It opens a PR, never auto-merges.

## Consequences
- **+** Version drift is surfaced automatically and bumped consistently across all four files.
- **+** A human eyeballs the diff before the new image builds, catching behavior changes.
- **−** Requires the repo setting "Allow GitHub Actions to create and approve pull requests"; without it, `create-pull-request` fails.
- **−** The bump is not applied until someone merges the PR (by design).

## Alternatives considered
- **Auto-merge version bumps** — rejected: ASP releases can change CLI behavior; an unattended merge could silently break the tutorials.
- **Manual bumps only** — rejected: easy to forget and to apply inconsistently across the four pinned locations.

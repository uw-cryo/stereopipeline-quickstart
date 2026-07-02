# 6. Pre-built image on GHCR under the bpurinton namespace

- **Date:** 2026-05-04
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § Pre-built container image hosted on GHCR

## Context
The Codespace needs ASP binaries plus the `asp_plot` conda env available at launch. Building that multi-GB image per Codespace would add minutes to every launch. Publishing a shared pre-built image is the fix, but it needs a public GHCR package, and flipping a `ghcr.io/uw-cryo/...` package to public requires uw-cryo org-admin rights that are not available. A uw-cryo-namespaced image was published once (build run 25228907289, 2026-05-01) and found to be stuck private with no path to public.

## Decision
Build and push `ghcr.io/bpurinton/stereopipeline-quickstart:latest` from CI on every change to the `Dockerfile` / `environment.yml`, plus a monthly cron rebuild. Codespaces pulls this image. The from-source `build:` block stays in `devcontainer.json` (commented out) as a fallback for forks without access to the namespace.

## Consequences
- **+** First-launch time drops from a full build to an image pull.
- **+** The package can actually be made public, unblocking the zero-setup launch.
- **−** The image lives under a personal namespace, not the org's; an orphan uw-cryo package sits harmlessly until an org admin deletes it.
- **−** The cross-namespace push needs explicit auth: a classic PAT with `write:packages` stored as the `GHCR_PAT` Actions secret, used by the workflow's GHCR login step. To revert to default `GITHUB_TOKEN` auth under the repo owner's namespace, swap those two lines and update `IMAGE_NAME`.

## Alternatives considered
- **Build per Codespace from the Dockerfile** — rejected as the default (kept as fallback): adds a multi-GB build to every launch.
- **Host under `ghcr.io/uw-cryo/...`** — blocked: making the package public needs org-admin access that is not available; the published attempt was stuck private.

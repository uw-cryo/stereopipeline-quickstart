# 10. 4-core Codespace floor

- **Date:** 2026-06-10
- **Status:** Accepted (supersedes the initial 8-core floor; further optimization tracked in [#12](https://github.com/uw-cryo/stereopipeline-quickstart/issues/12))
- **Context doc:** `AGENTS.md` § Codespace machine size; issues #3, #7

## Context
The repo initially required an 8-core Codespace. Issue #3 found that a collaborator could not launch one at all. A GitHub support response clarified that Codespace machine availability is governed by billing ownership and organization policy, not a per-user entitlement or support request: an org-billed Codespace restricted to 2/4-core machines will refuse an 8-core `hostRequirements` even though the devcontainer asks for it, and there is no override. 4 cores is the tier every account can launch without extra billing setup.

## Decision
Set `hostRequirements` to 4 cores / 16 GB / 32 GB storage. The 16 GB / 32 GB values match GitHub's 4-core tier; leaving them higher would force the machine back up to 8 cores. Retune the tutorials to run acceptably at this floor (see ADR-0011, ADR-0012). Larger machines still work by bumping the thread/process counts and `TR`.

## Consequences
- **+** Newcomers whose personal accounts lack a Codespaces payment method can launch, which is the whole point of a learning resource.
- **+** Removes an unpredictable "works for me, not for you" barrier rooted in billing/org policy.
- **−** Stereo correlation is slower than on 8 cores; the tutorials had to be retuned (coarser resolution, skip BA by default) to fit, trading some output quality for runtime.
- **−** Memory-heavy `asp_mgm` must run few-processes-many-threads on 16 GB (ADR-0011), not tile-parallel.

## Alternatives considered
- **Keep the 8-core floor** — rejected: unlaunchable for exactly the free-tier newcomers the repo targets.
- **Request higher-core machines via GitHub support** — not possible: support confirmed there is no per-user enablement path.

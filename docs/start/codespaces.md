# Run the tutorials in a Codespace

[GitHub Codespaces](https://docs.github.com/en/codespaces) gives you a Linux VM with VS Code in your browser. The Codespace boots with ASP and `asp_plot` already installed.

## Launch

1. Click the badge below (or the **Code → Codespaces → Create codespace** menu on the GitHub repo).

   ```{button-link} https://codespaces.new/uw-cryo/stereopipeline-quickstart?quickstart=1
   :color: primary
   :click-parent:
   Open in GitHub Codespaces
   ```

2. GitHub pulls a pre-built container image from [GHCR](https://ghcr.io/bpurinton/stereopipeline-quickstart) — ASP binaries and the `asp_plot` conda env are already baked in. (If the image isn't accessible from your fork, the devcontainer.json includes a commented-out `build:` block you can flip on for a from-source build.)

3. When VS Code opens in your browser, the terminal will show a friendly banner:

   ```
   stereopipeline-quickstart
   ASP + asp_plot, ready to go.
   Next steps:
     1. Open notebooks/01_aster_rainier.ipynb and click "Run All".
   ```

## Machine size

The minimum Codespace machine type for this repo is 8-core / 32 GB / 64 GB storage (set in `.devcontainer/devcontainer.json`). You can pick a larger machine at launch time via the "Create codespace with options" menu. Smaller machines aren't offered, as processing with ASP requires significant resources. Larger machines are billed at higher rates; see [Codespaces pricing](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).

## Run a tutorial

Open one of the notebooks under `notebooks/`:

| File | What it does |
|---|---|
| `01_aster_rainier.ipynb` | ASTER L1A → 30 m DEM of Mt. Rainier |
| `02_worldview_ucsd.ipynb` | WorldView-3 → 1 m DEM of UCSD campus |

Each notebook has a "Run All" button at the top. Cells are small enough to run them step by step.

## Persistence and storage

- Files in your Codespace persist between sessions as long as the Codespace exists.
- Codespaces are deleted after 30 days of inactivity by default. Commit anything important to git or download it.
- The `data/` directory is gitignored, since it can grow quite large with imagery and processed results.

## Costs

GitHub gives every personal account a monthly Codespaces allowance for free — see the [Codespaces billing page](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces) for the current numbers.

```{tip}
Students and educators with a `.edu` email get a larger allowance. Apply to the [GitHub Student Developer Pack](https://education.github.com/pack) or [GitHub for Teachers](https://education.github.com/teachers).
```

If you'd rather not use Codespaces, see [the local install guide](installation.md).

# Codespaces: machine size, costs and storage

The tutorials run in [GitHub Codespaces](https://docs.github.com/en/codespaces): a Linux machine with VS Code in your browser, which starts with ASP and [`asp-plot`](https://asp-plot.readthedocs.io/en/latest/) already installed. [The home page](../index.md) walks through the launch: sign in, click the button, click **Trust Folder & Continue**, and Tutorial 1 runs by itself. This page has the details.

```{button-link} https://codespaces.new/uw-cryo/stereopipeline-quickstart?quickstart=1
:color: primary
Open in GitHub Codespaces
```

## Machine size

The default machine is 4-core, 16 GB of memory, 32 GB of disk, which every GitHub account can launch. The run times in the tutorials are for it. The "Create codespace with options" menu on the repo's **Code → Codespaces** tab offers larger machines; stereo matching runs faster with more cores, and larger machines are billed at higher rates ([Codespaces pricing](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)).

```{tip}
On a machine with more than 4 cores, raise `--processes` in the `parallel_stereo` commands (and `--threads` in `bundle_adjust` and `mapproject`) to match.
```

## Running the tutorials

| Notebook | What it makes | Time |
|---|---|---|
| `01_aster_rainier.ipynb` | A 30 m DEM of Mount Rainier from two ASTER images, and a PDF report | about 10 min |
| `02_worldview_ucsd.ipynb` | A 2.4 m DEM of Mount Soledad from a WorldView-3 pair, compared with ICESat-2 | about 10 min |
| `03_worldview_ucsd_blend.ipynb` | Three WorldView-3 pairs of the same window, blended into one DEM | about 16 min more |

Tutorial 1 starts by itself the first time a new Codespace opens. For the others, open the notebook from the explorer and click **Run All** at the top, then scroll down to follow it. The code cells are shown as one line; click one to see its code.

While a step runs, its cell shows the command, the last few lines of its output and the time so far; ASP's full output goes to a log file in `data/<dataset>/logs/`. During stereo matching, a pop-up may say "High codespace CPU (100%) utilization detected": that's expected, since stereo uses every core. Close it.

If a step fails, the cell shows the end of its log. [Open a problem report](https://github.com/uw-cryo/stereopipeline-quickstart/issues/new?template=problem-report.yml) with it.

## Storage and persistence

- The files in your Codespace stay as long as the Codespace exists. GitHub stops it after 30 minutes without activity (your files are kept) and deletes it after 30 days without use.
- To keep results, download them: the last step of each tutorial zips them for you, and any file can be downloaded from the explorer with a right-click.
- The `data/` folder holds the images and results and can grow to a few GB. It is not under version control.

## Costs

GitHub gives every personal account a monthly Codespaces allowance for free; see the [Codespaces billing page](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces) for the current numbers. Stopping a Codespace stops the hours; deleting it frees the storage. Both are on the repo's **Code → Codespaces** tab and at [github.com/codespaces](https://github.com/codespaces).

```{tip}
Students and educators with a `.edu` email get a larger allowance through the [GitHub Student Developer Pack](https://education.github.com/pack) or [GitHub for Teachers](https://education.github.com/teachers).
```

If you'd rather not use Codespaces, see [the local install guide](../reference/installation.md).

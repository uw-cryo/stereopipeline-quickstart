# 26. A simplified VS Code window for the tutorials

- **Date:** 2026-10-26
- **Status:** Accepted; follows [0025](0025-back-to-vs-code.md)
- **Context doc:** `ARCHITECTURE.md` § A simplified window

## Context
[ADR-0025](0025-back-to-vs-code.md) kept the tutorials in VS Code's notebook editor and left the work of making VS Code friendlier for a first-time user. A colleague found the full VS Code window overwhelming: activity bar, status bar, tab strip, breadcrumbs, a file explorer full of repo infrastructure, and three notices on a new Codespace that had nothing to do with the tutorial: the git extension's "periodically run git fetch?", the PDF viewer's donation notice, and the Python Environments extension's "CONDA_PREFIX is set for this VS Code session".

## Decision
Hide what the tutorials don't use, with Codespace-only settings in `devcontainer.json`, so a new Codespace shows the file explorer (only `notebooks/` and `data/`) and Tutorial 1:

- Window: no activity bar, status bar, layout or command-center controls, breadcrumbs, minimap or "Open Editors" list; a single tab; no Welcome page or tips.
- Explorer: `files.exclude` also hides `README.md` and `scripts/`, rather than opening the Codespace on `notebooks/`, which would hide `data/`.
- Notices: `git.enabled: false` (the fetch prompt appears whenever autofetch is off); the existing close-panel extension also runs `notifications.clearAll` (the donation notice has no setting); `remoteEnv` clears `CONDA_PREFIX` and resets `CONDA_SHLVL` to `0` (the extension compares the selected env against `CONDA_PREFIX`).

## Consequences
- **+** A new Codespace shows the notebook and its files, with no notices to dismiss; the remaining clicks are the trust dialog and Run All.
- **+** Settings only: nothing new to start, and local development is unchanged.
- **−** The browser window has no menu, and no status bar for kernel or notification state; the command palette (F1) still works. Someone who wants the full window has to change the settings.
- **−** No git integration in the editor; `git` in a terminal still works.
- **−** The donation notice is cleared, not prevented: if it ever arrives after the extension's last attempt (5 s), it shows.

## Alternatives considered
- **Open the Codespace on `notebooks/`** (`workspaceFolder`, or a `.code-workspace` file) — rejected: `data/` holds the outputs the notebooks point users to, and the lifecycle commands' paths would change.
- **`git.autofetch: true`** — would also silence the fetch prompt, but leaves the git badges and the dimmed `data/` in the explorer.
- **Do Not Disturb mode for notifications** — rejected: its state is stored in the user's browser, so it would carry over to their other Codespaces, and a toggle can't be read before flipping it.
- **`userEnvProbe: "none"`** instead of `remoteEnv` — rejected: without the login shell, `/opt/conda/bin` isn't on `PATH` and `.bashrc`'s `source activate asp` fails.

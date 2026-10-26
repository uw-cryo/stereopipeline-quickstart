# 24. Tutorials open in JupyterLab on a forwarded port, from a start page

- **Date:** 2026-10-26
- **Status:** Accepted
- **Context doc:** `ARCHITECTURE.md` § Opening the tutorials

## Context
A new Codespace opens in VS Code in the browser. Even with the launch trimmed to the trust dialog and Run All (`ARCHITECTURE.md` § Notebook kernel registration), VS Code can be a lot for someone who has never used it: a file explorer, panels, a git-fetch prompt, a PDF viewer's donation notice. VS Code also cuts long cell output down to its last lines, and with the mouse over a long output, such as the stereo log, the scroll wheel scrolls that output instead of the notebook. The tutorials need a notebook and a Run All, not an editor to develop in.

JupyterLab is already in the image's `asp` environment. Codespaces has its own "Open in JupyterLab" (`https://github.com/codespaces/<name>?editor=jupyter`), but:

- a link that creates a new Codespace ignores `editor=jupyter`, and the default-editor setting belongs to each user, not to the repo;
- on an existing Codespace, that page loads JupyterLab in a frame from the forwarded port (`<name>-8888.app.github.dev`), and the frame fails on a first visit, every time, showing the browser's broken-page icon. It loads only after the forwarded port has been opened once as a page of its own, which a first-time user never does. Tested in fresh Codespaces on 2026-10-26.

The same forwarded port, opened as a page of its own, signs in through a redirect and loads.

## Decision
Keep the Codespace opening in VS Code, and hand the user to a JupyterLab server of the repo's own:

1. `postStart.sh` (`postStartCommand`, every start) starts JupyterLab from the `asp` environment on port 8890, rooted at the repo, with no token. A private forwarded port already requires the Codespace owner's GitHub sign-in. It also turns off JupyterLab's news pop-up and update check. Port 8890 because Codespaces' own JupyterLab uses 8888.
2. `devcontainer.json` forwards 8890 without a notification.
3. `postAttach.sh`, after the trust dialog, writes a gitignored `START_HERE.md` whose only content is a large "Click Here to Begin" link to `https://<CODESPACE_NAME>-8890.<forwarding domain>/lab/tree/notebooks/01_aster_rainier.ipynb`, and opens it in VS Code's Markdown preview. The link is built there, not in `onCreate.sh`, because in a prebuild `CODESPACE_NAME` is the prebuild's.
4. Clicking it opens JupyterLab in a new browser tab, on Tutorial 1, with the `asp` environment as its only kernel. Without a Codespace name, `postAttach.sh` opens Tutorial 1 in VS Code instead, as before.
5. JupyterLab shows a cell's whole output, where VS Code cut it down to its last lines, and the stereo log alone runs to thousands of lines. The cells that run `parallel_stereo`, `mapproject` and `bundle_adjust` carry `"scrolled": true` in their metadata, which JupyterLab shows as a fixed-height scroll box. The report cells don't, so their inline figures stay fully visible.

## Consequences
- **+** One click from the start page to Tutorial 1 in JupyterLab: no kernel picker, no git-fetch prompt, no donation notice, no terminal panel.
- **+** Long ASP logs sit in scroll boxes, and the rest of a cell's output shows in full. PDFs open in a JupyterLab tab with the browser's own viewer.
- **+** A clicked link is a user action, so pop-up blockers don't stop it, as they could an automatically opened tab.
- **−** VS Code and its trust dialog still come first, and the user ends up with two browser tabs. Reopening a stopped Codespace doesn't show the start page again; `START_HERE.md` stays in the file explorer.
- **−** JupyterLab's toolbar has no plain Run All: its ⏩ button restarts the kernel and runs all cells, after a "Restart Kernel?" dialog. The Run menu's "Run All Cells" stays greyed out until the user clicks into the notebook once.
- **−** Long-output cells need `"scrolled": true` kept in their metadata (`AGENTS.md` § Notebook conventions).
- **−** No token means the port must stay private: a public port would expose a JupyterLab that runs code for anyone with the URL.
- **−** VS Code's Codespace-only settings, such as hiding the repo's infrastructure files, don't apply in JupyterLab: going up from `notebooks/` shows every file. The JupyterLab terminal's PATH doesn't include the `asp` environment.
- **−** A lifecycle command's background jobs are killed when it ends, so `postStart.sh` starts the server with `setsid -f` and waits until the port listens.

## Alternatives considered
- **Codespaces' "Open in JupyterLab" (`?editor=jupyter`)** — rejected: fails on every first visit, as above, and a link that creates a Codespace can't ask for it.
- **Ask users to set JupyterLab as their default Codespaces editor** — rejected: an extra settings change for someone who has just made a GitHub account, and it changes every Codespace they open.
- **Open the JupyterLab tab automatically on attach** — rejected: browsers may block a tab that opens without a click.
- **Keep VS Code only** — still the fallback; the start page adds one click but removes VS Code's prompts and output problems from the tutorial itself.
- **Voilà / app mode** — rejected: it hides the code, and the tutorials teach the commands.
- **Binder** — rejected: no GitHub account needed, but its CPU and memory limits are likely too small for stereo.

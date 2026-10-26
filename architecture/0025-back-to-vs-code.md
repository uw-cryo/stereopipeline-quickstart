# 25. Back to VS Code: the JupyterLab start page is reverted

- **Date:** 2026-10-26
- **Status:** Accepted; supersedes [0024](0024-jupyterlab-start-page.md)
- **Context doc:** `ARCHITECTURE.md` § Notebook kernel registration

## Context
[ADR-0024](0024-jupyterlab-start-page.md) moved the tutorials from VS Code's notebook editor to JupyterLab: a Codespace still opened in VS Code, showed a one-link start page, and the link opened Tutorial 1 in a JupyterLab server of the repo's own on a forwarded port. It was merged in `e066115` and given to first-time users to try.

What testing showed:

- After a period of inactivity in the Codespace's VS Code tab, the Codespace stopped, and the JupyterLab kernel died with it.
- It added clicks on top of VS Code's: the trust dialog, then the start page link, then a second browser tab, then JupyterLab's ⏩ and a "Restart Kernel?" dialog to run the notebook.
- It needed infrastructure of its own: a server started by `postStart.sh` (with `setsid -f`, since a lifecycle command's background jobs are killed when it ends), a forwarded port with no token that must stay private, JupyterLab settings files for its pop-ups and dialogs, and `"scrolled": true` metadata on the long-output cells.
- VS Code can be made much simpler than the Codespace that 0024 compared against, by hiding most of its interface, to the point where it is not that different from the JupyterLab view.

## Decision
Revert `e066115`. The tutorials open in VS Code's notebook editor again, as before 0024: `postAttach.sh` opens Tutorial 1 after the trust dialog, and VS Code selects the `asp` kernel on its own. Further work goes into simplifying VS Code (hiding interface the tutorials don't need, opening on the notebooks) rather than into a second interface.

## Consequences
- **+** One browser tab and one set of prompts; nothing to start or forward, and no second server to keep alive or secure.
- **−** VS Code's problems that 0024 avoided are back and need their own fixes: long cell output is cut down to its last lines, the mouse wheel can get stuck inside a long output, the report PDF opens in an extension's viewer, and the git-fetch prompt and the PDF viewer's donation notice still appear.

Kept from the experiment, for anyone who tries again:

- A `codespaces/new` link ignores `?editor=jupyter`, and Codespaces' own "Open in JupyterLab" page (`github.com/codespaces/<name>?editor=jupyter`) embeds JupyterLab in a frame from the forwarded port, which failed on every first visit until the port had been opened once as a page of its own.
- A private forwarded port opened as a page of its own signs the user in through a redirect and works the first time.
- Background jobs started with `&` from a lifecycle command die when the command ends; `setsid -f` keeps them alive.
- JupyterLab has no setting to scroll long output; per-cell `"scrolled": true` metadata does it.
- JupyterLab's `skipKernelRestartDialog` (`@jupyterlab/apputils-extension:sessionDialogs`) removes the "Restart Kernel?" dialog from ⏩.

## Alternatives considered
- **Keep JupyterLab and work around the idle stop** (for example a longer idle timeout) — rejected: the timeout is a per-user setting or an organization policy, not the repo's, and it wouldn't remove the extra clicks or the infrastructure.
- **Open JupyterLab automatically, or run the notebook on open** — rejected along with the route: fewer clicks, but more infrastructure.

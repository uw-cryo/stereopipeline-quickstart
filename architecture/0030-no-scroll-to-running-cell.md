# 30. Start Tutorial 1 by itself; don't scroll to the running cell

- **Date:** 2026-10-28
- **Status:** Accepted
- **Context doc:** `.devcontainer/close-panel/extension.js`

## Context
A colleague noted that new users may not know to scroll down a notebook to see progress. Two kinds of automation were tried in the close-panel extension:

1. The first time Tutorial 1 opens in a new Codespace, the extension runs all its cells (Run All), once the `asp` kernel is attached.
2. During that run, the notebook scrolled each cell to the top of the view as it started. VS Code has no event for a cell starting, so the extension used `onDidChangeNotebookDocument`, which reports a cell's execution summary when it starts and when it ends.

Both were tested in a Codespace on 2026-10-28.

## Decision
Keep the automatic Run All of Tutorial 1. Don't scroll to the running cell. Tell the user in the tutorial to scroll down to follow the run.

Scrolling to each cell was jarring. Several cells finish in a second or two, so the view jumped past them before there was time to see what they did, and each jump pulled the view away from whatever the user was reading. Starting the run is enough automation to get a user going; from there, clear instructions to scroll do the rest.

## Consequences
- **+** The user controls the view: nothing moves the notebook while they read a figure or a cell's notes.
- **+** Less extension code, and no reliance on how VS Code reports queued and running cells.
- **−** A user who doesn't scroll sees only the top of Tutorial 1 while it runs. The tutorial's text has to say clearly that it runs by itself and that they should scroll down to follow it.

## Alternatives considered
- **Scroll to each cell as it starts** (tried, `0fe472c`): rejected for the reasons above. It also needed care at the start of Run All, when VS Code reports a change for every queued cell; the first version jumped to the last cell.
- **No automatic run**: rejected. Finding Run All is one more step for a new user, and the run takes about 10 minutes, so starting it at once saves time.

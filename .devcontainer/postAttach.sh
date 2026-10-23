#!/usr/bin/env bash
# Runs when VS Code attaches to the Codespace, after onCreate.sh and after
# the user has trusted the folder. Opens Tutorial 1 in the notebook editor, so
# a first-time user lands on the notebook they should run.
#
# This replaces customizations.codespaces.openFiles, which opened the notebook
# before the folder was trusted: in Restricted Mode it came up as raw JSON.
#
# Only on the first attach; a marker file keeps later reconnects from
# reopening the tutorial over whatever the user has open.

set -uo pipefail

NOTEBOOK="notebooks/01_aster_rainier.ipynb"
MARKER="${HOME}/.stereopipeline-quickstart-opened"

[[ -f "${MARKER}" ]] && exit 0

# The `code` CLI talks to the VS Code client over an IPC socket. Lifecycle
# commands may not inherit VSCODE_IPC_HOOK_CLI, so fall back to the newest
# socket and the remote CLI binary in the VS Code server install.
CODE_BIN="$(command -v code || ls -t /vscode/bin/*/*/bin/remote-cli/code 2>/dev/null | head -1)"
if [[ -z "${VSCODE_IPC_HOOK_CLI:-}" ]]; then
    VSCODE_IPC_HOOK_CLI="$(ls -t /tmp/vscode-ipc-*.sock 2>/dev/null | head -1)"
    export VSCODE_IPC_HOOK_CLI
fi

if [[ -n "${CODE_BIN}" && -n "${VSCODE_IPC_HOOK_CLI}" ]] && "${CODE_BIN}" "${NOTEBOOK}"; then
    touch "${MARKER}"
else
    echo "Open ${NOTEBOOK} from the file explorer on the left to start."
fi

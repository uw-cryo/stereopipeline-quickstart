#!/usr/bin/env bash
# Runs every time the Codespace starts (postStartCommand), including after it
# was stopped. Starts the JupyterLab server that the start page links to, on a
# forwarded port, so the tutorials open in a full browser tab straight on
# Tutorial 1 (postAttach.sh writes the link).
#
# Not Codespaces' own "Open in JupyterLab" (?editor=jupyter): that page loads
# JupyterLab in a frame from the forwarded port, and on a first visit the frame
# fails to load, because the port's sign-in doesn't complete inside a
# cross-site frame. A forwarded port opened as a page of its own signs in.
#
# No token: a private forwarded port already requires the Codespace owner's
# GitHub sign-in. The port is 8890 because Codespaces' own JupyterLab uses
# 8888; postAttach.sh and devcontainer.json's forwardPorts use the same number.
#
# Writes the server log to /tmp/stereopipeline-quickstart-jupyterlab.log.

set -uo pipefail

PORT=8890
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOG="/tmp/stereopipeline-quickstart-jupyterlab.log"

# Already running (e.g. the command re-ran without a restart).
if (echo > "/dev/tcp/127.0.0.1/${PORT}") 2>/dev/null; then
    exit 0
fi

# Turn off the "Would you like to get notified about official Jupyter news?"
# pop-up, unless the user has set it themselves.
NEWS_SETTINGS="${HOME}/.jupyter/lab/user-settings/@jupyterlab/apputils-extension/notification.jupyterlab-settings"
if [[ ! -f "${NEWS_SETTINGS}" ]]; then
    mkdir -p "$(dirname "${NEWS_SETTINGS}")"
    echo '{"fetchNews": "false"}' > "${NEWS_SETTINGS}"
fi

# setsid + nohup, so the server outlives this lifecycle command's terminal.
setsid nohup /opt/conda/envs/asp/bin/jupyter lab \
    --no-browser \
    --port "${PORT}" \
    --IdentityProvider.token='' \
    --ServerApp.root_dir="${REPO}" \
    > "${LOG}" 2>&1 < /dev/null &

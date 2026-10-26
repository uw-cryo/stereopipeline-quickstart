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
# GitHub sign-in. Making the port public would expose a JupyterLab that runs
# code for anyone with the URL. The port is 8890 because Codespaces' own
# JupyterLab uses 8888; postAttach.sh and devcontainer.json's forwardPorts use
# the same number.
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
# pop-up and the new-version check, unless the user has set them themselves.
NOTIFY_SETTINGS="${HOME}/.jupyter/lab/user-settings/@jupyterlab/apputils-extension/notification.jupyterlab-settings"
if [[ ! -f "${NOTIFY_SETTINGS}" ]]; then
    mkdir -p "$(dirname "${NOTIFY_SETTINGS}")"
    echo '{"fetchNews": "false", "checkForUpdates": false}' > "${NOTIFY_SETTINGS}"
fi

# setsid -f forks the server into its own session before this script exits,
# so it outlives the lifecycle command. Backgrounding it with `&` didn't: the
# creation log showed this script done in 0.08 s, and the background job was
# gone before it had even opened its log.
setsid -f /opt/conda/envs/asp/bin/jupyter lab \
    --no-browser \
    --port "${PORT}" \
    --IdentityProvider.token='' \
    --ServerApp.root_dir="${REPO}" \
    > "${LOG}" 2>&1 < /dev/null

# Stay until the server is listening, so the start page's link works as soon
# as setup is done.
for _ in $(seq 60); do
    (echo > "/dev/tcp/127.0.0.1/${PORT}") 2>/dev/null && exit 0
    sleep 1
done
echo "JupyterLab did not start on port ${PORT}; see ${LOG}"

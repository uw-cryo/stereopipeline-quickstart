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

# JupyterLab defaults for a first-time user, each written only if the user
# hasn't saved settings for that plugin themselves.
default_settings() {
    local file="${HOME}/.jupyter/lab/user-settings/@jupyterlab/$1.jupyterlab-settings"
    [[ -f "${file}" ]] && return
    mkdir -p "$(dirname "${file}")"
    echo "$2" > "${file}"
}
# No "Would you like to get notified about official Jupyter news?" pop-up,
# and no new-version check.
default_settings apputils-extension/notification \
    '{"fetchNews": "false", "checkForUpdates": false}'
# No "Restart Kernel?" dialog, so the toolbar's ⏩ (restart the kernel and
# run all cells) runs the notebook in one click. It's what the dialog's
# "Do not ask me again" box sets.
default_settings apputils-extension/sessionDialogs \
    '{"skipKernelRestartDialog": true}'

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

#!/usr/bin/env bash
# Runs when VS Code attaches to the Codespace, after onCreate.sh and after
# the user has trusted the folder. Writes START_HERE.md, a start page whose one
# link opens Tutorial 1 in JupyterLab, served by postStart.sh on a forwarded
# port, and opens it in the Markdown preview (devcontainer.json associates the
# file with the preview). The link needs the Codespace's name, so it is built
# here, not in onCreate.sh: in a prebuild, CODESPACE_NAME is the prebuild's.
# Without a name, it opens Tutorial 1 in the VS Code notebook editor instead.
#
# This replaces customizations.codespaces.openFiles, which opened files
# before the folder was trusted: in Restricted Mode a notebook came up as raw
# JSON.
#
# Then it installs .devcontainer/close-panel/, a tiny extension that closes the
# terminal panel Codespaces opened to run this script. devcontainer.json can't
# run VS Code commands; an extension can. The .vsix is zipped here from the
# source, so no packaging tool or binary lives in the repo.
#
# Only on the first attach; a marker file keeps later reconnects from
# reopening the start page over whatever the user has open.

set -uo pipefail

NOTEBOOK="notebooks/01_aster_rainier.ipynb"
START_PAGE="START_HERE.md"
JUPYTER_PORT=8890  # postStart.sh serves JupyterLab here
MARKER="${HOME}/.stereopipeline-quickstart-opened"
EXT_SRC="$(dirname "$0")/close-panel"
EXT_VSIX="/tmp/stereopipeline-quickstart-close-panel.vsix"

OPEN="${NOTEBOOK}"
if [[ -n "${CODESPACE_NAME:-}" ]]; then
    cat > "${START_PAGE}" <<EOF
# [Click Here to Begin](https://${CODESPACE_NAME}-${JUPYTER_PORT}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}/lab/tree/${NOTEBOOK})
EOF
    OPEN="${START_PAGE}"
fi

[[ -f "${MARKER}" ]] && exit 0

# The `code` CLI talks to the VS Code client over an IPC socket. Lifecycle
# commands may not inherit VSCODE_IPC_HOOK_CLI, so fall back to the newest
# socket and the remote CLI binary in the VS Code server install.
CODE_BIN="$(command -v code || ls -t /vscode/bin/*/*/bin/remote-cli/code 2>/dev/null | head -1)"
if [[ -z "${VSCODE_IPC_HOOK_CLI:-}" ]]; then
    VSCODE_IPC_HOOK_CLI="$(ls -t /tmp/vscode-ipc-*.sock 2>/dev/null | head -1)"
    export VSCODE_IPC_HOOK_CLI
fi

if [[ -n "${CODE_BIN}" && -n "${VSCODE_IPC_HOOK_CLI}" ]] && "${CODE_BIN}" "${OPEN}"; then
    touch "${MARKER}"
else
    echo "Open ${OPEN} from the file explorer on the left to start."
    exit 0
fi

# A .vsix is a zip with the extension under extension/ plus a manifest.
python3 - "${EXT_SRC}" "${EXT_VSIX}" <<'PY'
import json, sys, zipfile
from pathlib import Path

src, out = Path(sys.argv[1]), sys.argv[2]
pkg = json.loads((src / "package.json").read_text())
manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="{pkg['name']}" Version="{pkg['version']}" Publisher="{pkg['publisher']}"/>
    <DisplayName>{pkg['displayName']}</DisplayName>
    <Description xml:space="preserve">{pkg['description']}</Description>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{pkg['engines']['vscode']}"/>
    </Properties>
  </Metadata>
  <Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation>
  <Dependencies/>
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/>
  </Assets>
</PackageManifest>
"""
content_types = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension=".json" ContentType="application/json"/>
  <Default Extension=".js" ContentType="application/javascript"/>
  <Default Extension=".vsixmanifest" ContentType="text/xml"/>
</Types>
"""
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("extension.vsixmanifest", manifest)
    for f in ("package.json", "extension.js"):
        z.write(src / f, f"extension/{f}")
PY
"${CODE_BIN}" --install-extension "${EXT_VSIX}" || echo "Could not install the close-panel extension; the terminal panel stays open."

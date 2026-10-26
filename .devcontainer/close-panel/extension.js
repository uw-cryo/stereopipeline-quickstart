// Closes the panel (terminal, output) once, on a new Codespace's first launch.
//
// Codespaces runs the lifecycle commands in a terminal and opens the panel to
// show it, and devcontainer.json can't run a VS Code command to close it.
// postAttach.sh installs this extension right after it opens Tutorial 1; it
// closes the panel a few times over the next seconds, in case the lifecycle
// terminal reveals it again, and then never again (globalState flag).

const vscode = require("vscode");

const DONE = "stereopipeline-quickstart.panelClosed";
const DELAYS_MS = [500, 2000, 5000];

exports.activate = async function (context) {
    if (context.globalState.get(DONE)) {
        return;
    }
    for (const ms of DELAYS_MS) {
        await new Promise((resolve) => setTimeout(resolve, ms));
        await vscode.commands.executeCommand("workbench.action.closePanel");
    }
    await context.globalState.update(DONE, true);
};

exports.deactivate = function () {};

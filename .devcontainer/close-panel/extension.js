// Closes the panel (terminal, output) and clears notifications once, on a new
// Codespace's first launch. Also collapses the tutorials' code cells, and
// starts Tutorial 1 the first time it opens.
//
// Codespaces runs the lifecycle commands in a terminal and opens the panel to
// show it, and devcontainer.json can't run a VS Code command to close it.
// The PDF viewer (mathematic.vscode-pdf) shows a one-time donation notice when
// it starts, with no setting to turn it off. postAttach.sh installs this
// extension right after it opens Tutorial 1; it closes the panel and clears
// the notifications a few times over the next seconds, in case the lifecycle
// terminal reveals the panel again or a notice arrives late, and then never
// again (globalState flag).
//
// Each notebook under notebooks/ opens with its code cells collapsed: VS Code
// ignores the notebooks' jupyter.source_hidden metadata (microsoft/vscode#168807).
// The first time Tutorial 1 opens, it runs all cells, so a new user doesn't
// have to find Run All (globalState flag).

const vscode = require("vscode");

const DONE = "stereopipeline-quickstart.panelClosed";
const STARTED = "stereopipeline-quickstart.tutorialStarted";
const DELAYS_MS = [500, 2000, 5000];
const FIRST_TUTORIAL = "/notebooks/01_aster_rainier.ipynb";

// Notebooks already collapsed while open, so the user can expand cells again.
const collapsed = new Set();

function isTutorial(notebook) {
    return notebook.notebookType === "jupyter-notebook" && notebook.uri.path.includes("/notebooks/");
}

async function collapseCode(notebook) {
    const ranges = notebook
        .getCells()
        .filter((cell) => cell.kind === vscode.NotebookCellKind.Code)
        .map((cell) => ({ start: cell.index, end: cell.index + 1 }));
    await vscode.commands.executeCommand("notebook.cell.collapseCellInput", { ranges, document: notebook.uri });
}

async function startFirstTutorial(context, notebook) {
    if (context.globalState.get(STARTED) || !notebook.uri.path.endsWith(FIRST_TUTORIAL)) {
        return;
    }
    await context.globalState.update(STARTED, true);
    // Let the Jupyter extension finish starting, so Run All picks the asp
    // kernel by itself instead of asking for one.
    const jupyter = vscode.extensions.getExtension("ms-toolsai.jupyter");
    if (jupyter) {
        await jupyter.activate();
    }
    await vscode.commands.executeCommand("notebook.execute", notebook.uri);
}

async function onVisible(context, editors) {
    for (const editor of editors) {
        const key = editor.notebook.uri.toString();
        if (!isTutorial(editor.notebook) || collapsed.has(key)) {
            continue;
        }
        collapsed.add(key);
        await collapseCode(editor.notebook);
        await startFirstTutorial(context, editor.notebook);
    }
}

exports.activate = async function (context) {
    context.subscriptions.push(
        vscode.window.onDidChangeVisibleNotebookEditors((editors) => onVisible(context, editors)),
        vscode.workspace.onDidCloseNotebookDocument((notebook) => collapsed.delete(notebook.uri.toString())),
    );
    await onVisible(context, vscode.window.visibleNotebookEditors);

    if (context.globalState.get(DONE)) {
        return;
    }
    for (const ms of DELAYS_MS) {
        await new Promise((resolve) => setTimeout(resolve, ms));
        await vscode.commands.executeCommand("workbench.action.closePanel");
        await vscode.commands.executeCommand("notifications.clearAll");
    }
    await context.globalState.update(DONE, true);
};

exports.deactivate = function () {};

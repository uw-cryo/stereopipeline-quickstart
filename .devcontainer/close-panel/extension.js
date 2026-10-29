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
//
// When a tutorial's last cell writes its results zip (*_results.zip in the
// top folder, utils.zip_results), a notification says it's ready and offers
// to show it in the file explorer, where right-click → Download saves it. The
// folder is listed every few seconds: a file watcher didn't see zips written
// in data/, which devcontainer.json excludes from watching.

const vscode = require("vscode");

const DONE = "stereopipeline-quickstart.panelClosed";
const STARTED = "stereopipeline-quickstart.tutorialStarted";
const DELAYS_MS = [500, 2000, 5000];
const FIRST_TUTORIAL = "/notebooks/01_aster_rainier.ipynb";
const KERNEL_WAIT_MS = 5000;
const COLLAPSE_DELAYS_MS = [0, 500, 1500];

// Notebooks already collapsed while open, so the user can expand cells again.
const collapsed = new Set();

function isTutorial(notebook) {
    return notebook.notebookType === "jupyter-notebook" && notebook.uri.path.includes("/notebooks/");
}

// A notebook opened after this extension started is reported visible before
// its editor is ready, and the collapse command then does nothing, so it is
// repeated over the first seconds. Collapsing a collapsed cell does nothing.
async function collapseCode(notebook) {
    const ranges = notebook
        .getCells()
        .filter((cell) => cell.kind === vscode.NotebookCellKind.Code)
        .map((cell) => ({ start: cell.index, end: cell.index + 1 }));
    for (const ms of COLLAPSE_DELAYS_MS) {
        await new Promise((resolve) => setTimeout(resolve, ms));
        await vscode.commands.executeCommand("notebook.cell.collapseCellInput", { ranges, document: notebook.uri });
    }
}

async function startFirstTutorial(context, notebook) {
    if (context.globalState.get(STARTED) || !notebook.uri.path.endsWith(FIRST_TUTORIAL)) {
        return;
    }
    await context.globalState.update(STARTED, true);
    // Run All only once the asp kernel is attached, or VS Code opens a "Select
    // Kernel" picker. The Jupyter extension attaches it after the Python
    // extension has found the conda environments, and a few seconds later.
    const python = vscode.extensions.getExtension("ms-python.python");
    if (python) {
        const api = await python.activate();
        await api?.ready;
        await api?.environments?.refreshEnvironments();
    }
    const jupyter = vscode.extensions.getExtension("ms-toolsai.jupyter");
    if (jupyter) {
        await jupyter.activate();
    }
    await new Promise((resolve) => setTimeout(resolve, KERNEL_WAIT_MS));
    vscode.commands.executeCommand("notebook.execute", notebook.uri);
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

async function closePanel(context) {
    if (context.globalState.get(DONE)) {
        return;
    }
    for (const ms of DELAYS_MS) {
        await new Promise((resolve) => setTimeout(resolve, ms));
        await vscode.commands.executeCommand("workbench.action.closePanel");
        await vscode.commands.executeCommand("notifications.clearAll");
    }
    await context.globalState.update(DONE, true);
}

const RESULTS_POLL_MS = 3000;

// The modification time of each results zip already announced, or there when
// the extension started, so a zip is announced once each time it is written.
const seen = new Map();

async function findResults(folder) {
    let entries = [];
    try {
        entries = await vscode.workspace.fs.readDirectory(folder);
    } catch {
        return [];
    }
    const found = [];
    for (const [name, type] of entries) {
        if (type === vscode.FileType.File && name.endsWith("_results.zip")) {
            const uri = vscode.Uri.joinPath(folder, name);
            found.push([uri, (await vscode.workspace.fs.stat(uri)).mtime]);
        }
    }
    return found;
}

async function pollResults(folder) {
    for (const [uri, mtime] of await findResults(folder)) {
        if (seen.get(uri.toString()) !== mtime) {
            seen.set(uri.toString(), mtime);
            announceResults(uri);
        }
    }
}

async function announceResults(uri) {
    const name = vscode.workspace.asRelativePath(uri);
    const choice = await vscode.window.showInformationMessage(
        `Your results are ready: ${name}. To save them, right-click the file in the explorer and choose Download.`,
        "Show in Explorer",
    );
    if (choice) {
        // In case the explorer hasn't picked up the new file yet: it can't
        // reveal a file it doesn't know about.
        await vscode.commands.executeCommand("workbench.files.action.refreshFilesExplorer");
        await vscode.commands.executeCommand("revealInExplorer", uri);
    }
}

exports.activate = function (context) {
    const workspace = vscode.workspace.workspaceFolders?.[0];
    if (workspace) {
        findResults(workspace.uri).then((found) => {
            found.forEach(([uri, mtime]) => seen.set(uri.toString(), mtime));
            const timer = setInterval(() => pollResults(workspace.uri), RESULTS_POLL_MS);
            context.subscriptions.push({ dispose: () => clearInterval(timer) });
        });
    }
    context.subscriptions.push(
        vscode.window.onDidChangeVisibleNotebookEditors((editors) => onVisible(context, editors)),
        vscode.workspace.onDidCloseNotebookDocument((notebook) => collapsed.delete(notebook.uri.toString())),
    );
    // Neither waits for the other: starting Tutorial 1 waits for the kernel.
    onVisible(context, vscode.window.visibleNotebookEditors);
    closePanel(context);
};

exports.deactivate = function () {};

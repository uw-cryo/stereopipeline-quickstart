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
// Run All is tried again until a cell is seen running: once, it did nothing
// in a new Codespace (the panel closed and the cells collapsed, so the
// extension ran; no kernel picker appeared) and the user had to click it.
const RUN_TRIES = 4;
const RUN_CHECK_MS = 15000;

// "Quickstart launch" in the Output panel: what the extension did and when,
// for when a launch doesn't go as it should.
let log;

// Resolves once closePanel() has made its last notifications.clearAll call,
// so a progress notification shown after it is not cleared by it.
let panelClosed = Promise.resolve();

// A progress notification while Tutorial 1 is being started: between the
// Codespace looking ready and the first cell running, the Python extension
// scans the environments and the kernel starts on a cold disk, which can take
// a minute or two with nothing on screen to say so.
let progress;
let progressDone;

function showProgress() {
    const done = new Promise((resolve) => {
        progressDone = resolve;
    });
    panelClosed.then(() =>
        vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Starting Tutorial 1. It runs by itself in a moment; no click needed.",
            },
            (p) => {
                progress = p;
                return done;
            },
        ),
    );
}

function report(message) {
    note(message);
    progress?.report({ message });
}

function endProgress() {
    progressDone?.();
    progress = undefined;
}

function note(message) {
    log?.appendLine(`${new Date().toISOString()} ${message}`);
}
const COLLAPSE_DELAYS_MS = [0, 500, 1500, 4000, 8000, 15000];

// Notebooks already collapsed while open, so the user can expand cells again.
const collapsed = new Set();

function isTutorial(notebook) {
    return notebook.notebookType === "jupyter-notebook" && notebook.uri.path.includes("/notebooks/");
}

// A notebook opened after this extension started is reported visible before
// its editor is ready, and the collapse command then does nothing, so it is
// repeated over the first 15 seconds: when no README preview opens before
// Tutorial 1, its editor took more than 2 s to be ready. Collapsing a
// collapsed cell does nothing.
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

function hasStarted(notebook) {
    return notebook.getCells().some(
        (cell) => cell.kind === vscode.NotebookCellKind.Code && cell.executionSummary?.timing?.startTime,
    );
}

async function startFirstTutorial(context, notebook) {
    if (context.globalState.get(STARTED) || !notebook.uri.path.endsWith(FIRST_TUTORIAL)) {
        return;
    }
    showProgress();
    report("waiting for the Python and Jupyter extensions");
    // Run All only once the asp kernel is attached, or VS Code opens a "Select
    // Kernel" picker. The Jupyter extension attaches it after the Python
    // extension has found the conda environments, and a few seconds later.
    try {
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
        report("the Python and Jupyter extensions are ready; starting the kernel");
    } catch (error) {
        note(`waiting for the extensions failed: ${error}`);
    }
    await new Promise((resolve) => setTimeout(resolve, KERNEL_WAIT_MS));
    for (let attempt = 1; attempt <= RUN_TRIES; attempt++) {
        report(`Run All, attempt ${attempt} of ${RUN_TRIES}`);
        try {
            await vscode.commands.executeCommand("notebook.execute", notebook.uri);
        } catch (error) {
            note(`notebook.execute failed: ${error}`);
        }
        const deadline = Date.now() + RUN_CHECK_MS;
        while (Date.now() < deadline) {
            await new Promise((resolve) => setTimeout(resolve, 1000));
            if (hasStarted(notebook)) {
                note("a cell is running");
                endProgress();
                await context.globalState.update(STARTED, true);
                return;
            }
        }
        note("no cell started");
    }
    note("gave up; Run All at the top of the notebook starts it");
    endProgress();
    vscode.window.showInformationMessage("Tutorial 1 did not start by itself. Click Run All at the top of the notebook.");
    await context.globalState.update(STARTED, true);
}

async function onVisible(context, editors) {
    for (const editor of editors) {
        const key = editor.notebook.uri.toString();
        if (!isTutorial(editor.notebook) || collapsed.has(key)) {
            continue;
        }
        collapsed.add(key);
        note(`collapsing the code cells of ${editor.notebook.uri.path}`);
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
    log = vscode.window.createOutputChannel("Quickstart launch");
    context.subscriptions.push(log);
    note("extension activated");
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
    panelClosed = closePanel(context);
    onVisible(context, vscode.window.visibleNotebookEditors);
};

exports.deactivate = function () {};

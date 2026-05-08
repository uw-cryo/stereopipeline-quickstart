# GUI exploration

Prototypes for replacing ASP CLI invocations with browser-based controls.

## Why

ASP is a toolchain of dozens of CLI binaries with tens of options each. The current tutorials in `notebooks/` expose every flag verbatim, which is useful for learning but a barrier for end users. The longer-term direction (including the SNWG-funded effort) is to put a GUI in front of ASP so users adjust sliders, dropdowns, and checkboxes — never the CLI.

These notebooks are prototypes, not products. They each wrap a tiny slice of `parallel_stereo` (algorithm, subpixel mode, thread budget, paths) in a different UI library, render the resulting CLI command live, and offer a "Run" button. Goal: pick a direction.

## Prototypes in this folder

| File | Library | Runs as |
|---|---|---|
| `gui_ipywidgets.ipynb` | [ipywidgets](https://ipywidgets.readthedocs.io/) | Inline in the notebook |
| `gui_solara.ipynb` | [solara](https://solara.dev/) | Inline in the notebook AND as a standalone server (`solara run gui_solara.py`) |

## Library tradeoff

**ipywidgets**

- Pros: ships with Jupyter; users already have it; least magic; output cell is just a regular Python widget.
- Cons: imperative event-handling (write `observe` callbacks for every widget); state-sharing across widgets gets verbose; styling limited to widget defaults; no path to a hosted browser app outside Jupyter.

**solara**

- Pros: reactive, React-like component model; same code runs inline in the notebook AND `solara run script.py` serves it as a standalone web app on a port (suitable for a "no-Jupyter" GUI in a Codespace); modern styling.
- Cons: extra dependency; mental model less familiar; pinned to a fast-moving project.

**Other paths considered, not prototyped here**

- [Voila](https://voila.readthedocs.io/) — turns an ipywidgets notebook into a standalone web page. Pair with ipywidgets above. Useful if the goal is "publish the existing notebook as a kiosk".
- [panel](https://panel.holoviz.org/) — bigger ecosystem, more capable; arguably overkill for parameter forms.
- [Streamlit](https://streamlit.io/) — popular but Streamlit-style scripts re-run top-to-bottom on every interaction, awkward for "build a CLI command then run it".
- Custom React / Vue front-end → FastAPI back-end. Most flexible, most work.

## Open design questions

- **Where does the GUI live?** Inside the existing tutorial notebooks (replacing the CLI cells), in a separate "GUI mode" notebook, or as a standalone solara/voila app served from the Codespace?
- **What abstraction level?** Per-tool form (one form per `parallel_stereo` / `bundle_adjust` / `mapproject`), or a single end-to-end form that runs the whole pipeline?
- **How to handle file selection?** Text input is fine for prototypes; a real GUI needs a file picker (ipywidgets has [ipyfilechooser](https://github.com/crahan/ipyfilechooser); solara has a built-in `FileBrowser`).
- **How to surface long-running output?** Stream stdout into the page? Log file + tail? Status indicator + final diagnostics?
- **Per-sensor recipes.** A "create DEM" GUI almost certainly needs different fields per sensor (ASTER vs WV3 vs ISIS planetary). Templated forms vs separate apps.

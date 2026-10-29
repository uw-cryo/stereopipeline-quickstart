# 34. The notebooks' prose is for beginners; the docs site carries the detail

- **Date:** 2026-10-29
- **Status:** Accepted
- **Context doc:** `ARCHITECTURE.md` § ASTER tutorial

## Context
The notebooks had grown prose for an informed reader: how the download scripts work, what each ASP flag does, which helper in `notebooks/utils.py` draws which plot, Codespace timings with their reasons. A first-time user, who the tutorials are for, has to read past all of it to find out what a step does and what the figure shows. The docs site already explains the concepts, and the code cells, collapsed by default, show the commands with their flags to anyone who opens them.

## Decision
- **Each step's text says what happens and why, in two or three sentences,** in plain words, with the ASP tool named once. Nothing about the Codespace setup, the download scripts, the helper functions, or processing parameters: the code cell has the parameters, and the docs explain the method.
- **One link per step to the docs site,** to the page that explains the method (`concepts/…`), as a plain markdown link. VS Code in the browser opens web links in a new tab, and the docs site opens external links in a new tab, so no `target="_blank"` is needed.
- **A caption under every figure,** as a markdown cell after the figure's code cell, written for someone who has not seen such a figure before. `show_report_figures()` prints its captions below the figures for the same reason.
- **The report link is a heading** (`## 📄 Open the report (PDF)`), so it can't be missed, with the download instruction under it.
- **A timing line per step,** as a short quote (`> About a minute.`), for a 4-core Codespace.
- **Larger text in the Codespace:** `notebook.markup.fontSize` 17 and `notebook.output.fontSize` 15 in `devcontainer.json`, since the notebooks are read more than edited there. Settings rather than CSS in cells: VS Code's notebook renderer doesn't take styles from markdown cells, and a setting applies to every notebook.

## Consequences
- **+** A beginner can follow a tutorial by reading the headings, the step text and the captions.
- **+** The explanations live in one place, the docs site, and the notebooks link to them instead of repeating them.
- **−** Someone who wants to know what a flag does has to expand the code cell or follow a link.
- **−** The timing lines and captions describe today's data and settings; changing a tutorial means rereading them.

## Alternatives considered
- **Keep the detail in collapsible admonitions in the notebook:** VS Code's markdown cells don't render MyST admonitions, and `<details>` blocks still add length to scroll past.
- **CSS in the notebooks:** VS Code's markdown cells don't apply `<style>` or inline styles; the docs site has its own CSS already.

# Delphi — Academic Engine

A command-line engine that runs the whole lifecycle of a long academic document: it initialises the structure, gathers sources, drives the writing, lints the Markdown and compiles the result. The project is data on disk; the writing is delegated to NotebookLM, grounded on the sources that were loaded.

## Table of contents

- [The commands](#the-commands)
- [How it works](#how-it-works)
- [Decisions](#decisions)
- [Repository map](#repository-map)
- [Running it](#running-it)
- [Limitations](#limitations)

## The commands

| Command | What it does |
|---|---|
| `init` | creates a project skeleton: the chunk manifest, the metadata and the folder tree for a thesis or a paper |
| `setup` | creates a NotebookLM notebook, uploads the sources and runs the web research for that project |
| `fetch` | searches and downloads a book by title, author or ISBN |
| `sources` | lists the active sources of a project |
| `curate` | deactivates, reactivates or removes sources |
| `generate` | generates the project's content in chunks, in parallel, from roles, subjects and custom prompts |
| `lint` | checks the Markdown's integrity and fixes what can be fixed mechanically |
| `export` | compiles the project to PDF (typst or web), DOCX or EPUB, keeping the citations |
| `status` | shows the state of the notebooks attached to the projects |
| `clear_all` | garbage-collects resources that are no longer needed |
| `create-launcher` | generates the launcher for a batch generation |

## How it works

### The project is data

A project is a directory under `Projects/` with `delphi.json` (metadata: title, author, university, version) and `chunks.json` (the ordered plan of the document, one entry per section, with its role and subject). Everything else is generated from that plan. `Projects/` also contains real projects, which double as examples of what the manifest looks like for a real book: six chapters, twenty-two sections.

Treating a book as a manifest instead of a folder of files is what makes the rest possible: generation can resume at chunk 17, curate can talk about "the sources of chapter 3", and export can rebuild any format from the same plan.

### Generation runs on NotebookLM

`generate` does not call an LLM API. It drives **NotebookLM** through the `notebooklm` Python client, authenticated with a stored browser session (`NotebookLMClient.from_storage`). The reason is grounding: NotebookLM answers from the documents that were uploaded to that notebook, so the chapter is written against the sources rather than against the model's memory of the literature. The cost is that the pipeline depends on a web product and on its session, not on a stable API.

### Lint before export

`lint` is a Markdown linter written for one purpose: the document must survive pandoc and typst. It checks setext headers, malformed mermaid fences, glued lists, list indentation, ghost labels, runs of blank lines, orphan symbols, documents without an H2, empty math blocks. With `--fix` it repairs what is mechanical, and it never touches prose — structure is fixed by rule, content is never rewritten by a regex.

### Export

`export` compiles the plan into pandoc and then into **typst** for PDF, with Node scripts for merging PDFs and building the cover images; DOCX and EPUB go through pandoc with a stylesheet. Citations are carried by a BibTeX file parsed in the project, so the bibliography is regenerated rather than pasted.

## Decisions

**A manifest of chunks instead of a pile of files.** The document is generated in pieces by a remote service that can fail, time out or stop existing; a plan on disk makes every step resumable and every output replaceable.

**NotebookLM instead of an LLM API.** Grounding on uploaded sources is the whole point: a chapter that cites the bibliography has to be written with the bibliography in front of it. The trade-off is accepted explicitly — a web session instead of an API contract.

**Typst instead of LaTeX.** A full TeX installation is a heavy prerequisite for someone who only wants a PDF; typst is a single binary, compiles in seconds and is enough for a book with a cover.

**Structure fixed by rule, content never.** The linter with `--fix` exists because Markdown breaks the same way at scale — indentation, fences, blank lines. Rewriting prose with a regex is how a document starts lying about itself.

**External tools resolved from the PATH first.** `pandoc` and `typst` are looked up on the system before any bundled copy, so the same code works as a CLI and as a skill invoked by an agent.

## Repository map

```
delphi_cli.py        the Typer CLI: eleven commands
core/academic/lib/   project model, BibTeX parser, citation service, linter, compiler
core/export_module/  Node scripts for PDF merge and cover images, print and EPUB stylesheets
core/*.py            NotebookLM engine and integrations
Projects/            real projects, each with delphi.json and chunks.json
agent.md             instructions for an AI agent driving Delphi
```

## Running it

```bash
pip install -r requirements.txt
python delphi_cli.py --help
```

Beyond the Python dependencies, the export step needs **pandoc**, **typst** and **Node.js** on the PATH; `paths.py` falls back to a bundled copy when they are absent. NotebookLM commands need an authenticated session, created once and reused.

Typical sequence for a new document:

```bash
python delphi_cli.py init
python delphi_cli.py setup --project "My Project"
python delphi_cli.py generate --project "My Project"
python delphi_cli.py lint --project "My Project" --fix
python delphi_cli.py export --project "My Project" --format pdf
```

## Limitations

| Item | Impact | Status |
|---|---|---|
| The NotebookLM client is unofficial | it drives a web product through a stored session: a UI change or a session expiry stops generation until it is renewed | accepted, by design |
| `fetch` uses Z-Library | the sources come from a shadow library, so the legal position depends on the jurisdiction and on the material | accepted, worth stating |
| pandoc, typst and Node are not in `requirements.txt` | a clean install fails at the export step, not at import time | open, the first thing to fix |
| No automated tests | the linter has rules but no test fixtures: regressions are found on the document | open |
| `Projects/` contains real documents | the repository doubles as storage, so the content ships with the code | accepted |
| The quality of a generated chapter is not measured | there is no check of coverage or coherence per chunk, only the citation linter | open, the biggest gap |

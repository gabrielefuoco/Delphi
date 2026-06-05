# Agent Experience Report: thesisflow-manager
**Date**: 2026-02-21
**Session Context**: Structuring, drafting, and renaming the entire Chapter 2 of the thesis ("Fisiopatologia dello stress sociale").

## 🚨 Critical Friction (Bugs & Failures)
- **Issue**: Execution path failures for CLI commands. Running `python scripts/manage.py compile` from the project root fails because the actual path is nested inside the skill folder.
- **Cause**: Agents often run commands from the project root (`TESI VALE/`). Without explicitly changing directories first (e.g., `cd .agent/skill/thesisflow-manager`), the relative paths fail.
- **Proposed Fix**: Create a lightweight wrapper script at the project root (e.g., `manage.ps1` or `tf.bat`) that internally forwards commands to the hidden skill directory. Alternatively, update `SKILL.md` to explicitly state: "ALWAYS run commands from the `.agent/skill/thesisflow-manager` directory."

## ⚠️ User Experience (Usability)
- **Issue**: The `rename` command for paragraphs is intensely verbose. It requires the exact, full string match for both the `--chapter` name and the `old_name`. Example:
  `python scripts/manage.py rename --para --chapter "02_Fisiopatologia dello stress sociale - L'asse HPA e la vulnerabilità neurochimica" "01_La risposta neuroendocrina allo stress lasse HPA e il cortisolo" "01_La risposta neuroendocrina - asse HPA e cortisolo"`
- **Cause**: The CLI relies on exact string matching against the filesystem or `thesisflow.json`, making it highly susceptible to escaping errors or typos in long academic titles.
- **Proposed Fix**: Allow targeting paragraphs and chapters via their IDs or indices (e.g., `python manage.py rename --id 2.1 "Nuovo Titolo"`).

## 💡 Feature Proposals
- **Atomic Paragraph Creation and Population**: Currently, `add_paragraph` only creates the structural markdown file. To add content, agents must perform a separate and sometimes tricky file-write operation. Adding a `--content "testo"` or `--from-file source.md` argument to `add_paragraph` would allow creating and filling a section in one seamless transaction.

## 📝 Documentation Gaps
- The `SKILL.md` clearly states the script location, but under "Base Command" it shows `python scripts/manage.py [COMMAND]`. This implies `scripts/` is available in the current directory, which misleads agents into running it from the project root rather than from inside the skill folder.

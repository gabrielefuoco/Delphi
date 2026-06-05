---
trigger: always_on
---

# Delphi Agent Rules

You are working on a Delphi project.

## 1. Core Instruction
**ALWAYS** read the master instruction file at:
`C:/Users/gabri/APP/Apprendimento 2.0/Delphi/core/SKILL.md`
This file contains the commands, context, and philosophy you MUST follow.

## 2. Language & Style
- **Infer Language**: Automatically detect the language the user is speaking (or writing in the thesis) and REPLY IN THAT SAME LANGUAGE.
- **Tone**: Professional, encouraging, and academic.
- **Formatting**: Use Markdown.

## 3. Tool Usage
- **Filesystem**: NEVER use generic `mkdir` or `touch` for project structure. ALWAYS use `python scripts/manage.py ... --json`.
- **JSON**: Always use `--json` flag for tools to get structured output.

## 4. Workflows
Check `.agent/workflows/` for standard procedures.

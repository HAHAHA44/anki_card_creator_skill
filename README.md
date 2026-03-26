# Anki Card Creator Skill

Hybrid Anki card generation project with two parts:

- a Codex skill that drafts an editable Markdown deck spec
- a Python MCP implementation that validates that spec and generates `.apkg` files with `genanki`

The workflow is review-first: draft `deck-spec.md`, let the user edit it, then generate the final deck only after approval.

## What This Repository Contains

- `skill/anki-card-creator/`
  the installable skill source
- `mcp/`
  the parsing, validation, and packaging implementation
- `scripts/install_skill.py`
  copies the local skill into a Codex skills directory
- `docs/`
  design, planning, structure, and contribution docs

## Supported Workflow

1. Start from one of two inputs:
   `domain` or `extract`
2. Confirm:
   `card_type`, `deck_name`, `style_profile`
3. Draft a fixed-format Markdown deck spec
4. Let the user revise the Markdown directly
5. Validate and package it through the MCP layer

## Quick Start

Run tests:

```powershell
python -m pytest .\mcp\tests -q
```

Install the skill locally:

```powershell
python .\scripts\install_skill.py --source .\skill\anki-card-creator --dest "$env:USERPROFILE\.codex\skills" --name anki-card-creator
```

Validate the skill structure:

```powershell
python "C:\Users\27391\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skill\anki-card-creator"
```

## Key Files

- `skill/anki-card-creator/SKILL.md`
- `skill/anki-card-creator/assets/deck-spec-template.md`
- `skill/anki-card-creator/references/markdown-spec.md`
- `skill/anki-card-creator/references/precise-card-rules.md`
- `mcp/src/anki_card_creator_mcp/service.py`
- `mcp/src/anki_card_creator_mcp/server.py`

## Additional Docs

- `docs/project-structure.md`
- `docs/contributing.md`
- `docs/superpowers/specs/2026-03-26-anki-card-creator-design.md`
- `docs/superpowers/plans/2026-03-26-anki-card-creator-implementation.md`

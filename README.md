# Anki Card Creator Skill

A Codex or Claude Code skill that drafts an editable Markdown deck spec and packages it into an `.apkg` file via MCP.

The workflow is review-first: draft `deck-spec.md`, let the user edit it, then generate the final deck only after the user signals readiness.

## What This Repository Contains

- `skill/anki-card-creator/`
  the installable skill source
- `mcp/`
  the parsing, validation, and packaging implementation exposed as an MCP server
- `install.sh`
  installs the skill and MCP wiring for Codex, Claude Code, or both
- `scripts/install_skill.py`
  copies the local skill into a Codex skills directory
- `docs/`
  design, planning, structure, and contribution docs

## Supported Workflow

1. Start from one of two inputs: `domain` or `extract`
2. Draft a fixed-format Markdown deck spec with the default layout shown inline
3. Let the user revise the Markdown directly
4. Validate and package via MCP once the user signals readiness

## Quick Start

Run tests:

```bash
python -m pytest mcp/tests -q
```

Run the local CLI directly:

```bash
PYTHONPATH=mcp/src python -m anki_card_creator_mcp.cli mcp/tests/fixtures/qa_deck_spec.md --output-dir mcp/tests/output
```

Install the skill locally:

```bash
python scripts/install_skill.py --source skill/anki-card-creator --dest ~/.codex/skills --name anki-card-creator
```

Install the skill and MCP runtime for both Codex and Claude Code:

```bash
bash ./install.sh --target both --scope user
```

Install project-local guidance and Claude project MCP wiring for the current repo:

```bash
bash ./install.sh --target both --scope project --project-dir .
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
- `docs/install-prompts.md`
- `docs/superpowers/specs/2026-03-26-anki-card-creator-design.md`
- `docs/superpowers/specs/2026-03-29-cross-agent-installer-design.md`
- `docs/superpowers/plans/2026-03-26-anki-card-creator-implementation.md`
- `docs/superpowers/plans/2026-03-29-cross-agent-installer-implementation.md`

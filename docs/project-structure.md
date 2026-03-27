# Project Structure

## Top Level

```text
Anki_Card_Creator_Skill/
  docs/
  mcp/
  scripts/
  skill/
  README.md
```

## Directory Responsibilities

### `skill/`

Contains the installable Codex skill source.

- `skill/anki-card-creator/SKILL.md`
  main skill instructions
- `skill/anki-card-creator/agents/openai.yaml`
  UI-facing metadata
- `skill/anki-card-creator/assets/deck-spec-template.md`
  editable Markdown template shown to users
- `skill/anki-card-creator/references/markdown-spec.md`
  fixed deck spec contract
- `skill/anki-card-creator/references/precise-card-rules.md`
  drafting constraints derived from the approved article
- `skill/anki-card-creator/tests/acceptance-checklist.md`
  manual RED/GREEN validation record for the skill workflow

### `mcp/`

Contains the Python implementation of parsing, validation, and packaging exposed as an MCP server.

- `mcp/pyproject.toml`
  package metadata and dependencies
- `mcp/src/anki_card_creator_mcp/models.py`
  core dataclasses
- `mcp/src/anki_card_creator_mcp/markdown_parser.py`
  parses the Markdown deck spec
- `mcp/src/anki_card_creator_mcp/validators.py`
  validates deck metadata and rows
- `mcp/src/anki_card_creator_mcp/card_styles.py`
  CSS variants for card presentation
- `mcp/src/anki_card_creator_mcp/card_models.py`
  `genanki` note-model definitions
- `mcp/src/anki_card_creator_mcp/apkg_builder.py`
  builds `.apkg` files
- `mcp/src/anki_card_creator_mcp/service.py`
  high-level entry point used by callers and tests
- `mcp/src/anki_card_creator_mcp/server.py`
  thin MCP server wrapper
- `mcp/src/anki_card_creator_mcp/cli.py`
  thin CLI wrapper over the same service layer
- `mcp/tests/`
  unit and end-to-end tests plus Markdown fixtures

### `scripts/`

Contains repo-local helper scripts.

- `scripts/install_skill.py`
  copies the local skill tree into a target Codex skills directory

### `docs/`

Contains design and maintenance documentation.

- `docs/project-structure.md`
  this file
- `docs/contributing.md`
  contribution workflow
- `docs/superpowers/specs/`
  approved design specs
- `docs/superpowers/plans/`
  implementation plans

## Design Boundary

The repository is intentionally split:

- the skill owns user interaction and Markdown generation
- the MCP layer owns deterministic validation and packaging

Do not move deck-generation conversation logic into the MCP layer.

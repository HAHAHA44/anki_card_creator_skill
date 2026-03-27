# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A hybrid Anki card generation system split into two coordinated layers:

1. **Codex Skill** (`skill/anki-card-creator/`) — guides users to draft an editable Markdown deck spec
2. **Python MCP + CLI Fallback** (`mcp/`) — validates the spec and generates `.apkg` files using `genanki`

The workflow is always review-first: draft `deck-spec.md` → user edits → user approves → package.

## Commands

All commands below use forward slashes (Linux/WSL). The project runs in WSL but was originally developed on Windows.

**Run tests:**
```bash
python -m pytest mcp/tests -q
```

**Run a single test file:**
```bash
python -m pytest mcp/tests/test_validators.py -q
```

**Run the CLI directly (set PYTHONPATH first):**
```bash
PYTHONPATH=mcp/src python -m anki_card_creator_mcp.cli mcp/tests/fixtures/qa_deck_spec.md --output-dir mcp/tests/output
```

**Install skill locally:**
```bash
python scripts/install_skill.py --source skill/anki-card-creator --dest ~/.codex/skills --name anki-card-creator
```

## Architecture

### Design Boundary

The Markdown deck spec is the **single source of truth** between the skill and the packager. The skill drafts it; the user edits it directly; the packager reads it. Nothing else is shared state.

```
Skill (user interaction)
  → drafts Markdown deck spec
  → user edits Markdown
  → user signals readiness

MCP (packaging)
  → parses Markdown → DeckSpec dataclass  (markdown_parser.py)
  → validates fields and card rows         (validators.py)
  → builds genanki Note models             (card_models.py)
  → writes .apkg                           (apkg_builder.py)
  → returns {ok, errors, output_path}      (service.py)
```

### MCP Source (`mcp/src/anki_card_creator_mcp/`)

| File | Role |
|------|------|
| `models.py` | `CardRow` and `DeckSpec` dataclasses |
| `markdown_parser.py` | Parses Markdown → `DeckSpec` |
| `validators.py` | Returns list of error strings |
| `card_styles.py` | CSS variants |
| `card_models.py` | `genanki` note-model definitions with layout support |
| `apkg_builder.py` | Builds `.apkg`; stable deck IDs via name hash |
| `service.py` | Entry point: `build_apkg_from_markdown(spec_path, output_dir)` |
| `server.py` | Thin MCP wrapper (keep thin) |
| `cli.py` | Thin argparse wrapper (keep thin) |

### Card Field Architecture

All cards have exactly 5 fields: `Front`, `Back`, `Context`, `Example`, `Extra`. Fields are always stored even if empty. Layout (which fields appear where) is configured per-deck in the Markdown spec.

## Key Rules (from `docs/contributing.md`)

- **Never bypass the Markdown review stage** in the skill workflow
- **Never add hidden state** outside the Markdown deck spec
- **Keep `server.py` and `cli.py` thin** — logic belongs in `service.py`
- **Keep the Markdown contract synchronized**: any change to the spec format must update `markdown_parser.py`, `validators.py`, `assets/deck-spec-template.md`, `references/markdown-spec.md`, and `skill/anki-card-creator/SKILL.md` together

## Key Reference Files

- `skill/anki-card-creator/references/markdown-spec.md` — fixed Markdown contract
- `skill/anki-card-creator/references/precise-card-rules.md` — card drafting constraints
- `skill/anki-card-creator/assets/deck-spec-template.md` — editable template shown to users
- `mcp/tests/fixtures/` — test deck specs (minimal and QA variants)

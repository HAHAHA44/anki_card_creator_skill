# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An Anki card generation system split into two coordinated layers:

1. **Skill** (`skill/anki-card-creator/`) — guides users to draft an editable Markdown deck spec; contains the Python packager scripts under `scripts/`
2. **Installer** (`install.sh`) — provisions a Python venv with `genanki` and creates a `~/.anki-card-creator/bin/build-apkg` wrapper

The workflow is always review-first: draft `deck-spec.md` → user edits → user approves → package.

## Commands

All commands below use forward slashes (Linux/WSL). The project runs in WSL but was originally developed on Windows.

**Run tests:**
```bash
python -m pytest tests -q
```

**Run the packager directly:**
```bash
~/.anki-card-creator/bin/build-apkg tests/fixtures/qa_deck_spec.md --output-dir tests/output
```

**Run the script without the wrapper (set PYTHONPATH for venv first):**
```bash
~/.anki-card-creator/runtime/venv/bin/python skill/anki-card-creator/scripts/build_apkg.py tests/fixtures/qa_deck_spec.md
```

**Install:**
```bash
bash install.sh
```

## Architecture

### Design Boundary

The Markdown deck spec is the **single source of truth** between the skill and the packager. The skill drafts it; the user edits it directly; the packager reads it. Nothing else is shared state.

```
Skill (user interaction)
  → drafts Markdown deck spec
  → user edits Markdown
  → user signals readiness

Scripts (packaging)
  → parses Markdown → DeckSpec dataclass  (markdown_parser.py)
  → validates fields and card rows         (validators.py)
  → builds genanki Note models             (card_models.py)
  → writes .apkg                           (apkg_builder.py)
  → returns {ok, errors, output_path}      (service.py)
  → CLI entry point                        (build_apkg.py)
```

### Scripts Source (`skill/anki-card-creator/scripts/`)

| File | Role |
|------|------|
| `build_apkg.py` | CLI entry point: argparse wrapper, prints JSON result |
| `service.py` | Orchestration: parse → validate → build |
| `models.py` | `CardRow` and `DeckSpec` dataclasses |
| `markdown_parser.py` | Parses Markdown → `DeckSpec` |
| `validators.py` | Returns list of error strings |
| `card_styles.py` | CSS variants |
| `card_models.py` | `genanki` note-model definitions with layout support |
| `apkg_builder.py` | Builds `.apkg`; stable deck IDs via name hash |
| `requirements.txt` | Python dependencies (`genanki`) |

`build_apkg.py` adds its own directory to `sys.path` so all sibling modules are importable without package installation.

### Card Field Architecture

All cards have exactly 5 fields: `Prompt`, `Answer`, `Context`, `Example`, `Extra`. Fields are always stored even if empty. Layout (which fields appear where) is configured per-deck in the Markdown spec.

## Key Rules (from `docs/contributing.md`)

- **Never bypass the Markdown review stage** in the skill workflow
- **Never add hidden state** outside the Markdown deck spec
- **Keep `build_apkg.py` thin** — logic belongs in `service.py`
- **Keep the Markdown contract synchronized**: any change to the spec format must update `markdown_parser.py`, `validators.py`, `assets/deck-spec-template.md`, `references/markdown-spec.md`, and `skill/anki-card-creator/SKILL.md` together

## Key Reference Files

- `skill/anki-card-creator/references/markdown-spec.md` — fixed Markdown contract
- `skill/anki-card-creator/references/precise-card-rules.md` — card drafting constraints
- `skill/anki-card-creator/assets/deck-spec-template.md` — editable template shown to users
- `tests/fixtures/` — test deck specs (minimal and QA variants)

# Project Structure

## Top Level

```text
Anki_Card_Creator_Skill/
  docs/
  scripts/
  skill/
  tests/
  install.sh
  README.md
```

## Directory Responsibilities

### `skill/`

Contains the installable skill source and the Python packager scripts.

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
- `skill/anki-card-creator/scripts/build_apkg.py`
  CLI entry point — parses arguments, prints JSON result, exits 1 on failure
- `skill/anki-card-creator/scripts/service.py`
  orchestration: parse → validate → build
- `skill/anki-card-creator/scripts/models.py`
  `CardRow` and `DeckSpec` dataclasses
- `skill/anki-card-creator/scripts/markdown_parser.py`
  parses the Markdown deck spec into a `DeckSpec`
- `skill/anki-card-creator/scripts/validators.py`
  validates deck metadata and card rows
- `skill/anki-card-creator/scripts/card_styles.py`
  CSS variants for card presentation
- `skill/anki-card-creator/scripts/card_models.py`
  `genanki` note-model definitions
- `skill/anki-card-creator/scripts/apkg_builder.py`
  builds `.apkg` files
- `skill/anki-card-creator/scripts/requirements.txt`
  Python dependencies (`genanki`)

### `scripts/`

Contains repo-local helper scripts.

- `scripts/install_skill.py`
  copies the local skill tree into a target skills directory

### `tests/`

Contains unit and end-to-end tests plus Markdown fixtures.

- `tests/fixtures/`
  minimal and QA deck spec fixtures
- `tests/conftest.py`
  adds `skill/anki-card-creator/scripts/` to `sys.path`
- `tests/test_*.py`
  test files covering parser, validators, card models, builder, service, and CLI

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
- the scripts layer owns deterministic validation and packaging

Do not move deck-generation conversation logic into the scripts layer.

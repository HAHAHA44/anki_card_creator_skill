# Anki Card Creator Skill

A Codex or Claude Code skill that drafts an editable Markdown deck spec and packages it into an `.apkg` file via a bundled Python script.

The workflow is review-first: draft `deck-spec.md`, let the user edit it, then generate the final deck only after the user signals readiness.

## What This Repository Contains

- `skill/anki-card-creator/`
  the installable skill source, including the Python packager scripts under `scripts/`
- `install.sh`
  provisions a Python venv with `genanki` and creates a `~/.anki-card-creator/bin/build-apkg` wrapper
- `scripts/install_skill.py`
  copies the local skill into a skills directory
- `tests/`
  unit and end-to-end tests plus Markdown fixtures
- `docs/`
  design, planning, structure, and contribution docs

## Supported Workflow

1. Start from one of two inputs: `domain` or `extract`
2. Draft a fixed-format Markdown deck spec with the default layout shown inline
3. Let the user revise the Markdown directly
4. Run the build script once the user signals readiness

## Quick Start

Install the skill and runtime for both Codex and Claude Code:

```bash
bash ./install.sh --target both --scope user
```

Install project-local guidance for the current repo:

```bash
bash ./install.sh --target both --scope project --project-dir .
```

Run the packager directly after installing:

```bash
~/.anki-card-creator/bin/build-apkg tests/fixtures/qa_deck_spec.md --output-dir /tmp
```

Run tests:

```bash
python -m pytest tests -q
```

Install the skill only (no runtime):

```bash
python scripts/install_skill.py --source skill/anki-card-creator --dest ~/.codex/skills --name anki-card-creator
```

## Key Files

- `skill/anki-card-creator/SKILL.md`
- `skill/anki-card-creator/assets/deck-spec-template.md`
- `skill/anki-card-creator/references/markdown-spec.md`
- `skill/anki-card-creator/references/precise-card-rules.md`
- `skill/anki-card-creator/scripts/build_apkg.py`
- `skill/anki-card-creator/scripts/service.py`

## Additional Docs

- `docs/project-structure.md`
- `docs/contributing.md`
- `docs/install-prompts.md`
- `docs/superpowers/specs/2026-03-26-anki-card-creator-design.md`
- `docs/superpowers/specs/2026-03-29-cross-agent-installer-design.md`
- `docs/superpowers/plans/2026-03-26-anki-card-creator-implementation.md`
- `docs/superpowers/plans/2026-03-29-cross-agent-installer-implementation.md`

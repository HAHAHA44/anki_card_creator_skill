# Contributing Guide

## Scope

This project has two distinct layers:

- `skill/anki-card-creator/` — user interaction and Markdown generation
- `skill/anki-card-creator/scripts/` — parsing, validation, and packaging logic

Keep changes scoped to the correct layer. If a change affects both, make the boundary explicit in the commit and in the tests you run.

## Expected Workflow

1. Update or add tests first for behavior changes in `scripts/`
2. Run the failing test
3. Implement the smallest change that makes it pass
4. Re-run the targeted tests
5. Run the full test suite before closing the work
6. If the skill changes, update the Markdown template and references with it

## Verification Commands

Run the full test suite:

```bash
python -m pytest tests -q
```

Smoke-install the skill locally:

```bash
python scripts/install_skill.py --source skill/anki-card-creator --dest /tmp/codex-skills --name anki-card-creator
```

Smoke-test the packager script directly:

```bash
~/.anki-card-creator/bin/build-apkg tests/fixtures/qa_deck_spec.md --output-dir /tmp
```

Or without the installed wrapper:

```bash
python skill/anki-card-creator/scripts/build_apkg.py tests/fixtures/qa_deck_spec.md --output-dir /tmp
```

## Contribution Rules

- Do not bypass the Markdown review stage in the skill workflow.
- Do not add hidden state outside the Markdown deck spec.
- Keep `skill/anki-card-creator/scripts/build_apkg.py` thin; business logic belongs in `service.py`, `markdown_parser.py`, `validators.py`, or `apkg_builder.py`.
- Keep the Markdown contract stable unless you also update:
  - the skill instructions
  - the template
  - the references
  - the parser and validation tests
- Prefer small commits by responsibility.

## When Updating The Skill

If you change the skill workflow:

- update `SKILL.md`
- update `assets/deck-spec-template.md`
- update `references/markdown-spec.md`
- update `tests/acceptance-checklist.md`

## When Updating The Packager

If you change parser, validation, or packaging behavior:

- add or revise tests in `tests/`
- keep fixtures in `tests/fixtures/` readable and minimal
- verify that `.apkg` generation still succeeds for at least one fixture

# Contributing Guide

## Scope

This project has two distinct layers:

- `skill/anki-card-creator/`
- `mcp/`

Keep changes scoped to the correct layer. If a change affects both, make the boundary explicit in the commit and in the tests you run.

## Expected Workflow

1. Update or add tests first for behavior changes in `mcp/`
2. Run the failing test
3. Implement the smallest change that makes it pass
4. Re-run the targeted tests
5. Run the full `mcp` test suite before closing the work
6. If the skill changes, update the Markdown template and references with it

## Verification Commands

Run the full MCP test suite:

```bash
python -m pytest mcp/tests -q
```

Validate the skill structure:

```powershell
python "C:\Users\27391\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skill\anki-card-creator"
```

Smoke-install the skill locally:

```bash
python scripts/install_skill.py --source skill/anki-card-creator --dest /tmp/codex-skills --name anki-card-creator
```

Smoke-test the local CLI:

```bash
PYTHONPATH=mcp/src python -m anki_card_creator_mcp.cli mcp/tests/fixtures/qa_deck_spec.md --output-dir mcp/tests/output
```

## Contribution Rules

- Do not bypass the Markdown review stage in the skill workflow.
- Do not add hidden state outside the Markdown deck spec.
- Keep `mcp/src/anki_card_creator_mcp/server.py` thin; business logic belongs in parser, validator, service, or builder modules.
- Keep `mcp/src/anki_card_creator_mcp/cli.py` thin for the same reason.
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

## When Updating The MCP

If you change parser, validation, or packaging behavior:

- add or revise tests in `mcp/tests/`
- keep fixtures readable and minimal
- verify that `.apkg` generation still succeeds for at least one fixture

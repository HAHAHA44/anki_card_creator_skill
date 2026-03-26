# Anki Card Creator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a hybrid Anki card creator with a Codex skill that produces a fixed Markdown deck spec and a Python MCP server that validates the spec and generates `.apkg` files with `genanki`.

**Architecture:** Keep the system split into two layers. The `skill/` directory owns user interaction, card drafting rules, and the fixed `deck-spec.md` contract. The `mcp/` directory owns deterministic parsing, validation, style/model selection, and `.apkg` generation from Markdown. Add a small installer so the skill can live in this repository and also be copied into `~/.codex/skills`.

**Tech Stack:** Python 3.11+, `pytest`, `genanki`, Python MCP SDK, PowerShell for local setup, Markdown parsing with Python standard library helpers

---

## Preconditions

- The implementation should create a reusable source tree in this repository.
- The implementation should also make the skill installable into `~/.codex/skills`.

### Task 1: Bootstrap The Repository And Python Package

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\.gitignore`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\pyproject.toml`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\__init__.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_smoke.py`

- [ ] **Step 1: Write the failing smoke test**

```python
from anki_card_creator_mcp import __all__


def test_package_exports_module_symbol():
    assert "__version__" in __all__
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_smoke.py -q`
Expected: `ModuleNotFoundError` or import failure because the package does not exist yet.

- [ ] **Step 3: Write the minimal package bootstrap**

```python
__version__ = "0.1.0"
__all__ = ["__version__"]
```

Write `mcp/pyproject.toml` with:
- package name `anki-card-creator-mcp`
- Python version requirement
- dependencies `genanki` and `mcp`
- optional dev dependency `pytest`

Write `.gitignore` with at least:
- `__pycache__/`
- `.pytest_cache/`
- `.venv/`
- `dist/`
- `build/`
- `*.apkg`

- [ ] **Step 4: Re-run the smoke test**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_smoke.py -q`
Expected: `1 passed`

- [ ] **Step 5: Initialize git and make the first commit**

Run:

```powershell
git init
git add .gitignore mcp/pyproject.toml mcp/src/anki_card_creator_mcp/__init__.py mcp/tests/test_package_smoke.py
git commit -m "chore: bootstrap anki card creator workspace"
```

Expected: new repository initialized and first commit created.

### Task 2: Implement The Markdown Parser

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\models.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\markdown_parser.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\fixtures\minimal_deck_spec.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_markdown_parser.py`

- [ ] **Step 1: Write failing parser tests**

```python
from pathlib import Path

from anki_card_creator_mcp.markdown_parser import parse_deck_spec


def test_parse_deck_metadata_and_cards():
    spec = parse_deck_spec(Path("mcp/tests/fixtures/minimal_deck_spec.md"))
    assert spec.deck_name == "Biology Basics"
    assert spec.source_mode == "domain"
    assert spec.card_type == "term"
    assert spec.output_file == "biology-basics.apkg"
    assert len(spec.cards) == 2
    assert spec.cards[0].front == "What organelle produces ATP in eukaryotic cells?"
```

- [ ] **Step 2: Run the parser tests to verify they fail**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_markdown_parser.py -q`
Expected: import failure because `parse_deck_spec` does not exist yet.

- [ ] **Step 3: Implement the parser with small data models**

Create dataclasses like:

```python
from dataclasses import dataclass


@dataclass
class CardRow:
    id: str
    note_type: str
    front: str
    back: str
    context: str = ""
    example: str = ""
    extra: str = ""
    tags: str = ""


@dataclass
class DeckSpec:
    deck_name: str
    source_mode: str
    card_type: str
    output_file: str
    style_profile: str
    strict_precise_mode: bool
    generation_notes: str
    cards: list[CardRow]
```

Implement `parse_deck_spec(path: Path) -> DeckSpec` by:
- locating the required headings
- parsing bullet metadata lines of the form `- key: value`
- parsing the schema-free card table in `## Cards`
- ignoring blank lines outside the required sections

- [ ] **Step 4: Re-run the parser tests**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_markdown_parser.py -q`
Expected: parser tests pass.

- [ ] **Step 5: Commit the parser slice**

```powershell
git add mcp/src/anki_card_creator_mcp/models.py mcp/src/anki_card_creator_mcp/markdown_parser.py mcp/tests/fixtures/minimal_deck_spec.md mcp/tests/test_markdown_parser.py
git commit -m "feat: parse markdown deck specs"
```

### Task 3: Implement Validation Rules

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\validators.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_validators.py`

- [ ] **Step 1: Write failing validation tests**

```python
from anki_card_creator_mcp.models import CardRow, DeckSpec
from anki_card_creator_mcp.validators import validate_deck_spec


def test_rejects_invalid_note_type():
    spec = DeckSpec(
        deck_name="Bad Deck",
        source_mode="domain",
        card_type="term",
        output_file="bad.apkg",
        style_profile="concise",
        strict_precise_mode=True,
        generation_notes="",
        cards=[CardRow(id="1", note_type="bad", front="Q", back="A")],
    )
    errors = validate_deck_spec(spec)
    assert errors == ["cards[0].note_type must be one of term, language, qa"]
```

- [ ] **Step 2: Run the validation tests to verify they fail**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_validators.py -q`
Expected: import failure because the validator module does not exist yet.

- [ ] **Step 3: Implement minimal validation**

Implement `validate_deck_spec(spec: DeckSpec) -> list[str]` with checks for:
- required metadata values are not empty
- `source_mode` is `domain` or `extract`
- `card_type` is `term`, `language`, or `qa`
- `style_profile` is `concise`, `exam`, `example-rich`, or `mnemonic`
- every card `note_type` is valid
- every card `note_type` matches deck-level `card_type`
- every card has non-empty `id`, `front`, and `back`
- card ids are unique
- `output_file` ends with `.apkg`

- [ ] **Step 4: Re-run the validation tests**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_validators.py -q`
Expected: validator tests pass.

- [ ] **Step 5: Commit the validator slice**

```powershell
git add mcp/src/anki_card_creator_mcp/validators.py mcp/tests/test_validators.py
git commit -m "feat: validate parsed deck specs"
```

### Task 4: Implement Style Profiles And Note Models

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\card_styles.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\card_models.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_card_models.py`

- [ ] **Step 1: Write failing tests for style and model lookup**

```python
from anki_card_creator_mcp.card_models import get_note_model
from anki_card_creator_mcp.card_styles import get_style_css


def test_returns_css_for_example_rich_profile():
    css = get_style_css("example-rich")
    assert ".example-block" in css


def test_returns_qa_model():
    model = get_note_model("qa", "concise")
    assert model.name == "anki-card-creator-qa"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_card_models.py -q`
Expected: import failure because the modules do not exist yet.

- [ ] **Step 3: Implement the style/profile layer**

Implement:
- `get_style_css(style_profile: str) -> str`
- `get_note_model(card_type: str, style_profile: str) -> genanki.Model`

Keep version 1 simple:
- `term`, `language`, and `qa` each get one note model
- all models use the same fields: `Front`, `Back`, `Context`, `Example`, `Extra`
- the HTML template conditionally renders empty fields away
- the CSS varies by `style_profile`

Use small, deterministic names:

```python
MODEL_NAMES = {
    "term": "anki-card-creator-term",
    "language": "anki-card-creator-language",
    "qa": "anki-card-creator-qa",
}
```

- [ ] **Step 4: Re-run the tests**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_card_models.py -q`
Expected: style/model tests pass.

- [ ] **Step 5: Commit the style/model slice**

```powershell
git add mcp/src/anki_card_creator_mcp/card_styles.py mcp/src/anki_card_creator_mcp/card_models.py mcp/tests/test_card_models.py
git commit -m "feat: add note models and style profiles"
```

### Task 5: Implement The `.apkg` Builder

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\apkg_builder.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_apkg_builder.py`

- [ ] **Step 1: Write the failing builder test**

```python
from pathlib import Path

from anki_card_creator_mcp.apkg_builder import build_apkg
from anki_card_creator_mcp.markdown_parser import parse_deck_spec


def test_build_apkg_writes_output_file(tmp_path):
    spec = parse_deck_spec(Path("mcp/tests/fixtures/minimal_deck_spec.md"))
    output_path = build_apkg(spec, tmp_path)
    assert output_path.exists()
    assert output_path.suffix == ".apkg"
    assert output_path.stat().st_size > 0
```

- [ ] **Step 2: Run the builder test to verify it fails**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_apkg_builder.py -q`
Expected: import failure because the builder does not exist yet.

- [ ] **Step 3: Implement minimal deck packaging**

Implement:
- `build_apkg(spec: DeckSpec, output_dir: Path) -> Path`

Builder behavior:
- derive a stable deck id from `deck_name`
- create the correct `genanki.Deck`
- choose the note model from `get_note_model(spec.card_type, spec.style_profile)`
- create one `genanki.Note` per card row
- map fields in this order: `Front`, `Back`, `Context`, `Example`, `Extra`
- split comma-separated tags into a tag list
- write the package to `output_dir / spec.output_file`

- [ ] **Step 4: Re-run the builder test**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_apkg_builder.py -q`
Expected: builder test passes and a temporary `.apkg` file is created.

- [ ] **Step 5: Commit the builder slice**

```powershell
git add mcp/src/anki_card_creator_mcp/apkg_builder.py mcp/tests/test_apkg_builder.py
git commit -m "feat: generate apkg files with genanki"
```

### Task 6: Add A Thin Service Layer And MCP Server

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\service.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\server.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_service.py`

- [ ] **Step 1: Write failing service tests**

```python
from pathlib import Path

from anki_card_creator_mcp.service import build_apkg_from_markdown


def test_service_returns_success_payload(tmp_path):
    result = build_apkg_from_markdown(
        Path("mcp/tests/fixtures/minimal_deck_spec.md"),
        tmp_path,
    )
    assert result["ok"] is True
    assert result["output_path"].endswith(".apkg")
    assert result["errors"] == []
```

- [ ] **Step 2: Run the service tests to verify they fail**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_service.py -q`
Expected: import failure because the service layer does not exist yet.

- [ ] **Step 3: Implement the service layer and MCP wrapper**

Implement `build_apkg_from_markdown(spec_path: Path, output_dir: Path | None = None) -> dict`:
- parse the Markdown file
- validate the parsed spec
- return `{"ok": False, "errors": [...], "output_path": ""}` on validation failure
- call `build_apkg` on success
- return `{"ok": True, "errors": [], "output_path": "..."}` on success

Implement `server.py` as a thin MCP wrapper exposing one tool like:

```python
def build_apkg_from_spec(spec_path: str, output_dir: str | None = None) -> dict:
    ...
```

Keep protocol code thin. The tests should target `service.py`, not the wire protocol internals.

- [ ] **Step 4: Re-run the service tests**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_service.py -q`
Expected: service tests pass.

- [ ] **Step 5: Add a command-line smoke check**

Run:

```powershell
python -c "from pathlib import Path; from anki_card_creator_mcp.service import build_apkg_from_markdown; print(build_apkg_from_markdown(Path(r'mcp/tests/fixtures/minimal_deck_spec.md'), Path(r'mcp/tests/output')))"
```

Expected: printed dictionary with `"ok": True` and an `.apkg` path.

- [ ] **Step 6: Commit the service/MCP slice**

```powershell
git add mcp/src/anki_card_creator_mcp/service.py mcp/src/anki_card_creator_mcp/server.py mcp/tests/test_service.py
git commit -m "feat: expose apkg generation through an mcp service"
```

### Task 7: Author The Skill And Its References

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\SKILL.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\agents\openai.yaml`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\references\precise-card-rules.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\references\markdown-spec.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\assets\deck-spec-template.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\tests\acceptance-checklist.md`

- [ ] **Step 1: Write the skill acceptance checks before writing the skill**

Create `skill/tests/acceptance-checklist.md` with at least these scenarios:
- user gives a domain but no `card_type`
- user gives extracted text and selects `qa`
- user asks to generate `.apkg` before reviewing Markdown

For each scenario, write expected skill behavior in checklist form:
- ask for missing required fields
- generate `deck-spec.md`
- wait for user approval before MCP call

- [ ] **Step 2: Record the current baseline failure**

Document in `skill/tests/acceptance-checklist.md` that the repository currently has no skill, so all three scenarios fail.

- [ ] **Step 3: Write the skill and support references**

`skill/SKILL.md` should include:
- trigger description for Anki deck generation from domain or source text
- mandatory clarification of `card_type`, `deck_name`, and `style_profile`
- fixed process `input -> clarify -> draft markdown -> user edits markdown -> explicit approval -> MCP call`
- explicit use of the precise-card rules
- instruction to produce the exact fixed Markdown layout

`skill/references/precise-card-rules.md` should summarize the allowed rules from the approved article.

`skill/references/markdown-spec.md` should mirror the final `deck-spec.md` contract with one worked example.

`skill/assets/deck-spec-template.md` should contain a ready-to-fill template with the final sections and table headers.

- [ ] **Step 4: Add skill metadata**

Write `skill/agents/openai.yaml` with:
- human-facing display name
- short description
- default prompt that tells Codex to gather inputs, draft `deck-spec.md`, and wait for approval before packaging

- [ ] **Step 5: Manually validate the skill against the acceptance checklist**

Read `skill/SKILL.md` against each scenario in `skill/tests/acceptance-checklist.md` and verify:
- every required question is covered
- the Markdown review gate is mandatory
- the MCP call happens only after approval

If subagent validation is later authorized, add a forward-test pass before merging. Do not block version 1 on that authorization.

- [ ] **Step 6: Commit the skill slice**

```powershell
git add skill/SKILL.md skill/agents/openai.yaml skill/references/precise-card-rules.md skill/references/markdown-spec.md skill/assets/deck-spec-template.md skill/tests/acceptance-checklist.md
git commit -m "feat: add anki card creator skill"
```

### Task 8: Add The Local Skill Installer

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\scripts\install_skill.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_install_skill.py`

- [ ] **Step 1: Write the failing installer test**

```python
from pathlib import Path

from scripts.install_skill import install_skill


def test_install_skill_copies_skill_tree(tmp_path):
    target = tmp_path / "skills"
    installed_path = install_skill(
        source=Path("skill"),
        destination_root=target,
        skill_name="anki-card-creator",
    )
    assert installed_path.exists()
    assert (installed_path / "SKILL.md").exists()
    assert (installed_path / "agents" / "openai.yaml").exists()
```

- [ ] **Step 2: Run the installer test to verify it fails**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_install_skill.py -q`
Expected: import failure because the installer does not exist yet.

- [ ] **Step 3: Implement the installer**

Implement `install_skill.py` with:
- callable function `install_skill(source: Path, destination_root: Path, skill_name: str) -> Path`
- CLI support:

```powershell
python scripts/install_skill.py --source skill --dest "$env:USERPROFILE\.codex\skills" --name anki-card-creator
```

Installer behavior:
- remove any existing target directory for that skill
- copy the current repository's `skill/` tree into the target
- return the final installed path

- [ ] **Step 4: Re-run the installer test**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_install_skill.py -q`
Expected: installer test passes.

- [ ] **Step 5: Smoke-test a local install**

Run:

```powershell
python scripts/install_skill.py --source skill --dest "$env:TEMP\codex-skills" --name anki-card-creator
```

Expected: a copied skill tree under `%TEMP%\codex-skills\anki-card-creator`.

- [ ] **Step 6: Commit the installer slice**

```powershell
git add scripts/install_skill.py mcp/tests/test_install_skill.py
git commit -m "feat: add local skill installer"
```

### Task 9: End-To-End Verification

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\fixtures\qa_deck_spec.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_e2e.py`

- [ ] **Step 1: Write the failing end-to-end test**

```python
from pathlib import Path

from anki_card_creator_mcp.service import build_apkg_from_markdown


def test_end_to_end_builds_apkg_from_markdown(tmp_path):
    result = build_apkg_from_markdown(
        Path("mcp/tests/fixtures/qa_deck_spec.md"),
        tmp_path,
    )
    assert result["ok"] is True
    assert Path(result["output_path"]).exists()
```

- [ ] **Step 2: Run the end-to-end test to verify it fails**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_e2e.py -q`
Expected: failure because the fixture does not exist yet.

- [ ] **Step 3: Add the final fixture and make the test pass**

Create a realistic `qa_deck_spec.md` fixture with:
- `card_type: qa`
- `style_profile: concise`
- at least three rows
- one `context` value
- one `example` value

Then re-run the end-to-end test until it passes.

- [ ] **Step 4: Run the full test suite**

Run: `python -m pytest d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests -q`
Expected: full test suite passes with no failures.

- [ ] **Step 5: Run final smoke checks**

Run:

```powershell
python scripts/install_skill.py --source skill --dest "$env:TEMP\codex-skills" --name anki-card-creator
python -c "from pathlib import Path; from anki_card_creator_mcp.service import build_apkg_from_markdown; print(build_apkg_from_markdown(Path(r'mcp/tests/fixtures/qa_deck_spec.md'), Path(r'mcp/tests/output')))"
```

Expected:
- skill install succeeds
- printed service result has `"ok": True`
- `.apkg` file exists in `mcp/tests/output`

- [ ] **Step 6: Commit the verified system**

```powershell
git add .
git commit -m "feat: ship hybrid anki card creator"
```

## Notes For The Implementer

- Keep Markdown parsing strict. Version 1 should reject malformed tables instead of trying to guess user intent.
- Keep the MCP server thin. Most logic belongs in parser, validator, and builder modules.
- Do not introduce multiple note-model grammars in version 1. Use one shared field set and validate that per-row `note_type` matches the deck-level `card_type`.
- Keep CSS simple and deterministic. Style profiles should alter presentation, not data structure.
- Treat `skill/assets/deck-spec-template.md` as the canonical template shown to users.
- Re-run targeted tests after every slice before moving on.
- If implementation starts to sprawl, split utility code into small modules instead of growing one large file.

# Anki Card Layout Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the Anki deck contract and rendering flow so that deck-level layout configuration controls which fields appear on the front and back, while preserving the Markdown-first approval workflow.

**Architecture:** Keep the existing hybrid split. The `skill/anki-card-creator/` layer owns user interaction, layout explanation, and Markdown drafting. The `mcp/src/anki_card_creator_mcp/` layer owns parsing, validation, layout-aware note rendering, and `.apkg` generation. The deck spec becomes simpler by removing card-type/style metadata and replacing it with a shared `Card Layout` section.

**Tech Stack:** Python 3.11+, `pytest`, `genanki`, Python MCP SDK, Markdown parsing with Python standard library helpers

---

## Scope Notes

- This plan updates the existing implementation. Do not follow the old implementation plan for the removed `card_type`, `style_profile`, `strict_precise_mode`, or `note_type` concepts.
- The redesign is deck-level only. Do not introduce per-card layout overrides.
- The `extra` marker is fixed to `※`. Do not make it user-configurable in this iteration.

## File Structure Impact

Expected write set:

- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\models.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\markdown_parser.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\validators.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\card_models.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\apkg_builder.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\service.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\fixtures\minimal_deck_spec.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\fixtures\qa_deck_spec.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_markdown_parser.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_validators.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_card_models.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_apkg_builder.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_service.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_e2e.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\SKILL.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\references\layout-preview.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\references\markdown-spec.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\assets\deck-spec-template.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\tests\acceptance-checklist.md`

### Task 1: Update Data Models And Markdown Parsing

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\models.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\markdown_parser.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\fixtures\minimal_deck_spec.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_markdown_parser.py`

- [ ] **Step 1: Write the failing parser tests for the new contract**

Update the parser test to assert:

```python
spec = parse_deck_spec(Path("mcp/tests/fixtures/minimal_deck_spec.md"))
assert spec.deck_name == "Biology Basics"
assert spec.source_mode == "domain"
assert spec.output_file == "biology-basics.apkg"
assert spec.front_layout == ["context", "front", "example"]
assert spec.back_layout == ["back", "extra"]
assert spec.cards[0].example == "ATP production happens here in most eukaryotic cells."
```

- [ ] **Step 2: Run the parser tests to verify they fail**

Run: `python -m pytest .\mcp\tests\test_markdown_parser.py -q`
Expected: failure because current models and parser still expect `Card Policy`, `card_type`, and `style_profile`.

- [ ] **Step 3: Implement the new deck model and parser**

Replace the current `DeckSpec` shape with something like:

```python
@dataclass
class DeckSpec:
    deck_name: str
    source_mode: str
    output_file: str
    front_layout: list[str]
    back_layout: list[str]
    generation_notes: str
    cards: list[CardRow]
```

Keep `CardRow` with:
- `id`
- `front`
- `back`
- `context`
- `example`
- `extra`
- `tags`

Update parsing logic to:
- require `## Card Layout` instead of `## Card Policy`
- parse comma-separated field lists from `front_layout` and `back_layout`
- parse the simplified cards table without `note_type`

- [ ] **Step 4: Re-run the parser tests**

Run: `python -m pytest .\mcp\tests\test_markdown_parser.py -q`
Expected: parser test passes under the new deck spec contract.

- [ ] **Step 5: Commit the parser/model slice**

```powershell
git add mcp/src/anki_card_creator_mcp/models.py mcp/src/anki_card_creator_mcp/markdown_parser.py mcp/tests/fixtures/minimal_deck_spec.md mcp/tests/test_markdown_parser.py
git commit -m "feat: parse deck-level card layout configuration"
```

### Task 2: Replace Validation With Layout-Aware Validation

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\validators.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_validators.py`

- [ ] **Step 1: Write failing validator tests for the new layout rules**

Add tests for:
- invalid field name in `front_layout`
- duplicate field across `front_layout` and `back_layout`
- empty `front_layout`
- non-`.apkg` output file

Example:

```python
spec = make_spec(front_layout=["context", "bad"], back_layout=["back", "extra"])
errors = validate_deck_spec(spec)
assert "front_layout contains unsupported field: bad" in errors
```

- [ ] **Step 2: Run the validator tests to verify they fail**

Run: `python -m pytest .\mcp\tests\test_validators.py -q`
Expected: failure because current validator still enforces `card_type`, `style_profile`, and `note_type`.

- [ ] **Step 3: Implement the new validator**

Validate:
- `deck_name` is non-empty
- `source_mode` is `domain` or `extract`
- `output_file` ends with `.apkg`
- `front_layout` is non-empty
- `back_layout` is non-empty
- layout fields are only from `front`, `back`, `context`, `example`, `extra`
- no duplicate field appears in both layouts
- each card has `id`, `front`, and `back`
- card ids are unique

Do not validate:
- `style_profile`
- `strict_precise_mode`
- `card_type`
- `note_type`

- [ ] **Step 4: Re-run the validator tests**

Run: `python -m pytest .\mcp\tests\test_validators.py -q`
Expected: validator tests pass for the new layout-based rules.

- [ ] **Step 5: Commit the validator slice**

```powershell
git add mcp/src/anki_card_creator_mcp/validators.py mcp/tests/test_validators.py
git commit -m "feat: validate deck layout configuration"
```

### Task 3: Replace Fixed Note Templates With Layout Rendering

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\card_models.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_card_models.py`

- [ ] **Step 1: Write failing tests for layout-aware templates**

Add tests that assert:
- `example` can render on the question side when included in `front_layout`
- `extra` renders with a `※` prefix when included in `back_layout`

Example:

```python
model = get_note_model(front_layout=["context", "front", "example"], back_layout=["back", "extra"])
template = model.templates[0]
assert "{{#Example}}" in template["qfmt"]
assert "※" in template["afmt"]
```

- [ ] **Step 2: Run the card-model tests to verify they fail**

Run: `python -m pytest .\mcp\tests\test_card_models.py -q`
Expected: failure because the current note model still hard-codes `Example` on the back and depends on `card_type/style_profile`.

- [ ] **Step 3: Implement layout-aware template construction**

Replace `get_note_model(card_type, style_profile)` with something like:

```python
def get_note_model(front_layout: list[str], back_layout: list[str]) -> genanki.Model:
    ...
```

Behavior:
- keep the same field set: `Front`, `Back`, `Context`, `Example`, `Extra`
- build `qfmt` from `front_layout`
- build `afmt` from `back_layout`
- render `extra` as `※ {{Extra}}`
- remove any dependency on `card_type` or `style_profile`

- [ ] **Step 4: Re-run the card-model tests**

Run: `python -m pytest .\mcp\tests\test_card_models.py -q`
Expected: tests pass and confirm the new front/back field placement.

- [ ] **Step 5: Commit the template/rendering slice**

```powershell
git add mcp/src/anki_card_creator_mcp/card_models.py mcp/tests/test_card_models.py
git commit -m "feat: render cards from deck-level layout rules"
```

### Task 4: Update Packaging And Service Layers

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\apkg_builder.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\service.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_apkg_builder.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_service.py`

- [ ] **Step 1: Write failing tests for the builder and service under the new contract**

Update tests to assert:
- packaging succeeds without `card_type`
- packaging succeeds without `style_profile`
- `.apkg` generation still works with `front_layout/back_layout`

- [ ] **Step 2: Run the builder/service tests to verify they fail**

Run:

```powershell
python -m pytest .\mcp\tests\test_apkg_builder.py .\mcp\tests\test_service.py -q
```

Expected: failure because `build_apkg` still calls `get_note_model(spec.card_type, spec.style_profile)`.

- [ ] **Step 3: Update the builder and service code**

Builder changes:
- call `get_note_model(spec.front_layout, spec.back_layout)`
- keep mapping note fields in the existing storage order:
  `Front`, `Back`, `Context`, `Example`, `Extra`

Service changes:
- keep the same API surface
- return validation failures from the new layout checks

- [ ] **Step 4: Re-run the builder/service tests**

Run:

```powershell
python -m pytest .\mcp\tests\test_apkg_builder.py .\mcp\tests\test_service.py -q
```

Expected: builder and service tests pass.

- [ ] **Step 5: Commit the packaging/service slice**

```powershell
git add mcp/src/anki_card_creator_mcp/apkg_builder.py mcp/src/anki_card_creator_mcp/service.py mcp/tests/test_apkg_builder.py mcp/tests/test_service.py
git commit -m "feat: package decks using shared layout configuration"
```

### Task 5: Rewrite Fixtures And End-To-End Tests

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\fixtures\qa_deck_spec.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_e2e.py`

- [ ] **Step 1: Write or update the end-to-end test for the new layout spec**

Ensure the e2e test uses a fixture with:
- no `card_type`
- no `style_profile`
- `## Card Layout`
- `example` content placed on the front by layout

- [ ] **Step 2: Run the e2e test to verify it fails**

Run: `python -m pytest .\mcp\tests\test_e2e.py -q`
Expected: failure until the fixture and the updated parser/builder fully align.

- [ ] **Step 3: Update the fixture and make the test pass**

Use a realistic fixture with:
- `front_layout: context, front, example`
- `back_layout: back, extra`
- at least three rows
- one non-empty `example`
- one non-empty `extra`

- [ ] **Step 4: Re-run the e2e test**

Run: `python -m pytest .\mcp\tests\test_e2e.py -q`
Expected: e2e test passes and writes a non-empty `.apkg`.

- [ ] **Step 5: Commit the e2e slice**

```powershell
git add mcp/tests/fixtures/qa_deck_spec.md mcp/tests/test_e2e.py
git commit -m "test: cover layout-based deck generation end to end"
```

### Task 6: Rewrite Skill References, Template, And Workflow

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\SKILL.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\references\layout-preview.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\references\markdown-spec.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\assets\deck-spec-template.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\tests\acceptance-checklist.md`

- [ ] **Step 1: Update the skill acceptance checklist before editing the skill**

Replace old scenarios with layout-focused ones:
- user requests a deck and receives the default ASCII layout preview
- user changes the front/back field assignment before drafting
- user tries to generate `.apkg` before approving the current Markdown spec

- [ ] **Step 2: Record the current baseline mismatch**

Document that the current skill still references:
- `card_type`
- `style_profile`
- old `Card Policy`
- no ASCII layout preview

- [ ] **Step 3: Rewrite `SKILL.md`**

The new skill must:
- remove all `card_type` and `style_profile` clarification requirements
- introduce a mandatory default-layout explanation step
- present the default layout using the ASCII preview reference
- ask whether the user accepts or changes the default front/back layout
- convert user changes into deck-level `front_layout` and `back_layout`
- continue with the Markdown-first workflow and explicit approval gate

- [ ] **Step 4: Add the new layout reference**

Create `references/layout-preview.md` with:
- a reusable ASCII preview
- the default front-side field list
- the default back-side field list
- the `※` rendering rule for `extra`

- [ ] **Step 5: Rewrite the markdown reference and template**

`references/markdown-spec.md` and `assets/deck-spec-template.md` must:
- use `## Card Layout`
- remove `Card Policy`
- remove `required`
- remove `note_type`
- show the simplified `Cards` table

- [ ] **Step 6: Manually validate the skill against the updated checklist**

Read the updated `SKILL.md`, `layout-preview.md`, and `markdown-spec.md` together and verify that:
- the ASCII layout preview is mandatory
- default configuration is explained before drafting
- user changes map into `front_layout/back_layout`
- approval still gates MCP packaging

- [ ] **Step 7: Run skill validation**

Run:

```powershell
python "C:\Users\27391\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skill\anki-card-creator"
```

Expected: `Skill is valid!`

- [ ] **Step 8: Commit the skill rewrite**

```powershell
git add skill/anki-card-creator/SKILL.md skill/anki-card-creator/references/layout-preview.md skill/anki-card-creator/references/markdown-spec.md skill/anki-card-creator/assets/deck-spec-template.md skill/anki-card-creator/tests/acceptance-checklist.md
git commit -m "feat: redesign skill workflow around deck-level layout"
```

### Task 7: Full Verification

**Files:**
- No new files expected unless verification exposes gaps

- [ ] **Step 1: Run the full MCP test suite**

Run: `python -m pytest .\mcp\tests -q`
Expected: full suite passes under the new deck contract.

- [ ] **Step 2: Validate the skill**

Run:

```powershell
python "C:\Users\27391\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skill\anki-card-creator"
```

Expected: `Skill is valid!`

- [ ] **Step 3: Smoke-test local skill installation**

Run:

```powershell
python .\scripts\install_skill.py --source .\skill\anki-card-creator --dest "$env:TEMP\codex-skills" --name anki-card-creator
```

Expected: installed skill tree appears under `%TEMP%\codex-skills\anki-card-creator`.

- [ ] **Step 4: Smoke-test `.apkg` generation from the new layout spec**

Run:

```powershell
New-Item -ItemType Directory -Force .\mcp\tests\output | Out-Null
python -c "from pathlib import Path; import sys; sys.path.insert(0, str(Path('mcp/src').resolve())); from anki_card_creator_mcp.service import build_apkg_from_markdown; print(build_apkg_from_markdown(Path(r'mcp/tests/fixtures/qa_deck_spec.md'), Path(r'mcp/tests/output')))"
```

Expected:
- printed result has `"ok": True`
- output path ends with `.apkg`
- file exists in `mcp/tests/output`

- [ ] **Step 5: Commit the verified redesign**

```powershell
git add .
git commit -m "feat: redesign anki deck layout workflow"
```

## Notes For The Implementer

- Do not preserve compatibility with the old `Card Policy` format unless tests explicitly require it.
- Keep the MCP API surface stable if possible; prefer changing internal parsing/rendering over changing the top-level service function name.
- Keep the `extra` marker hard-coded as `※` in the renderer.
- Use the new `layout-preview.md` reference to avoid duplicating ASCII preview content in multiple places.
- Do not reintroduce `card_type`, `style_profile`, or `note_type` in new tests or fixtures.

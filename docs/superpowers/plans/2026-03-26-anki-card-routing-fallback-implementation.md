# Anki Card Routing Fallback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Route approved deck packaging through MCP when available and through a local CLI fallback skill when MCP is unavailable, while keeping both paths behaviorally identical.

**Architecture:** Keep one packaging core in `mcp/src/anki_card_creator_mcp/`. Add a CLI transport that reuses the same service function as the MCP server. Update the primary drafting skill to route between the MCP tool and a new fallback packaging skill. Keep approval gating in the primary skill and keep the fallback skill packaging-only.

**Tech Stack:** Python 3.11+, `pytest`, `argparse`, `genanki`, Python MCP SDK, Markdown-based Codex skills

---

## File Structure Impact

Expected write set:

- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\SKILL.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\tests\acceptance-checklist.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\SKILL.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\tests\acceptance-checklist.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\pyproject.toml`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\cli.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\src\anki_card_creator_mcp\__init__.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_cli.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\README.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\contributing.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\project-structure.md`

### Task 1: Add RED Tests For CLI Packaging

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_cli.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\pyproject.toml`

- [ ] **Step 1: Write the failing CLI test**

Add a test that runs the module CLI against `mcp/tests/fixtures/qa_deck_spec.md` and asserts:

```python
assert result.returncode == 0
assert '"ok": true' in result.stdout.lower()
assert output_path.exists()
```

- [ ] **Step 2: Run the CLI test to verify it fails**

Run: `python -m pytest .\mcp\tests\test_cli.py -q`
Expected: fail because no CLI module or script entrypoint exists yet.

- [ ] **Step 3: Implement the minimal CLI transport**

Create `mcp/src/anki_card_creator_mcp/cli.py` that:

- parses `spec_path`
- optionally parses `--output-dir`
- calls `build_apkg_from_markdown()`
- prints JSON to stdout
- exits non-zero when `ok` is false

Update `mcp/pyproject.toml` with a console script entrypoint.

- [ ] **Step 4: Re-run the CLI test**

Run: `python -m pytest .\mcp\tests\test_cli.py -q`
Expected: pass.

### Task 2: Add RED Acceptance Coverage For Routing

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\tests\acceptance-checklist.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\tests\acceptance-checklist.md`

- [ ] **Step 1: Extend the primary skill acceptance checklist**

Add scenarios for:

- MCP tool available after approval
- MCP tool unavailable after approval
- fallback path must invoke the packaging skill, not draft cards again

- [ ] **Step 2: Add the fallback skill acceptance checklist**

Document expected behavior:

- package an approved spec through CLI
- surface validation errors
- avoid drafting or editing cards

- [ ] **Step 3: Record the RED baseline**

Document that the current repository fails these scenarios because:

- the primary skill only references MCP
- no fallback packaging skill exists
- no local CLI transport exists

### Task 3: Update The Primary Skill Routing

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-creator\SKILL.md`

- [ ] **Step 1: Rewrite the packaging handoff section**

Change the handoff from MCP-only to routing:

- check for `mcp__ankiCardCreator__build_apkg_from_spec`
- use MCP if available
- otherwise invoke `anki-card-packager-cli`

- [ ] **Step 2: Keep the approval gate explicit**

Ensure the skill still says:

- no packaging before approval
- no hidden state
- validation failures return to Markdown editing

### Task 4: Create The Fallback Packaging Skill

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\SKILL.md`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\tests\acceptance-checklist.md`

- [ ] **Step 1: Write the fallback skill narrowly**

The skill should:

- accept `spec_path`
- optionally accept `output_dir`
- call the CLI
- return success/errors/output path

The skill must not:

- draft cards
- revise deck content silently
- bypass approval

### Task 5: Update Documentation

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\README.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\contributing.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\project-structure.md`

- [ ] **Step 1: Document both packaging modes**

Describe:

- MCP-preferred flow
- CLI fallback flow
- CLI invocation examples

### Task 6: Verify End To End

**Files:**
- No additional files unless verification exposes a gap

- [ ] **Step 1: Run targeted tests**

Run:

```powershell
python -m pytest .\mcp\tests\test_cli.py -q
python -m pytest .\mcp\tests\test_e2e.py -q
```

- [ ] **Step 2: Run the full MCP test suite**

Run: `python -m pytest .\mcp\tests -q`

- [ ] **Step 3: Validate the main skill**

Run:

```powershell
python "C:\Users\27391\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skill\anki-card-creator"
```

- [ ] **Step 4: Validate the fallback skill**

Run:

```powershell
python "C:\Users\27391\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skill\anki-card-packager-cli"
```

- [ ] **Step 5: Smoke-test the CLI directly**

Run:

```powershell
python -m anki_card_creator_mcp.cli .\mcp\tests\fixtures\qa_deck_spec.md --output-dir .\mcp\tests\output
```

Expected:

- JSON payload printed
- `"ok": true`
- `.apkg` file written

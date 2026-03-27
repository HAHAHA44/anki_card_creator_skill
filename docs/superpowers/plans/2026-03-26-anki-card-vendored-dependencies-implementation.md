# Anki Card Vendored Dependencies Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vendor `genanki` and its runtime dependencies into the fallback skill so the installed fallback skill can package decks without requiring preinstalled third-party packages.

**Architecture:** Extend `scripts/package_fallback_runtime.py` so it copies the repository runtime into `runtime/anki_card_creator_mcp/` and copies third-party runtime packages into `runtime/vendor/`. Update `runtime/run_cli.py` to prepend both vendored paths. Verify with `python -S` so tests do not rely on global site-packages.

**Tech Stack:** Python 3.11+, `pytest`, `importlib.metadata`, `shutil`, vendored package copying from the build environment

---

## File Structure Impact

Expected write set:

- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\scripts\package_fallback_runtime.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_fallback_runtime.py`
- Refresh: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\runtime\vendor\`
- Refresh: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\runtime\run_cli.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\SKILL.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\README.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\contributing.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\project-structure.md`

### Task 1: Add RED Tests That Prove Vendoring Is Required

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_fallback_runtime.py`

- [ ] **Step 1: Add a failing test for vendored dependencies**

Assert that packaging creates:

- `runtime/vendor/`
- vendored `genanki`
- vendored dependency modules

- [ ] **Step 2: Add a failing execution test using `python -S`**

Run:

```powershell
python -S <runtime>\run_cli.py <spec_path> --output-dir <dir>
```

Expected before implementation: import failure for `genanki` or another dependency.

### Task 2: Extend The Packaging Script

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\scripts\package_fallback_runtime.py`

- [ ] **Step 1: Implement dependency vendoring from the local build environment**

Copy the importable runtime contents for:

- `genanki`
- `cached-property`
- `frozendict`
- `chevron`
- `pyyaml`

into `runtime/vendor/`.

- [ ] **Step 2: Update the wrapper**

Prepend:

- `runtime/vendor`
- `runtime`

to `sys.path`.

- [ ] **Step 3: Re-run the vendored runtime tests**

Run: `python -m pytest .\mcp\tests\test_package_fallback_runtime.py -q`
Expected: pass.

### Task 3: Update Documentation

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\SKILL.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\README.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\contributing.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\project-structure.md`

- [ ] **Step 1: Document the third-party vendoring behavior**

Explain that:

- the fallback skill ships third-party runtime dependencies in `runtime/vendor/`
- the packaging script must be rerun after runtime dependency changes
- no runtime `pip install` happens during skill execution

### Task 4: Verify

**Files:**
- No additional files unless verification exposes a gap

- [ ] **Step 1: Run targeted tests**

Run:

```powershell
python -m pytest .\mcp\tests\test_package_fallback_runtime.py -q
python -m pytest .\mcp\tests\test_cli.py -q
```

- [ ] **Step 2: Run the full MCP test suite**

Run: `python -m pytest .\mcp\tests -q`

- [ ] **Step 3: Validate the fallback skill**

Run:

```powershell
python "C:\Users\27391\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skill\anki-card-packager-cli"
```

- [ ] **Step 4: Refresh and smoke-test the real vendored runtime**

Run:

```powershell
python .\scripts\package_fallback_runtime.py
python -S .\skill\anki-card-packager-cli\runtime\run_cli.py .\mcp\tests\fixtures\qa_deck_spec.md --output-dir .\mcp\tests\output
```

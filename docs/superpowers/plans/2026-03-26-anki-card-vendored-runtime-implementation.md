# Anki Card Vendored Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package the fallback Anki runtime into the fallback skill directory so installed skills can generate `.apkg` files without relying on the repository `mcp/` path.

**Architecture:** Keep `mcp/src/anki_card_creator_mcp/` as the source runtime. Add a packaging script that copies a curated runtime subset into `skill/anki-card-packager-cli/runtime/anki_card_creator_mcp/` and generates a wrapper script in the same runtime directory. Update the fallback skill to invoke the vendored wrapper by relative path.

**Tech Stack:** Python 3.11+, `pytest`, `shutil`, `pathlib`, vendored Python modules inside the skill tree

---

## File Structure Impact

Expected write set:

- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\scripts\package_fallback_runtime.py`
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_fallback_runtime.py`
- Create or refresh: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\runtime\run_cli.py`
- Create or refresh: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\runtime\anki_card_creator_mcp\*.py`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\SKILL.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\README.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\contributing.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\project-structure.md`

### Task 1: Add RED Tests For Vendored Runtime Packaging

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_fallback_runtime.py`

- [ ] **Step 1: Write the failing test for the packaging script**

Test expectations:

- importing the packaging script helper succeeds
- the helper copies the approved runtime subset into a target directory
- `server.py` is not copied
- `cli.py` is copied
- `run_cli.py` is generated

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest .\mcp\tests\test_package_fallback_runtime.py -q`
Expected: fail because the packaging script does not exist yet.

### Task 2: Add RED Tests For Vendored Runtime Execution

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\mcp\tests\test_package_fallback_runtime.py`

- [ ] **Step 1: Add a failing execution test**

After packaging into a temp skill directory:

- run `python <temp-skill>\runtime\run_cli.py <spec_path> --output-dir <dir>`
- verify it returns JSON with `"ok": true`
- verify `.apkg` is created

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest .\mcp\tests\test_package_fallback_runtime.py -q`
Expected: fail because no packaging script or wrapper exists.

### Task 3: Implement The Packaging Script

**Files:**
- Create: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\scripts\package_fallback_runtime.py`

- [ ] **Step 1: Implement the minimal helper API**

Expose functions that:

- locate the source runtime
- remove any existing target runtime
- copy the approved file whitelist
- write `runtime\run_cli.py`

- [ ] **Step 2: Add a small CLI entrypoint**

Support a default target of:

- `skill/anki-card-packager-cli/runtime/`

Allow an override target for tests.

- [ ] **Step 3: Re-run the runtime packaging tests**

Run: `python -m pytest .\mcp\tests\test_package_fallback_runtime.py -q`
Expected: pass.

### Task 4: Update The Fallback Skill To Use The Vendored Wrapper

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\skill\anki-card-packager-cli\SKILL.md`

- [ ] **Step 1: Replace the old module invocation guidance**

The skill should instruct callers to run the vendored wrapper from the installed skill directory, not `mcp/src`.

- [ ] **Step 2: Keep the skill packaging-only**

Do not reintroduce drafting or hidden state.

### Task 5: Update Documentation

**Files:**
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\README.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\contributing.md`
- Modify: `d:\Documents\GIt Projects\Anki_Card_Creator_Skill\docs\project-structure.md`

- [ ] **Step 1: Document the vendoring step**

Show:

- how to refresh the vendored runtime
- that the fallback skill ships with its own runtime subset
- that `mcp/src` remains the source of truth

### Task 6: Verify

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

- [ ] **Step 4: Run the packaging script against the real skill target**

Run:

```powershell
python .\scripts\package_fallback_runtime.py
```

Expected:

- vendored runtime exists under `skill/anki-card-packager-cli/runtime/`
- `server.py` is absent
- `run_cli.py` exists

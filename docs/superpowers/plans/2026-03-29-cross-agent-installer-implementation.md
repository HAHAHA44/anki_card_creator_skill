# Cross-Agent Installer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single bash installer that provisions the Anki Card Creator skill and MCP wiring for Codex, Claude Code, or both at either user or project scope.

**Architecture:** Keep one repository-root `install.sh` as the public entry point. Let it provision a shared runtime venv, copy the skill tree into the requested platform directories, register MCP through available CLIs, and upsert project guidance files when project scope is requested. Validate the behavior with pytest-driven black-box tests that invoke the bash script with fake toolchain shims.

**Tech Stack:** Bash, Python 3.11+, `pytest`, repository-local MCP package install, JSON file generation, Markdown managed-block upserts

---

### Task 1: Add installer tests first

**Files:**
- Create: `mcp/tests/test_install_sh.py`
- Test: `mcp/tests/test_install_sh.py`

- [ ] **Step 1: Write the failing test**

```python
def test_install_sh_user_scope_installs_skills_and_registers_mcp(tmp_path: Path) -> None:
    result = run_install(...)
    assert result.returncode == 0
    assert (home / ".codex" / "skills" / "anki-card-creator" / "SKILL.md").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest mcp/tests/test_install_sh.py -q`
Expected: FAIL because `install.sh` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create a first-pass `install.sh` that parses args, copies the skill tree, provisions a runtime, and writes the expected files.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest mcp/tests/test_install_sh.py -q`
Expected: PASS for the new installer coverage.

- [ ] **Step 5: Commit**

```bash
git add mcp/tests/test_install_sh.py install.sh
git commit -m "feat: add cross-agent installer"
```

### Task 2: Document the installer surface

**Files:**
- Modify: `README.md`
- Modify: `mcp/README.md`
- Create: `docs/install-prompts.md`

- [ ] **Step 1: Write the failing test**

Manual documentation test:
- installer usage appears in the root README
- MCP server name matches the skill's expected tool prefix
- prompt snippets are copyable

- [ ] **Step 2: Run test to verify it fails**

Run: `rg -n "install.sh|ankiCardCreator|Install anki-card-creator" README.md mcp/README.md docs/install-prompts.md`
Expected: missing installer docs before edits.

- [ ] **Step 3: Write minimal implementation**

Add concise install docs and prompt snippets.

- [ ] **Step 4: Run test to verify it passes**

Run: `rg -n "install.sh|ankiCardCreator|Install anki-card-creator" README.md mcp/README.md docs/install-prompts.md`
Expected: matching lines found in all three files.

- [ ] **Step 5: Commit**

```bash
git add README.md mcp/README.md docs/install-prompts.md
git commit -m "docs: add cross-agent installer usage"
```

### Task 3: Verify the full repository state

**Files:**
- Modify: `.gitignore`
- Test: `mcp/tests/test_install_sh.py`
- Test: `mcp/tests/test_install_skill.py`

- [ ] **Step 1: Write the failing test**

Confirm the repo ignores project-local runtime output and that installer coverage still passes.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest mcp/tests/test_install_sh.py mcp/tests/test_install_skill.py -q`
Expected: any remaining installer regressions fail here.

- [ ] **Step 3: Write minimal implementation**

Add `.anki-card-creator/` to `.gitignore` and clean up any remaining installer mismatches.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest mcp/tests/test_install_sh.py mcp/tests/test_install_skill.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .gitignore mcp/tests/test_install_sh.py mcp/tests/test_install_skill.py
git commit -m "test: cover cross-agent installer"
```

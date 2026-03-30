# Cross-Agent Installer Design

## Goal

Add a single bash installer entrypoint that can install the Anki Card Creator skill and MCP wiring for both Codex and Claude Code.

## Requirements

1. One script must support `codex`, `claude`, or both.
2. One script must support user-scoped install and project-scoped install.
3. The installer must copy the reusable skill tree from `skill/anki-card-creator/`.
4. The installer must provision a runnable MCP environment instead of assuming a preconfigured `PYTHONPATH`.
5. Project-scoped installation should create shareable project files where the platform supports them.
6. The repository should include copyable prompt text so users can ask Codex or Claude Code to run the installer in a gstack-like flow.

## Design

### Installer Entry Point

Create `install.sh` in the repository root.

Supported flags:

- `--target codex|claude|both`
- `--scope user|project`
- `--project-dir <path>` for project-scoped writes
- `--python <path>` to select the Python interpreter used to build the MCP runtime
- `--server-name <name>` to keep the MCP server identifier configurable while defaulting to `ankiCardCreator`

Defaults:

- `target=both`
- `scope=user`
- `project-dir=$PWD`
- `server-name=ankiCardCreator`

### Runtime Provisioning

The installer should create a lightweight venv and install `./mcp` into it.

- User scope runtime root: `~/.anki-card-creator/runtime/venv`
- Project scope runtime root: `<project>/.anki-card-creator/runtime/venv`

This keeps MCP registration stable and removes the need for users to manage `PYTHONPATH` by hand.

### Skill Installation

The installer should copy `skill/anki-card-creator/` into:

- Codex user scope: `~/.codex/skills/anki-card-creator`
- Claude user scope: `~/.claude/skills/anki-card-creator`
- Codex project scope: `<project>/.codex/skills/anki-card-creator`
- Claude project scope: `<project>/.claude/skills/anki-card-creator`

Existing skill copies should be replaced so repeated installs refresh the skill content.

### MCP Registration

#### User Scope

- Codex: use `codex mcp add <server-name> -- <venv-python> -m anki_card_creator_mcp.server`
- Claude Code: use `claude mcp add <server-name> -- <venv-python> -m anki_card_creator_mcp.server`

If either CLI is unavailable, the installer should warn clearly and continue with the file-copy portion.

#### Project Scope

- Claude Code: write `<project>/.mcp.json` with a server entry pointing at the project runtime.
- Codex: no stable project-local MCP config was confirmed, so the installer should still perform best-effort local registration through `codex mcp add` when the CLI is available.

This keeps Claude Code project setup shareable, while Codex still becomes usable immediately on the installing machine.

### Project Guidance Files

For project-scoped installs, upsert managed instruction blocks into:

- `CLAUDE.md`
- `AGENTS.md`

The managed block should:

- mention the `anki-card-creator` skill
- point packaging to `mcp__ankiCardCreator__build_apkg_from_spec`
- mention the JSON fallback tool name

The block must be idempotent so re-running the installer updates only the managed section.

## Testing

Add automated tests that run the bash installer with fake `python`, `codex`, and `claude` binaries.

The tests should verify:

1. user-scoped install copies both skill trees and calls both MCP registration CLIs
2. project-scoped install writes `.mcp.json`, `CLAUDE.md`, and `AGENTS.md`
3. project-scoped install copies the project-local skill trees

## Documentation

Update:

- `README.md` with installer usage and examples
- `mcp/README.md` so the documented server name matches the skill's expected MCP tool prefix
- `docs/install-prompts.md` with copyable Codex and Claude prompts

---
title: Anki Card Routing Fallback
date: 2026-03-26
status: draft
---

# Anki Card Routing Fallback

## Goal

Allow the Anki card workflow to package approved Markdown deck specs in two modes:

1. use the installed MCP tool when it is available
2. fall back to a local CLI packaging path when the MCP tool is unavailable

The review-first Markdown workflow remains unchanged. The routing change only affects the final packaging handoff after explicit user approval.

## Approved Changes

The redesign is based on these approved requirements:

1. The primary skill must test whether the MCP tool is installed before packaging.
2. If the MCP tool is installed, the workflow should keep using MCP.
3. If the MCP tool is not installed, the workflow should invoke a separate fallback skill dedicated to packaging.
4. The fallback path must generate the same `.apkg` output format as the MCP path.
5. The fallback path must be callable from terminal environments such as OpenClaw through a CLI.

## Stable Boundary

The project keeps the same layer split:

- `skill/anki-card-creator/` owns user interaction, Markdown drafting, approval gating, and routing decisions.
- `skill/anki-card-packager-cli/` owns the fallback packaging workflow when MCP is unavailable.
- `mcp/src/anki_card_creator_mcp/` owns deterministic parsing, validation, and `.apkg` generation logic used by both transport layers.

This means there is still only one packaging implementation. MCP and CLI are two entrypoints over the same core service.

## Routing Rule

After the user approves the current Markdown deck spec:

1. check whether the MCP tool `mcp__ankiCardCreator__build_apkg_from_spec` is available
2. if available, call the MCP tool with `spec_path` and optional `output_dir`
3. if unavailable, invoke the fallback packaging skill
4. the fallback skill calls the local CLI, which reuses the same parser, validator, and builder code as the MCP layer

The skill must not silently switch before approval. Approval remains the only gate to final packaging in both branches.

## Fallback Packaging Skill

The fallback skill is a narrow execution skill, not another drafting skill.

Its responsibilities:

- accept a Markdown deck spec path
- optionally accept an output directory
- call the local CLI entrypoint
- surface success or validation errors back to the caller

Its non-goals:

- drafting cards
- changing the Markdown structure
- bypassing approval
- implementing a second parser or builder

## CLI Contract

The local CLI should expose the same effective operation as the MCP tool:

- input: `spec_path`
- optional input: `output_dir`
- output: success flag, error list, and `output_path`

The CLI should reuse `build_apkg_from_markdown()` so that MCP and CLI stay behaviorally aligned.

## Detection Policy

The skill-level routing check is instruction-level detection of the MCP tool name, not package import probing inside the Python codebase.

That keeps the decision aligned with the actual runtime environment:

- if the tool exists in the session, use MCP
- if the tool does not exist in the session, use the fallback packaging skill

## Files Affected

- `skill/anki-card-creator/SKILL.md`
- `skill/anki-card-creator/tests/acceptance-checklist.md`
- `skill/anki-card-packager-cli/SKILL.md` (new)
- `skill/anki-card-packager-cli/tests/acceptance-checklist.md` (new)
- `mcp/pyproject.toml`
- `mcp/src/anki_card_creator_mcp/cli.py` (new)
- `mcp/tests/test_cli.py` (new)
- `README.md`
- `docs/contributing.md`
- `docs/project-structure.md`

## Non-Goals

This change does not:

- replace MCP as the preferred packaging path
- change the Markdown deck spec contract
- move drafting logic into the fallback skill
- create a second implementation of parsing, validation, or `.apkg` generation

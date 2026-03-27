---
title: Anki Card Vendored Runtime
date: 2026-03-26
status: draft
---

# Anki Card Vendored Runtime

## Goal

Make the fallback packaging skill self-contained after installation.

Today the fallback skill assumes the Python module `anki_card_creator_mcp` is available from the repository or from a separately installed package. That is not reliable for external users who only install the skill directory.

The new design vendors the packaging runtime into the fallback skill so the installed skill can package approved deck specs without depending on the repository layout.

## Approved Changes

The redesign is based on these approved requirements:

1. Add a packaging script that copies the runtime subset into the fallback skill directory.
2. The fallback skill must default to the vendored runtime, not to `mcp/src` in the repository.
3. External users who install the fallback skill should not need the repository `mcp/` path.
4. The vendored runtime should include only the files needed for local CLI packaging.
5. The vendored runtime must keep using the same parser, validator, and builder code as the main MCP implementation source.

## Runtime Boundary

The vendored runtime lives under:

- `skill/anki-card-packager-cli/runtime/anki_card_creator_mcp/`

This directory is a publishable runtime subset, not a second independently authored implementation.

The source of truth remains:

- `mcp/src/anki_card_creator_mcp/`

The packaging script copies a curated subset from the source of truth into the vendored runtime directory.

## Included Runtime Files

The vendored runtime should include:

- `__init__.py`
- `apkg_builder.py`
- `card_models.py`
- `card_styles.py`
- `cli.py`
- `markdown_parser.py`
- `models.py`
- `service.py`
- `validators.py`

The vendored runtime should exclude:

- `server.py`
- `__pycache__/`
- tests
- repository-only docs

## Wrapper Contract

The fallback skill should call a wrapper script stored inside the skill directory, not a repo-relative import path.

Recommended wrapper:

- `skill/anki-card-packager-cli/runtime/run_cli.py`

Responsibilities:

- add the vendored runtime directory to `sys.path`
- execute `anki_card_creator_mcp.cli`
- preserve the same CLI contract as the source runtime

## Packaging Script Contract

Recommended script:

- `scripts/package_fallback_runtime.py`

Responsibilities:

- delete any previously packaged vendored runtime directory
- copy the approved runtime subset from `mcp/src/anki_card_creator_mcp/`
- create or refresh the wrapper script
- optionally print the target path for downstream tooling

Non-goals:

- package dependencies like `genanki`
- install Python packages
- modify the source runtime in `mcp/src/`

## Verification Expectations

The change is complete when:

1. the packaging script creates the vendored runtime directory
2. the vendored runtime excludes `server.py`
3. the wrapper can package a deck spec without using `mcp/src`
4. the fallback skill instructions point to the vendored wrapper
5. external installation no longer depends on the repository `mcp/` path

## Files Affected

- `scripts/package_fallback_runtime.py` (new)
- `scripts/tests/test_package_fallback_runtime.py` or equivalent test location (new)
- `skill/anki-card-packager-cli/runtime/` (generated)
- `skill/anki-card-packager-cli/SKILL.md`
- `README.md`
- `docs/contributing.md`
- `docs/project-structure.md`

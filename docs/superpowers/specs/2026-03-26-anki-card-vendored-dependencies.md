---
title: Anki Card Vendored Dependencies
date: 2026-03-26
status: draft
---

# Anki Card Vendored Dependencies

## Goal

Make the fallback packaging skill runnable without assuming the target Python environment already has `genanki` or its dependencies installed.

The current vendored runtime only includes repository-owned modules. That is not sufficient for external users because the fallback path still imports third-party packages from the host environment.

## Approved Changes

The redesign is based on these approved requirements:

1. The fallback skill must not assume `genanki` exists in the target environment.
2. The packaging script must vendor third-party runtime dependencies into the fallback skill.
3. The wrapper must load vendored dependencies before importing the vendored runtime.
4. The fallback path should not run `pip install` at skill execution time.

## Vendored Dependency Boundary

The source runtime remains:

- `mcp/src/anki_card_creator_mcp/`

The packaged fallback skill now carries two vendored layers:

- `skill/anki-card-packager-cli/runtime/anki_card_creator_mcp/`
- `skill/anki-card-packager-cli/runtime/vendor/`

`runtime/vendor/` is for third-party packages only.

## Third-Party Dependency Scope

The current packaging runtime depends on:

- `genanki`
- `cached-property`
- `frozendict`
- `chevron`
- `pyyaml`

The packaging script should vendor the importable package contents needed at runtime from the local Python environment used to prepare the skill.

## Wrapper Contract

`runtime/run_cli.py` must prepend these paths to `sys.path` in this order:

1. `runtime/vendor`
2. `runtime`

That ensures vendored dependencies and vendored repository runtime are used even if the host environment has different versions installed.

## Verification Expectations

The change is complete when:

1. the packaging script creates `runtime/vendor/`
2. vendored dependency modules exist under `runtime/vendor/`
3. `python -S runtime/run_cli.py ...` succeeds
4. no dependency import relies on site-packages from the host environment

## Non-Goals

This change does not:

- support arbitrary non-Python binary dependency trees
- build wheels
- install dependencies on the end user's machine at runtime

---
title: Anki Card Layout Redesign
date: 2026-03-26
status: draft
---

# Anki Card Layout Redesign

## Goal

Refine the current Anki card workflow so that card layout is configurable at the deck level, while keeping the Markdown-first workflow intact.

This redesign changes three areas:

1. the deck spec format
2. the skill conversation flow
3. the MCP protocol and note rendering behavior

## Approved Changes

The redesign is based on these approved requirements:

1. `example` should appear on the front side by default.
2. `extra` should appear on the back side with a `※` marker.
3. Remove `style_profile`, `strict_precise_mode`, and `card_type` from the Markdown deck spec.
4. Remove the `required` column from `Field Schema`.
5. Add a skill step that shows the default card layout to the user before drafting the deck, using ASCII layout preview.
6. Let the user change front/back field assignment before the deck is generated.
7. Treat layout configuration as deck-level only. No per-card layout override.

## New Deck Spec Contract

The Markdown file remains the single source of truth, but its structure changes.

### Required Section Order

1. `# Anki Deck Spec`
2. `## Deck Metadata`
3. `## Card Layout`
4. `## Field Schema`
5. `## Cards`

### Deck Metadata

```md
## Deck Metadata
- deck_name: ...
- source_mode: domain | extract
- output_file: ...
```

Removed fields:

- `card_type`
- `style_profile`
- `strict_precise_mode`

### Card Layout

This is the new deck-level layout configuration:

```md
## Card Layout
- front_layout: context, front, example
- back_layout: back, extra
- generation_notes: ...
```

Rules:

- `front_layout` applies to all cards in the deck
- `back_layout` applies to all cards in the deck
- field order is defined by the layout config
- the first version does not allow per-card layout override
- `extra` renders with a fixed `※` prefix when displayed

### Field Schema

The schema becomes informational only:

```md
## Field Schema
| field | description |
| --- | --- |
| id | Stable card id |
| front | Main prompt or term |
| back | Main answer or definition |
| context | Topic cue shown with the front side |
| example | Example sentence or usage |
| extra | Additional explanation shown with a `※` marker |
| tags | Comma-separated tags |
```

The `required` column is removed.

### Cards Table

The cards table is simplified:

```md
## Cards
| id | front | back | context | example | extra | tags |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ... | ... | ... | ... | ... | ... |
```

Removed card columns:

- `note_type`

## New Skill Flow

The skill keeps the Markdown-first workflow but inserts a new confirmation stage before drafting the deck.

### Updated Workflow

1. Detect whether the request is `domain` or `extract`.
2. Present the default card layout to the user.
3. Show an ASCII card preview for the default layout.
4. Explain the default field placement in a bullet list.
5. Ask whether the user wants to keep the default layout or change it.
6. If the user changes the layout, convert those changes into deck-level `front_layout` and `back_layout`.
7. Continue with the existing flow:
   - collect any remaining deck metadata
   - generate `deck-spec.md`
   - let the user edit the Markdown
   - ask for explicit approval
   - call MCP after approval

### Default Layout Preview

The skill should use a reusable reference document to display the layout preview.

Recommended reference file:

`skill/anki-card-creator/references/layout-preview.md`

The default ASCII preview should look like:

```text
Default Card Layout

Front
+----------------------------------+
| [Context]                        |
| [Front]                          |
| [Example]                        |
+----------------------------------+

Back
+----------------------------------+
| [Back]                           |
| ※ [Extra]                        |
+----------------------------------+
```

This preview is part of the skill conversation flow, not part of the generated deck spec.

## MCP Changes

The MCP must stop assuming a hard-coded front/back template.

### Current Limitation

The current implementation hard-codes this note structure:

- front side: `Context`, then `Front`
- back side: `Back`, then `Example`, then `Extra`

That is no longer sufficient.

### New MCP Responsibilities

The MCP must:

1. parse `## Card Layout`
2. validate `front_layout`
3. validate `back_layout`
4. render the front side from the configured field list
5. render the back side from the configured field list
6. render `extra` with a `※` marker when included in the layout

### Validation Expectations

`front_layout` and `back_layout` should only allow these field names:

- `front`
- `back`
- `context`
- `example`
- `extra`

Validation should also reject:

- unknown field names
- empty layout groups
- the same field appearing on both front and back if the project decides that duplication should be forbidden

The initial implementation can choose one of two policies for duplication:

1. allow it
2. reject it

The recommended policy is to reject duplicates across front and back because the layout is meant to define field placement cleanly.

### Rendering Rule For `extra`

If `extra` is displayed, MCP should render it as:

```text
※ {extra}
```

This marker should be built into the renderer and should not require a user-configurable field.

## Conceptual Simplification

The redesign intentionally removes deck-level content typing from the first version.

Removed concepts:

- `term`
- `language`
- `qa`

The deck is now defined by:

- its source mode
- its deck metadata
- its shared field layout
- its actual card rows

This keeps the deck contract simpler and makes the layout system easier to understand.

## Impact On Existing Files

These files will need coordinated updates:

- `skill/anki-card-creator/SKILL.md`
- `skill/anki-card-creator/references/markdown-spec.md`
- `skill/anki-card-creator/references/precise-card-rules.md`
- `skill/anki-card-creator/references/layout-preview.md` (new)
- `skill/anki-card-creator/assets/deck-spec-template.md`
- `skill/anki-card-creator/tests/acceptance-checklist.md`
- `mcp/src/anki_card_creator_mcp/models.py`
- `mcp/src/anki_card_creator_mcp/markdown_parser.py`
- `mcp/src/anki_card_creator_mcp/validators.py`
- `mcp/src/anki_card_creator_mcp/card_models.py`
- `mcp/src/anki_card_creator_mcp/apkg_builder.py`
- `mcp/src/anki_card_creator_mcp/service.py`
- relevant fixtures and tests in `mcp/tests/`

## Non-Goals

This redesign does not introduce:

- per-card layout overrides
- freeform template DSLs
- user-defined field ordering beyond the layout lists
- user-defined marker configuration for `extra`

The goal is a simpler, clearer deck-level layout contract, not a full template engine.

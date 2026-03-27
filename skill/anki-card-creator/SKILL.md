---
name: anki-card-creator
description: Use when creating Anki decks from a topic/domain or from source text, especially when Codex should draft an editable Markdown deck spec, explain the card layout, and only generate an .apkg after explicit user approval.
---

# Anki Card Creator

## Overview

Create Anki decks through a review-first workflow. Draft a fixed-format `deck-spec.md`, show the layout inline so the user can see how fields map to card sides, let the user edit the Markdown, and package via MCP once the user signals readiness.

## Required Inputs

Before drafting cards, confirm these values with the user:

- `deck_name`
- `source_mode`: `domain` or `extract` (infer from the request when obvious)

Do not ask for `card_type` or `style_profile` - these concepts no longer exist.

## Entry Modes

Support exactly two entry modes:

1. `domain`
The user gives a subject area. Generate a candidate vocabulary or concept set for that domain.

2. `extract`
The user provides source text. Extract candidate vocabulary or question-answer items from that text.

## Required Workflow

Follow this exact order:

1. Identify whether the request is `domain` or `extract`.
2. Infer `deck_name` from the request; confirm only if genuinely ambiguous.
3. Draft a fixed-format Markdown deck spec using the default layout. Show the ASCII layout preview from [references/layout-preview.md](references/layout-preview.md) above the fenced spec block so the user can see how fields map to card sides before editing.
4. Present the Markdown deck spec as the editable source of truth. The layout is visible in `## Card Layout` — users can move fields by editing those lines directly.
5. Let the user revise metadata, layout, and card rows directly in Markdown.
6. Once the user signals readiness — explicitly ("package it", "generate", "go ahead") or contextually ("looks good", "that's fine") — re-read the current Markdown deck spec and route packaging through MCP if available, otherwise through the CLI fallback skill.

Never skip the Markdown review phase. Never generate the `.apkg` from hidden intermediate state.

## Layout Presentation

When drafting the deck spec, show the ASCII layout preview from [references/layout-preview.md](references/layout-preview.md) above the fenced Markdown block. Do not ask a separate confirmation question about the layout. Users who want a different layout can edit `front_layout` and `back_layout` directly in `## Card Layout`.

Default field lists:

- Front: context, prompt, example
- Back: answer, extra

If the user requests a layout change during conversation, update `front_layout` and `back_layout` accordingly. Valid field names are: `prompt`, `answer`, `context`, `example`, `extra`. A field may only appear on one side.

## Markdown Contract

Use the fixed layout described in [references/markdown-spec.md](references/markdown-spec.md).

For user-facing drafting, start from [assets/deck-spec-template.md](assets/deck-spec-template.md) and fill it in. Keep the section order and card-table headers unchanged.

The Markdown deck spec is the single source of truth:

- the user edits it directly
- you read it when continuing the workflow
- the MCP packages only from it

## Card Quality Rules

Apply the precise-card rules summarized in [references/precise-card-rules.md](references/precise-card-rules.md).

When drafting or revising cards:

- keep one card focused on one knowledge point
- prefer prompts with one intended answer
- avoid "give an example" prompts unless rewritten into recognition form
- avoid list-enumeration prompts
- avoid yes-no prompts when a more informative prompt is available
- include enough context so the prompt makes sense in isolation
- rewrite or split ambiguous cards before packaging

If a candidate card violates these rules, fix it before calling the MCP.

## Card Table Guidance

Each row in `## Cards` is one card. Use one shared table for all content types:

- for terms: `prompt` is the term or question, `answer` is the definition
- for language: `prompt` is the word or phrase, `answer` is the meaning
- for QA: `prompt` is the question, `answer` is the answer

Use `context`, `example`, `extra`, and `tags` only when they add signal.

If the user wants to remove a card, delete the row. There is no enabled/disabled flag.

## Packaging Handoff

Once the user signals readiness, re-read the current Markdown deck spec and call `mcp__ankiCardCreator__build_apkg_from_spec` with:

- path to the Markdown deck spec
- optional output directory if the user requests a specific location

If the MCP tool is not available in the current session, tell the user that the MCP server needs to be registered before packaging can proceed.

If validation fails, surface the returned errors to the user and continue editing the Markdown spec instead of trying to guess a fix silently.

## Output Discipline

When presenting the drafted deck:

- preserve the exact Markdown structure
- avoid extra prose inside the deck spec itself
- keep comments or guidance outside the fenced Markdown block when possible
- if the user revises the Markdown, work from the revised version instead of regenerating from scratch unless asked

## References

- Use [references/layout-preview.md](references/layout-preview.md) for the ASCII layout preview and layout rules.
- Use [references/markdown-spec.md](references/markdown-spec.md) for the exact Markdown structure.
- Use [references/precise-card-rules.md](references/precise-card-rules.md) for card drafting constraints.

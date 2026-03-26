---
name: anki-card-creator
description: Use when creating Anki decks from a topic/domain or from source text, especially when Codex should draft an editable Markdown deck spec, enforce precise-card rules, and only generate an .apkg after explicit user approval.
---

# Anki Card Creator

## Overview

Create Anki decks through a review-first workflow. Gather the required card settings, draft a fixed-format `deck-spec.md`, let the user edit that Markdown, and only then call the packaging MCP to generate an `.apkg`.

## Required Inputs

Before drafting cards, confirm these values with the user:

- `card_type`: `term`, `language`, or `qa`
- `deck_name`
- `style_profile`: `concise`, `exam`, `example-rich`, or `mnemonic`

Do not skip this clarification step. If one of these fields is missing, ask for it.

## Entry Modes

Support exactly two entry modes:

1. `domain`
The user gives a subject area. Generate a candidate vocabulary or concept set for that domain.

2. `extract`
The user provides source text. Extract candidate vocabulary or question-answer items from that text.

## Required Workflow

Follow this exact order:

1. Identify whether the request is `domain` or `extract`.
2. Gather any missing required inputs.
3. Draft a fixed-format Markdown deck spec.
4. Show the Markdown deck spec to the user as the editable source of truth.
5. Let the user revise metadata and card rows directly in Markdown.
6. Re-read the current Markdown deck spec.
7. Ask for explicit approval to generate the final deck.
8. Only after approval, call the MCP tool that validates the spec and writes the `.apkg`.

Never skip the Markdown review phase. Never generate the `.apkg` from hidden intermediate state.

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

Each row in `## Cards` is one card. The first version uses one shared table for all card types:

- `term`: `front` is the term or its prompt, `back` is the definition/explanation
- `language`: `front` is the word/phrase, `back` is the meaning/translation
- `qa`: `front` is the question, `back` is the answer

Use `context`, `example`, `extra`, and `tags` only when they add signal.

If the user wants to remove a card, delete the row. There is no enabled/disabled flag.

## MCP Handoff

Once the user approves the current Markdown deck spec, call the MCP tool that validates and packages the deck.

The MCP input should be:

- path to the Markdown deck spec
- optional output directory if the user requests a specific location

If validation fails, surface the returned errors to the user and continue editing the Markdown spec instead of trying to guess a fix silently.

## Output Discipline

When presenting the drafted deck:

- preserve the exact Markdown structure
- avoid extra prose inside the deck spec itself
- keep comments or guidance outside the fenced Markdown block when possible
- if the user revises the Markdown, work from the revised version instead of regenerating from scratch unless asked

## References

- Use [references/markdown-spec.md](references/markdown-spec.md) for the exact Markdown structure.
- Use [references/precise-card-rules.md](references/precise-card-rules.md) for card drafting constraints derived from the approved article.

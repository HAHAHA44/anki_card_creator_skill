---
name: anki-card-creator
description: Use when creating Anki decks from a topic/domain or from source text, especially for editable review-first deck drafting and bilingual study decks that need sensible default field direction.
---

# Anki Card Creator

## Overview

Create Anki decks through a review-first workflow. Draft or continue a fixed-format `deck-spec.md`, show the layout inline so the user can see how fields map to card sides, lock the card field convention with 3-5 sample rows, let the user edit the Markdown, and package via MCP once the user signals readiness.

For clear Chinese-English bilingual requests, default immediately to an English-front / Chinese-back convention with richer study fields:

- `prompt`: English term or phrase
- `answer`: Chinese equivalent
- `example`: original English usage sentence
- `extra`: Chinese explanatory note

Show sample rows in that format directly. Do not ask a separate preliminary question just to decide front/back language direction when the bilingual intent is already clear.

## Required Inputs

Before drafting cards, infer these values from the request:

- `deck_name`
- `source_mode`: `domain` or `extract` (infer from the request when obvious)

Only confirm `deck_name` if it is genuinely ambiguous.

## Entry Modes

Support exactly two entry modes:

1. `domain`
The user gives a subject area. Generate a candidate vocabulary or concept set for that domain.

2. `extract`
The user provides source text. Extract candidate vocabulary or question-answer items from that text.

If the provided source is already a Markdown deck spec file that matches the deck-spec contract, still treat it as `extract`. In that case:

- detect that the input is already a spec file
- read that spec instead of regenerating hidden intermediate state
- continue the normal review-first workflow from the current spec
- keep the current spec as the single source of truth

## Bilingual Default Detection

Treat the request as a Chinese-English bilingual deck when one or more of these signals are present:

- the user explicitly says bilingual, Chinese-English, English-Chinese, 中英双语, 中英对照, 英文在前, 中文在后, translation, terminology reference, or vocabulary handbook
- the source contains repeated Chinese/English term pairs
- the task is clearly to learn or review cross-language terminology rather than open-ended QA

When bilingual mode is active:

- default to `prompt = English` and `answer = Chinese`
- default to `example = English sentence`
- default to `extra = Chinese note`
- show sample rows directly in that format
- do not ask a separate front/back language-direction question before showing examples unless the user gave conflicting signals

When the request is not clearly bilingual:

- infer the most sensible direction from the content
- keep one deck-wide language convention
- never let front/back languages cross unpredictably across rows

## Required Workflow

Follow this exact order:

1. Identify whether the request is `domain` or `extract`.
2. Infer `deck_name` from the request; confirm only if genuinely ambiguous.
3. Decide whether bilingual default mode applies.
4. Establish the card field convention before full-spec drafting. Show 3-5 representative sample rows using the same column structure as `## Cards`, and make sure each column is vertically consistent across the examples.
5. If bilingual default mode applies, present those rows directly using English `prompt`, Chinese `answer`, English `example`, and Chinese `extra` without first asking a separate language-direction question.
6. Let the user revise the sample rows if desired. If the user does not object, treat those rows as the working convention.
7. Lock the convention from those examples and generate or continue the fixed-format Markdown deck spec using that convention. Show the ASCII layout preview from [references/layout-preview.md](references/layout-preview.md) above the fenced spec block so the user can see how fields map to card sides before editing.
8. Perform a consistency pass on the generated spec before presenting it: confirm every card follows the agreed example convention, especially that `prompt` and `answer` are directionally consistent across all rows.
9. Present the Markdown deck spec as the editable source of truth. The layout is visible in `## Card Layout` - users can move fields by editing those lines directly.
10. Let the user revise metadata, layout, and card rows directly in Markdown.
11. Once the user signals readiness - explicitly ("package it", "generate", "go ahead") or contextually ("looks good", "that's fine") - re-read the current Markdown deck spec and run `~/.anki-card-creator/bin/build-apkg` via the Bash tool.

Never skip the Markdown review phase. Never generate the `.apkg` from hidden intermediate state.
Never skip the example-confirmation step before drafting a new full spec from extracted content.
Never ask an unnecessary preliminary direction-setting question when bilingual default mode already determines the convention.

## Layout Presentation

When drafting the deck spec, show the ASCII layout preview from [references/layout-preview.md](references/layout-preview.md) above the fenced Markdown block. Do not ask a separate confirmation question about the layout. Users who want a different layout can edit `front_layout` and `back_layout` directly in `## Card Layout`.

Default field lists:

- Front: context, prompt, example
- Back: answer, extra

If the user requests a layout change during conversation, update `front_layout` and `back_layout` accordingly. Valid field names are: `prompt`, `answer`, `context`, `example`, `extra`. A field may only appear on one side.

For bilingual default decks, the semantic default is:

- front content centers on English recognition (`prompt` and `example`)
- back content centers on Chinese understanding (`answer` and `extra`)

## Markdown Contract

Use the fixed layout described in [references/markdown-spec.md](references/markdown-spec.md).

For user-facing drafting, start from [assets/deck-spec-template.md](assets/deck-spec-template.md) and fill it in. Keep the section order and card-table headers unchanged.

The Markdown deck spec is the single source of truth:

- the user edits it directly
- you read it when continuing the workflow
- the packager reads only from it

If the user provides an existing deck spec file, that file becomes the starting source of truth immediately. Do not rewrite it from scratch unless the user asks.

## Example Convention Checkpoint

Before generating a new full spec from extracted content:

- show 3-5 sample rows using the same columns and order as `## Cards`
- use representative rows, not placeholders
- make the examples vertically consistent by column
- explicitly sanity-check column direction, such as whether `prompt` is always English and `answer` is always Chinese
- for bilingual default decks, also keep `example` as English and `extra` as Chinese
- present the default rows first when the direction is already clear; do not ask a separate direction-setting question before showing them
- let the user revise the sample rows in conversation before drafting the full spec

Treat the approved sample rows as the output contract for the full spec:

- all later rows must follow the same field direction and content pattern
- do not flip `prompt` and `answer` in later rows
- do not flip the language roles of `example` and `extra` in later rows when those columns are part of the convention
- do not mix multiple conventions in one deck unless the user explicitly requests it
- if the user changes the examples, regenerate or revise the spec to match the updated convention

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
- for bilingual study decks, make `example` and `extra` teach the term rather than merely restate it

If a candidate card violates these rules, fix it before packaging.

## Card Table Guidance

Each row in `## Cards` is one card. Use one shared table for all content types:

- for terms: `prompt` is the term or question, `answer` is the definition
- for language: `prompt` is the word or phrase, `answer` is the meaning
- for QA: `prompt` is the question, `answer` is the answer

Use `context`, `example`, `extra`, and `tags` only when they add signal.

For Chinese-English bilingual decks, the default interpretation is:

- `prompt`: English term or phrase
- `answer`: Chinese equivalent
- `example`: English sentence that demonstrates realistic usage
- `extra`: Chinese explanation of meaning, workflow usage, or distinctions

For non-bilingual decks, infer the most sensible mapping from the source, but keep one consistent front/back language convention throughout the deck.

If the user wants to remove a card, delete the row. There is no enabled/disabled flag.

When examples establish a language direction or mapping convention, preserve that convention for every row in the table.
Never alternate front/back languages across rows unless the user explicitly asks for a mixed-direction deck.

## Consistency Check

After generating or revising the spec, run a self-check before presenting completion or packaging:

- confirm all `prompt` values follow the same agreed direction and format
- confirm all `answer` values follow the same agreed direction and format
- confirm `example` and `extra` follow the agreed language roles when they are part of the convention
- confirm `prompt` and `answer` stay aligned with the approved sample-row convention
- confirm front/back languages do not cross unpredictably across rows
- fix mismatched rows before presenting the spec as ready

If the deck intentionally mixes conventions, state that explicitly and tie each variation back to the user's instruction.

## Packaging Handoff

Once the user signals readiness, re-read the current Markdown deck spec and use the Bash tool to run:

```bash
~/.anki-card-creator/bin/build-apkg <spec_path> [--output-dir <dir>]
```

The command writes JSON to stdout: `{"ok": true|false, "errors": [...], "output_path": "..."}`.

- On success (`ok: true`): report the output path to the user.
- On failure (`ok: false`): surface the `errors` list to the user and continue editing the Markdown spec. Do not attempt to guess a fix silently.
- If `~/.anki-card-creator/bin/build-apkg` is not found: tell the user to run `bash install.sh` from the skill repository first.

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

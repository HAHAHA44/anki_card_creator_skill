---
title: Anki Card Creator Skill Design
date: 2026-03-26
status: draft
---

# Anki Card Creator Skill Design

## Goal

Build a hybrid Anki card generation system with two coordinated parts:

1. A Codex skill that interacts with the user, drafts cards, applies card-quality rules, and produces a fixed Markdown specification.
2. An MCP service that validates the Markdown specification and generates an `.apkg` package through `genanki`.

The Markdown spec is the single source of truth between user review and package generation.

## User-Facing Workflow

### Entry Modes

The skill supports exactly two entry modes:

1. `domain`
The user gives a topic or domain. The skill proposes a vocabulary or concept set for that domain.

2. `extract`
The user provides source content. The skill extracts vocabulary or question-answer candidates from that content.

### Required Clarification Step

Before drafting cards, the skill must explicitly confirm:

- `card_type`: one of `term`, `language`, or `qa`
- `deck_name`
- `style_profile`

If any of these values are missing, the skill must ask the user and wait for an answer before continuing.

### Draft-Review-Generate Flow

The skill follows this fixed process:

1. Receive `domain` or `extract` input.
2. Clarify the required deck attributes.
3. Generate `deck-spec.md`.
4. Present the Markdown spec to the user as the editable review artifact.
5. Let the user modify metadata and cards.
6. Re-read the updated Markdown spec.
7. Call the MCP only after the user explicitly approves the current Markdown spec for generation.
8. MCP validates the spec and outputs `.apkg`.

The skill must not skip the Markdown review phase.

## System Architecture

### Hybrid Boundary

The recommended architecture is hybrid:

- The skill owns conversation, card drafting, user collaboration, and card-quality enforcement.
- The MCP owns structured validation and `.apkg` generation.

This keeps creative work and deterministic packaging separate.

### Responsibility Split

#### Skill Responsibilities

- detect which entry mode applies
- ask for missing required attributes
- generate candidate cards
- enforce precise-card design rules before proposing cards
- produce the fixed Markdown spec
- help the user revise the Markdown spec
- call the MCP once the spec is approved

#### MCP Responsibilities

- parse the Markdown spec
- validate required sections and column structure
- validate card rows
- map validated rows to `genanki` note objects
- emit a final `.apkg` file
- return clear errors when the Markdown spec is invalid

### Single Source of Truth

The Markdown spec is the only authoritative input for packaging.

- Users edit the Markdown file directly.
- The skill reads from the Markdown file when continuing the workflow.
- The MCP generates the deck only from the Markdown file.

No hidden state should exist outside the spec once the draft is created.

## Markdown Contract

The intermediate document is a fixed-format file, initially named `deck-spec.md`.

### Section Layout

The file contains these sections in order:

1. `# Anki Deck Spec`
2. `## Deck Metadata`
3. `## Card Policy`
4. `## Field Schema`
5. `## Cards`

### Minimal Metadata

Only the following top-level metadata is required in the first version:

```md
## Deck Metadata
- deck_name: ...
- source_mode: domain | extract
- card_type: term | language | qa
- output_file: ...
```

### Card Policy

The first version keeps policy minimal:

```md
## Card Policy
- style_profile: concise | exam | example-rich | mnemonic
- strict_precise_mode: true
- generation_notes: ...
```

Most generation rules stay implicit in the skill rather than expanding metadata.

### Field Schema

The schema section documents the stable card columns used by both the skill and the MCP.

```md
## Field Schema
| field | required | description |
| --- | --- | --- |
| id | yes | Stable card id |
| note_type | yes | term/language/qa |
| front | yes | Front side text |
| back | yes | Back side text |
| context | no | Topic cue shown with front |
| example | no | Example sentence or use case |
| extra | no | Additional explanation |
| tags | no | Comma-separated tags |
```

### Cards Table

The `## Cards` section stores one card per row:

```md
## Cards
| id | note_type | front | back | context | example | extra | tags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | term | ... | ... | ... | ... | ... | ... |
```

### Editing Rules

- The user may edit any metadata value.
- The user may revise any card row.
- To remove a card, the user deletes the row directly.
- `note_type` must stay within `term`, `language`, or `qa`.
- The MCP reads card content only from the rows in the `## Cards` table.

## Card-Type Behavior

The first version uses one shared table for all card types.

### `term`

- `front`: term prompt or term itself
- `back`: definition or explanation

### `language`

- `front`: word or phrase
- `back`: meaning or translation
- `example`: commonly used

### `qa`

- `front`: question
- `back`: answer
- `context`: strongly recommended

This avoids separate Markdown grammars in the first version while still supporting three user-selected card styles.

## Precise Card Rules

The skill must apply card design rules based on Soren Bjornstad's article "Rules for Designing Precise Anki Cards":

https://controlaltbackspace.org/precise/

The first version should treat these as default generation rules:

1. One card tests one thing.
2. Each prompt should lead to one intended answer.
3. Avoid prompts that ask for examples unless the example is inverted into a recognition-style card.
4. Avoid prompts that ask the learner to enumerate a list.
5. Avoid yes-no prompts when a more informative prompt can be created.
6. Include enough context in the front side so the question is understandable in isolation.
7. If a draft card is ambiguous, rewrite or split it before packaging.

The skill should prefer rewriting bad cards during drafting instead of passing low-quality cards through to packaging.

## MCP Interface

### Input

The MCP should accept at least one operation that takes:

- path to a Markdown deck spec
- optional output directory

### Output

The MCP returns:

- success flag
- generated `.apkg` path on success
- validation errors on failure

### Validation Expectations

The MCP validates:

- required sections exist
- metadata keys exist
- `## Cards` table headers match the expected schema
- each card row has required values
- `note_type` values are valid
- output filename is safe and writable

Validation errors should point to the broken section or row when possible.

## Proposed Project Layout

The repository should evolve toward this structure:

```text
anki-card-creator-skill/
  skill/
    SKILL.md
    agents/
      openai.yaml
    references/
      precise-card-rules.md
      markdown-spec.md
  mcp/
    pyproject.toml
    src/
      anki_card_creator_mcp/
        __init__.py
        server.py
        markdown_parser.py
        validators.py
        apkg_builder.py
  docs/
    superpowers/
      specs/
        2026-03-26-anki-card-creator-design.md
```

The exact naming can change during implementation, but the split between `skill/` and `mcp/` should remain.

## Non-Goals for Version 1

The first version should not try to solve all advanced Anki workflows.

Out of scope initially:

- multiple unrelated note models
- media packaging
- pronunciation audio generation
- image occlusion
- multiple deck outputs from one Markdown spec
- fully automatic generation without user review

## Implementation Guidance

Implementation should prioritize:

1. a stable Markdown contract
2. deterministic validation
3. clean error reporting
4. simple `genanki` integration
5. a skill flow that forces explicit user confirmation before packaging

The first version should optimize for correctness and editability, not maximum feature count.

# Markdown Deck Spec

Use this exact section order:

1. `# Anki Deck Spec`
2. `## Deck Metadata`
3. `## Card Policy`
4. `## Field Schema`
5. `## Cards`

## Required Metadata

```md
## Deck Metadata
- deck_name: ...
- source_mode: domain | extract
- card_type: term | language | qa
- output_file: ...
```

## Card Policy

```md
## Card Policy
- style_profile: concise | exam | example-rich | mnemonic
- strict_precise_mode: true
- generation_notes: ...
```

## Field Schema

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

## Cards Table

```md
## Cards
| id | note_type | front | back | context | example | extra | tags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | term | What organelle produces ATP in eukaryotic cells? | Mitochondria. | Biology: Cells |  | Main site of aerobic respiration. | biology,cell |
```

## Notes

- Delete a row to remove a card.
- Do not invent extra columns.
- Keep `note_type` aligned with the deck-level `card_type`.
- The MCP packages only from the rows in `## Cards`.

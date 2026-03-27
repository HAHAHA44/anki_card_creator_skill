# Markdown Deck Spec

Use this exact section order:

1. `# Anki Deck Spec`
2. `## Deck Metadata`
3. `## Card Layout`
4. `## Cards`

## Required Metadata

```md
## Deck Metadata
- deck_name: ...
- source_mode: domain | extract
- output_file: ...
```

## Card Layout

```md
## Card Layout
- front_layout: context, prompt, example
- back_layout: answer, extra
```

`front_layout` and `back_layout` are comma-separated lists of field names. Valid fields: `prompt`, `answer`, `context`, `example`, `extra`. A field may only appear on one side.

## Cards Table

```md
## Cards
| id | prompt | answer | context | example | extra | tags |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | What organelle produces ATP in eukaryotic cells? | Mitochondria. | Biology: Cells | ATP production happens here. | Main site of aerobic respiration. | biology,cell |
```

## Notes

- Delete a row to remove a card.
- Do not invent extra columns.
- The `extra` field renders with a `※` prefix wherever it appears.
- The MCP packages only from the rows in `## Cards`.

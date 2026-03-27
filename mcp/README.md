# anki-card-creator-mcp

MCP server and CLI for generating Anki `.apkg` files from a structured deck spec.

## Installation

```bash
pip install anki-card-creator-mcp
```

Or with `uv`:

```bash
uv add anki-card-creator-mcp
```

## MCP Registration

After installation, register the server with Claude:

```bash
claude mcp add anki-card-creator -- uvx anki-card-creator-mcp
```

This exposes two tools in Claude:

| Tool | Input | Description |
|------|-------|-------------|
| `build_apkg_from_spec` | path to a Markdown deck spec file | Parse, validate, and package |
| `build_apkg_from_json` | deck spec as a JSON object | Validate and package without a file |

## CLI Usage

```bash
anki-card-creator-mcp path/to/deck-spec.md
anki-card-creator-mcp path/to/deck-spec.md --output-dir ~/Anki
```

## Deck Spec Format

```markdown
# Anki Deck Spec

## Deck Metadata
- deck_name: My Deck
- source_mode: domain
- output_file: my-deck.apkg

## Card Layout
- front_layout: context, prompt, example
- back_layout: answer, extra

## Cards
| id | prompt | answer | context | example | extra | tags |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | What is X? | Y. | Topic | X appears when... | See also Z. | tag1,tag2 |
```

Valid layout fields: `prompt`, `answer`, `context`, `example`, `extra`.

## JSON Input Format

```json
{
  "deck_name": "My Deck",
  "source_mode": "domain",
  "output_file": "my-deck.apkg",
  "front_layout": ["context", "prompt", "example"],
  "back_layout": ["answer", "extra"],
  "cards": [
    {
      "id": "1",
      "prompt": "What is X?",
      "answer": "Y.",
      "context": "Topic",
      "example": "",
      "extra": "",
      "tags": "tag1,tag2"
    }
  ]
}
```

## License

MIT

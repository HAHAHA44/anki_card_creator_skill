from pathlib import Path

from anki_card_creator_mcp.models import CardRow, DeckSpec


REQUIRED_HEADINGS = (
    "## Deck Metadata",
    "## Card Layout",
    "## Cards",
)


def parse_deck_spec(path: Path) -> DeckSpec:
    lines = path.read_text(encoding="utf-8").splitlines()
    sections = _split_sections(lines)

    metadata = _parse_key_value_bullets(sections["## Deck Metadata"])
    layout = _parse_key_value_bullets(sections["## Card Layout"])
    cards = _parse_cards_table(sections["## Cards"])

    front_layout = [f.strip() for f in layout.get("front_layout", "").split(",") if f.strip()]
    back_layout = [f.strip() for f in layout.get("back_layout", "").split(",") if f.strip()]

    return DeckSpec(
        deck_name=metadata["deck_name"],
        source_mode=metadata["source_mode"],
        output_file=metadata["output_file"],
        front_layout=front_layout,
        back_layout=back_layout,
        cards=cards,
    )


def _split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None

    for line in lines:
        if line in REQUIRED_HEADINGS:
            current_heading = line
            sections[current_heading] = []
            continue
        if current_heading is not None:
            sections[current_heading].append(line)

    missing = [heading for heading in REQUIRED_HEADINGS if heading not in sections]
    if missing:
        raise ValueError(f"Missing required sections: {', '.join(missing)}")

    return sections


def _parse_key_value_bullets(lines: list[str]) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw_line in lines:
        line = raw_line.strip()
        if not line or not line.startswith("- "):
            continue
        key, value = line[2:].split(":", 1)
        data[key.strip()] = value.strip()
    return data


def _parse_cards_table(lines: list[str]) -> list[CardRow]:
    table_lines = [line.strip() for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return []

    headers = _split_table_row(table_lines[0])
    cards: list[CardRow] = []

    for row_line in table_lines[2:]:
        values = _split_table_row(row_line)
        row = dict(zip(headers, values, strict=False))
        cards.append(
            CardRow(
                id=row.get("id", ""),
                prompt=row.get("prompt", ""),
                answer=row.get("answer", ""),
                context=row.get("context", ""),
                example=row.get("example", ""),
                extra=row.get("extra", ""),
                tags=row.get("tags", ""),
            )
        )

    return cards


def _split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip("|").split("|")]

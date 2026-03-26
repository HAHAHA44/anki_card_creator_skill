from pathlib import Path

from anki_card_creator_mcp.models import CardRow, DeckSpec


REQUIRED_HEADINGS = (
    "## Deck Metadata",
    "## Card Policy",
    "## Field Schema",
    "## Cards",
)


def parse_deck_spec(path: Path) -> DeckSpec:
    lines = path.read_text(encoding="utf-8").splitlines()
    sections = _split_sections(lines)

    metadata = _parse_key_value_bullets(sections["## Deck Metadata"])
    policy = _parse_key_value_bullets(sections["## Card Policy"])
    cards = _parse_cards_table(sections["## Cards"])

    return DeckSpec(
        deck_name=metadata["deck_name"],
        source_mode=metadata["source_mode"],
        card_type=metadata["card_type"],
        output_file=metadata["output_file"],
        style_profile=policy["style_profile"],
        strict_precise_mode=policy["strict_precise_mode"].lower() == "true",
        generation_notes=policy.get("generation_notes", ""),
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
                note_type=row.get("note_type", ""),
                front=row.get("front", ""),
                back=row.get("back", ""),
                context=row.get("context", ""),
                example=row.get("example", ""),
                extra=row.get("extra", ""),
                tags=row.get("tags", ""),
            )
        )

    return cards


def _split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip("|").split("|")]

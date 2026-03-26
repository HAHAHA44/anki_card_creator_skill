from pathlib import Path

from anki_card_creator_mcp.markdown_parser import parse_deck_spec


def test_parse_deck_metadata_and_cards() -> None:
    spec = parse_deck_spec(Path("mcp/tests/fixtures/minimal_deck_spec.md"))

    assert spec.deck_name == "Biology Basics"
    assert spec.source_mode == "domain"
    assert spec.output_file == "biology-basics.apkg"
    assert spec.front_layout == ["context", "front", "example"]
    assert spec.back_layout == ["back", "extra"]
    assert spec.cards[0].example == "ATP production happens here in most eukaryotic cells."

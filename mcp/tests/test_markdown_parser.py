from pathlib import Path

from anki_card_creator_mcp.markdown_parser import parse_deck_spec


def test_parse_deck_metadata_and_cards() -> None:
    spec = parse_deck_spec(Path("mcp/tests/fixtures/minimal_deck_spec.md"))

    assert spec.deck_name == "Biology Basics"
    assert spec.source_mode == "domain"
    assert spec.card_type == "term"
    assert spec.output_file == "biology-basics.apkg"
    assert len(spec.cards) == 2
    assert spec.cards[0].front == "What organelle produces ATP in eukaryotic cells?"

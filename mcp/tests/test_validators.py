from anki_card_creator_mcp.models import CardRow, DeckSpec
from anki_card_creator_mcp.validators import validate_deck_spec


def make_spec(**overrides: object) -> DeckSpec:
    base = {
        "deck_name": "Biology Basics",
        "source_mode": "domain",
        "card_type": "term",
        "output_file": "biology-basics.apkg",
        "style_profile": "concise",
        "strict_precise_mode": True,
        "generation_notes": "",
        "cards": [CardRow(id="1", note_type="term", front="Q", back="A")],
    }
    base.update(overrides)
    return DeckSpec(**base)


def test_rejects_invalid_note_type() -> None:
    spec = make_spec(cards=[CardRow(id="1", note_type="bad", front="Q", back="A")])

    errors = validate_deck_spec(spec)

    assert errors == ["cards[0].note_type must be one of term, language, qa"]


def test_rejects_duplicate_card_ids() -> None:
    spec = make_spec(
        cards=[
            CardRow(id="1", note_type="term", front="Q1", back="A1"),
            CardRow(id="1", note_type="term", front="Q2", back="A2"),
        ]
    )

    errors = validate_deck_spec(spec)

    assert "cards ids must be unique" in errors


def test_rejects_non_apkg_output_file() -> None:
    spec = make_spec(output_file="biology-basics.txt")

    errors = validate_deck_spec(spec)

    assert "output_file must end with .apkg" in errors

from anki_card_creator_mcp.models import CardRow, DeckSpec
from anki_card_creator_mcp.validators import validate_deck_spec


def make_spec(**overrides: object) -> DeckSpec:
    base = {
        "deck_name": "Biology Basics",
        "source_mode": "domain",
        "output_file": "biology-basics.apkg",
        "front_layout": ["context", "front"],
        "back_layout": ["back", "extra"],
        "generation_notes": "",
        "cards": [CardRow(id="1", front="Q", back="A")],
    }
    base.update(overrides)
    return DeckSpec(**base)


def test_rejects_invalid_front_layout_field() -> None:
    spec = make_spec(front_layout=["context", "bad"], back_layout=["back", "extra"])

    errors = validate_deck_spec(spec)

    assert "front_layout contains unsupported field: bad" in errors


def test_rejects_duplicate_layout_field() -> None:
    spec = make_spec(front_layout=["context", "front"], back_layout=["context", "back"])

    errors = validate_deck_spec(spec)

    assert "field appears in both front_layout and back_layout: context" in errors


def test_rejects_empty_front_layout() -> None:
    spec = make_spec(front_layout=[])

    errors = validate_deck_spec(spec)

    assert "front_layout must not be empty" in errors


def test_rejects_non_apkg_output_file() -> None:
    spec = make_spec(output_file="biology-basics.txt")

    errors = validate_deck_spec(spec)

    assert "output_file must end with .apkg" in errors


def test_rejects_duplicate_card_ids() -> None:
    spec = make_spec(
        cards=[
            CardRow(id="1", front="Q1", back="A1"),
            CardRow(id="1", front="Q2", back="A2"),
        ]
    )

    errors = validate_deck_spec(spec)

    assert "cards ids must be unique" in errors

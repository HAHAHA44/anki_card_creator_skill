from models import CardRow, DeckSpec
from validators import validate_deck_spec


def make_spec(**overrides: object) -> DeckSpec:
    base = {
        "deck_name": "Biology Basics",
        "source_mode": "domain",
        "output_file": "biology-basics.apkg",
        "front_layout": ["context", "prompt"],
        "back_layout": ["answer", "extra"],
        "cards": [CardRow(id="1", prompt="Q", answer="A")],
    }
    base.update(overrides)
    return DeckSpec(**base)


def test_rejects_invalid_front_layout_field() -> None:
    spec = make_spec(front_layout=["context", "bad"], back_layout=["answer", "extra"])

    errors = validate_deck_spec(spec)

    assert "front_layout contains unsupported field: bad" in errors


def test_rejects_duplicate_layout_field() -> None:
    spec = make_spec(front_layout=["context", "prompt"], back_layout=["context", "answer"])

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
            CardRow(id="1", prompt="Q1", answer="A1"),
            CardRow(id="1", prompt="Q2", answer="A2"),
        ]
    )

    errors = validate_deck_spec(spec)

    assert "cards ids must be unique" in errors

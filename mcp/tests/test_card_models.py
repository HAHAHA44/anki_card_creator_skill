from anki_card_creator_mcp.card_models import get_note_model
from anki_card_creator_mcp.card_styles import get_style_css


def test_returns_css_for_example_rich_profile() -> None:
    css = get_style_css("example-rich")

    assert ".example-block" in css


def test_returns_qa_model() -> None:
    model = get_note_model("qa", "concise")

    assert model.name == "anki-card-creator-qa"
    assert [field["name"] for field in model.fields] == [
        "Front",
        "Back",
        "Context",
        "Example",
        "Extra",
    ]

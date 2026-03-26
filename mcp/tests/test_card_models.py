from anki_card_creator_mcp.card_models import get_note_model


def test_example_on_front_when_in_front_layout() -> None:
    model = get_note_model(
        front_layout=["context", "front", "example"],
        back_layout=["back", "extra"],
    )
    template = model.templates[0]

    assert "{{#Example}}" in template["qfmt"]


def test_extra_renders_with_marker_on_back() -> None:
    model = get_note_model(
        front_layout=["context", "front", "example"],
        back_layout=["back", "extra"],
    )
    template = model.templates[0]

    assert "※" in template["afmt"]


def test_field_names_unchanged() -> None:
    model = get_note_model(front_layout=["front"], back_layout=["back"])

    assert [field["name"] for field in model.fields] == [
        "Front",
        "Back",
        "Context",
        "Example",
        "Extra",
    ]


def test_answer_side_css_owns_separator_and_background_continuity() -> None:
    model = get_note_model(
        front_layout=["context", "front", "example", "extra"],
        back_layout=["back"],
    )

    assert "#answer {" in model.css
    assert "background-attachment: fixed;" in model.css

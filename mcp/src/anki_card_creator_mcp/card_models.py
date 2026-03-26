import genanki

from anki_card_creator_mcp.card_styles import get_style_css


MODEL_IDS = {
    "term": 1_400_001,
    "language": 1_400_002,
    "qa": 1_400_003,
}

MODEL_NAMES = {
    "term": "anki-card-creator-term",
    "language": "anki-card-creator-language",
    "qa": "anki-card-creator-qa",
}

MODEL_FIELDS = [
    {"name": "Front"},
    {"name": "Back"},
    {"name": "Context"},
    {"name": "Example"},
    {"name": "Extra"},
]

MODEL_TEMPLATES = [
    {
        "name": "Card 1",
        "qfmt": (
            "{{#Context}}<div class=\"context-block\">{{Context}}</div>{{/Context}}"
            "<div class=\"front-block\">{{Front}}</div>"
        ),
        "afmt": (
            "{{FrontSide}}"
            "<hr id=\"answer\">"
            "<div class=\"back-block\">{{Back}}</div>"
            "{{#Example}}<div class=\"example-block\">{{Example}}</div>{{/Example}}"
            "{{#Extra}}<div class=\"extra-block\">{{Extra}}</div>{{/Extra}}"
        ),
    }
]


def get_note_model(card_type: str, style_profile: str) -> genanki.Model:
    return genanki.Model(
        MODEL_IDS[card_type],
        MODEL_NAMES[card_type],
        fields=MODEL_FIELDS,
        templates=MODEL_TEMPLATES,
        css=get_style_css(style_profile),
    )

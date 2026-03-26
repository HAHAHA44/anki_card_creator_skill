from hashlib import sha1

import genanki


MODEL_FIELDS = [
    {"name": "Front"},
    {"name": "Back"},
    {"name": "Context"},
    {"name": "Example"},
    {"name": "Extra"},
]

FIELD_RENDERERS = {
    "front": '<div class="front-block">{{Front}}</div>',
    "back": '<div class="back-block">{{Back}}</div>',
    "context": '{{#Context}}<div class="context-block">{{Context}}</div>{{/Context}}',
    "example": '{{#Example}}<div class="example-block">{{Example}}</div>{{/Example}}',
    "extra": '{{#Extra}}<div class="extra-block">※ {{Extra}}</div>{{/Extra}}',
}

DEFAULT_CSS = """
.card { font-family: sans-serif; font-size: 16px; text-align: left; }
.context-block { color: #666; font-size: 0.85em; margin-bottom: 0.5em; }
.front-block { font-weight: bold; margin-bottom: 0.5em; }
.back-block { margin-top: 0.5em; }
.example-block { color: #444; font-style: italic; margin-top: 0.5em; }
.extra-block { color: #555; font-size: 0.9em; margin-top: 0.5em; }
"""


def get_note_model(front_layout: list[str], back_layout: list[str]) -> genanki.Model:
    model_id = _stable_model_id(front_layout, back_layout)
    qfmt = "".join(FIELD_RENDERERS[f] for f in front_layout if f in FIELD_RENDERERS)
    afmt = '{{FrontSide}}<hr id="answer">' + "".join(
        FIELD_RENDERERS[f] for f in back_layout if f in FIELD_RENDERERS
    )
    return genanki.Model(
        model_id,
        "anki-card-creator-custom",
        fields=MODEL_FIELDS,
        templates=[{"name": "Card 1", "qfmt": qfmt, "afmt": afmt}],
        css=DEFAULT_CSS,
    )


def _stable_model_id(front_layout: list[str], back_layout: list[str]) -> int:
    key = ",".join(front_layout) + "|" + ",".join(back_layout)
    digest = sha1(key.encode("utf-8")).hexdigest()[:10]
    return int(digest, 16)

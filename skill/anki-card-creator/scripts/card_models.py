from hashlib import sha1

import genanki


MODEL_FIELDS = [
    {"name": "Prompt"},
    {"name": "Answer"},
    {"name": "Context"},
    {"name": "Example"},
    {"name": "Extra"},
]

FIELD_RENDERERS = {
    "prompt": '<div class="prompt-block">{{Prompt}}</div>',
    "answer": '<div class="answer-block">{{Answer}}</div>',
    "context": '{{#Context}}<div class="context-block">{{Context}}</div>{{/Context}}',
    "example": '{{#Example}}<div class="example-block">{{Example}}</div>{{/Example}}',
    "extra": '{{#Extra}}<div class="extra-block">※ {{Extra}}</div>{{/Extra}}',
}

DEFAULT_CSS = """
.card {
  --card-bg: linear-gradient(180deg, #f4efe6 0%, #fcfaf6 100%);
  --card-surface: rgba(255, 255, 255, 0.84);
  --card-text: #18212f;
  --card-muted: #6b7280;
  --card-accent: #0f766e;
  --card-border: rgba(24, 33, 47, 0.08);
  font-family: Inter, "SF Pro Text", "Segoe UI", "PingFang SC", "Hiragino Sans",
    "Hiragino Kaku Gothic ProN", "Microsoft YaHei", "Noto Sans CJK SC",
    "Noto Sans CJK JP", "Yu Gothic UI", Meiryo, sans-serif;
  font-size: 18px;
  line-height: 1.65;
  text-align: left;
  color: var(--card-text);
  background-color: #fcfaf6;
  background-image: var(--card-bg);
  background-repeat: no-repeat;
  background-size: 100% 100%;
  background-attachment: fixed;
  max-width: 34rem;
  margin: 0 auto;
  padding: 24px 22px;
  border: 1px solid var(--card-border);
  border-radius: 20px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  box-sizing: border-box;
  min-height: 100vh;
}

.context-block {
  margin-bottom: 14px;
  color: var(--card-accent);
  font-size: 0.72em;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.prompt-block,
.answer-block,
.example-block,
.extra-block {
  margin-top: 0;
}

.prompt-block {
  margin-bottom: 12px;
  font-size: 1.32em;
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.02em;
}

.answer-block {
  margin-top: 18px;
  font-size: 1.02em;
}

#answer {
  border: 0;
  height: 1px;
  margin: 20px 0 0;
  background: linear-gradient(90deg, rgba(15, 118, 110, 0), rgba(15, 118, 110, 0.32), rgba(15, 118, 110, 0));
}

.example-block,
.extra-block {
  padding: 12px 14px;
  border-radius: 14px;
  background: var(--card-surface);
  border: 1px solid rgba(24, 33, 47, 0.06);
}

.example-block {
  margin-top: 16px;
  color: #334155;
  font-size: 0.94em;
  font-style: italic;
}

.extra-block {
  margin-top: 12px;
  color: var(--card-muted);
  font-size: 0.9em;
}

@media (max-width: 480px) {
  .card {
    font-size: 16px;
    padding: 18px 16px;
    border-radius: 16px;
  }

  .prompt-block {
    font-size: 1.2em;
  }
}
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

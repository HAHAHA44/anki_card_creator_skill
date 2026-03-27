BASE_CSS = """
.card {
  font-family: Arial, sans-serif;
  font-size: 20px;
  text-align: left;
  color: #1f2933;
  background: #f8fafc;
}

.context-block {
  color: #486581;
  font-size: 14px;
  margin-bottom: 10px;
  text-transform: uppercase;
}

.prompt-block,
.answer-block {
  margin: 12px 0;
}

.example-block,
.extra-block {
  margin-top: 14px;
  font-size: 16px;
  color: #334e68;
}
""".strip()


STYLE_OVERRIDES = {
    "concise": ".card { line-height: 1.4; }",
    "exam": ".card { line-height: 1.5; } .prompt-block { font-weight: 700; }",
    "example-rich": ".card { line-height: 1.6; } .example-block { border-top: 1px solid #bcccdc; padding-top: 10px; }",
    "mnemonic": ".card { line-height: 1.5; } .extra-block { font-style: italic; }",
}


def get_style_css(style_profile: str) -> str:
    return "\n\n".join([BASE_CSS, STYLE_OVERRIDES[style_profile]])

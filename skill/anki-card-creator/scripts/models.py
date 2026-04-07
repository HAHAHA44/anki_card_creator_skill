from dataclasses import dataclass


@dataclass
class CardRow:
    id: str
    prompt: str
    answer: str
    context: str = ""
    example: str = ""
    extra: str = ""
    tags: str = ""


@dataclass
class DeckSpec:
    deck_name: str
    source_mode: str
    output_file: str
    front_layout: list[str]
    back_layout: list[str]
    cards: list[CardRow]

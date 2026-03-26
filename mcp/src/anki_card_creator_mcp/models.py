from dataclasses import dataclass


@dataclass
class CardRow:
    id: str
    note_type: str
    front: str
    back: str
    context: str = ""
    example: str = ""
    extra: str = ""
    tags: str = ""


@dataclass
class DeckSpec:
    deck_name: str
    source_mode: str
    card_type: str
    output_file: str
    style_profile: str
    strict_precise_mode: bool
    generation_notes: str
    cards: list[CardRow]

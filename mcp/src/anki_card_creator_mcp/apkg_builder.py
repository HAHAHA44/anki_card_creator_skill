from hashlib import sha1
from pathlib import Path

import genanki

from anki_card_creator_mcp.card_models import get_note_model
from anki_card_creator_mcp.models import DeckSpec


def build_apkg(spec: DeckSpec, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    deck = genanki.Deck(_stable_deck_id(spec.deck_name), spec.deck_name)
    model = get_note_model(spec.card_type, spec.style_profile)

    for card in spec.cards:
        note = genanki.Note(
            model=model,
            fields=[
                card.front,
                card.back,
                card.context,
                card.example,
                card.extra,
            ],
            tags=_split_tags(card.tags),
        )
        deck.add_note(note)

    output_path = output_dir / spec.output_file
    genanki.Package(deck).write_to_file(output_path)
    return output_path


def _stable_deck_id(deck_name: str) -> int:
    digest = sha1(deck_name.encode("utf-8")).hexdigest()[:10]
    return int(digest, 16)


def _split_tags(tags: str) -> list[str]:
    return [tag.strip() for tag in tags.split(",") if tag.strip()]

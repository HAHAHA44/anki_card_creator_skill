from anki_card_creator_mcp.models import DeckSpec


VALID_SOURCE_MODES = {"domain", "extract"}
VALID_CARD_TYPES = {"term", "language", "qa"}
VALID_STYLE_PROFILES = {"concise", "exam", "example-rich", "mnemonic"}


def validate_deck_spec(spec: DeckSpec) -> list[str]:
    errors: list[str] = []

    if not spec.deck_name:
        errors.append("deck_name is required")
    if spec.source_mode not in VALID_SOURCE_MODES:
        errors.append("source_mode must be one of domain, extract")
    if spec.card_type not in VALID_CARD_TYPES:
        errors.append("card_type must be one of term, language, qa")
    if spec.style_profile not in VALID_STYLE_PROFILES:
        errors.append("style_profile must be one of concise, exam, example-rich, mnemonic")
    if not spec.output_file.endswith(".apkg"):
        errors.append("output_file must end with .apkg")

    seen_ids: set[str] = set()
    for index, card in enumerate(spec.cards):
        if not card.id:
            errors.append(f"cards[{index}].id is required")
        elif card.id in seen_ids:
            errors.append("cards ids must be unique")
        else:
            seen_ids.add(card.id)

        if card.note_type not in VALID_CARD_TYPES:
            errors.append(f"cards[{index}].note_type must be one of term, language, qa")
        elif card.note_type != spec.card_type:
            errors.append(f"cards[{index}].note_type must match deck card_type {spec.card_type}")

        if not card.front:
            errors.append(f"cards[{index}].front is required")
        if not card.back:
            errors.append(f"cards[{index}].back is required")

    return errors

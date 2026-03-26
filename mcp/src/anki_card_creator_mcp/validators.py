from anki_card_creator_mcp.models import DeckSpec


VALID_SOURCE_MODES = {"domain", "extract"}
VALID_LAYOUT_FIELDS = {"front", "back", "context", "example", "extra"}


def validate_deck_spec(spec: DeckSpec) -> list[str]:
    errors: list[str] = []

    if not spec.deck_name:
        errors.append("deck_name is required")
    if spec.source_mode not in VALID_SOURCE_MODES:
        errors.append("source_mode must be one of domain, extract")
    if not spec.output_file.endswith(".apkg"):
        errors.append("output_file must end with .apkg")

    if not spec.front_layout:
        errors.append("front_layout must not be empty")
    if not spec.back_layout:
        errors.append("back_layout must not be empty")

    for field in spec.front_layout:
        if field not in VALID_LAYOUT_FIELDS:
            errors.append(f"front_layout contains unsupported field: {field}")
    for field in spec.back_layout:
        if field not in VALID_LAYOUT_FIELDS:
            errors.append(f"back_layout contains unsupported field: {field}")

    duplicate_fields = set(spec.front_layout) & set(spec.back_layout)
    for field in sorted(duplicate_fields):
        errors.append(f"field appears in both front_layout and back_layout: {field}")

    seen_ids: set[str] = set()
    for index, card in enumerate(spec.cards):
        if not card.id:
            errors.append(f"cards[{index}].id is required")
        elif card.id in seen_ids:
            errors.append("cards ids must be unique")
        else:
            seen_ids.add(card.id)

        if not card.front:
            errors.append(f"cards[{index}].front is required")
        if not card.back:
            errors.append(f"cards[{index}].back is required")

    return errors

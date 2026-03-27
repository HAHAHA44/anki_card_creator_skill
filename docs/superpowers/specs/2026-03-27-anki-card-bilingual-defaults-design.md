# Anki Card Bilingual Defaults Design

## Goal

Update the `anki-card-creator` skill so bilingual Chinese-English requests no longer need an explicit direction-setting conversation before sample rows are shown.

## Approved Behavior

- If the user request clearly indicates a bilingual Chinese-English deck, the skill should default to:
  - `prompt`: English
  - `answer`: Chinese
  - `example`: English example sentence
  - `extra`: Chinese explanatory note
- The skill should show 3-5 sample rows in that format immediately instead of first asking which language belongs on the front.
- The user may still revise the sample rows or the final Markdown spec, but the default should be ready without extra dialogue.

## Scope Rules

- Apply the bilingual default only when the request or source clearly signals Chinese-English bilingual learning content.
- For non-bilingual requests, infer the most sensible direction from the provided content.
- In every case, keep one deck-wide language convention for `prompt` and `answer`.
- Do not allow front/back language direction to alternate across rows unless the user explicitly asks for a mixed deck.

## Field Defaults For Bilingual Decks

- `prompt`: English term or phrase
- `answer`: Chinese equivalent
- `example`: original English sentence that demonstrates realistic usage
- `extra`: Chinese note explaining the concept, typical workflow usage, or distinctions

## Documentation Updates Needed

- Update `skill/anki-card-creator/SKILL.md` to encode the bilingual trigger, default field mapping, and no-preliminary-direction-question behavior.
- Update `skill/anki-card-creator/tests/acceptance-checklist.md` to cover the new default behavior.
- Update `skill/anki-card-creator/assets/deck-spec-template.md` placeholders so the sample table hints at the richer `example` and `extra` defaults.

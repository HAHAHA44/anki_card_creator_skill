# Finance Middle Office Deck Enrichment Design

## Goal

Upgrade the finance middle office bilingual deck from a bare term-mapping deck into a study deck that teaches meaning and usage.

## Approved Direction

- `prompt`: English term
- `answer`: Chinese equivalent
- `example`: original English business sentence written from domain knowledge, not copied from the source document
- `extra`: Chinese note explaining what the term means, where it appears in the workflow, and any important distinctions

## Content Strategy

- Keep all existing cards and preserve the current prompt/answer direction.
- Use context-sensitive sentence templates so examples feel like real finance middle office work.
- Use context-sensitive Chinese notes so cards explain process relevance, not just literal translation.
- Preserve source remarks and source IDs by folding them into `extra` where helpful.
- Keep notes concise enough for Anki review, but rich enough to support recall.

## Exceptions

- If the source document does not provide a Chinese translation, keep the source abbreviation on the back and explicitly note that the source lacks an official Chinese rendering.
- Avoid list-style explanations and avoid copying source text verbatim into examples.

## Verification

- Spot-check representative cards across all major sections.
- Confirm every card has non-empty `example` and `extra`.
- Confirm the deck still matches the Markdown deck spec contract.

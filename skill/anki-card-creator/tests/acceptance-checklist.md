# Skill Acceptance Checklist

## RED Phase Baseline

Current baseline before writing the real skill:

- The repository did not contain a usable Anki skill.
- No workflow existed to force `card_type`, `deck_name`, and `style_profile`.
- No fixed `deck-spec.md` contract existed.
- No rule required explicit approval before `.apkg` generation.

Result: all acceptance scenarios failed before the skill was written.

## Acceptance Scenarios

### Scenario 1: Domain Input With Missing Card Type

Prompt pattern:

```text
Create an Anki deck about cell biology.
```

Expected skill behavior:

- [x] Detect `domain` mode
- [x] Ask for missing `card_type`
- [x] Ask for missing `deck_name` if not supplied
- [x] Ask for missing `style_profile`
- [x] Draft a fixed-format Markdown deck spec
- [x] Wait for user review before packaging

### Scenario 2: Extracted Text With QA Cards

Prompt pattern:

```text
Use this paragraph to make a QA deck: ...
```

Expected skill behavior:

- [x] Detect `extract` mode
- [x] Confirm or record `card_type=qa`
- [x] Confirm `deck_name`
- [x] Confirm `style_profile`
- [x] Extract question-answer pairs into the Markdown deck spec
- [x] Apply precise-card rules before packaging

### Scenario 3: User Tries To Skip Markdown Review

Prompt pattern:

```text
Just generate the apkg now.
```

Expected skill behavior:

- [x] Refuse to skip Markdown review
- [x] Show or reference the current Markdown deck spec
- [x] Ask for explicit approval of the current spec
- [x] Call the MCP only after approval

## GREEN Phase Manual Validation

Validation method:

- Read `SKILL.md`
- Read `references/markdown-spec.md`
- Read `references/precise-card-rules.md`
- Check each scenario against the documented workflow

Result:

- The written skill now satisfies all three acceptance scenarios.
- The exact Markdown review gate is documented.
- The MCP handoff is explicitly gated on user approval.

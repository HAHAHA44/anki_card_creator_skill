# Skill Acceptance Checklist

## RED Phase Baseline

Current baseline before the layout redesign:

- The skill still referenced `card_type`, `style_profile`, and `Card Policy`.
- No ASCII layout preview existed.
- Front/back field assignment was not user-configurable.
- The deck format included `note_type` per card row.

Result: all layout-focused scenarios failed before the redesign.

## Acceptance Scenarios

### Scenario 1: Domain Input Receives Default Layout Preview

Prompt pattern:

```text
Create an Anki deck about cell biology.
```

Expected skill behavior:

- [ ] Detect `domain` mode
- [ ] Ask for missing `deck_name` if not supplied
- [ ] Present the default ASCII layout preview from `references/layout-preview.md`
- [ ] Ask whether the user accepts the default layout or wants to change it
- [ ] Draft a fixed-format Markdown deck spec with `## Card Layout`
- [ ] Wait for user review before packaging

### Scenario 2: User Changes Front/Back Field Assignment

Prompt pattern:

```text
I want the example on the back, not the front.
```

Expected skill behavior:

- [ ] Identify the requested layout change
- [ ] Update `front_layout` and `back_layout` accordingly in the deck spec
- [ ] Show the revised `## Card Layout` section to the user
- [ ] Continue with the Markdown-first workflow

### Scenario 3: User Tries To Skip Markdown Review

Prompt pattern:

```text
Just generate the apkg now.
```

Expected skill behavior:

- [ ] Refuse to skip Markdown review
- [ ] Show or reference the current Markdown deck spec
- [ ] Ask for explicit approval of the current spec
- [ ] Call the MCP only after approval

## GREEN Phase Manual Validation

Validation method:

- Read `SKILL.md`
- Read `references/layout-preview.md`
- Read `references/markdown-spec.md`
- Check each scenario against the documented workflow

Result:

- The redesigned skill satisfies all three layout-focused acceptance scenarios.
- The ASCII layout preview is mandatory before drafting.
- User layout changes map to `front_layout`/`back_layout` in the deck spec.
- The MCP handoff is explicitly gated on user approval.

# Anki Card Bilingual Defaults Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Teach the `anki-card-creator` skill to default bilingual Chinese-English decks to English-front / Chinese-back with richer example and note fields.

**Architecture:** Update the skill document as the single behavior source, then align the acceptance checklist and template hints so the intended default behavior is visible, testable, and consistent.

**Tech Stack:** Markdown documentation, skill acceptance checklist

---

### Task 1: Record The Approved Rules

**Files:**
- Create: `docs/superpowers/specs/2026-03-27-anki-card-bilingual-defaults-design.md`
- Create: `docs/superpowers/plans/2026-03-27-anki-card-bilingual-defaults-implementation.md`

- [ ] Save the approved bilingual-default behavior in a short design doc.
- [ ] Save a focused implementation plan for the documentation update.

### Task 2: Update The Skill Document

**Files:**
- Modify: `skill/anki-card-creator/SKILL.md`

- [ ] Add bilingual-trigger rules.
- [ ] Add the default English-front / Chinese-back mapping for bilingual decks.
- [ ] State that sample rows should be shown directly without a preliminary direction-setting question.
- [ ] Require deck-wide language consistency for all generated rows.

### Task 3: Update Acceptance Coverage

**Files:**
- Modify: `skill/anki-card-creator/tests/acceptance-checklist.md`
- Modify: `skill/anki-card-creator/assets/deck-spec-template.md`

- [ ] Add acceptance scenarios for bilingual defaults and no-preliminary-direction-question behavior.
- [ ] Update template hints so `example` and `extra` reflect the richer default behavior.

### Task 4: Verify The New Rules

**Files:**
- Modify: `skill/anki-card-creator/SKILL.md`
- Modify: `skill/anki-card-creator/tests/acceptance-checklist.md`
- Modify: `skill/anki-card-creator/assets/deck-spec-template.md`

- [ ] Re-read the updated skill.
- [ ] Confirm the new bilingual default and consistency rules are explicitly documented.
- [ ] Summarize any remaining ambiguity.

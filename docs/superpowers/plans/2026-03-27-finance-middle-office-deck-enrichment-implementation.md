# Finance Middle Office Deck Enrichment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enrich the finance middle office deck with English example sentences and Chinese explanatory notes for every card.

**Architecture:** Read the existing Markdown deck spec, generate context-aware `example` and `extra` fields using section-specific heuristics plus domain-language templates, then rewrite the same spec with the enriched content and verify consistency by spot-checking representative rows.

**Tech Stack:** Markdown deck spec, Python bulk-edit script, Anki deck contract

---

### Task 1: Capture The Approved Enrichment Rules

**Files:**
- Create: `docs/superpowers/specs/2026-03-27-finance-middle-office-deck-enrichment-design.md`
- Create: `docs/superpowers/plans/2026-03-27-finance-middle-office-deck-enrichment-implementation.md`

- [ ] Record the approved field direction and enrichment rules.
- [ ] Keep the rules short and specific so the deck rewrite stays consistent.

### Task 2: Enrich The Deck Spec

**Files:**
- Modify: `finance-middle-office-en-front-zh-back-deck-spec.md`

- [ ] Read the current deck spec.
- [ ] Generate an English example sentence for every row based on term type and workflow context.
- [ ] Generate a Chinese explanatory note for every row based on meaning and workflow usage.
- [ ] Preserve prompt, answer, context, and tags.

### Task 3: Verify Consistency

**Files:**
- Modify: `finance-middle-office-en-front-zh-back-deck-spec.md`

- [ ] Confirm every card has non-empty `example` and `extra`.
- [ ] Spot-check representative rows from all major sections.
- [ ] Summarize any unavoidable exceptions from the source document.

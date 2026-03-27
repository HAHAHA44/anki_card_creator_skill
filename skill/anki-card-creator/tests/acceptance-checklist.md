# Skill Acceptance Checklist

## RED Phase Baseline

Current baseline before the sample-convention and spec-file-input update:

- The skill only describes `domain` and raw-text `extract` inputs.
- The skill does not say that an existing deck spec file can enter through `extract`.
- The skill drafts a full spec immediately instead of locking a 3-5 row example convention first.
- The skill does not require vertical consistency checks across sample rows.
- The skill does not require a post-generation consistency pass for all `prompt` and `answer` rows.

Result: all scenarios below fail against the previous version of `SKILL.md`.

## Acceptance Scenarios

### Scenario 1: Existing Spec File Enters Through Extract

Prompt pattern:

```text
Use this Markdown deck spec file and package it.
```

Expected skill behavior:

- [ ] Detect that the provided input is already a deck spec file
- [ ] Keep `source_mode` as `extract`
- [ ] Treat the provided spec as the current source of truth
- [ ] Continue the normal review-first workflow from that spec
- [ ] Do not regenerate the deck from hidden intermediate state

### Scenario 2: New Extract Flow Shows 3-5 Vertically Consistent Examples First

Prompt pattern:

```text
Extract cards from this source text and draft the deck.
```

Expected skill behavior:

- [ ] Show 3-5 representative sample rows before generating the full spec
- [ ] Use the same column order as `## Cards`
- [ ] Make the examples vertically consistent by field
- [ ] Explicitly sanity-check the direction of `prompt` and `answer`
- [ ] Let the user revise the examples in conversation

### Scenario 3: Approved Examples Become The Deck-Wide Contract

Prompt pattern:

```text
These examples look right. Continue.
```

Expected skill behavior:

- [ ] Treat the approved examples as the contract for later rows
- [ ] Keep `prompt` and `answer` aligned with the approved direction
- [ ] Avoid mixing multiple row conventions unless the user explicitly asks
- [ ] Revise or regenerate the full spec if the examples change

### Scenario 4: Full Spec Gets A Consistency Pass Before Presentation

Prompt pattern:

```text
Generate the full spec now.
```

Expected skill behavior:

- [ ] Check that all `prompt` rows follow the approved convention
- [ ] Check that all `answer` rows follow the approved convention
- [ ] Fix mismatched rows before presenting the generated spec
- [ ] State exceptions only when the user explicitly requested mixed conventions

### Scenario 5: Approved Deck Uses MCP When MCP Tool Is Available

Prompt pattern:

```text
The current Markdown deck spec is approved. Generate the final deck.
```

Expected skill behavior:

- [ ] Confirm the current Markdown deck spec is the approved source of truth
- [ ] Check whether `mcp__ankiCardCreator__build_apkg_from_spec` is available
- [ ] Call MCP when the tool is available
- [ ] Pass `spec_path` and optional `output_dir` to MCP
- [ ] Surface validation errors back into the Markdown editing loop if packaging fails

## GREEN Phase Manual Validation

Validation method:

- Read `SKILL.md`
- Check each scenario against the documented workflow
- Verify the workflow explicitly names the example-confirmation and consistency-check steps

Result:

- Pending validation after the `SKILL.md` update.

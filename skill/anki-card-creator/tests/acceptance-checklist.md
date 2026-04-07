# Skill Acceptance Checklist

## RED Phase Baseline

Current baseline before the bilingual-default update:

- The skill does not define a bilingual detection rule.
- The skill does not say that clear Chinese-English bilingual decks should default to English `prompt` and Chinese `answer`.
- The skill does not require bilingual sample rows to use English `example` and Chinese `extra`.
- The skill still implies a conversation checkpoint before the convention is locked, rather than showing the bilingual default rows immediately when intent is obvious.
- The skill does not explicitly forbid front/back language crossing in non-bilingual inference mode.

Result: all scenarios below fail against the previous version of `SKILL.md`.

## Acceptance Scenarios

### Scenario 1: Bilingual Request Defaults To English Front / Chinese Back

Prompt pattern:

```text
根据这个中英对照术语表生成 Anki 卡。
```

Expected skill behavior:

- [ ] Detect that the request is clearly Chinese-English bilingual
- [ ] Default `prompt` to English
- [ ] Default `answer` to Chinese
- [ ] Keep one deck-wide direction instead of asking the user to choose front/back language first

### Scenario 2: Bilingual Sample Rows Include Example And Extra Defaults

Prompt pattern:

```text
根据这份中英双语手册生成卡片，并先给我看几张示例。
```

Expected skill behavior:

- [ ] Show 3-5 representative sample rows before generating the full spec
- [ ] Use the same column order as `## Cards`
- [ ] Make the examples vertically consistent by field
- [ ] In bilingual mode, make `prompt` English and `answer` Chinese
- [ ] In bilingual mode, make `example` an English usage sentence
- [ ] In bilingual mode, make `extra` a Chinese explanatory note

### Scenario 3: No Preliminary Direction Question When Bilingual Intent Is Clear

Prompt pattern:

```text
请根据这个中英对照词表直接先出几张卡片示例。
```

Expected skill behavior:

- [ ] Do not ask a separate “英文在前还是中文在前” question before showing sample rows
- [ ] Present the bilingual default rows directly
- [ ] Still allow the user to revise the rows after seeing them

### Scenario 4: Approved Examples Become The Deck-Wide Contract

Prompt pattern:

```text
这些示例可以，继续。
```

Expected skill behavior:

- [ ] Treat the shown examples as the contract for later rows
- [ ] Keep `prompt` and `answer` aligned with the approved direction
- [ ] Keep `example` and `extra` aligned with the approved language roles
- [ ] Avoid mixing multiple row conventions unless the user explicitly asks

### Scenario 5: Non-Bilingual Requests Still Infer A Stable Direction

Prompt pattern:

```text
从这份产品概念说明里提取卡片。
```

Expected skill behavior:

- [ ] Infer the most sensible direction from the source content
- [ ] Keep one deck-wide front/back mapping
- [ ] Do not cross languages unpredictably across rows
- [ ] State mixed conventions only if the user explicitly requested them

### Scenario 6: Existing Spec File Still Enters Through Extract

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

### Scenario 7: Approved Deck Runs Build Script

Prompt pattern:

```text
The current Markdown deck spec is approved. Generate the final deck.
```

Expected skill behavior:

- [ ] Confirm the current Markdown deck spec is the approved source of truth
- [ ] Run `~/.anki-card-creator/bin/build-apkg <spec_path>` via the Bash tool
- [ ] Report the output path on success
- [ ] Surface validation errors back into the Markdown editing loop if packaging fails

## GREEN Phase Manual Validation

Validation method:

- Read `SKILL.md`
- Check each scenario against the documented workflow
- Verify the workflow explicitly names the bilingual trigger, default field mapping, and deck-wide consistency rules

Result:

- Pending validation after the `SKILL.md` update.

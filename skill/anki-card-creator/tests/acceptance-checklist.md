# Skill Acceptance Checklist

## RED Phase Baseline

Current baseline before the MCP-or-CLI routing redesign:

- The skill only references MCP packaging.
- The skill does not describe any fallback when the MCP tool is unavailable.
- No separate packaging-only fallback skill exists.
- No local CLI packaging path exists for terminal callers.

Result: all routing-focused scenarios fail before the redesign.

## Acceptance Scenarios

### Scenario 1: Approved Deck Uses MCP When MCP Tool Is Available

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

### Scenario 2: Approved Deck Falls Back To Packaging Skill When MCP Is Unavailable

Prompt pattern:

```text
The current Markdown deck spec is approved. Generate the final deck, but MCP is not installed in this session.
```

Expected skill behavior:

- [ ] Confirm the current Markdown deck spec is the approved source of truth
- [ ] Check whether `mcp__ankiCardCreator__build_apkg_from_spec` is available
- [ ] Detect that the MCP tool is unavailable
- [ ] Invoke the fallback packaging skill instead of MCP
- [ ] Keep the same `spec_path` and optional `output_dir` contract
- [ ] Surface validation errors back into the Markdown editing loop if packaging fails

### Scenario 3: Fallback Path Stays Packaging-Only

Prompt pattern:

```text
MCP is unavailable. Use the fallback path to generate the final deck.
```

Expected skill behavior:

- [ ] Do not re-draft cards
- [ ] Do not regenerate Markdown from hidden state
- [ ] Do not bypass explicit approval
- [ ] Hand off only the approved spec path and packaging options to the fallback skill

## GREEN Phase Manual Validation

Validation method:

- Read `SKILL.md`
- Check each routing scenario against the documented workflow
- Read the fallback packaging skill once it exists

Result:

- Pending redesign.
- Current skill does not satisfy the MCP-unavailable scenarios.
- Current repository has no fallback packaging skill or CLI transport.

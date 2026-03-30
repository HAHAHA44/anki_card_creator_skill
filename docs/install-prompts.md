# Install Prompts

## Claude Code

```text
Install anki-card-creator: run git clone --single-branch --depth 1 https://github.com/HAHAHA44/anki_card_creator_skill.git ~/.claude/skills/anki-card-creator-repo && cd ~/.claude/skills/anki-card-creator-repo && bash ./install.sh --target claude --scope user. Then ask whether I also want to enable it for the current project with bash ./install.sh --target claude --scope project --project-dir .
```

## Codex

```text
Install anki-card-creator: run git clone --single-branch --depth 1 https://github.com/HAHAHA44/anki_card_creator_skill.git ~/.codex/skills/anki-card-creator-repo && cd ~/.codex/skills/anki-card-creator-repo && bash ./install.sh --target codex --scope user. Then ask whether I also want to enable it for the current project with bash ./install.sh --target codex --scope project --project-dir .
```

## Both

```text
Install anki-card-creator for both Claude Code and Codex: run git clone --single-branch --depth 1 https://github.com/HAHAHA44/anki_card_creator_skill.git ~/.anki-card-creator-installer && cd ~/.anki-card-creator-installer && bash ./install.sh --target both --scope user. Then ask whether I also want to enable it for the current project with bash ./install.sh --target both --scope project --project-dir .
```

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
SKILL_NAME="anki-card-creator"
TARGET="both"
SCOPE="user"
PROJECT_DIR="$PWD"
HOME_DIR=""
PYTHON_BIN=""
CODEX_BIN="${CODEX_BIN:-codex}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

usage() {
  cat <<'EOF'
Usage: bash ./install.sh [options]

Options:
  --target codex|claude|both   Install for Codex, Claude Code, or both. Default: both
  --scope user|project         Install at user scope or project scope. Default: user
  --project-dir PATH           Project directory for project-scoped files. Default: current directory
  --home-dir PATH              Home directory override for user-scoped installs
  --python PATH                Python interpreter to use for runtime provisioning
  -h, --help                   Show this help text
EOF
}

log() {
  printf '[anki-card-creator] %s\n' "$*"
}

warn() {
  printf '[anki-card-creator] warning: %s\n' "$*" >&2
}

die() {
  printf '[anki-card-creator] error: %s\n' "$*" >&2
  exit 1
}

resolve_path() {
  local path="$1"
  if [[ -d "$path" ]]; then
    (cd "$path" && pwd)
  else
    local parent
    parent="$(cd "$(dirname "$path")" && pwd)"
    printf '%s/%s\n' "$parent" "$(basename "$path")"
  fi
}

copy_skill_tree() {
  local destination_root="$1"
  local target="$destination_root/$SKILL_NAME"
  mkdir -p "$destination_root"
  rm -rf "$target"
  cp -R "$REPO_ROOT/skill/$SKILL_NAME" "$target"
  log "Installed skill into $target"
}

find_runtime_python() {
  local venv_dir="$1"
  local candidate
  for candidate in \
    "$venv_dir/bin/python" \
    "$venv_dir/Scripts/python.exe" \
    "$venv_dir/Scripts/python"
  do
    if [[ -f "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

create_runtime() {
  local runtime_root="$1"
  local venv_dir="$runtime_root/runtime/venv"
  mkdir -p "$runtime_root/runtime"
  "$PYTHON_BIN" -m venv "$venv_dir"
  RUNTIME_PYTHON="$(find_runtime_python "$venv_dir")" || die "Unable to find the venv Python inside $venv_dir"
  "$RUNTIME_PYTHON" -m pip install genanki >/dev/null
  log "Provisioned runtime at $venv_dir"
}

create_bin_wrapper() {
  local scripts_dir="$1"
  local wrapper_dir="$RUNTIME_ROOT/bin"
  local wrapper_path="$wrapper_dir/build-apkg"
  mkdir -p "$wrapper_dir"
  cat > "$wrapper_path" <<EOF
#!/usr/bin/env bash
exec "$RUNTIME_PYTHON" "$scripts_dir/build_apkg.py" "\$@"
EOF
  chmod +x "$wrapper_path"
  log "Created wrapper at $wrapper_path"
}

upsert_managed_block() {
  local file_path="$1"
  local start_marker="$2"
  local end_marker="$3"
  local content="$4"
  local tmp_file
  mkdir -p "$(dirname "$file_path")"
  tmp_file="$(mktemp)"

  if [[ -f "$file_path" ]]; then
    awk -v start="$start_marker" -v end="$end_marker" '
      $0 == start { skip = 1; next }
      $0 == end { skip = 0; next }
      !skip { print }
    ' "$file_path" > "$tmp_file"
  else
    : > "$tmp_file"
  fi

  if [[ -s "$tmp_file" ]]; then
    printf '\n' >> "$tmp_file"
  fi

  printf '%s\n' "$start_marker" >> "$tmp_file"
  printf '%s\n' "$content" >> "$tmp_file"
  printf '%s\n' "$end_marker" >> "$tmp_file"
  mv "$tmp_file" "$file_path"
}

write_project_guidance() {
  local project_dir="$1"
  local claude_block
  local agents_block

  claude_block=$(cat <<EOF
## anki-card-creator

Use the project-local \`anki-card-creator\` skill for Anki deck drafting workflows.
When the current \`deck-spec.md\` is approved, package it by running:
  ~/.anki-card-creator/bin/build-apkg <spec_path> [--output-dir <dir>]
EOF
)

  agents_block=$(cat <<EOF
## anki-card-creator

The project includes a local \`anki-card-creator\` skill under \`.codex/skills/${SKILL_NAME}\`.
Prefer that skill for drafting and packaging Anki decks.
When packaging an approved spec, run:
  ~/.anki-card-creator/bin/build-apkg <spec_path> [--output-dir <dir>]
EOF
)

  upsert_managed_block \
    "$project_dir/CLAUDE.md" \
    "<!-- anki-card-creator:begin -->" \
    "<!-- anki-card-creator:end -->" \
    "$claude_block"

  upsert_managed_block \
    "$project_dir/AGENTS.md" \
    "<!-- anki-card-creator:begin -->" \
    "<!-- anki-card-creator:end -->" \
    "$agents_block"

  log "Updated project guidance files"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --scope)
      SCOPE="${2:-}"
      shift 2
      ;;
    --project-dir)
      PROJECT_DIR="${2:-}"
      shift 2
      ;;
    --home-dir)
      HOME_DIR="${2:-}"
      shift 2
      ;;
    --python)
      PYTHON_BIN="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1"
      ;;
  esac
done

case "$TARGET" in
  codex|claude|both) ;;
  *)
    die "Invalid --target: $TARGET"
    ;;
esac

case "$SCOPE" in
  user|project) ;;
  *)
    die "Invalid --scope: $SCOPE"
    ;;
esac

if [[ ! -d "$REPO_ROOT/skill/$SKILL_NAME" ]]; then
  die "Missing skill source at $REPO_ROOT/skill/$SKILL_NAME"
fi

if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python)"
  else
    die "Could not find a Python interpreter; pass one with --python"
  fi
elif [[ "$PYTHON_BIN" == */* ]]; then
  PYTHON_BIN="$(resolve_path "$PYTHON_BIN")"
else
  if command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v "$PYTHON_BIN")"
  else
    die "Could not resolve the Python interpreter: $PYTHON_BIN"
  fi
fi

if [[ "$SCOPE" == "user" ]]; then
  if [[ -n "$HOME_DIR" ]]; then
    INSTALL_ROOT="$(resolve_path "$HOME_DIR")"
  else
    INSTALL_ROOT="$(resolve_path "${HOME:-$PWD}")"
  fi
else
  INSTALL_ROOT="$(resolve_path "$PROJECT_DIR")"
  mkdir -p "$INSTALL_ROOT"
fi

RUNTIME_ROOT="$INSTALL_ROOT/.anki-card-creator"
create_runtime "$RUNTIME_ROOT"

LAST_SCRIPTS_DIR=""

if [[ "$TARGET" == "codex" || "$TARGET" == "both" ]]; then
  copy_skill_tree "$INSTALL_ROOT/.codex/skills"
  LAST_SCRIPTS_DIR="$INSTALL_ROOT/.codex/skills/$SKILL_NAME/scripts"
fi

if [[ "$TARGET" == "claude" || "$TARGET" == "both" ]]; then
  copy_skill_tree "$INSTALL_ROOT/.claude/skills"
  LAST_SCRIPTS_DIR="$INSTALL_ROOT/.claude/skills/$SKILL_NAME/scripts"
fi

create_bin_wrapper "$LAST_SCRIPTS_DIR"

if [[ "$SCOPE" == "project" ]]; then
  write_project_guidance "$INSTALL_ROOT"
fi

cat <<EOF

Install complete.

- Target: $TARGET
- Scope: $SCOPE
- Runtime: $RUNTIME_ROOT/runtime/venv
- Wrapper: $RUNTIME_ROOT/bin/build-apkg

Restart Codex or Claude Code if they were already running.
EOF

import os
import stat
import subprocess
import sys
from pathlib import Path


def _to_bash_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix()[2:]
    return f"/mnt/{drive}{tail}"


def _write_executable(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


def _make_fake_python(
    bin_dir: Path,
    fake_python_log: str,
    fake_runtime_python_log: str,
) -> Path:
    fake_python = bin_dir / "python"
    script = r"""#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "-m" && "${2:-}" == "venv" ]]; then
  venv_dir="${3:?}"
  runtime_log="__FAKE_RUNTIME_PYTHON_LOG__"
  mkdir -p "$venv_dir/bin"
  cat > "$venv_dir/bin/python" <<EOF
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "\$*" >> "$runtime_log"
if [[ "\${1:-}" == "-m" && "\${2:-}" == "pip" ]]; then
  exit 0
fi
echo "unexpected runtime python args: \$*" >&2
exit 1
EOF
  chmod +x "$venv_dir/bin/python"
  exit 0
fi

if [[ "${1:-}" == "-m" && "${2:-}" == "pip" ]]; then
  printf '%s\n' "$*" >> "__FAKE_PYTHON_LOG__"
  exit 0
fi

echo "unexpected fake python args: $*" >&2
exit 1
"""
    script = script.replace("__FAKE_PYTHON_LOG__", fake_python_log)
    script = script.replace("__FAKE_RUNTIME_PYTHON_LOG__", fake_runtime_python_log)
    _write_executable(
        fake_python,
        script,
    )
    return fake_python


def _make_fake_cli(bin_dir: Path, name: str, log_path: str) -> None:
    _write_executable(
        bin_dir / name,
        f"""#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> "{log_path}"
if [[ "${{1:-}}" == "mcp" && "${{2:-}}" == "get" ]]; then
  exit 1
fi
exit 0
""",
    )


def _run_install(
    *args: str,
    home: Path,
    env_extra: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    repo_root = Path(__file__).resolve().parents[2]
    bin_dir = home / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    fake_python_log = home / "fake-python.log"
    fake_runtime_python_log = home / "fake-runtime-python.log"
    fake_codex_log = home / "fake-codex.log"
    fake_claude_log = home / "fake-claude.log"

    fake_python = _make_fake_python(
        bin_dir,
        _to_bash_path(fake_python_log),
        _to_bash_path(fake_runtime_python_log),
    )
    fake_codex = bin_dir / "codex"
    fake_claude = bin_dir / "claude"
    _make_fake_cli(bin_dir, "codex", _to_bash_path(fake_codex_log))
    _make_fake_cli(bin_dir, "claude", _to_bash_path(fake_claude_log))

    env = os.environ.copy()
    env.update(
        {
            "HOME": _to_bash_path(home),
            "PATH": "/usr/bin:/bin",
            "CODEX_BIN": _to_bash_path(fake_codex),
            "CLAUDE_BIN": _to_bash_path(fake_claude),
        }
    )
    if env_extra:
        env.update(env_extra)

    bash_args = list(args)
    if "--project-dir" in bash_args:
        index = bash_args.index("--project-dir") + 1
        bash_args[index] = _to_bash_path(Path(bash_args[index]))

    return subprocess.run(
        [
            "bash",
            "./install.sh",
            *bash_args,
            "--home-dir",
            _to_bash_path(home),
            "--python",
            _to_bash_path(fake_python),
        ],
        cwd=repo_root,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def test_install_sh_user_scope_installs_skills_and_registers_mcp(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()

    result = _run_install("--target", "both", "--scope", "user", home=home)

    assert result.returncode == 0, result.stderr
    assert (home / ".codex" / "skills" / "anki-card-creator" / "SKILL.md").exists()
    assert (home / ".claude" / "skills" / "anki-card-creator" / "SKILL.md").exists()
    assert (home / ".anki-card-creator" / "runtime" / "venv" / "bin" / "python").exists()

    runtime_log = (home / "fake-runtime-python.log").read_text(encoding="utf-8")

    assert "-m pip install" in runtime_log


def test_install_sh_project_scope_writes_project_files(tmp_path: Path) -> None:
    home = tmp_path / "home"
    project_dir = tmp_path / "project"
    home.mkdir()
    project_dir.mkdir()

    result = _run_install(
        "--target",
        "both",
        "--scope",
        "project",
        "--project-dir",
        str(project_dir),
        home=home,
    )

    assert result.returncode == 0, result.stderr
    assert (project_dir / ".claude" / "skills" / "anki-card-creator" / "SKILL.md").exists()
    assert (project_dir / ".codex" / "skills" / "anki-card-creator" / "SKILL.md").exists()
    assert (project_dir / ".mcp.json").exists()
    assert (project_dir / "CLAUDE.md").exists()
    assert (project_dir / "AGENTS.md").exists()

    mcp_json = (project_dir / ".mcp.json").read_text(encoding="utf-8")
    claude_md = (project_dir / "CLAUDE.md").read_text(encoding="utf-8")
    agents_md = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
    assert "ankiCardCreator" in mcp_json
    assert "mcp__ankiCardCreator__build_apkg_from_spec" in claude_md
    assert "mcp__ankiCardCreator__build_apkg_from_json" in agents_md

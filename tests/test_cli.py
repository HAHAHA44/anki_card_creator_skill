import json
import subprocess
import sys
from pathlib import Path


_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "skill" / "anki-card-creator" / "scripts"
_BUILD_APKG = _SCRIPTS_DIR / "build_apkg.py"


def test_cli_builds_apkg_from_markdown(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(_BUILD_APKG),
            "tests/fixtures/qa_deck_spec.md",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[1],
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert Path(str(payload["output_path"])).exists()


def test_cli_exits_nonzero_on_invalid_spec(tmp_path: Path) -> None:
    bad_spec = tmp_path / "bad.md"
    bad_spec.write_text("# Anki Deck Spec\n\n## Deck Metadata\n- deck_name: Bad\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(_BUILD_APKG), str(bad_spec)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["errors"]

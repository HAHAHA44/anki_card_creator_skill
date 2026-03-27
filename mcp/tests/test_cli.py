import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_builds_apkg_from_markdown(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path("mcp/src").resolve())

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "anki_card_creator_mcp.cli",
            "mcp/tests/fixtures/qa_deck_spec.md",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert Path(str(payload["output_path"])).exists()

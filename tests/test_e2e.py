from pathlib import Path

from service import build_apkg_from_markdown


def test_end_to_end_builds_apkg_from_markdown(tmp_path: Path) -> None:
    result = build_apkg_from_markdown(
        Path("tests/fixtures/qa_deck_spec.md"),
        tmp_path,
    )

    assert result["ok"] is True
    assert Path(str(result["output_path"])).exists()

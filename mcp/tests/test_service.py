from pathlib import Path

from anki_card_creator_mcp.service import build_apkg_from_markdown


def test_service_returns_success_payload(tmp_path: Path) -> None:
    result = build_apkg_from_markdown(
        Path("mcp/tests/fixtures/minimal_deck_spec.md"),
        tmp_path,
    )

    assert result["ok"] is True
    assert result["output_path"].endswith(".apkg")
    assert result["errors"] == []


def test_service_returns_validation_errors(tmp_path: Path) -> None:
    bad_spec = tmp_path / "bad.md"
    bad_spec.write_text(
        "# Anki Deck Spec\n\n## Deck Metadata\n- deck_name: Bad\n",
        encoding="utf-8",
    )

    result = build_apkg_from_markdown(bad_spec, tmp_path)

    assert result["ok"] is False
    assert result["output_path"] == ""
    assert result["errors"]

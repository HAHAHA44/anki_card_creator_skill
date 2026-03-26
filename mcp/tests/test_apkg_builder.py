from pathlib import Path

from anki_card_creator_mcp.apkg_builder import build_apkg
from anki_card_creator_mcp.markdown_parser import parse_deck_spec


def test_build_apkg_writes_output_file(tmp_path: Path) -> None:
    spec = parse_deck_spec(Path("mcp/tests/fixtures/minimal_deck_spec.md"))

    output_path = build_apkg(spec, tmp_path)

    assert output_path.exists()
    assert output_path.suffix == ".apkg"
    assert output_path.stat().st_size > 0

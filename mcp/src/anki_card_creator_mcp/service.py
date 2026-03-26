from pathlib import Path

from anki_card_creator_mcp.apkg_builder import build_apkg
from anki_card_creator_mcp.markdown_parser import parse_deck_spec
from anki_card_creator_mcp.validators import validate_deck_spec


def build_apkg_from_markdown(spec_path: Path, output_dir: Path | None = None) -> dict[str, object]:
    try:
        spec = parse_deck_spec(spec_path)
    except Exception as exc:
        return {"ok": False, "errors": [str(exc)], "output_path": ""}

    errors = validate_deck_spec(spec)
    if errors:
        return {"ok": False, "errors": errors, "output_path": ""}

    target_dir = output_dir if output_dir is not None else spec_path.parent
    output_path = build_apkg(spec, target_dir)
    return {"ok": True, "errors": [], "output_path": str(output_path)}

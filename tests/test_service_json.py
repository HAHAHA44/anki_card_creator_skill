from pathlib import Path

from service import build_apkg_from_dict


MINIMAL_SPEC = {
    "deck_name": "Test Deck",
    "source_mode": "domain",
    "output_file": "test.apkg",
    "front_layout": ["context", "prompt", "example"],
    "back_layout": ["answer", "extra"],
    "cards": [
        {
            "id": "1",
            "prompt": "What is the powerhouse of the cell?",
            "answer": "Mitochondria",
            "context": "Biology",
            "example": "",
            "extra": "",
            "tags": "biology",
        }
    ],
}


def test_build_apkg_from_dict_returns_success(tmp_path: Path) -> None:
    result = build_apkg_from_dict(MINIMAL_SPEC, tmp_path)

    assert result["ok"] is True
    assert result["errors"] == []
    assert Path(str(result["output_path"])).exists()


def test_build_apkg_from_dict_returns_validation_errors(tmp_path: Path) -> None:
    bad_spec = {**MINIMAL_SPEC, "deck_name": "", "source_mode": "bad"}

    result = build_apkg_from_dict(bad_spec, tmp_path)

    assert result["ok"] is False
    assert result["errors"]


def test_build_apkg_from_dict_validates_card_fields(tmp_path: Path) -> None:
    spec = {**MINIMAL_SPEC, "cards": [{"id": "1", "prompt": "", "answer": "A"}]}

    result = build_apkg_from_dict(spec, tmp_path)

    assert result["ok"] is False
    assert any("prompt" in e for e in result["errors"])

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from anki_card_creator_mcp import __all__


def test_package_exports_module_symbol() -> None:
    assert "__version__" in __all__

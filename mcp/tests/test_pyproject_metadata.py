from pathlib import Path
import tomllib


def test_license_file_stays_within_mcp_package_root() -> None:
    package_root = Path("mcp").resolve()
    pyproject = tomllib.loads((package_root / "pyproject.toml").read_text(encoding="utf-8"))

    license_config = pyproject["project"]["license"]
    assert "file" in license_config

    license_path = (package_root / license_config["file"]).resolve()
    assert package_root == license_path.parent or package_root in license_path.parents

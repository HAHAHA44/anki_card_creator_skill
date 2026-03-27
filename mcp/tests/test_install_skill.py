from pathlib import Path

from scripts.install_skill import install_skill


def test_install_skill_copies_skill_tree(tmp_path: Path) -> None:
    target = tmp_path / "skills"

    installed_path = install_skill(
        source=Path("skill/anki-card-creator"),
        destination_root=target,
        skill_name="anki-card-creator",
    )

    assert installed_path.exists()
    assert (installed_path / "SKILL.md").exists()
    assert (installed_path / "agents" / "openai.yaml").exists()


def test_skill_markdown_is_ascii_compatible() -> None:
    skill_bytes = Path("skill/anki-card-creator/SKILL.md").read_bytes()
    assert all(byte < 128 for byte in skill_bytes)

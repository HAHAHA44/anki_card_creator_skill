import argparse
import shutil
from pathlib import Path


def install_skill(source: Path, destination_root: Path, skill_name: str) -> Path:
    target = destination_root / skill_name
    destination_root.mkdir(parents=True, exist_ok=True)

    if target.exists():
        shutil.rmtree(target)

    shutil.copytree(source, target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Install the local skill into a target skills directory.")
    parser.add_argument("--source", required=True, help="Path to the source skill directory")
    parser.add_argument("--dest", required=True, help="Destination root for installed skills")
    parser.add_argument("--name", required=True, help="Installed skill directory name")
    args = parser.parse_args()

    installed_path = install_skill(
        source=Path(args.source),
        destination_root=Path(args.dest),
        skill_name=args.name,
    )
    print(installed_path)


if __name__ == "__main__":
    main()

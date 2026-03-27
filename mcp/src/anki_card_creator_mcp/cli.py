import argparse
import json
import sys
from pathlib import Path

from anki_card_creator_mcp.service import build_apkg_from_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a Markdown deck spec and build an Anki .apkg file."
    )
    parser.add_argument("spec_path", help="Path to the Markdown deck spec file.")
    parser.add_argument(
        "--output-dir",
        help="Directory to write the .apkg into. Defaults to the spec file directory.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    result = build_apkg_from_markdown(
        Path(args.spec_path),
        Path(args.output_dir) if args.output_dir else None,
    )
    print(json.dumps(result))

    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()

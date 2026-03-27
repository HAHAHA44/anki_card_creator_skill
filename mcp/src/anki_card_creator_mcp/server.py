from pathlib import Path

import anyio
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from anki_card_creator_mcp.service import build_apkg_from_dict, build_apkg_from_markdown

_CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "id":      {"type": "string"},
        "prompt":  {"type": "string"},
        "answer":  {"type": "string"},
        "context": {"type": "string"},
        "example": {"type": "string"},
        "extra":   {"type": "string"},
        "tags":    {"type": "string"},
    },
    "required": ["id", "prompt", "answer"],
}

server = Server("anki-card-creator-mcp", version="0.1.0")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="build_apkg_from_spec",
            description="Validate a Markdown deck spec file and generate an Anki .apkg file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_path":  {"type": "string", "description": "Absolute path to the Markdown deck spec file."},
                    "output_dir": {"type": "string", "description": "Directory to write the .apkg into. Defaults to the spec file's directory."},
                },
                "required": ["spec_path"],
            },
        ),
        types.Tool(
            name="build_apkg_from_json",
            description="Validate a deck spec supplied as a JSON object and generate an Anki .apkg file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "Deck spec as a structured object.",
                        "properties": {
                            "deck_name":    {"type": "string"},
                            "source_mode":  {"type": "string", "enum": ["domain", "extract"]},
                            "output_file":  {"type": "string"},
                            "front_layout": {"type": "array", "items": {"type": "string"}},
                            "back_layout":  {"type": "array", "items": {"type": "string"}},
                            "cards":        {"type": "array", "items": _CARD_SCHEMA},
                        },
                        "required": ["deck_name", "source_mode", "output_file", "front_layout", "back_layout", "cards"],
                    },
                    "output_dir": {"type": "string", "description": "Directory to write the .apkg into."},
                },
                "required": ["spec", "output_dir"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, object]) -> list[types.TextContent]:
    if name == "build_apkg_from_spec":
        result = build_apkg_from_markdown(
            Path(str(arguments["spec_path"])),
            Path(str(arguments["output_dir"])) if arguments.get("output_dir") else None,
        )
    elif name == "build_apkg_from_json":
        result = build_apkg_from_dict(
            dict(arguments["spec"]),  # type: ignore[arg-type]
            Path(str(arguments["output_dir"])),
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [types.TextContent(type="text", text=str(result))]


async def run_stdio_server() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    anyio.run(run_stdio_server)


if __name__ == "__main__":
    main()

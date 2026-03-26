from pathlib import Path

import anyio
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from anki_card_creator_mcp.service import build_apkg_from_markdown


server = Server("anki-card-creator-mcp", version="0.1.0")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="build_apkg_from_spec",
            description="Validate a markdown deck spec and generate an Anki .apkg file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_path": {"type": "string"},
                    "output_dir": {"type": "string"},
                },
                "required": ["spec_path"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, object]) -> list[types.TextContent]:
    if name != "build_apkg_from_spec":
        raise ValueError(f"Unknown tool: {name}")

    result = build_apkg_from_markdown(
        Path(str(arguments["spec_path"])),
        Path(str(arguments["output_dir"])) if arguments.get("output_dir") else None,
    )
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

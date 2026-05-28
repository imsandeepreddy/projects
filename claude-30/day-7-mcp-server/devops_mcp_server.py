from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import os
from pathlib import Path
import shutil
import asyncio

server = Server("devops-assistant")

# Define the ONLY allowed folder path
ALLOWED_FOLDER = Path(r"C:\Users\sande\OneDrive\Desktop\TestFolder").resolve()

@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="check_disk_usage",
            description="Check disk usage for a given path inside the allowed TestFolder directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to check (must be inside TestFolder)"
                    }
                },
                "required": ["path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "check_disk_usage":
        # Resolve target path cleanly to avoid symlink/relative path directory traversal attacks
        target_path = Path(arguments["path"]).resolve()
        
        # Check if the target path starts with the allowed folder path
        if ALLOWED_FOLDER not in target_path.parents and target_path != ALLOWED_FOLDER:
            return [types.TextContent(
                type="text",
                text=f"Access Denied: Path '{arguments['path']}' is outside the permitted workspace directory."
            )]
            
        try:
            usage = shutil.disk_usage(target_path)
            return [types.TextContent(
                type="text",
                text=f"Total: {usage.total // (2**30)}GB, "
                     f"Used: {usage.used // (2**30)}GB, "
                     f"Free: {usage.free // (2**30)}GB"
            )]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error checking disk: {str(e)}")]

# Dynamically find the absolute path of the file in the same folder
LOG_FILE_PATH = ALLOWED_FOLDER / "app.log"

@server.list_resources()
async def list_resources():
    return [
        types.Resource(
            uri=LOG_FILE_PATH.as_uri(),
            name="Application Log",
            description="Latest application log file",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def read_resource(uri):
    if str(uri) == LOG_FILE_PATH.as_uri():
        if not LOG_FILE_PATH.exists():
            return [types.TextContent(type="text", text="Error: app.log file does not exist yet.")]
            
        file_content = LOG_FILE_PATH.read_text(encoding="utf-8")
        
        # Fixed: Directly return the content block inside a list for universal host parsing
        return [
            types.TextResourceContents(
                uri=str(uri),
                mimeType="text/plain",
                text=file_content
            )
        ]
    raise ValueError(f"Resource not found: {uri}")


@server.list_prompts()
async def list_prompts():
    return [
        types.Prompt(
            name="analyse-logs",
            description="Analyse log file for errors and suggest fixes",
            arguments=[
                types.PromptArgument(
                    name="severity",
                    description="Minimum severity: ERROR or WARN",
                    required=False
                )
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name, arguments):
    severity = arguments.get("severity", "ERROR")
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Read the app.log resource and identify all "
                         f"{severity} level entries. Summarise root causes "
                         f"and suggest fixes for each."
                )
            )
        ]
    )

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream,
                        server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())

import os

from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DISABLED_TOOLS = ",".join(
    [
        "assistant",          # AI assistant meta-tool, not needed
        "atlas-local",        # local Atlas CLI, not used
        "mongodb-logs",       # log inspection, not used by agents
        "export",             # bulk export, not needed
        "rename-collection",  # DDL ops, agents never rename
        "drop-collection",    # DDL ops, safety guard
        "drop-database",      # DDL ops, safety guard
        "create-index",       # DDL ops, not needed at runtime
    ]
)


def mongodb_mcp_toolset(*, read_only: bool) -> MCPToolset:
    """Build a MongoDB MCP toolset with consistent startup settings."""
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise RuntimeError("MONGODB_URI is required for MongoDB MCP tools.")

    package = os.getenv("MONGODB_MCP_PACKAGE", "mongodb-mcp-server@latest")
    timeout = int(os.getenv("MONGODB_MCP_TIMEOUT", "90"))
    args = ["--yes", "--prefer-offline", package]
    if read_only:
        args.append("--readOnly")

    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=args,
                env={
                    "MDB_MCP_CONNECTION_STRING": mongodb_uri,
                    "MDB_MCP_DATABASE_NAME": os.getenv("MONGODB_DB_NAME", "clinicalops"),
                    "MDB_MCP_DISABLED_TOOLS": os.getenv(
                        "MDB_MCP_DISABLED_TOOLS",
                        DEFAULT_DISABLED_TOOLS,
                    ),
                    "MDB_MCP_TELEMETRY": os.getenv("MDB_MCP_TELEMETRY", "disabled"),
                },
            ),
            timeout=timeout,
        ),
    )


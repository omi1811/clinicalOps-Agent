from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv

load_dotenv()

root_agent = Agent(
    model="gemini-3.5-flash",
    name="clinicalops_mongodb_agent",
    instruction="""
    You are a clinical operations assistant. Use MongoDB MCP tools to:
    - Query patient records for trial eligibility screening
    - Search trial protocols by criteria  
    - Log adverse events with proper severity classification
    Always return structured, concise responses. Cite data sources.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "mongodb-mcp-server@latest"],
                    env={
                        "MDB_MCP_CONNECTION_STRING": os.getenv("MONGODB_URI"),
                    },
                ),
                timeout=30,
            ),
        )
    ],
)


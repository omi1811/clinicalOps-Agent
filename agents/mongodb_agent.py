from dotenv import load_dotenv
from google.adk.agents import Agent
from agents.shared_mcp import shared_mcp_toolset

load_dotenv()

root_agent = Agent(
    model="gemini-2.5-flash",
    name="clinicalops_mongodb_agent",
    instruction="""
    You are a clinical operations assistant.

    Use MongoDB MCP tools to:
    - Query patient records
    - Search trial protocols
    - Log adverse events

    Always return concise structured responses.
    """,
    tools=[shared_mcp_toolset]
)
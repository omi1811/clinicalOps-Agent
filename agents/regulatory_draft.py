from dotenv import load_dotenv
from google.adk.agents import Agent
from agents.shared_mcp import shared_mcp_toolset

load_dotenv()

regulatory_draft_agent = Agent(
    model="gemini-2.5-flash",
    name="regulatory_draft",
    description="Generate ICH-compliant regulatory documents.",
    instruction="""
    You are a regulatory writing specialist.

    Database name: clinicalops
    Collections: patients, trials, adverse_events

    STEPS:
    1. Use MongoDB MCP to fetch the patient, trial, and adverse event records from the clinicalops database
    2. Identify any missing required ICH E2A fields and flag them explicitly
    3. Generate the requested document

    OUTPUT (Markdown only, sponsor-ready):
    - ICH E2A SAE narrative or ICF summary as requested
    - Flag section for any missing/incomplete data
    """,
    tools=[shared_mcp_toolset],
)
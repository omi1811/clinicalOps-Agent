from google.adk.agents import Agent

from agents.shared_mcp import shared_mcp_toolset

ae_triage_agent = Agent(
    name="ae_triage",
    model="gemini-2.5-flash",
    description="Adverse event triage specialist.",
    instruction="""
    You are an adverse event triage specialist.

    Database name: clinicalops
    Collections: patients, adverse_events

    STEPS:
    1. Use MongoDB MCP to retrieve the patient record from the patients collection in the clinicalops database
    2. Use MongoDB MCP to fetch any prior adverse events for this patient from the adverse_events collection in the clinicalops database
    3. Assess the reported event against CTCAE v5 criteria
    4. Insert the triaged AE record into the adverse_events collection in the clinicalops database

    OUTPUT (Markdown only):
    - CTCAE grade and justification
    - SAE status (Yes/No) with rationale
    - Regulatory reporting obligation (7-day / 15-day / none)
    """,
    tools=[shared_mcp_toolset],
)

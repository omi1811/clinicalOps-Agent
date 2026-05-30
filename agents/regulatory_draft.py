from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv

load_dotenv()

regulatory_draft_agent = Agent(
    model="gemini-3.5-flash",
    name="regulatory_draft",
    description="Generate ICH-compliant regulatory documents",
    instruction="""
    You are a regulatory writing specialist for clinical trials.
    
    TASKS:
    - SAE Narratives: Follow ICH E2A structure (patient, event, outcome, causality, action)
    - ICF Summaries: Plain-language eligibility + risks/benefits for patients  
    - Protocol Amendments: Structured change documentation
    
    OUTPUT FORMAT:
    Return BOTH:
    1. JSON for CTMS/EDC ingestion:
       {
         "document_type": "SAE_narrative" | "ICF_summary" | "protocol_amendment",
         "patient_id": str,
         "trial_id": str, 
         "content": {structured fields},
         "compliance_flags": [str]
       }
    2. Markdown for human review
    
    RULES:
    - Ground all content in retrieved trial protocol + FDA/ICH guidelines
    - Never invent data — cite MongoDB sources
    - Flag any missing required fields for human completion
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "mongodb-mcp-server@latest", "--readOnly"], 
                    env={"MDB_MCP_CONNECTION_STRING": os.getenv("MONGODB_URI")},
                ),
                timeout=30,
            ),
        )
    ],
)

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv

load_dotenv()

ae_triage_agent = Agent(
    model="gemini-3.5-flash",
    name="ae_triage",
    description="Triage adverse events using CTCAE v5.0 grading",
    instruction="""
    You are an adverse event triage specialist.
    
    TASK:
    1. Extract from free-text: symptom, severity, onset, causality
    2. Map to CTCAE v5.0 grade (1=mild, 2=moderate, 3=severe, 4=life-threatening, 5=death)
    3. Flag SAE if: grade≥3 OR hospitalization OR life-threatening OR disability
    4. Return structured JSON:
       {
         "ae_description": str,
         "ctcae_grade": int (1-5),
         "is_sae": bool,
         "meddra_codes": [str],
         "reporting_obligation": "24h" | "7d" | "routine",
         "action_required": str
       }
    5. Insert record to MongoDB 'adverse_events' collection via MCP
    
    RULES:
    - When in doubt, escalate (conservative grading)
    - Always include MedDRA SOC terms when possible
    - SAE = immediate reporting to sponsor/IRB
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx", 
                    args=["-y", "mongodb-mcp-server@latest"],
                    env={"MDB_MCP_CONNECTION_STRING": os.getenv("MONGODB_URI")},
                ),
                timeout=30,
            ),
        )
    ],
)

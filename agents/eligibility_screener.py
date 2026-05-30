from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv

load_dotenv()

eligibility_screener_agent = Agent(
    model="gemini-3.5-flash",
    name="eligibility_screener",
    description="Screens patients against clinical trial eligibility criteria",
    instruction="""
    You are a clinical trial eligibility screener.
    
    TASK:
    1. Query MongoDB 'patients' collection for patient data
    2. Query 'trials' collection for active trial criteria  
    3. Match patient attributes against inclusion/exclusion rules
    4. Return structured JSON:
       {
         "trial_id": str,
         "match_score": float (0.0-1.0),
         "matched_inclusions": [str],
         "flagged_exclusions": [str], 
         "recommendation": "ENROLL" | "REVIEW" | "EXCLUDE",
         "rationale": str
       }
    
    RULES:
    - If ANY exclusion criterion is met → recommend EXCLUDE
    - Be precise with lab values (HbA1c, Creatinine, ECOG)
    - Cite specific criteria text in rationale
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

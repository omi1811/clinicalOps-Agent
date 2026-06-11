
# agents/orchestrator.py

from google.adk.agents import Agent

from agents.eligibility_screener import eligibility_screener_agent
from agents.ae_triage import ae_triage_agent
from agents.regulatory_draft import regulatory_draft_agent
from utils.logger import get_logger
      
logger = get_logger(__name__)  


# CLINICALOPS ORCHESTRATOR


orchestrator_agent = Agent(
    name="clinicalops_orchestrator",

    model="gemini-2.5-flash",

    description="Central orchestration agent for ClinicalOps workflows.",

    instruction="""
    You are the ClinicalOps AI Orchestrator. Route tasks to the correct specialist agent.

    AGENTS:
    - eligibility_screener: patient-trial matching, vector search
    - ae_triage: adverse events, CTCAE grading, SAE status
    - regulatory_draft: ICH narratives, regulatory summaries

    RULES:
    - Delegate — do not answer clinical questions yourself
    - Chain agents for multi-step workflows (match → triage → narrative)
    - Return concise professional Markdown only, never raw JSON
    - Prioritize patient safety and regulatory compliance
    """,

    sub_agents=[
        eligibility_screener_agent,
        ae_triage_agent,
        regulatory_draft_agent,
    ],
)

logger.info("✅ ClinicalOps Orchestrator Agent initialized")

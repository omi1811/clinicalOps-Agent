# ClinicalOps Orchestrator App

from google.adk import App

from agents.orchestrator import orchestrator_agent
from agents.eligibility_screener import eligibility_screener_agent
from agents.ae_triage import ae_triage_agent
from agents.regulatory_draft import regulatory_draft_agent
from utils.logger import get_logger
      
# MAIN ADK APPLICATION
logger = get_logger(__name__)  

app = App(
    name="clinicalops",

    # Root orchestrator agent
    root_agent=orchestrator_agent,

    # Registered agents
    agents={
        "orchestrator": orchestrator_agent,
        "eligibility_screener": eligibility_screener_agent,
        "ae_triage": ae_triage_agent,
        "regulatory_draft": regulatory_draft_agent,
    }
)

logger.info("✅ ClinicalOps Orchestrator Loaded")
logger.info("✅ Registered Agents:")
logger.info("   - Orchestrator")
logger.info("   - Eligibility Screener")
logger.info("   - AE Triage")
logger.info("   - Regulatory Draft")

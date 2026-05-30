# app.py - ClinicalOps Orchestrator App
# Routes user intent to the correct specialized agent

from google.adk.agents import Agent
from google.adk.apps.app import App
from agents.eligibility_screener import eligibility_screener_agent
from agents.ae_triage import ae_triage_agent
from agents.regulatory_draft import regulatory_draft_agent

# Create a router agent that delegates to specialists
orchestrator_agent = Agent(
    model="gemini-3.5-flash",
    name="clinicalops_orchestrator",
    instruction="""
    You are the ClinicalOps Orchestrator. Your job is to route user requests to the right specialist:
    
    ROUTING RULES:
    - If user mentions: "screen", "eligibility", "trial match", "enroll" 
      → Delegate to: eligibility_screener_agent
      
    - If user mentions: "adverse event", "AE", "side effect", "symptom", "triage", "grade"
      → Delegate to: ae_triage_agent
      
    - If user mentions: "draft", "report", "narrative", "ICF", "SAE", "regulatory", "document"
      → Delegate to: regulatory_draft_agent
      
    - If unclear: Ask clarifying question first
    
    DELEGATION FORMAT:
    When delegating, provide context:
    "Forwarding to [agent_name]. Context: [brief summary of patient/trial/AE details]"
    
    Never execute specialist tasks yourself — always delegate.
    """,
    sub_agents=[
      eligibility_screener_agent,
      ae_triage_agent,
      regulatory_draft_agent,
    ],
)

# Register the app with all agents
app = App(
    name="clinicalops",
    root_agent=orchestrator_agent,
)

print("✅ ClinicalOps App loaded:")
print("   🎛️  orchestrator (router)")
print("   🟢 eligibility_screener")
print("   🟠 ae_triage") 
print("   🔵 regulatory_draft")

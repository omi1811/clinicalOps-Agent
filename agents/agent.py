# agents/agent.py
# Entry point for `adk web` — exposes root_agent directly from the orchestrator
# to avoid circular imports with app.py

from agents.orchestrator import orchestrator_agent

root_agent = orchestrator_agent

# agents/eligibility_screener.py

import os

from dotenv import load_dotenv
from google.adk.agents import Agent
import google.genai as genai

from agents.mcp_config import mongodb_mcp_toolset
from utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

_genai_client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location="asia-south1"
)

# Read-only MCP toolset — eligibility screener never writes
_read_only_mcp = mongodb_mcp_toolset(read_only=True)


def generate_embedding(text: str) -> list:
    """Generate semantic embeddings using Vertex AI (text-embedding-004)."""
    try:
        result = _genai_client.models.embed_content(
            model="models/text-embedding-004",
            contents=[text],
        )
        return result.embeddings[0].values
    except Exception as e:
        logger.info(f"Embedding generation failed: {e}")
        return [0.0] * 768


eligibility_screener_agent = Agent(
    model="gemini-2.5-flash",
    name="eligibility_screener",
    description="Screens patients against clinical trial eligibility criteria.",
    instruction="""
    You are a clinical trial eligibility specialist.

    Database name: clinicalops
    Collections: patients, trials

    STEPS:
    1. Use MongoDB MCP to query the patient by patient_id from the patients collection in the clinicalops database
    2. Use MongoDB MCP to query all active trials from the trials collection in the clinicalops database
    3. Compare patient conditions, labs, and medications against each trial's criteria
    4. Use generate_embedding for semantic similarity when criteria text is ambiguous

    OUTPUT (Markdown only, no JSON):
    - Patient summary
    - Matched trials with confidence and rationale
    - Recommended next steps
    """,
    tools=[_read_only_mcp, generate_embedding],
)

logger.info("✅ Eligibility Screener Agent initialized")

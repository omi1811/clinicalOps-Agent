# db.py
#
# MongoDB access is handled by the MongoDB MCP server through the ADK agents.
# Direct PyMongo calls have been replaced with MCP-based operations.
#
# This module is kept for any utility scripts (seed_db.py, generate_embeddings.py)
# that need a direct connection outside of the agent runtime.
#
# For all agent-level DB operations, use agents/shared_mcp.py.

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def _get_db():
    """Return a PyMongo database handle. Used only by utility scripts."""
    client = MongoClient(os.getenv("MONGODB_URI"))
    return client[os.getenv("MONGODB_DB_NAME", "clinicalops")]


def insert_adverse_event(data: dict) -> dict:
    """
    Insert an adverse event directly via PyMongo.
    Only used by utility/seed scripts — agent workflows use MCP instead.
    """
    db = _get_db()
    result = db.adverse_events.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}


def get_patient(patient_id: str) -> dict | None:
    """
    Fetch a patient record directly via PyMongo.
    Only used by utility/seed scripts — agent workflows use MCP instead.
    """
    db = _get_db()
    return db.patients.find_one({"patient_id": patient_id})

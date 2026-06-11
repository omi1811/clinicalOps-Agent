import os
import sys
import asyncio
from time import perf_counter

from dotenv import load_dotenv
from google.genai import types
from utils.logger import get_logger
      
logger = get_logger(__name__) 

started_at = perf_counter()


def log(message: str) -> None:
    elapsed = perf_counter() - started_at
    print(f"[{elapsed:6.1f}s] {message}", flush=True)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

log("Importing MongoDB MCP agent...")
from agents.mongodb_agent import root_agent

log("Importing ADK Runner and session service...")
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

log("Testing ADK v2 + MongoDB MCP integration...")
log(f"Project: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
log(f"DB: {os.getenv('MONGODB_DB_NAME')}")

session_service = InMemorySessionService()
log("Creating ADK session...")
asyncio.run(
    session_service.create_session(
        app_name="clinicalops-mcp-test",
        user_id="demo_user",
        session_id="test_session",
    )
)

log("Creating ADK Runner...")
runner = Runner(
    app_name="clinicalops-mcp-test",
    agent=root_agent,
    session_service=session_service,
)

user_message = types.Content(
    role="user",
    parts=[
        types.Part(
            text=(
                "Use MongoDB MCP to list collections, then query the patients "
                "collection with limit 1. Return only the collection names and "
                "one patient_id."
            )
        )
    ],
)

log("Agent & Session loaded. Querying MongoDB via MCP...")

response_text = ""
try:
    async def collect_response() -> str:
        collected = ""
        async for event in runner.run_async(
            user_id="demo_user",
            session_id="test_session",
            new_message=user_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    text = getattr(part, "text", "")
                    if text:
                        collected += text
        return collected

    response_text = asyncio.run(
        asyncio.wait_for(collect_response(), timeout=90)
    )

    log("Agent response preview:")
    preview = response_text[:400] + "..." if len(response_text) > 400 else response_text
    print(preview, flush=True)
    log("ADK -> MongoDB MCP integration verified!")
except Exception as exc:
    log(f"Error during run: {exc}")
    import traceback

    traceback.print_exc()

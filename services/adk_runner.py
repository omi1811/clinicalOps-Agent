# services/adk_runner.py

import asyncio
import threading
from concurrent.futures import TimeoutError

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.orchestrator import orchestrator_agent
from utils.logger import get_logger

logger = get_logger(__name__)

session_service = InMemorySessionService()

runner = Runner(
    app_name="clinicalops",
    agent=orchestrator_agent,
    session_service=session_service,
)

logger.info("Global ADK Runner initialized")

# ---- Persistent event loop (daemon thread) ----
# Keeps the MCP server subprocess alive across requests.
_loop = asyncio.new_event_loop()

def _run_loop():
    asyncio.set_event_loop(_loop)
    _loop.run_forever()

_loop_thread = threading.Thread(target=_run_loop, daemon=True)
_loop_thread.start()
logger.info("Persistent ADK event loop started")


async def _run_agent_async(user_id: str, session_id: str, message: str) -> str:
    """Run agent on the persistent event loop."""
    try:
        await session_service.create_session(
            app_name="clinicalops",
            user_id=user_id,
            session_id=session_id,
        )
    except Exception:
        pass

    content = types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )

    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text
    return response_text


def run_agent_sync(user_id: str, session_id: str, message: str, timeout: int = 300) -> str:
    """Submit agent task to the persistent loop and wait for result."""
    future = asyncio.run_coroutine_threadsafe(
        _run_agent_async(user_id, session_id, message),
        _loop,
    )
    try:
        return future.result(timeout=timeout)
    except TimeoutError:
        return "Request timed out."

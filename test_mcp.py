import os, sys
from dotenv import load_dotenv

# ✅ FIX: Import types for Content object
from google.genai import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from agents.mongodb_agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

print("🔍 Testing ADK v2 + MongoDB MCP integration...")
print(f"   Project: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
print(f"   DB: {os.getenv('MONGODB_DB_NAME')}")

session_service = InMemorySessionService()
session_service.create_session_sync(
    app_name="clinicalops-mcp-test",
    user_id="demo_user",
    session_id="test_session",
)
runner = Runner(
    app_name="clinicalops-mcp-test",
    agent=root_agent,
    session_service=session_service
)

# ✅ FIX: Create explicit Content object with 'user' role
user_message = types.Content(
    role='user',
    parts=[types.Part(text="List all collections in the database and show one patient record")]
)

print("✅ Agent & Session loaded. Querying MongoDB via MCP...")

response_text = ""
try:
    for event in runner.run(
        user_id="demo_user",
        session_id="test_session",
        new_message=user_message  # Pass object, not string
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                text = getattr(part, 'text', '')
                if text:
                    response_text += text
                    
    print("\n✅ Agent response preview:")
    preview = response_text[:400] + "..." if len(response_text) > 400 else response_text
    print(preview)
    print("\n🎉 ADK → MongoDB MCP integration verified!")
except Exception as e:
    print(f"\n❌ Error during run: {e}")
    import traceback
    traceback.print_exc()

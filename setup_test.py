# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print("🔍 Checking .env variables...")
print(f"✅ GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
print(f"✅ GOOGLE_API_KEY: {'AIza...' + os.getenv('GOOGLE_API_KEY')[6:10]}...")  # Masked
print(f"✅ MONGODB_URI: {'mongodb+srv://' in os.getenv('MONGODB_URI', '')}")
print(f"✅ MONGODB_DB_NAME: {os.getenv('MONGODB_DB_NAME')}")

# Test MongoDB connection
from pymongo import MongoClient
try:
    client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("✅ MongoDB connection: SUCCESS")
except Exception as e:
    print(f"❌ MongoDB connection: {e}")

# Test Gemini API (light check)
try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    # Just check client init, no actual call to save credits
    print("✅ Gemini API client: READY")
except Exception as e:
    print(f"⚠️  Gemini API client: {e}")
    
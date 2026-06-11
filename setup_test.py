# test_env.py
from dotenv import load_dotenv
import os
from utils.logger import get_logger
      
logger = get_logger(__name__) 

load_dotenv()

logger.info("🔍 Checking .env variables...")
logger.info(f"✅ GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
logger.info(f"✅ GOOGLE_API_KEY: {'AIza...' + os.getenv('GOOGLE_API_KEY')[6:10]}...")  # Masked
logger.info(f"✅ MONGODB_URI: {'mongodb+srv://' in os.getenv('MONGODB_URI', '')}")
logger.info(f"✅ MONGODB_DB_NAME: {os.getenv('MONGODB_DB_NAME')}")

# Test MongoDB connection
from pymongo import MongoClient
try:
    client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    logger.info("✅ MongoDB connection: SUCCESS")
except Exception as e:
    logger.info(f"❌ MongoDB connection: {e}")

# Test Gemini API (light check)
try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    # Just check client init, no actual call to save credits
    logger.info("✅ Gemini API client: READY")
except Exception as e:
    logger.info(f"⚠️  Gemini API client: {e}")
    
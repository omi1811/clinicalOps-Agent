from pymongo import MongoClient
import os
from dotenv import load_dotenv
from utils.logger import get_logger
      
logger = get_logger(__name__)  


load_dotenv()
uri = os.getenv("MONGODB_URI")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    logger.info("MongoDB Atlas connection successful!")
    logger.info(f"Available databases: {client.list_database_names()}")
except Exception as exc:
    logger.info(f"Connection failed: {exc}")

# test_connection.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # if using .env
uri = os.getenv("MONGODB_URI")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("✅ MongoDB Atlas connection successful!")
    print(f"📦 Available databases: {client.list_database_names()}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
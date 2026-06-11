# data/generate_embeddings.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from google import genai
from utils.logger import get_logger
      
logger = get_logger(__name__)  

load_dotenv()

_genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_embedding(text: str) -> list:
    """Generate embedding using Vertex AI text-embedding-004"""
    try:
        result = _genai_client.models.embed_content(
            model="models/text-embedding-004",
            contents=[text],
        )
        return result.embeddings[0].values
    except Exception as e:
        logger.info(f"Embedding failed: {e}")
        return [0.0] * 768

mongo_client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
db = mongo_client[os.getenv("MONGODB_DB_NAME", "clinicalops")]

logger.info("/ Generating embeddings...")

# Embed Trial Criteria
trials = db.trials.find()
for trial in trials:
    criteria_text = " ".join([c["text"] for c in trial.get("criteria", [])])
    embedding = get_embedding(criteria_text)
    db.trials.update_one({"_id": trial["_id"]}, {"$set": {"criteria_embedding": embedding}})
    logger.info(f"✅ Embedded criteria for {trial['trial_id']}")

# Embed Patient Summaries
patients = db.patients.find()
for pat in patients:
    summary = pat.get("summary", "")
    if summary:
        embedding = get_embedding(summary)
        db.patients.update_one({"_id": pat["_id"]}, {"$set": {"patient_embedding": embedding}})
        logger.info(f"✅ Embedded summary for {pat['patient_id']}")

logger.info("\n🎉 All embeddings generated!")
mongo_client.close()
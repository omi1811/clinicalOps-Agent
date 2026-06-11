# test_auth.py
import os
from dotenv import load_dotenv
from auth.firebase_auth import ClinicalAuth
from utils.logger import get_logger
      
logger = get_logger(__name__) 

load_dotenv()

logger.info("Testing Firebase Auth initialization...")
auth = ClinicalAuth()

# Test mock mode (if no service account loaded)
claims = auth.verify_token("dummy_token")
logger.info(f"Verified claims: {claims}")
logger.info(f"Role extraction: {auth.get_user_role(claims)}")

# If you have real Firebase setup, test custom token:
if os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH"):
    try:
        token = auth.create_custom_token("test_user_01", "coordinator")
        real_claims = auth.verify_token(token)
        logger.info(f"Real Firebase token verified: {real_claims['sub']}")
    except Exception as e:
        logger.info(f"Real token test skipped: {e}")

logger.info("\n Auth layer ready for Frontend!")

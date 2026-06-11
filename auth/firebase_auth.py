# auth/firebase_auth.py
import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from typing import Dict
from utils.logger import get_logger
      
logger = get_logger(__name__)  

class ClinicalAuth:
    """Thread-safe Firebase/JWT auth manager for ADK clinical workflows"""
    
    _initialized = False
    _mode = "mock"

    def __init__(self):
        if not ClinicalAuth._initialized:
            sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
            if sa_path and os.path.exists(sa_path):
                if not firebase_admin._apps:
                    cred = credentials.Certificate(sa_path)
                    firebase_admin.initialize_app(cred, name="clinicalops-auth")
                ClinicalAuth._mode = "prod"
                logger.info("✅ Firebase Auth initialized (Production Mode)")
            else:
                logger.info("⚠️  Firebase Auth running in LOCAL MOCK mode")
            ClinicalAuth._initialized = True

    def verify_token(self, id_token: str) -> Dict:
        """Verify token and return decoded claims"""
        if ClinicalAuth._mode == "mock":
            return {
                "sub": "demo_user",
                "email": "demo@clinicalops.local",
                "role": "coordinator",
                "auth_time": 0
            }
        
        try:
            decoded = firebase_auth.verify_id_token(id_token)
            return {
                "sub": decoded.get("sub"),
                "email": decoded.get("email"),
                "role": decoded.get("role", "viewer"),
                "auth_time": decoded.get("auth_time")
            }
        except Exception as e:
            raise ValueError(f"Auth verification failed: {e}")

    @staticmethod
    def get_user_role(claims: Dict) -> str:
        return claims.get("role", "viewer")

    def create_custom_token(self, uid: str, role: str = "viewer") -> str:
        if ClinicalAuth._mode == "mock":
            return "mock_token_for_local_dev"
        return firebase_auth.create_custom_token(uid, {"role": role}).decode("utf-8")
import os
import sys

# Ensure root and backend directory are in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

class Settings:
    PROJECT_NAME: str = "POLARIS - Polar Knowledge & Outreach Intelligence System"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    SECRET_KEY: str = "polaris_sih26063_super_secret_jwt_key_ncpor_moes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    DATABASE_PATH: str = os.path.join(BASE_DIR, "database", "polaris.db")
    
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

settings = Settings()

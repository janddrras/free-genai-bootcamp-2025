from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Language Learning Portal"
    
    # CORS Origins
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./words.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Ensure the database directory exists
db_path = Path(settings.DATABASE_URL.replace("sqlite:///", "")).parent
db_path.mkdir(parents=True, exist_ok=True) 
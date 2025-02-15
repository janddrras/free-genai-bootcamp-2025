from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./words.db"
    DATABASE_CONNECT_DICT: dict = {"check_same_thread": False}
    
    # API settings
    API_TITLE: str = "Language Learning Portal API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for managing language learning, study sessions, and vocabulary"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

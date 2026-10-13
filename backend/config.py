import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Adaptive DSA Recommendation Engine"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "adaptive-dsa-super-secret-key-change-in-production-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # Default to SQLite aiosqlite for zero-setup execution, supports PostgreSQL asyncpg seamlessly
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite+aiosqlite:///./dsa_adaptive.db"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

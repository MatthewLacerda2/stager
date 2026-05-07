from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Stager"
    
    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None  # Optional, only needed for tests
    
    model_config = SettingsConfigDict(
        case_sensitive=True, 
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    """
    PROJECT_NAME: str = "Fig API Core"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "dev"
    
    # Required
    INTERNAL_API_KEY: str 
    DATABASE_URL: str
    
    # Header configuration
    INTERNAL_API_KEY_HEADER_NAME: str = "X-Internal-Token"
    
    # Security
    INTERNAL_API_KEY: str # Must be set in .env
    
    # Optional - Pydantic won't complain if these are missing now
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    
    # Model configuration tells Pydantic how to load the settings
    model_config = SettingsConfigDict(
        # Look for a .env file to load variables
        env_file=".env",
        # Case insensitive matching (DATABASE_URL matches database_url)
        case_sensitive=False
    )

# Instantiate the settings object to be imported across the application
settings = Settings()
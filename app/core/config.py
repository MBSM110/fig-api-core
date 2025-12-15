from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    """
    # Define the core database URL using a Pydantic type for validation
    # This expects the format: postgresql+asyncpg://user:password@host/dbname
    DATABASE_URL: PostgresDsn

    # Model configuration tells Pydantic how to load the settings
    model_config = SettingsConfigDict(
        # Look for a .env file to load variables
        env_file=".env",
        # Case insensitive matching (DATABASE_URL matches database_url)
        case_sensitive=False
    )

# Instantiate the settings object to be imported across the application
settings = Settings()
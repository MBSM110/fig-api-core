from fastapi import FastAPI
# Import the settings object
from app.core.config import settings

# Initialize the application
app = FastAPI(
    title="Fig API Core",
    description="Backend API for the Fig Crypto Analysis Platform",
    version="1.0.0"
)

# Optional: Print the database URL (hidden portion) on startup to verify loading
# DO NOT DO THIS IN PRODUCTION! We are doing it now for a quick test.
print(f"Loading DB URL (first 20 chars): {str(settings.DATABASE_URL)[:20]}...")


@app.get("/")
def health_check():
    """
    Root endpoint to verify the API is running.
    """
    # You can now access config variables safely:
    return {"status": "ok", "project": settings.title}
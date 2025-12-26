from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.logging import setup_logging
from app.core.config import settings

# 1. Initialize professional logging
setup_logging()

# 2. Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Professional Crypto Analysis API Core",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 3. Include the modular API Router
# This replaces all your old @app.get and @app.post lines
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Infrastructure"])
def health_check():
    """
    Standard health check for Docker/Kubernetes orchestration.
    """
    return {
        "status": "healthy", 
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION
    }
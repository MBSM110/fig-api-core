from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings
from app.core.security import validate_internal_access

# We use Security/APIKeyHeader instead of Header to make the 'Authorize' button work
api_key_header = APIKeyHeader(
    name=settings.INTERNAL_API_KEY_HEADER_NAME, 
    auto_error=False
)

async def get_internal_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency that:
    1. Triggers the padlock/Authorize button in Swagger.
    2. Pulls the token from the header defined in settings.
    3. Validates it via our security logic.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required header: {settings.INTERNAL_API_KEY_HEADER_NAME}"
        )
    
    validate_internal_access(api_key)
    
    return api_key
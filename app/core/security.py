import secrets
from fastapi import HTTPException, status
from app.core.config import settings

def verify_api_key(provided_key: str) -> bool:
    """
    Performs a constant-time string comparison to prevent timing attacks.
    This is the standard way to compare secrets in professional apps.
    """
    if not provided_key:
        return False
        
    # secrets.compare_digest protects against side-channel timing attacks
    return secrets.compare_digest(provided_key, settings.INTERNAL_API_KEY)

def validate_internal_access(api_key: str):
    """
    High-level validation that raises the 403 error if the key is wrong.
    """
    if not verify_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate internal service credentials",
        )
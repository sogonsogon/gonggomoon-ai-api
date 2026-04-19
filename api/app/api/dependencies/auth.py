from fastapi import HTTPException, status
from app.core.config import get_settings

INTERNAL_API_KEY = get_settings().internal_api_key

def verify_internal_api_key(x_internal_api_key: str | None) -> None:
    if x_internal_api_key != INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid internal API key.",
        )

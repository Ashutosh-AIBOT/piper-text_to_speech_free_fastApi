from fastapi import HTTPException, Header
from typing import Optional

from app.config import settings

async def verify_password(authorization: Optional[str] = Header(None)):
    """
    Simple password authentication
    Expects password in Authorization header
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )
    
    if authorization != settings.API_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    
    return authorization

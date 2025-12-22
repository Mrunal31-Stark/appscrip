from fastapi import Security, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

# Rate Limiter Configuration
# Uses the client's IP address to track usage
limiter = Limiter(key_func=get_remote_address)

# Simple API Key Authentication
# Expects header "x-api-key"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

    
async def verify_api_key(api_key_header: str = Security(api_key_header)):  # Verifies the existence and validity of the API key in the request header.           
    
    if not api_key_header:
         raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials: API Key missing"
        )
    
    if api_key_header != settings.API_SECRET_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials: Invalid API Key"
        )
    return api_key_header

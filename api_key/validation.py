import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader

# * API KEY SETUP
api_key_header = APIKeyHeader(name="X-API-KEY")

# create a dependency that checks for the API key in incoming requests.
async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API key",
        )

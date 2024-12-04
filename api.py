import os

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from contextlib import asynccontextmanager
import ray

from routers import user, onboarding

from utils.parse_date import GOOGLE_SEARCH_DATE_FORMAT

from api_key.validation import verify_api_key

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Ray when the app starts
    env_vars = {k: str(v) for k, v in os.environ.items()}
    env_vars["RAY_DEDUP_LOGS"] = "0"
    ray.init(runtime_env={"env_vars": env_vars})
    yield
    # Shutdown Ray when the app stops
    ray.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(onboarding.router)


# ! Test AUTH end point
@app.get("/test-auth/", dependencies=[Depends(verify_api_key)])
async def test_auth():
    return {"message": "Authentication successful"}


# @app.get("/")
# async def root():
#     return {"message": "Hoja Juank"}

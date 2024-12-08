import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from contextlib import asynccontextmanager
import ray
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from motor.motor_asyncio import AsyncIOMotorClient
from routers import user, onboarding, core_agent
from agents.core.CoreAgent import CoreAgent
from api_key.validation import verify_api_key

# Initialize MongoDB client
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.your_database_name  # Replace with your actual database name

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Ray when the app starts
    env_vars = {k: str(v) for k, v in os.environ.items()}
    env_vars["RAY_DEDUP_LOGS"] = "0"
    ray.init(runtime_env={"env_vars": env_vars})
    
    # Initialize CoreAgent and scheduler
    core_agent = CoreAgent()
    scheduler = AsyncIOScheduler()
    
    # Schedule the core agent to run every 2 minutes (for testing)
    # TODO: Change to 1 hour in production using:
    scheduler.add_job(core_agent.process_all_users, 'interval', hours=24)
    # scheduler.add_job(core_agent.process_all_users, 'interval', minutes=5)
    
    # Start the scheduler
    scheduler.start()
    
    yield
    
    # Cleanup
    scheduler.shutdown()
    ray.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(onboarding.router)
app.include_router(core_agent.router)

@app.get("/test-auth/", dependencies=[Depends(verify_api_key)])
async def test_auth():
    return {"message": "Authentication successful"}

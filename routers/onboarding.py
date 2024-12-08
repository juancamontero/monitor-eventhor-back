import os

from time import time
from typing import Dict, List


from api_key.validation import verify_api_key

# import psutil

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import APIKeyHeader
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tqdm import tqdm


from agents.onboarding_agent.OnboardingChat import OnboardingAgent
from utils.user_utils import get_active_users_onboarded
from db.models.user import UserModel

# Define the structure of the input data using Pydantic models for data validation
class OnboardingData(BaseModel):
    model: str
    messages: list
    beforeTimestamp: int | None = None


router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"],
    responses={
        status.HTTP_404_NOT_FOUND: {"message": "NOT FOUND - Onboarding end point"}
    },
    dependencies=[Depends(verify_api_key)],
)

@router.post("/")
async def onboarding_endpoint(data: OnboardingData):
    # Create instance of agent
    onboarding_agent = OnboardingAgent(
        model=data.model,
        beforeTimestamp=data.beforeTimestamp,
    )

    response = await onboarding_agent.completions(data.messages)

    return StreamingResponse(response, media_type="application/json")

@router.get("/active-users", response_model=List[UserModel])
async def get_active_onboarded_users():
    """
    Get a list of all active users who have completed onboarding.
    
    Returns:
        List[UserModel]: List of active users who have completed onboarding
    """
    return await get_active_users_onboarded()

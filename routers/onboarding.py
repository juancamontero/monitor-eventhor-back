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

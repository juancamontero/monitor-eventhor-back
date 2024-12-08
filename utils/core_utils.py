from datetime import datetime, timedelta, timezone
from typing import List
from db.models.user import UserModel
from db.models.onboarding import Question
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.client import users_collection, questions_collection

async def get_active_onboarded_users() -> List[dict]:
    """Get all active users who have completed onboarding"""
    users = await users_collection.find({
        "isActive": True,
        "hasCompletedOnboarding": True
    }).to_list(length=None)
    return users

async def get_pending_questions(user_id: str) -> List[dict]:
    """Get questions that need to be processed for a user"""
    current_date = datetime.now(timezone.utc)
    questions = await questions_collection.find({
        "userId": user_id,
        "$or": [
            {"nextsResponseDate": None},
            {"nextsResponseDate": {"$lte": current_date}}
        ]
    }).to_list(length=None)
    return questions

async def update_question_next_response(
    question_id: str, 
    search_interval: int
):
    """Update the nextResponseDate for a question"""
    next_date = datetime.now(timezone.utc) + timedelta(hours=search_interval)
    await questions_collection.update_one(
        {"_id": question_id},
        {"$set": {"nextsResponseDate": next_date}}
    )
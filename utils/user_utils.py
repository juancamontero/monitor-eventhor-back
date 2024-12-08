from typing import Optional, List
from fastapi import HTTPException, status
from db.models.user import UserModel
from db.client import users_collection

async def check_user_active(user_id: str) -> bool:
    """
    Check if a user is active in the system.
    
    Args:
        user_id (str): The ID of the user to check
        
    Returns:
        bool: True if the user is active, False otherwise
        
    Raises:
        HTTPException: If the user is not found or if the user is not active
    """
    user_data = await users_collection.find_one({"_id": user_id})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    user = UserModel(**user_data)
    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active"
        )
    
    return True

async def get_user_by_id(user_id: str) -> Optional[UserModel]:
    """
    Retrieve a user by their ID.
    
    Args:
        user_id (str): The ID of the user to retrieve
        
    Returns:
        Optional[User]: The user if found, None otherwise
    """
    user_data = await users_collection.find_one({"_id": user_id})
    if user_data:
        return UserModel(**user_data)
    return None 

async def get_active_users_onboarded() -> List[UserModel]:
    """
    Retrieve all active users from the database who have completed onboarding.
    
    Returns:
        List[UserModel]: A list of active users who have completed onboarding
    """
    cursor = users_collection.find({
        "isActive": True,
        "hasCompletedOnboarding": True
    })
    active_users = []
    async for user_data in cursor:
        active_users.append(UserModel(**user_data))
    return active_users

###OLD -  Users DB API ###

# https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/

from fastapi import APIRouter, Body, HTTPException, status

from db.client import users_collection
from db.models.user import UserModel

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found!"}},
)


@router.post(
    "/",
    response_description="Add user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserModel = Body(...)):
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude={"id"})
    )
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return created_user


@router.get("/test/")
def test():
    return {"message": "Hello! You are in the users router"}

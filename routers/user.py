### Users DB API ###

from fastapi import APIRouter, Body, HTTPException, status

from db.client import user_collection
from db.models.user import UserModel

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not founder ni rent"}},
)


@router.post(
    "/",
    response_description="Create a new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserModel = Body(...)):
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude={"id"})
    )
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return created_user


@router.get("/test/")
def test():
    return {"message": "Hello Testing world"}

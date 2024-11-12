# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### User model ###

from typing import Optional, List, Annotated
from pydantic import BaseModel, BeforeValidator, Field, EmailStr

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    """
    Basis user information to handle auth and payments / state
    """

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    name: str = Field(...)
    email: EmailStr = Field(...)


class UpdateUserModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    users: List[UserModel]

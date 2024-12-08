from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, field_model):
        field_schema.update(type="string")
        return field_schema

class UserRole(str, Enum):
    SUPER = "super"
    ADMIN = "admin"
    USER = "user"

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    emailVerified: Optional[datetime] = None
    isActive: bool = False
    role: List[UserRole] = [UserRole.USER]
    image: Optional[str] = None
    hasCompletedOnboarding: bool = False
    firstReporgenerated: bool = False
    availableForecasts: Optional[int] = 10
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

class Account(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: str
    type: str
    provider: str
    providerAccountId: str
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    expires_at: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    session_state: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

class Session(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sessionToken: str
    userId: str
    expires: datetime
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

class VerificationToken(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    identifier: str
    token: str
    expires: datetime

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

class Authenticator(BaseModel):
    credentialID: str = Field(..., alias="_id")
    userId: str
    providerAccountId: str
    credentialPublicKey: str
    counter: int
    credentialDeviceType: str
    credentialBackedUp: bool
    transports: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True 
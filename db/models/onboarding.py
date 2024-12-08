from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
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

class Question(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    topicId: Optional[str] = None
    userId: Optional[str] = None
    question_text: str
    event_type: str
    search_interval: int = 24
    report_interval: int = 168
    nextsResponseDate: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

class Topic(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: Optional[str] = None
    topicText: Optional[str] = None
    keyActors: List[str] = []
    report_interval: int = 168
    nextReportDate: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True 
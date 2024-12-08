from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
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

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ForecastState(str, Enum):
    NEW = "new"
    PARSED = "parsed"

class Message(BaseModel):
    content: str
    role: Role

class Forecast(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: Optional[str] = None
    name: Optional[str] = None
    emails: List[str] = []
    messages: List[Message] = []
    sources: Dict[str, Any] = Field(default_factory=dict)
    settings: Dict[str, Any]
    relatedForecasts: Dict[str, Any] = Field(default_factory=dict)
    answerProbability: Optional[float] = None
    state: ForecastState = ForecastState.NEW
    public: bool = False
    extraInfo: Dict[str, Any] = Field(default_factory=dict)
    questionId: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

class Source(BaseModel):
    id: str = Field(..., alias="_id")
    query: str
    title: Optional[str] = None
    favicon: Optional[str] = None
    snippet: Optional[str] = None
    link: Optional[str] = None
    summarized_content: Optional[str] = None
    date: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class Benchmark(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    benchmarkType: Optional[str] = None
    question: str
    backgroundText: Optional[str] = None
    category: Optional[str] = None
    beforeTimestamp: Optional[int] = None
    resolution: Optional[float] = None
    predictions: Optional[Dict[str, Any]] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True 
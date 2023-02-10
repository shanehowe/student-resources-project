from pydantic import BaseModel, Field
from bson import ObjectId
from models.pyobjectId import PyObjectId
from typing import Optional, Any
from dotenv import load_dotenv

import os


load_dotenv("../.env")
X_RapidAPI_Key = os.getenv("X_RapidAPI_Key")
X_RapidAPI_Host = os.getenv("X_RapidAPI_Host")

class CodeSubmission(BaseModel):
    functionName: str
    sourceCode: str
    sampleInput: Optional[str]


class ChallengeDocument(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    functionName: str
    boilerPlateCode: str
    prompt: str
    examples: list[dict]
    sampleInput: Any
    assumptions: Optional[list[str]]
    category: str

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from models.pyobjectId import PyObjectId


class UserDocument(BaseModel):
    name: str
    username: str
    email: EmailStr
    passwordHash: str
    resourcePosts: list = []

class UserIn(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    username: str
    resourcePosts: Optional[list]

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }


class UserLoginIn(BaseModel):
    username: str
    password: str


class UserLogin(UserOut):
    passwordHash: str
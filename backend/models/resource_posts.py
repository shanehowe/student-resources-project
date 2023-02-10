from typing import Optional, Union
from pydantic import BaseModel, Field
from bson import ObjectId
from models.pyobjectId import PyObjectId


class PostUserPopulater(BaseModel):
    """
    Used to populate user field in resource post
    """
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    username: str

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

class ResourcePostIn(BaseModel):
    """
    To be used on incoming POST request
    """
    title: str
    description: str
    url: str
    moduleName: str
    semester: int
    user: Union[Optional[PyObjectId], Optional[PostUserPopulater]]
    tags: Optional[list[str]] = []


class ResourcePostOut(BaseModel):
    """
    To be used on outgoing GET request
    """
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    title: str
    description: str
    url: str 
    moduleName: str
    semester: int
    user: Union[Optional[ObjectId], PostUserPopulater]
    tags: Optional[list[str]]

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }


class UpdateResourcePost(BaseModel):
    """
    To be used on incoming PUT request
    """
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    moduleName: Optional[str]
    semester: Optional[int]
    user: Optional[PyObjectId]
    tags: Optional[list[str]]

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }


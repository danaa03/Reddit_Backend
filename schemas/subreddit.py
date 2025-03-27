from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal
import re

class SubredditCreate(BaseModel):
    name: str 
    description: str

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("Subreddit name must be at least 3 characters long.")
        return value

class SubredditResponse(BaseModel):
    id: str
    name: str   
    description: str

    class Config:
        from_attributes = True

class SubredditUpdateStatus(BaseModel):
    status : Literal["public", "private"] = "public"
    subreddit_id: str

class SubredditUpdateDescription(BaseModel):
    description: str
    subreddit_id: str
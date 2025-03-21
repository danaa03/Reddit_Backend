from pydantic import BaseModel
from typing import Literal

class UserSubredditBase(BaseModel):
    role: Literal["member", "moderator"] = "member"

class UserSubredditCreate(UserSubredditBase):
    user_id: str
    subreddit_id: str

class UserSubredditResponse(UserSubredditBase):
    user_id: str
    subreddit_id: str

    class Config:
        from_attributes = True 


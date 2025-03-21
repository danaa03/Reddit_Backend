from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    subreddit_id: str

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: str
    user_id: str
    upvotes: int
    downvotes: int
    created_at: datetime

    class Config:
        from_attributes = True  

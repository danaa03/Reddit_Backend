from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: str
    parent_comment_id: Optional[str] = None
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: str
    post_id: str
    user_id: str
    upvotes: int
    downvotes: int
    parent_comment_id: Optional[str]
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  

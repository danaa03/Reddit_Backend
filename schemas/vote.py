from pydantic import BaseModel, model_validator
from typing import Optional, Literal

class VoteCreate(BaseModel):
    post_id: Optional[str] = None
    comment_id: Optional[str] = None
    vote_type: Literal['upvote', 'downvote']  

    @model_validator(mode="before")
    def validate_target(cls, values):
        post_id = values.get("post_id")
        comment_id = values.get("comment_id")

        if (post_id and comment_id) or (not post_id and not comment_id):
            raise ValueError("You can provide either post_id or comment_id, not both.")
        
        return values
    
class CheckVote(BaseModel):
    post_id: Optional[str] = None
    comment_id: Optional[str] = None

    @model_validator(mode="before")
    def validate_target(cls, values):
        post_id = values.get("post_id")
        comment_id = values.get("comment_id")

        if (post_id and comment_id) or (not post_id and not comment_id):
            raise ValueError("You can provide either post_id or comment_id, not both.")
        
        return values

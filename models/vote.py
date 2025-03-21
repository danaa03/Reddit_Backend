from sqlalchemy import Column, String, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import uuid

class Vote(Base):
    __tablename__ = "votes"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    post_id = Column(String, ForeignKey("posts.id"), nullable=True)
    comment_id = Column(String, ForeignKey("comments.id"), nullable=True)
    vote_type = Column(Enum("upvote", "downvote", name="vote_enum"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")
    comment = relationship("Comment")

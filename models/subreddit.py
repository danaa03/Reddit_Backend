from sqlalchemy import Column, String, ForeignKey, Enum, TIMESTAMP, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base
from models.user_subreddit import UserSubreddit

class Subreddit(Base):
    __tablename__ = "subreddits"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum("public", "private", name="subreddit_status"), default="public")
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #one subreddit has many posts
    posts = relationship("Post", back_populates="subreddit", cascade="all, delete-orphan")  

    # Many-to-Many Relationship with User
    user_subreddits = relationship("UserSubreddit", back_populates="subreddit")

    # One-to-Many: A subreddit is created by one user
    creator = relationship("User", back_populates="created_subreddits")
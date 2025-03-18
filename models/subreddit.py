from sqlalchemy import Column, String, ForeignKey, Enum, TIMESTAMP, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Subreddit(Base):
    __tablename__ = "subreddits"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    creator = relationship("User", back_populates="subreddits")  
    posts = relationship("Post", back_populates="subreddit", cascade="all, delete-orphan")  
    members = relationship("UserSubreddit", back_populates="subreddit")  

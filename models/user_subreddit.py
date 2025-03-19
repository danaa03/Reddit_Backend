from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base

class UserSubreddit(Base):
    __tablename__ = "user_subreddit"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    subreddit_id = Column(String, ForeignKey("subreddits.id"), primary_key=True)
    role = Column(Enum("member", "moderator", name="role_enum"), nullable=False, default="member")

    user = relationship("User", back_populates="user_subreddits")
    subreddit = relationship("Subreddit", back_populates="user_subreddits")
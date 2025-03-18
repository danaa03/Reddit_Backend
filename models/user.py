from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    karma = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    votes = relationship("Vote", back_populates="user")
    messages_sent = relationship("DirectMessage", foreign_keys="DirectMessage.sender_id")
    messages_received = relationship("DirectMessage", foreign_keys="DirectMessage.receiver_id")
    notifications = relationship("Notification", back_populates="user")

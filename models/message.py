from sqlalchemy import Column, String, Text, ForeignKey, Integer, TIMESTAMP
from datetime import datetime
from database import Base

class DirectMessage(Base):
    __tablename__ = "direct_messages"

    id = Column(String, primary_key=True, index=True)
    sender_id = Column(String, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_read = Column(Integer, default=0)

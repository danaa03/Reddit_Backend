from sqlalchemy import Column, String, Text, ForeignKey, Integer, TIMESTAMP
from datetime import datetime
from database import Base
import uuid

class DirectMessage(Base):
    __tablename__ = "direct_messages"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(String, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_read = Column(Integer, default=0)

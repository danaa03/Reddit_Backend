from sqlalchemy import Column, String, ForeignKey, Enum, TIMESTAMP, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(Enum("vote", "comment", "message", name="notification_type_enum"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_read = Column(Integer, default=0)

    user = relationship("User", back_populates="notifications")

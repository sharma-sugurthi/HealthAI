"""
Chat history model for storing conversation messages.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from .user import Base


class ChatHistory(Base):
    """Chat history model for storing user conversations with AI"""

    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="chat_history")

    # Indexes for performance
    __table_args__ = (Index("idx_user_timestamp", "user_id", "timestamp"),)

    def __repr__(self) -> str:
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, timestamp='{self.timestamp}')>"

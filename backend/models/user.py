"""
User model for authentication and user management.
"""

from datetime import datetime

import bcrypt
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model for authentication and profile management"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    treatment_plans = relationship(
        "TreatmentPlan", back_populates="user", cascade="all, delete-orphan"
    )
    health_metrics = relationship(
        "HealthMetric", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verify password"""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', full_name='{self.full_name}')>"

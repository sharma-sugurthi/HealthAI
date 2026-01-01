"""
Pydantic schemas for user-related requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    """Base user schema"""

    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., max_length=20)


class UserCreate(UserBase):
    """Schema for user registration"""

    password: str = Field(..., min_length=6, max_length=100)

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.replace("_", "").isalnum(), "Username must be alphanumeric"
        return v


class UserLogin(BaseModel):
    """Schema for user login"""

    username: str
    password: str


class UserResponse(UserBase):
    """Schema for user response"""

    id: int

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for token response"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh"""

    refresh_token: str

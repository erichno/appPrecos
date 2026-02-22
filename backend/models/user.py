from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    city_id: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    password_hash: str
    reputation_score: int = 0
    role: str = "user"  # user | moderator | admin
    favorites: dict = Field(default_factory=lambda: {"products": [], "supermarkets": []})
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserResponse(UserBase):
    id: str
    reputation_score: int
    role: str
    favorites: dict
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

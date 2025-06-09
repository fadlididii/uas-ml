from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# Re-export User model from auth for consistency
from app.auth.models import User, UserBase, UserCreate, UserRead, UserUpdate


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    
    id: UUID = Field(primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    bio: Optional[str] = Field(default=None, max_length=500)
    avatar_url: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None, max_length=20)
    date_of_birth: Optional[datetime] = Field(default=None)
    location: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class UserProfileCreate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    location: Optional[str] = None
    website: Optional[str] = None


class UserProfileRead(SQLModel):
    id: UUID
    user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserProfileUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    location: Optional[str] = None
    website: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserWithProfile(UserRead):
    profile: Optional[UserProfileRead] = None
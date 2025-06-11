from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


class UserListResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserProfileRequest(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=100)

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Invalid phone number format')
        return v


class UserProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    location: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserWithProfileResponse(UserDetailResponse):
    profile: Optional[UserProfileResponse] = None


class UsersListResponse(BaseModel):
    users: List[UserListResponse]
    total: int
    page: int
    size: int
    pages: int


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=100)
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class MessageResponse(BaseModel):
    message: str
    success: bool = True
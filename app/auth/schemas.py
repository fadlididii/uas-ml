from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    date_of_birth: datetime
    gender: GenderEnum
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v):
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: GenderEnum
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(BaseModel):
    user: UserResponse
    token: TokenResponse
    preferences_status: Optional[dict] = None


class MessageResponse(BaseModel):
    message: str
    success: bool = True


class RegisterResponse(BaseModel):
    message: str
    success: bool = True
    user: UserResponse


class ProfileStatusResponse(BaseModel):
    is_complete: bool
    missing_fields: List[str]
    redirect_to: str


class UserWithProfileStatusResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: GenderEnum
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    profile_status: ProfileStatusResponse
    
    class Config:
        from_attributes = True
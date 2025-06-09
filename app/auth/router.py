from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from datetime import timedelta

from app.database import get_session
from app.auth.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    AuthResponse,
    UserResponse,
    TokenResponse,
    MessageResponse
)
from app.auth.service import auth_service
from app.auth.dependencies import get_current_active_user
from app.auth.models import User
from app.config import settings


router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def register(
    user_data: UserRegisterRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Register a new user"""
    # Create user
    user = await auth_service.create_user(session, user_data)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    # Prepare response
    user_response = UserResponse.model_validate(user)
    token_response = TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return AuthResponse(
        user=user_response,
        token=token_response
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login user",
    description="Authenticate user with email and password"
)
async def login(
    login_data: UserLoginRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Login user"""
    # Authenticate user
    user = await auth_service.authenticate_user(session, login_data)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    # Prepare response
    user_response = UserResponse.model_validate(user)
    token_response = TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return AuthResponse(
        user=user_response,
        token=token_response
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user information"
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get current user information"""
    return UserResponse.model_validate(current_user)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user",
    description="Logout current user (client should discard the token)"
)
async def logout(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Logout user"""
    # In a stateless JWT system, logout is handled client-side
    # The client should discard the token
    # For more security, you could implement a token blacklist
    return MessageResponse(
        message="Logout successful. Please discard your access token.",
        success=True
    )
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
    MessageResponse,
    RegisterResponse,
    ProfileStatusResponse,
    UserWithProfileStatusResponse
)
from app.auth.service import auth_service
from app.auth.dependencies import get_current_active_user
from app.auth.models import User
from app.config import settings
from app.preferences.service import preferences_service

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with complete profile information",
    responses={
        201: {"description": "User successfully registered"},
        400: {"description": "Invalid input data"},
        409: {"description": "Email already exists"},
        422: {"description": "Validation error"}
    }
)
async def register(
    user_data: UserRegisterRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Register a new user with complete profile information"""
    try:
        # Create user
        user = await auth_service.create_user(session, user_data)
        
        # Prepare response
        user_response = UserResponse.model_validate(user)
        
        return RegisterResponse(
            message="User registered successfully",
            success=True,
            user=user_response
        )
    
    except Exception as e:
        # Re-raise the exception to be handled by FastAPI's exception handlers
        raise e


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
    
    # Check preferences completion status
    preferences_status = await preferences_service.check_preferences_completion(
        session, user.id
    )
    
    return AuthResponse(
        user=user_response,
        token=token_response,
        preferences_status=preferences_status
    )


@router.get(
    "/me",
    response_model=UserWithProfileStatusResponse,
    summary="Get current user with profile status",
    description="Get current authenticated user information with profile completeness status"
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Get current user information with profile status"""
    from app.users.service import user_service
    
    # Get profile completeness status
    profile_status = await user_service.check_profile_completeness(session, current_user.id)
    
    # Create response with profile status
    user_data = UserResponse.model_validate(current_user).model_dump()
    user_data["profile_status"] = ProfileStatusResponse(**profile_status)
    
    return UserWithProfileStatusResponse(**user_data)


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
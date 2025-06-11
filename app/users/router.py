from fastapi import APIRouter, Depends, HTTPException, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from uuid import UUID
import math
import os
from datetime import datetime

from app.database import get_session
from app.users.schemas import (
    UserListResponse,
    UserDetailResponse,
    UserUpdateRequest,
    UserProfileRequest,
    UserProfileResponse,
    UserWithProfileResponse,
    UsersListResponse,
    PasswordChangeRequest,
    MessageResponse
)
from app.users.service import user_service
from app.users.dependencies import (
    get_user_by_id,
    get_user_or_current,
    validate_user_access,
    validate_superuser_access,
    get_pagination_params,
    PaginationParams
)
from app.auth.dependencies import get_current_active_user, get_current_superuser
from app.auth.models import User


router = APIRouter()


@router.get(
    "/",
    response_model=UsersListResponse,
    summary="Get users list",
    description="Get paginated list of users (superuser only)"
)
async def get_users(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_superuser)],
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """Get list of users with pagination"""
    users, total = await user_service.get_users(
        session=session,
        skip=pagination.skip,
        limit=pagination.limit,
        is_active=is_active
    )
    
    pages = math.ceil(total / pagination.size) if total > 0 else 1
    
    return UsersListResponse(
        users=[UserListResponse.model_validate(user) for user in users],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages
    )


@router.get(
    "/{user_id}",
    response_model=UserDetailResponse,
    summary="Get user by ID",
    description="Get user details by ID"
)
async def get_user(
    user: Annotated[User, Depends(get_user_by_id)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get user by ID"""
    # Users can view their own profile, superusers can view any profile
    if user.id != current_user.id and not current_user.is_superuser:
        # Return limited information for other users
        return UserListResponse.model_validate(user)
    
    return UserDetailResponse.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserDetailResponse,
    summary="Update user",
    description="Update user information"
)
async def update_user(
    user_id: Annotated[UUID, Depends(validate_user_access)],
    user_data: UserUpdateRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Update user information"""
    updated_user = await user_service.update_user(
        session=session,
        user_id=user_id,
        user_data=user_data,
        current_user=current_user
    )
    
    return UserDetailResponse.model_validate(updated_user)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Delete user",
    description="Delete user (superuser only)"
)
async def delete_user(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_superuser)]
):
    """Delete user (soft delete)"""
    await user_service.delete_user(
        session=session,
        user_id=user_id,
        current_user=current_user
    )
    
    return MessageResponse(
        message="User deleted successfully",
        success=True
    )


@router.post(
    "/{user_id}/change-password",
    response_model=MessageResponse,
    summary="Change user password",
    description="Change user password"
)
async def change_password(
    user_id: Annotated[UUID, Depends(validate_user_access)],
    password_data: PasswordChangeRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Change user password"""
    await user_service.change_password(
        session=session,
        user_id=user_id,
        password_data=password_data,
        current_user=current_user
    )
    
    return MessageResponse(
        message="Password changed successfully",
        success=True
    )


@router.get(
    "/{user_id}/profile",
    response_model=UserProfileResponse,
    summary="Get user profile",
    description="Get user profile information"
)
async def get_user_profile(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get user profile"""
    profile = await user_service.get_user_profile(session, user_id)
    if not profile:
        # Return empty profile structure
        return UserProfileResponse(
            id=user_id,
            user_id=user_id,
            created_at=current_user.created_at
        )
    
    return UserProfileResponse.model_validate(profile)


@router.put(
    "/{user_id}/profile",
    response_model=UserProfileResponse,
    summary="Update user profile",
    description="Update user profile information"
)
async def update_user_profile(
    user_id: Annotated[UUID, Depends(validate_user_access)],
    profile_data: UserProfileRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Update user profile"""
    profile = await user_service.update_user_profile(
        session=session,
        user_id=user_id,
        profile_data=profile_data,
        current_user=current_user
    )
    
    return UserProfileResponse.model_validate(profile)


@router.get(
    "/{user_id}/with-profile",
    response_model=UserWithProfileResponse,
    summary="Get user with profile",
    description="Get user information along with profile data"
)
async def get_user_with_profile(
    user: Annotated[User, Depends(get_user_or_current)],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get user with profile information"""
    # Get user profile
    profile = await user_service.get_user_profile(session, user.id)
    
    # Create response
    user_response = UserDetailResponse.model_validate(user)
    profile_response = UserProfileResponse.model_validate(profile) if profile else None
    
    return UserWithProfileResponse(
        **user_response.model_dump(),
        profile=profile_response
    )


@router.post(
    "/{user_id}/upload-avatar",
    response_model=UserProfileResponse,
    summary="Upload user avatar",
    description="Upload user profile picture"
)
async def upload_avatar(
    user_id: Annotated[UUID, Depends(validate_user_access)],
    file: UploadFile,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Upload user avatar"""
    # Check file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save file to static/img/avatars directory
    filename = f"{user_id}_{datetime.utcnow().timestamp()}{os.path.splitext(file.filename)[1]}"
    file_path = f"static/img/avatars/{filename}"
    
    # Create directory if it doesn't exist
    os.makedirs("static/img/avatars", exist_ok=True)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Update user profile with avatar URL
    profile_data = UserProfileRequest(avatar_url=f"/static/img/avatars/{filename}")
    profile = await user_service.update_user_profile(
        session=session,
        user_id=user_id,
        profile_data=profile_data,
        current_user=current_user
    )
    
    return UserProfileResponse.model_validate(profile)
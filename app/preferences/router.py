from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.database import get_session
from app.auth.dependencies import get_current_active_user
from app.auth.models import User
from app.preferences.models import (
    UserPreferencesRead,
    UserPreferencesCreate,
    UserPreferencesUpdate
)
from app.preferences.service import preferences_service

router = APIRouter()


@router.get(
    "/status",
    response_model=dict,
    summary="Get user preferences completion status",
    description="Check which parts of preferences test are completed"
)
async def get_preferences_status(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Get user preferences completion status"""
    status_data = await preferences_service.check_preferences_completion(
        session, current_user.id
    )
    return {
        "message": "Preferences status retrieved successfully",
        "data": status_data,
        "success": True
    }


@router.get(
    "/",
    response_model=dict,
    summary="Get user preferences",
    description="Get current user's preferences data"
)
async def get_user_preferences(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Get user preferences"""
    preferences = await preferences_service.get_user_preferences(
        session, current_user.id
    )
    
    if not preferences:
        return {
            "message": "No preferences found",
            "data": None,
            "success": True
        }
    
    preferences_data = UserPreferencesRead.model_validate(preferences)
    return {
        "message": "Preferences retrieved successfully",
        "data": preferences_data,
        "success": True
    }


@router.post(
    "/basic",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Update basic preferences",
    description="Update basic preferences (Questions 1-13)"
)
async def update_basic_preferences(
    preferences_data: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Update basic preferences (Q1-13)"""
    updated_preferences = await preferences_service.update_basic_preferences(
        session, current_user.id, preferences_data
    )
    
    preferences_response = UserPreferencesRead.model_validate(updated_preferences)
    return {
        "message": "Basic preferences updated successfully",
        "data": preferences_response,
        "success": True
    }


@router.post(
    "/text",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Update text preferences",
    description="Update text preferences (Questions 14-22)"
)
async def update_text_preferences(
    preferences_data: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Update text preferences (Q14-22)"""
    updated_preferences = await preferences_service.update_text_preferences(
        session, current_user.id, preferences_data
    )
    
    preferences_response = UserPreferencesRead.model_validate(updated_preferences)
    return {
        "message": "Text preferences updated successfully",
        "data": preferences_response,
        "success": True
    }


@router.post(
    "/visual",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Update visual preferences",
    description="Update visual test preferences"
)
async def update_visual_preferences(
    visual_data: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Update visual test preferences"""
    import json
    visual_json = json.dumps(visual_data)
    
    updated_preferences = await preferences_service.update_visual_preferences(
        session, current_user.id, visual_json
    )
    
    preferences_response = UserPreferencesRead.model_validate(updated_preferences)
    return {
        "message": "Visual preferences updated successfully",
        "data": preferences_response,
        "success": True
    }


@router.put(
    "/",
    response_model=dict,
    summary="Update preferences",
    description="Update user preferences"
)
async def update_preferences(
    preferences_data: UserPreferencesUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Update user preferences"""
    updated_preferences = await preferences_service.update_user_preferences(
        session, current_user.id, preferences_data
    )
    
    preferences_response = UserPreferencesRead.model_validate(updated_preferences)
    return {
        "message": "Preferences updated successfully",
        "data": preferences_response,
        "success": True
    }
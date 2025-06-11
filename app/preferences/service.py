from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID

from app.preferences.models import (
    UserPreferences,
    UserPreferencesCreate,
    UserPreferencesUpdate
)
from app.exceptions import NotFoundError


class PreferencesService:
    
    async def get_user_preferences(self, session: AsyncSession, user_id: UUID) -> Optional[UserPreferences]:
        """Get user preferences by user_id"""
        result = await session.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create_user_preferences(self, session: AsyncSession, user_id: UUID, preferences_data: UserPreferencesCreate) -> UserPreferences:
        """Create new user preferences"""
        preferences = UserPreferences(
            user_id=user_id,
            **preferences_data.model_dump(exclude_unset=True)
        )
        
        session.add(preferences)
        await session.commit()
        await session.refresh(preferences)
        return preferences
    
    async def update_user_preferences(self, session: AsyncSession, user_id: UUID, preferences_data: UserPreferencesUpdate) -> UserPreferences:
        """Update existing user preferences"""
        # Get existing preferences
        existing_preferences = await self.get_user_preferences(session, user_id)
        
        if not existing_preferences:
            # Create new if doesn't exist
            create_data = UserPreferencesCreate(**preferences_data.model_dump(exclude_unset=True))
            return await self.create_user_preferences(session, user_id, create_data)
        
        # Update existing
        update_data = preferences_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_preferences, field, value)
        
        # Check completion status
        existing_preferences.basic_completed = self._check_basic_completion(existing_preferences)
        existing_preferences.text_completed = self._check_text_completion(existing_preferences)
        existing_preferences.all_completed = (
            existing_preferences.basic_completed and 
            existing_preferences.text_completed and 
            existing_preferences.visual_test_completed
        )
        
        await session.commit()
        await session.refresh(existing_preferences)
        return existing_preferences
    
    async def update_basic_preferences(self, session: AsyncSession, user_id: UUID, preferences_data: dict) -> UserPreferences:
        """Update basic preferences (Q1-13)"""
        update_data = UserPreferencesUpdate(**preferences_data)
        update_data.basic_completed = True
        return await self.update_user_preferences(session, user_id, update_data)
    
    async def update_text_preferences(self, session: AsyncSession, user_id: UUID, preferences_data: dict) -> UserPreferences:
        """Update text preferences (Q14-22)"""
        update_data = UserPreferencesUpdate(**preferences_data)
        update_data.text_completed = True
        return await self.update_user_preferences(session, user_id, update_data)
    
    async def update_visual_preferences(self, session: AsyncSession, user_id: UUID, visual_data: str) -> UserPreferences:
        """Update visual test preferences"""
        update_data = UserPreferencesUpdate(
            visual_preferences=visual_data,
            visual_test_completed=True
        )
        return await self.update_user_preferences(session, user_id, update_data)
    
    def _check_basic_completion(self, preferences: UserPreferences) -> bool:
        """Check if basic preferences (Q1-13) are completed"""
        required_fields = [
            'gender', 'age', 'age_min', 'age_max', 'location',
            'education', 'occupation', 'income', 'religion',
            'smoking', 'drinking', 'exercise', 'relationship_type'
        ]
        
        for field in required_fields:
            if getattr(preferences, field) is None:
                return False
        return True
    
    def _check_text_completion(self, preferences: UserPreferences) -> bool:
        """Check if text preferences (Q14-22) are completed"""
        required_fields = [
            'communication_style', 'love_language', 'conflict_resolution',
            'social_preference', 'travel_preference', 'food_preference',
            'weekend_activity', 'financial_approach', 'future_goals'
        ]
        
        for field in required_fields:
            if getattr(preferences, field) is None:
                return False
        return True
    
    async def check_preferences_completion(self, session: AsyncSession, user_id: UUID) -> dict:
        """Check completion status of user preferences"""
        preferences = await self.get_user_preferences(session, user_id)
        
        if not preferences:
            return {
                'has_preferences': False,
                'basic_completed': False,
                'text_completed': False,
                'visual_completed': False,
                'all_completed': False
            }
        
        return {
            'has_preferences': True,
            'basic_completed': preferences.basic_completed,
            'text_completed': preferences.text_completed,
            'visual_completed': preferences.visual_test_completed,
            'all_completed': preferences.all_completed
        }


# Create service instance
preferences_service = PreferencesService()
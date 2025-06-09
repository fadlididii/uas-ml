from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.auth.models import User
from app.users.models import UserProfile, UserProfileCreate, UserProfileUpdate
from app.users.schemas import (
    UserUpdateRequest,
    UserProfileRequest,
    PasswordChangeRequest
)
from app.auth.service import auth_service
from app.exceptions import NotFoundError, ConflictError, UnauthorizedError


class UserService:
    async def get_user_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_users(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> tuple[List[User], int]:
        """Get list of users with pagination"""
        query = select(User)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        # Get total count
        count_query = select(func.count(User.id))
        if is_active is not None:
            count_query = count_query.where(User.is_active == is_active)
        
        total_result = await session.execute(count_query)
        total = total_result.scalar()
        
        # Get users with pagination
        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await session.execute(query)
        users = result.scalars().all()
        
        return list(users), total
    
    async def update_user(
        self,
        session: AsyncSession,
        user_id: UUID,
        user_data: UserUpdateRequest,
        current_user: User
    ) -> User:
        """Update user information"""
        # Check if user exists
        user = await self.get_user_by_id(session, user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Check permissions (users can only update themselves, unless superuser)
        if user_id != current_user.id and not current_user.is_superuser:
            raise UnauthorizedError("Not enough permissions")
        
        # Check if email is already taken by another user
        if user_data.email and user_data.email != user.email:
            existing_user = await auth_service.get_user_by_email(session, user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ConflictError("Email already taken")
        
        # Update user fields
        update_data = user_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            for field, value in update_data.items():
                setattr(user, field, value)
            
            await session.commit()
            await session.refresh(user)
        
        return user
    
    async def delete_user(
        self,
        session: AsyncSession,
        user_id: UUID,
        current_user: User
    ) -> bool:
        """Delete user (soft delete by setting is_active to False)"""
        # Check if user exists
        user = await self.get_user_by_id(session, user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Check permissions (only superuser can delete users)
        if not current_user.is_superuser:
            raise UnauthorizedError("Not enough permissions")
        
        # Soft delete
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        await session.commit()
        return True
    
    async def change_password(
        self,
        session: AsyncSession,
        user_id: UUID,
        password_data: PasswordChangeRequest,
        current_user: User
    ) -> bool:
        """Change user password"""
        # Check if user exists
        user = await self.get_user_by_id(session, user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Check permissions (users can only change their own password)
        if user_id != current_user.id:
            raise UnauthorizedError("Not enough permissions")
        
        # Verify current password
        if not auth_service.verify_password(password_data.current_password, user.hashed_password):
            raise UnauthorizedError("Current password is incorrect")
        
        # Update password
        user.hashed_password = auth_service.get_password_hash(password_data.new_password)
        user.updated_at = datetime.utcnow()
        
        await session.commit()
        return True
    
    async def get_user_profile(self, session: AsyncSession, user_id: UUID) -> Optional[UserProfile]:
        """Get user profile"""
        result = await session.execute(select(UserProfile).where(UserProfile.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def create_user_profile(
        self,
        session: AsyncSession,
        user_id: UUID,
        profile_data: UserProfileRequest
    ) -> UserProfile:
        """Create user profile"""
        # Check if profile already exists
        existing_profile = await self.get_user_profile(session, user_id)
        if existing_profile:
            raise ConflictError("User profile already exists")
        
        # Create profile
        profile = UserProfile(
            user_id=user_id,
            **profile_data.model_dump(exclude_unset=True)
        )
        
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        return profile
    
    async def update_user_profile(
        self,
        session: AsyncSession,
        user_id: UUID,
        profile_data: UserProfileRequest,
        current_user: User
    ) -> UserProfile:
        """Update user profile"""
        # Check permissions
        if user_id != current_user.id and not current_user.is_superuser:
            raise UnauthorizedError("Not enough permissions")
        
        # Get or create profile
        profile = await self.get_user_profile(session, user_id)
        if not profile:
            return await self.create_user_profile(session, user_id, profile_data)
        
        # Update profile
        update_data = profile_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            for field, value in update_data.items():
                setattr(profile, field, value)
            
            await session.commit()
            await session.refresh(profile)
        
        return profile


user_service = UserService()
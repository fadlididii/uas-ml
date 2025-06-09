from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID

from app.database import get_session
from app.users.service import user_service
from app.auth.models import User
from app.auth.dependencies import get_current_active_user, get_current_superuser
from app.exceptions import NotFoundError, UnauthorizedError


async def get_user_by_id(
    user_id: Annotated[UUID, Path(description="User ID")],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> User:
    """Get user by ID dependency"""
    user = await user_service.get_user_by_id(session, user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


async def get_user_or_current(
    user_id: Annotated[UUID, Path(description="User ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Get user by ID or return current user if accessing own profile"""
    if user_id == current_user.id:
        return current_user
    
    user = await user_service.get_user_by_id(session, user_id)
    if not user:
        raise NotFoundError("User not found")
    
    return user


async def validate_user_access(
    user_id: Annotated[UUID, Path(description="User ID")],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> UUID:
    """Validate that current user can access the specified user"""
    if user_id != current_user.id and not current_user.is_superuser:
        raise UnauthorizedError("Not enough permissions to access this user")
    return user_id


async def validate_superuser_access(
    current_user: Annotated[User, Depends(get_current_superuser)]
) -> User:
    """Validate superuser access"""
    return current_user


class PaginationParams:
    """Pagination parameters"""
    def __init__(
        self,
        page: int = 1,
        size: int = 20
    ):
        self.page = max(1, page)
        self.size = min(100, max(1, size))  # Limit max size to 100
        self.skip = (self.page - 1) * self.size
        self.limit = self.size


def get_pagination_params(
    page: int = 1,
    size: int = 20
) -> PaginationParams:
    """Get pagination parameters"""
    return PaginationParams(page=page, size=size)
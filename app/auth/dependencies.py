from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.database import get_session
from app.auth.service import auth_service
from app.auth.models import User
from app.exceptions import UnauthorizedError


security = HTTPBearer()


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User:
    """Get current authenticated user"""
    try:
        user = await auth_service.get_current_user(session, credentials.credentials)
        return user
    except Exception as e:
        raise UnauthorizedError("Could not validate credentials")


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise UnauthorizedError("Inactive user")
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Get current superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
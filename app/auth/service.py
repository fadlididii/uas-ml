from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from app.auth.models import User, UserCreate
from app.auth.schemas import UserRegisterRequest, UserLoginRequest
from app.config import settings
from app.exceptions import ConflictError, UnauthorizedError, NotFoundError


class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return email"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except JWTError:
            return None
    
    async def get_user_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create_user(self, session: AsyncSession, user_data: UserRegisterRequest) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(session, user_data.email)
        if existing_user:
            raise ConflictError("User with this email already exists")
        
        # Hash password and create user
        hashed_password = self.get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def authenticate_user(self, session: AsyncSession, login_data: UserLoginRequest) -> User:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(session, login_data.email)
        if not user:
            raise UnauthorizedError("Invalid email or password")
        
        if not self.verify_password(login_data.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        
        if not user.is_active:
            raise UnauthorizedError("User account is disabled")
        
        return user
    
    async def get_current_user(self, session: AsyncSession, token: str) -> User:
        """Get current user from JWT token"""
        email = self.verify_token(token)
        if email is None:
            raise UnauthorizedError("Invalid token")
        
        user = await self.get_user_by_email(session, email)
        if user is None:
            raise NotFoundError("User not found")
        
        return user


auth_service = AuthService()
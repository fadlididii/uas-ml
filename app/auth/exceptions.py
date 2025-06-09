from app.exceptions import BaseAPIException
from fastapi import status


class AuthenticationError(BaseAPIException):
    """Authentication failed exception"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class InvalidCredentialsError(AuthenticationError):
    """Invalid credentials exception"""
    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(detail=detail)


class UserAlreadyExistsError(BaseAPIException):
    """User already exists exception"""
    def __init__(self, detail: str = "User with this email already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class InactiveUserError(AuthenticationError):
    """Inactive user exception"""
    def __init__(self, detail: str = "User account is disabled"):
        super().__init__(detail=detail)


class InvalidTokenError(AuthenticationError):
    """Invalid token exception"""
    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(detail=detail)


class WeakPasswordError(BaseAPIException):
    """Weak password exception"""
    def __init__(self, detail: str = "Password does not meet security requirements"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EmailAlreadyVerifiedError(BaseAPIException):
    """Email already verified exception"""
    def __init__(self, detail: str = "Email is already verified"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class PasswordResetTokenExpiredError(AuthenticationError):
    """Password reset token expired exception"""
    def __init__(self, detail: str = "Password reset token has expired"):
        super().__init__(detail=detail)
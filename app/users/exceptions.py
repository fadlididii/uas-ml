from app.exceptions import BaseAPIException
from fastapi import status


class UserNotFoundError(BaseAPIException):
    """User not found exception"""
    def __init__(self, detail: str = "User not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class UserProfileNotFoundError(BaseAPIException):
    """User profile not found exception"""
    def __init__(self, detail: str = "User profile not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class UserProfileExistsError(BaseAPIException):
    """User profile already exists exception"""
    def __init__(self, detail: str = "User profile already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class EmailAlreadyTakenError(BaseAPIException):
    """Email already taken exception"""
    def __init__(self, detail: str = "Email address is already taken"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class InvalidPhoneNumberError(BaseAPIException):
    """Invalid phone number exception"""
    def __init__(self, detail: str = "Invalid phone number format"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class InvalidWebsiteError(BaseAPIException):
    """Invalid website URL exception"""
    def __init__(self, detail: str = "Website must start with http:// or https://"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PasswordMismatchError(BaseAPIException):
    """Password mismatch exception"""
    def __init__(self, detail: str = "Passwords do not match"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CurrentPasswordIncorrectError(BaseAPIException):
    """Current password incorrect exception"""
    def __init__(self, detail: str = "Current password is incorrect"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class InsufficientPermissionsError(BaseAPIException):
    """Insufficient permissions exception"""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class CannotDeleteSelfError(BaseAPIException):
    """Cannot delete self exception"""
    def __init__(self, detail: str = "Cannot delete your own account"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class CannotDeactivateSelfError(BaseAPIException):
    """Cannot deactivate self exception"""
    def __init__(self, detail: str = "Cannot deactivate your own account"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class InvalidUserDataError(BaseAPIException):
    """Invalid user data exception"""
    def __init__(self, detail: str = "Invalid user data provided"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserDeactivatedError(BaseAPIException):
    """User deactivated exception"""
    def __init__(self, detail: str = "User account is deactivated"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)
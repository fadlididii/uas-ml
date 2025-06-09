# User management constants

# Pagination settings
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1

# Profile field limits
MAX_FIRST_NAME_LENGTH = 50
MAX_LAST_NAME_LENGTH = 50
MAX_BIO_LENGTH = 500
MAX_PHONE_LENGTH = 20
MAX_LOCATION_LENGTH = 100

# User status
USER_STATUS = {
    "ACTIVE": True,
    "INACTIVE": False
}

# Error messages
ERROR_MESSAGES = {
    "USER_NOT_FOUND": "User not found",
    "PROFILE_NOT_FOUND": "User profile not found",
    "PROFILE_EXISTS": "User profile already exists",
    "EMAIL_TAKEN": "Email address is already taken",
    "INVALID_PHONE": "Invalid phone number format",
    "INVALID_WEBSITE": "Website must start with http:// or https://",
    "PASSWORDS_NOT_MATCH": "Passwords do not match",
    "CURRENT_PASSWORD_INCORRECT": "Current password is incorrect",
    "INSUFFICIENT_PERMISSIONS": "Not enough permissions",
    "CANNOT_DELETE_SELF": "Cannot delete your own account",
    "CANNOT_DEACTIVATE_SELF": "Cannot deactivate your own account"
}

# Success messages
SUCCESS_MESSAGES = {
    "USER_UPDATED": "User updated successfully",
    "USER_DELETED": "User deleted successfully",
    "USER_DEACTIVATED": "User deactivated successfully",
    "USER_ACTIVATED": "User activated successfully",
    "PROFILE_CREATED": "User profile created successfully",
    "PROFILE_UPDATED": "User profile updated successfully",
    "PASSWORD_CHANGED": "Password changed successfully"
}

# User roles
USER_ROLES = {
    "USER": "user",
    "ADMIN": "admin",
    "SUPERUSER": "superuser"
}

# Profile validation patterns
VALIDATION_PATTERNS = {
    "PHONE": r'^[+]?[1-9]?[0-9]{7,15}$',
    "WEBSITE": r'^https?://[\w\.-]+\.[a-zA-Z]{2,}',
    "NAME": r'^[a-zA-Z\s\-\']{1,50}$'
}

# Default values
DEFAULTS = {
    "AVATAR_URL": None,
    "BIO": None,
    "LOCATION": None,
    "WEBSITE": None
}

# File upload settings
FILE_UPLOAD = {
    "MAX_SIZE_MB": 5,
    "ALLOWED_EXTENSIONS": [".jpg", ".jpeg", ".png", ".gif"],
    "AVATAR_FOLDER": "avatars"
}
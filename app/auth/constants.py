# Authentication constants

# Token settings
TOKEN_TYPE = "bearer"
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password settings
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 100

# Error messages
ERROR_MESSAGES = {
    "INVALID_CREDENTIALS": "Invalid email or password",
    "USER_EXISTS": "User with this email already exists",
    "USER_NOT_FOUND": "User not found",
    "INACTIVE_USER": "User account is disabled",
    "INVALID_TOKEN": "Invalid or expired token",
    "INSUFFICIENT_PERMISSIONS": "Not enough permissions",
    "WEAK_PASSWORD": "Password must be at least 8 characters long",
    "INVALID_EMAIL": "Invalid email format"
}

# Success messages
SUCCESS_MESSAGES = {
    "USER_REGISTERED": "User registered successfully",
    "LOGIN_SUCCESS": "Login successful",
    "LOGOUT_SUCCESS": "Logout successful",
    "PASSWORD_CHANGED": "Password changed successfully"
}

# HTTP status codes
HTTP_STATUS = {
    "OK": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "CONFLICT": 409,
    "UNPROCESSABLE_ENTITY": 422,
    "INTERNAL_SERVER_ERROR": 500
}
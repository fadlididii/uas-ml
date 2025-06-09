import re
from typing import Optional
from datetime import datetime, timedelta
import secrets
import string


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """Validate password strength and return errors if any"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if len(password) > 100:
        errors.append("Password must be less than 100 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors


def generate_random_password(length: int = 12) -> str:
    """Generate a random secure password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def generate_verification_token() -> str:
    """Generate a random verification token"""
    return secrets.token_urlsafe(32)


def is_token_expired(created_at: datetime, expiry_hours: int = 24) -> bool:
    """Check if a token has expired"""
    expiry_time = created_at + timedelta(hours=expiry_hours)
    return datetime.utcnow() > expiry_time


def sanitize_email(email: str) -> str:
    """Sanitize email by converting to lowercase and stripping whitespace"""
    return email.lower().strip()


def mask_email(email: str) -> str:
    """Mask email for privacy (e.g., j***@example.com)"""
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    if len(local) <= 1:
        return email
    
    masked_local = local[0] + '*' * (len(local) - 1)
    return f"{masked_local}@{domain}"


def extract_domain_from_email(email: str) -> Optional[str]:
    """Extract domain from email address"""
    if '@' not in email:
        return None
    return email.split('@')[1]


def is_disposable_email(email: str) -> bool:
    """Check if email is from a disposable email provider"""
    # List of common disposable email domains
    disposable_domains = {
        '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
        'mailinator.com', 'throwaway.email', 'temp-mail.org'
    }
    
    domain = extract_domain_from_email(email)
    return domain in disposable_domains if domain else False
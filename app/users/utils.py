import re
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID
import hashlib
import secrets
from app.users.constants import VALIDATION_PATTERNS


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format"""
    if not phone:
        return True  # Optional field
    
    # Remove spaces, dashes, and parentheses
    cleaned_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    # Check if it matches the pattern
    pattern = VALIDATION_PATTERNS["PHONE"]
    return bool(re.match(pattern, cleaned_phone))


def validate_website_url(url: str) -> bool:
    """Validate website URL format"""
    if not url:
        return True  # Optional field
    
    pattern = VALIDATION_PATTERNS["WEBSITE"]
    return bool(re.match(pattern, url))


def validate_name(name: str) -> bool:
    """Validate name format (first name, last name)"""
    if not name:
        return True  # Optional field
    
    pattern = VALIDATION_PATTERNS["NAME"]
    return bool(re.match(pattern, name))


def format_phone_number(phone: str) -> str:
    """Format phone number to a standard format"""
    if not phone:
        return phone
    
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Add + if not present and starts with country code
    if not cleaned.startswith('+') and len(cleaned) > 10:
        cleaned = '+' + cleaned
    
    return cleaned


def calculate_age(birth_date: date) -> Optional[int]:
    """Calculate age from birth date"""
    if not birth_date:
        return None
    
    today = date.today()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age


def generate_avatar_url(user_id: UUID, email: str) -> str:
    """Generate Gravatar URL for user avatar"""
    # Create MD5 hash of email
    email_hash = hashlib.md5(email.lower().encode()).hexdigest()
    
    # Generate Gravatar URL
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=200"
    
    return gravatar_url


def sanitize_bio(bio: str) -> str:
    """Sanitize bio text by removing potentially harmful content"""
    if not bio:
        return bio
    
    # Remove HTML tags
    bio = re.sub(r'<[^>]+>', '', bio)
    
    # Remove excessive whitespace
    bio = re.sub(r'\s+', ' ', bio).strip()
    
    # Limit length
    if len(bio) > 500:
        bio = bio[:497] + '...'
    
    return bio


def mask_sensitive_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Mask sensitive user data for logging"""
    masked_data = user_data.copy()
    
    # Mask email
    if 'email' in masked_data:
        email = masked_data['email']
        if '@' in email:
            local, domain = email.split('@', 1)
            masked_local = local[0] + '*' * (len(local) - 1) if len(local) > 1 else local
            masked_data['email'] = f"{masked_local}@{domain}"
    
    # Mask phone
    if 'phone' in masked_data and masked_data['phone']:
        phone = masked_data['phone']
        if len(phone) > 4:
            masked_data['phone'] = phone[:2] + '*' * (len(phone) - 4) + phone[-2:]
    
    # Remove sensitive fields
    sensitive_fields = ['hashed_password', 'password']
    for field in sensitive_fields:
        if field in masked_data:
            masked_data[field] = '[MASKED]'
    
    return masked_data


def generate_username_suggestions(email: str, existing_usernames: list = None) -> list[str]:
    """Generate username suggestions based on email"""
    if existing_usernames is None:
        existing_usernames = []
    
    base_username = email.split('@')[0]
    base_username = re.sub(r'[^a-zA-Z0-9_]', '', base_username)
    
    suggestions = []
    
    # Add base username if available
    if base_username not in existing_usernames:
        suggestions.append(base_username)
    
    # Add numbered variations
    for i in range(1, 10):
        suggestion = f"{base_username}{i}"
        if suggestion not in existing_usernames:
            suggestions.append(suggestion)
    
    # Add random suffix variations
    for _ in range(3):
        random_suffix = secrets.token_hex(2)
        suggestion = f"{base_username}_{random_suffix}"
        if suggestion not in existing_usernames:
            suggestions.append(suggestion)
    
    return suggestions[:5]  # Return top 5 suggestions


def is_valid_date_of_birth(birth_date: datetime) -> bool:
    """Validate date of birth (must be in the past and reasonable)"""
    if not birth_date:
        return True  # Optional field
    
    today = datetime.now().date()
    birth_date_only = birth_date.date() if isinstance(birth_date, datetime) else birth_date
    
    # Must be in the past
    if birth_date_only >= today:
        return False
    
    # Must be reasonable (not more than 150 years ago)
    max_age_date = date(today.year - 150, today.month, today.day)
    if birth_date_only < max_age_date:
        return False
    
    return True


def get_user_display_name(user_data: Dict[str, Any]) -> str:
    """Get display name for user (first name + last name or email)"""
    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')
    email = user_data.get('email', '')
    
    if first_name and last_name:
        return f"{first_name} {last_name}"
    elif first_name:
        return first_name
    elif last_name:
        return last_name
    else:
        return email.split('@')[0] if email else 'Unknown User'
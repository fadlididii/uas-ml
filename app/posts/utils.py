import re
from typing import List, Optional
from datetime import datetime
from html import escape, unescape
from urllib.parse import quote, unquote
import hashlib

from app.posts.constants import (
    CONTENT_SETTINGS,
    VALIDATION_PATTERNS,
    SLUG_SEPARATOR,
    SLUG_MAX_WORDS
)


def generate_slug(text: str, max_length: int = 100) -> str:
    """Generate URL-friendly slug from text"""
    if not text:
        return ""
    
    # Convert to lowercase
    slug = text.lower()
    
    # Remove HTML tags
    slug = re.sub(r'<[^>]+>', '', slug)
    
    # Replace special characters with spaces
    slug = re.sub(r'[^a-z0-9\s-]', ' ', slug)
    
    # Replace multiple spaces/dashes with single dash
    slug = re.sub(r'[\s-]+', SLUG_SEPARATOR, slug)
    
    # Remove leading/trailing dashes
    slug = slug.strip(SLUG_SEPARATOR)
    
    # Limit number of words
    words = slug.split(SLUG_SEPARATOR)
    if len(words) > SLUG_MAX_WORDS:
        words = words[:SLUG_MAX_WORDS]
        slug = SLUG_SEPARATOR.join(words)
    
    # Limit total length
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip(SLUG_SEPARATOR)
    
    return slug or "post"


def validate_slug(slug: str) -> bool:
    """Validate slug format"""
    if not slug:
        return False
    
    pattern = VALIDATION_PATTERNS["SLUG"]
    return bool(re.match(pattern, slug))


def generate_excerpt(content: str, max_length: int = None) -> str:
    """Generate excerpt from content"""
    if not content:
        return ""
    
    if max_length is None:
        max_length = CONTENT_SETTINGS["EXCERPT_AUTO_LENGTH"]
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', content)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate to max length
    if len(text) <= max_length:
        return text
    
    # Find last complete word within limit
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.8:  # If last space is reasonably close to limit
        truncated = truncated[:last_space]
    
    return truncated + "..."


def sanitize_html(content: str, allowed_tags: List[str] = None) -> str:
    """Sanitize HTML content by removing dangerous tags"""
    if not content:
        return content
    
    if allowed_tags is None:
        allowed_tags = CONTENT_SETTINGS["ALLOWED_HTML_TAGS"]
    
    forbidden_tags = CONTENT_SETTINGS["FORBIDDEN_HTML_TAGS"]
    
    # Remove forbidden tags and their content
    for tag in forbidden_tags:
        pattern = f'<{tag}[^>]*>.*?</{tag}>'
        content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
        
        # Also remove self-closing versions
        pattern = f'<{tag}[^>]*/>'
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # Remove any remaining script/style content
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove dangerous attributes
    dangerous_attrs = ['onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'onblur']
    for attr in dangerous_attrs:
        pattern = f'{attr}\s*=\s*["\'][^"\'>]*["\']'
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    return content


def extract_text_from_html(html_content: str) -> str:
    """Extract plain text from HTML content"""
    if not html_content:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    
    # Decode HTML entities
    text = unescape(text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def calculate_reading_time(content: str, words_per_minute: int = 200) -> int:
    """Calculate estimated reading time in minutes"""
    if not content:
        return 0
    
    # Extract text from HTML
    text = extract_text_from_html(content)
    
    # Count words
    words = len(text.split())
    
    # Calculate reading time
    reading_time = max(1, round(words / words_per_minute))
    
    return reading_time


def generate_content_hash(content: str) -> str:
    """Generate hash for content to detect changes"""
    if not content:
        return ""
    
    # Normalize content (remove extra whitespace, convert to lowercase)
    normalized = re.sub(r'\s+', ' ', content.lower().strip())
    
    # Generate MD5 hash
    return hashlib.md5(normalized.encode()).hexdigest()


def validate_tag_name(tag_name: str) -> bool:
    """Validate tag name format"""
    if not tag_name:
        return False
    
    # Check length
    if len(tag_name) > 50:
        return False
    
    # Check pattern
    pattern = VALIDATION_PATTERNS["TAG_NAME"]
    return bool(re.match(pattern, tag_name))


def normalize_tag_name(tag_name: str) -> str:
    """Normalize tag name (lowercase, trim whitespace)"""
    if not tag_name:
        return ""
    
    return tag_name.lower().strip()


def extract_tags_from_content(content: str) -> List[str]:
    """Extract potential tags from content (hashtags)"""
    if not content:
        return []
    
    # Find hashtags in content
    hashtags = re.findall(r'#([a-zA-Z0-9_]+)', content)
    
    # Normalize and validate
    tags = []
    for tag in hashtags:
        normalized = normalize_tag_name(tag)
        if validate_tag_name(normalized) and normalized not in tags:
            tags.append(normalized)
    
    return tags[:10]  # Limit to 10 tags


def format_post_url(slug: str, base_url: str = "") -> str:
    """Format post URL from slug"""
    if not slug:
        return base_url
    
    # Ensure slug is URL-safe
    safe_slug = quote(slug, safe='-')
    
    if base_url:
        return f"{base_url.rstrip('/')}/posts/{safe_slug}"
    else:
        return f"/posts/{safe_slug}"


def parse_post_url(url: str) -> Optional[str]:
    """Extract slug from post URL"""
    if not url:
        return None
    
    # Match pattern like /posts/my-post-slug
    match = re.search(r'/posts/([^/?]+)', url)
    if match:
        return unquote(match.group(1))
    
    return None


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix"""
    if not text or len(text) <= max_length:
        return text
    
    # Account for suffix length
    truncate_length = max_length - len(suffix)
    
    if truncate_length <= 0:
        return suffix[:max_length]
    
    # Find last space within limit for word boundary
    truncated = text[:truncate_length]
    last_space = truncated.rfind(' ')
    
    if last_space > truncate_length * 0.8:
        truncated = truncated[:last_space]
    
    return truncated + suffix


def count_words(text: str) -> int:
    """Count words in text"""
    if not text:
        return 0
    
    # Extract text from HTML if needed
    clean_text = extract_text_from_html(text)
    
    # Split by whitespace and count
    words = clean_text.split()
    return len(words)


def count_characters(text: str, include_spaces: bool = True) -> int:
    """Count characters in text"""
    if not text:
        return 0
    
    # Extract text from HTML if needed
    clean_text = extract_text_from_html(text)
    
    if include_spaces:
        return len(clean_text)
    else:
        return len(clean_text.replace(' ', ''))


def format_publish_date(date: datetime, format_string: str = "%B %d, %Y") -> str:
    """Format publish date for display"""
    if not date:
        return ""
    
    return date.strftime(format_string)


def is_recent_post(publish_date: datetime, days: int = 7) -> bool:
    """Check if post was published recently"""
    if not publish_date:
        return False
    
    now = datetime.utcnow()
    diff = now - publish_date
    
    return diff.days <= days
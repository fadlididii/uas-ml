# Posts management constants

# Post settings
MAX_TITLE_LENGTH = 200
MAX_EXCERPT_LENGTH = 500
MAX_CONTENT_LENGTH = 50000
MAX_SLUG_LENGTH = 100
MAX_TAGS_PER_POST = 10

# Tag settings
MAX_TAG_NAME_LENGTH = 50
MAX_TAG_DESCRIPTION_LENGTH = 200
MAX_TAG_SLUG_LENGTH = 60

# Comment settings
MAX_COMMENT_LENGTH = 1000
DEFAULT_COMMENT_APPROVAL = True

# Pagination settings
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1

# Post status options
POST_STATUSES = {
    "DRAFT": "draft",
    "PUBLISHED": "published",
    "ARCHIVED": "archived"
}

# Slug generation settings
SLUG_SEPARATOR = "-"
SLUG_MAX_WORDS = 10

# Error messages
ERROR_MESSAGES = {
    "POST_NOT_FOUND": "Post not found",
    "TAG_NOT_FOUND": "Tag not found",
    "COMMENT_NOT_FOUND": "Comment not found",
    "POST_SLUG_EXISTS": "Post with this slug already exists",
    "TAG_NAME_EXISTS": "Tag with this name already exists",
    "TAG_SLUG_EXISTS": "Tag with this slug already exists",
    "INVALID_POST_STATUS": "Invalid post status",
    "TITLE_TOO_LONG": f"Title must be less than {MAX_TITLE_LENGTH} characters",
    "EXCERPT_TOO_LONG": f"Excerpt must be less than {MAX_EXCERPT_LENGTH} characters",
    "CONTENT_TOO_LONG": f"Content must be less than {MAX_CONTENT_LENGTH} characters",
    "TOO_MANY_TAGS": f"Maximum {MAX_TAGS_PER_POST} tags allowed per post",
    "TAG_NAME_TOO_LONG": f"Tag name must be less than {MAX_TAG_NAME_LENGTH} characters",
    "COMMENT_TOO_LONG": f"Comment must be less than {MAX_COMMENT_LENGTH} characters",
    "INSUFFICIENT_PERMISSIONS": "Not enough permissions",
    "CANNOT_PUBLISH_EMPTY_POST": "Cannot publish post without content",
    "INVALID_TAG_NAME": "Tag name contains invalid characters",
    "DUPLICATE_TAGS": "Duplicate tags are not allowed"
}

# Success messages
SUCCESS_MESSAGES = {
    "POST_CREATED": "Post created successfully",
    "POST_UPDATED": "Post updated successfully",
    "POST_DELETED": "Post deleted successfully",
    "POST_PUBLISHED": "Post published successfully",
    "POST_UNPUBLISHED": "Post unpublished successfully",
    "POST_ARCHIVED": "Post archived successfully",
    "TAG_CREATED": "Tag created successfully",
    "TAG_UPDATED": "Tag updated successfully",
    "TAG_DELETED": "Tag deleted successfully",
    "COMMENT_CREATED": "Comment created successfully",
    "COMMENT_UPDATED": "Comment updated successfully",
    "COMMENT_DELETED": "Comment deleted successfully",
    "COMMENT_APPROVED": "Comment approved successfully",
    "COMMENT_REJECTED": "Comment rejected successfully"
}

# Validation patterns
VALIDATION_PATTERNS = {
    "SLUG": r'^[a-z0-9-]+$',
    "TAG_NAME": r'^[a-zA-Z0-9\s\-_]+$',
    "TITLE": r'^[\w\s\-_.,!?()]+$'
}

# Content formatting
CONTENT_SETTINGS = {
    "EXCERPT_AUTO_LENGTH": 150,
    "PREVIEW_LENGTH": 300,
    "ALLOWED_HTML_TAGS": [
        'p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre',
        'a', 'img'
    ],
    "FORBIDDEN_HTML_TAGS": [
        'script', 'style', 'iframe', 'object', 'embed',
        'form', 'input', 'button'
    ]
}

# SEO settings
SEO_SETTINGS = {
    "META_TITLE_MAX_LENGTH": 60,
    "META_DESCRIPTION_MAX_LENGTH": 160,
    "CANONICAL_URL_REQUIRED": True
}

# Featured post settings
FEATURED_POST_SETTINGS = {
    "MAX_FEATURED_POSTS": 5,
    "AUTO_UNFEATURE_OLDER": True,
    "FEATURED_POST_PRIORITY": 1
}

# View tracking
VIEW_TRACKING = {
    "TRACK_ANONYMOUS_VIEWS": True,
    "TRACK_AUTHOR_VIEWS": False,
    "VIEW_COUNT_CACHE_TTL": 300  # 5 minutes
}

# Search settings
SEARCH_SETTINGS = {
    "MIN_SEARCH_LENGTH": 3,
    "MAX_SEARCH_LENGTH": 100,
    "SEARCH_FIELDS": ['title', 'content', 'excerpt'],
    "SEARCH_RESULTS_LIMIT": 50
}
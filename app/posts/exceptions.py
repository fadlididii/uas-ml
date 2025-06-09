from app.exceptions import BaseAPIException
from fastapi import status


class PostNotFoundError(BaseAPIException):
    """Post not found exception"""
    def __init__(self, detail: str = "Post not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class TagNotFoundError(BaseAPIException):
    """Tag not found exception"""
    def __init__(self, detail: str = "Tag not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class CommentNotFoundError(BaseAPIException):
    """Comment not found exception"""
    def __init__(self, detail: str = "Comment not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class PostSlugExistsError(BaseAPIException):
    """Post slug already exists exception"""
    def __init__(self, detail: str = "Post with this slug already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class TagNameExistsError(BaseAPIException):
    """Tag name already exists exception"""
    def __init__(self, detail: str = "Tag with this name already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class TagSlugExistsError(BaseAPIException):
    """Tag slug already exists exception"""
    def __init__(self, detail: str = "Tag with this slug already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class InvalidPostStatusError(BaseAPIException):
    """Invalid post status exception"""
    def __init__(self, detail: str = "Invalid post status"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PostTitleTooLongError(BaseAPIException):
    """Post title too long exception"""
    def __init__(self, detail: str = "Post title is too long"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PostContentTooLongError(BaseAPIException):
    """Post content too long exception"""
    def __init__(self, detail: str = "Post content is too long"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TooManyTagsError(BaseAPIException):
    """Too many tags exception"""
    def __init__(self, detail: str = "Too many tags assigned to post"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class InvalidTagNameError(BaseAPIException):
    """Invalid tag name exception"""
    def __init__(self, detail: str = "Tag name contains invalid characters"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CommentTooLongError(BaseAPIException):
    """Comment too long exception"""
    def __init__(self, detail: str = "Comment is too long"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CannotPublishEmptyPostError(BaseAPIException):
    """Cannot publish empty post exception"""
    def __init__(self, detail: str = "Cannot publish post without content"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PostAccessDeniedError(BaseAPIException):
    """Post access denied exception"""
    def __init__(self, detail: str = "Access denied to this post"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class PostModificationDeniedError(BaseAPIException):
    """Post modification denied exception"""
    def __init__(self, detail: str = "Not enough permissions to modify this post"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class CommentNotApprovedError(BaseAPIException):
    """Comment not approved exception"""
    def __init__(self, detail: str = "Comment is not approved for public viewing"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class DuplicateTagsError(BaseAPIException):
    """Duplicate tags exception"""
    def __init__(self, detail: str = "Duplicate tags are not allowed"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class InvalidSlugError(BaseAPIException):
    """Invalid slug exception"""
    def __init__(self, detail: str = "Invalid slug format"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PostAlreadyPublishedError(BaseAPIException):
    """Post already published exception"""
    def __init__(self, detail: str = "Post is already published"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class PostNotPublishedError(BaseAPIException):
    """Post not published exception"""
    def __init__(self, detail: str = "Post is not published"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class SearchQueryTooShortError(BaseAPIException):
    """Search query too short exception"""
    def __init__(self, detail: str = "Search query is too short"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SearchQueryTooLongError(BaseAPIException):
    """Search query too long exception"""
    def __init__(self, detail: str = "Search query is too long"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
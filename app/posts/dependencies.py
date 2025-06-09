from fastapi import Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from uuid import UUID

from app.database import get_session
from app.posts.service import post_service
from app.posts.models import Post, PostStatus
from app.auth.models import User
from app.auth.dependencies import get_current_active_user
from app.exceptions import NotFoundError, UnauthorizedError


async def get_post_by_id(
    post_id: Annotated[UUID, Path(description="Post ID")],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> Post:
    """Get post by ID dependency"""
    post = await post_service.get_post_by_id(session, post_id)
    if not post:
        raise NotFoundError("Post not found")
    return post


async def get_post_by_slug(
    slug: Annotated[str, Path(description="Post slug")],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> Post:
    """Get post by slug dependency"""
    post = await post_service.get_post_by_slug(session, slug)
    if not post:
        raise NotFoundError("Post not found")
    return post


async def validate_post_access(
    post: Annotated[Post, Depends(get_post_by_id)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Post:
    """Validate that current user can access/modify the post"""
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise UnauthorizedError("Not enough permissions to access this post")
    return post


def validate_user_access_to_post(post: Post, user: User) -> None:
    """Validate that user has access to modify the post"""
    if post.author_id != user.id and not user.is_superuser:
        raise UnauthorizedError("Not enough permissions to access this post")


async def get_post_by_id_or_slug(
    identifier: Annotated[str, Path(description="Post ID or slug")],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> Post:
    """Get post by ID or slug dependency"""
    # Try to parse as UUID first
    try:
        post_id = UUID(identifier)
        post = await post_service.get_post_by_id(session, post_id)
    except ValueError:
        # If not a valid UUID, treat as slug
        post = await post_service.get_post_by_slug(session, identifier)
    
    if not post:
        raise NotFoundError("Post not found")
    return post


async def validate_published_post(
    post: Annotated[Post, Depends(get_post_by_id)]
) -> Post:
    """Validate that post is published (for public access)"""
    if post.status != PostStatus.PUBLISHED:
        raise NotFoundError("Post not found")
    return post


def validate_post_is_published(post: Post) -> None:
    """Validate that post is published"""
    if post.status != PostStatus.PUBLISHED:
        raise NotFoundError("Post not found")


class PostFilterParams:
    """Post filtering parameters"""
    def __init__(
        self,
        status: Optional[PostStatus] = Query(None, description="Filter by post status"),
        author_id: Optional[UUID] = Query(None, description="Filter by author ID"),
        tag_slug: Optional[str] = Query(None, description="Filter by tag slug"),
        search: Optional[str] = Query(None, description="Search in title, content, and excerpt"),
        is_featured: Optional[bool] = Query(None, description="Filter by featured status")
    ):
        self.status = status
        self.author_id = author_id
        self.tag_slug = tag_slug
        self.search = search
        self.is_featured = is_featured


class PaginationParams:
    """Pagination parameters"""
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(20, ge=1, le=100, description="Page size")
    ):
        self.page = page
        self.size = size
        self.skip = (page - 1) * size
        self.limit = size


def get_post_filter_params(
    status: Optional[PostStatus] = Query(None, description="Filter by post status"),
    author_id: Optional[UUID] = Query(None, description="Filter by author ID"),
    tag_slug: Optional[str] = Query(None, description="Filter by tag slug"),
    search: Optional[str] = Query(None, description="Search in title, content, and excerpt"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status")
) -> PostFilterParams:
    """Get post filtering parameters"""
    return PostFilterParams(
        status=status,
        author_id=author_id,
        tag_slug=tag_slug,
        search=search,
        is_featured=is_featured
    )


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size")
) -> PaginationParams:
    """Get pagination parameters"""
    return PaginationParams(page=page, size=size)


def get_public_post_filter_params(
    tag_slug: Optional[str] = Query(None, description="Filter by tag slug"),
    search: Optional[str] = Query(None, description="Search in title, content, and excerpt"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status")
) -> PostFilterParams:
    """Get post filtering parameters for public access (only published posts)"""
    return PostFilterParams(
        status=PostStatus.PUBLISHED,
        author_id=None,
        tag_slug=tag_slug,
        search=search,
        is_featured=is_featured
    )
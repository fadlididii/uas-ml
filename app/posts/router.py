from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional

from app.database import get_session
from app.posts.schemas import (
    PostCreateRequest,
    PostUpdateRequest,
    PostDetailResponse,
    PostsListResponse,
    TagCreateRequest,
    TagDetailResponse,
    TagsListResponse,
    CommentCreateRequest,
    CommentResponse,
    CommentsListResponse,
    MessageResponse
)
from app.posts.service import post_service
from app.posts.dependencies import (
    get_post_by_id_or_slug,
    validate_user_access_to_post,
    validate_post_is_published,
    PostFilterParams,
    PaginationParams
)
from app.auth.dependencies import get_current_active_user, get_current_user
from app.auth.models import User
from app.posts.models import Post


router = APIRouter()


@router.post(
    "/",
    response_model=PostDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
    description="Create a new blog post"
)
async def create_post(
    post_data: PostCreateRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Create a new post"""
    post = await post_service.create_post(session, post_data, current_user.id)
    return PostDetailResponse.model_validate(post)


@router.get(
    "/",
    response_model=PostsListResponse,
    summary="Get posts list",
    description="Get a paginated list of posts with optional filtering"
)
async def get_posts(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[PostFilterParams, Depends()],
    pagination: Annotated[PaginationParams, Depends()],
    current_user: Annotated[Optional[User], Depends(get_current_user)] = None
):
    """Get posts list with filtering and pagination"""
    posts, total = await post_service.get_posts_list(
        session, filters, pagination, current_user
    )
    
    return PostsListResponse(
        posts=[PostDetailResponse.model_validate(post) for post in posts],
        total=total,
        page=pagination.page,
        per_page=pagination.per_page,
        pages=(total + pagination.per_page - 1) // pagination.per_page
    )


@router.get(
    "/{post_id_or_slug}",
    response_model=PostDetailResponse,
    summary="Get post by ID or slug",
    description="Get a specific post by its ID or slug"
)
async def get_post(
    post: Annotated[Post, Depends(get_post_by_id_or_slug)],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[Optional[User], Depends(get_current_user)] = None
):
    """Get post by ID or slug"""
    # Increment view count if post is published
    if post.status == "published":
        await post_service.increment_view_count(session, post.id)
    
    return PostDetailResponse.model_validate(post)


@router.put(
    "/{post_id_or_slug}",
    response_model=PostDetailResponse,
    summary="Update post",
    description="Update an existing post"
)
async def update_post(
    post_data: PostUpdateRequest,
    post: Annotated[Post, Depends(get_post_by_id_or_slug)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Update post"""
    # Validate user access
    validate_user_access_to_post(post, current_user)
    
    updated_post = await post_service.update_post(session, post.id, post_data)
    return PostDetailResponse.model_validate(updated_post)


@router.delete(
    "/{post_id_or_slug}",
    response_model=MessageResponse,
    summary="Delete post",
    description="Delete an existing post"
)
async def delete_post(
    post: Annotated[Post, Depends(get_post_by_id_or_slug)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Delete post"""
    # Validate user access
    validate_user_access_to_post(post, current_user)
    
    await post_service.delete_post(session, post.id)
    return MessageResponse(
        message="Post deleted successfully",
        success=True
    )


# Tag endpoints
@router.post(
    "/tags",
    response_model=TagDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tag",
    description="Create a new tag"
)
async def create_tag(
    tag_data: TagCreateRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Create a new tag"""
    tag = await post_service.create_tag(session, tag_data)
    return TagDetailResponse.model_validate(tag)


@router.get(
    "/tags",
    response_model=TagsListResponse,
    summary="Get tags list",
    description="Get a list of all tags"
)
async def get_tags(
    session: Annotated[AsyncSession, Depends(get_session)],
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Get tags list"""
    tags, total = await post_service.get_tags_list(session, page, per_page)
    
    return TagsListResponse(
        tags=[TagDetailResponse.model_validate(tag) for tag in tags],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page
    )
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum

from app.posts.models import PostStatus


class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    status: PostStatus = PostStatus.DRAFT
    is_featured: bool = False
    tag_names: Optional[List[str]] = Field(default=None)
    
    @validator('tag_names')
    def validate_tag_names(cls, v):
        if v is not None:
            # Remove duplicates and empty strings
            v = list(set([tag.strip() for tag in v if tag.strip()]))
            # Limit number of tags
            if len(v) > 10:
                raise ValueError('Maximum 10 tags allowed')
        return v


class PostUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    status: Optional[PostStatus] = None
    is_featured: Optional[bool] = None
    tag_names: Optional[List[str]] = Field(default=None)
    
    @validator('tag_names')
    def validate_tag_names(cls, v):
        if v is not None:
            v = list(set([tag.strip() for tag in v if tag.strip()]))
            if len(v) > 10:
                raise ValueError('Maximum 10 tags allowed')
        return v


class AuthorResponse(BaseModel):
    id: UUID
    email: str
    
    class Config:
        from_attributes = True


class TagResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    id: UUID
    title: str
    excerpt: Optional[str] = None
    status: PostStatus
    is_featured: bool
    slug: str
    view_count: int
    author: AuthorResponse
    tags: List[TagResponse] = []
    created_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PostDetailResponse(BaseModel):
    id: UUID
    title: str
    content: str
    excerpt: Optional[str] = None
    status: PostStatus
    is_featured: bool
    slug: str
    view_count: int
    author_id: UUID
    author: AuthorResponse
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PostsListResponse(BaseModel):
    posts: List[PostListResponse]
    total: int
    page: int
    size: int
    pages: int


class TagCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class TagUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class TagDetailResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    post_count: int = 0
    
    class Config:
        from_attributes = True


class TagsListResponse(BaseModel):
    tags: List[TagDetailResponse]
    total: int
    page: int
    size: int
    pages: int


class CommentCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class CommentUpdateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class CommentResponse(BaseModel):
    id: UUID
    post_id: UUID
    author_id: UUID
    author: AuthorResponse
    content: str
    is_approved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CommentsListResponse(BaseModel):
    comments: List[CommentResponse]
    total: int
    page: int
    size: int
    pages: int


class PostStatsResponse(BaseModel):
    total_posts: int
    published_posts: int
    draft_posts: int
    featured_posts: int
    total_views: int
    total_comments: int


class MessageResponse(BaseModel):
    message: str
    success: bool = True
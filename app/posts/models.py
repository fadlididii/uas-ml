from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from app.auth.models import User


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# Link table for many-to-many relationship between posts and tags
class PostTagLink(SQLModel, table=True):
    __tablename__ = "post_tags"
    
    post_id: UUID = Field(foreign_key="posts.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tags.id", primary_key=True)


class PostBase(SQLModel):
    title: str = Field(max_length=200)
    content: str
    excerpt: Optional[str] = Field(default=None, max_length=500)
    status: PostStatus = Field(default=PostStatus.DRAFT)
    is_featured: bool = Field(default=False)
    published_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class Post(PostBase, table=True):
    __tablename__ = "posts"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    author_id: UUID = Field(foreign_key="users.id")
    slug: str = Field(unique=True, index=True)
    view_count: int = Field(default=0)
    
    # Relationships
    author: "User" = Relationship(back_populates="posts")
    tags: List["Tag"] = Relationship(back_populates="posts", link_model=PostTagLink)
    comments: List["Comment"] = Relationship(back_populates="post")


class PostCreate(SQLModel):
    title: str = Field(max_length=200)
    content: str
    excerpt: Optional[str] = Field(default=None, max_length=500)
    status: PostStatus = PostStatus.DRAFT
    is_featured: bool = False
    tag_names: Optional[List[str]] = Field(default=None)


class PostRead(PostBase):
    id: UUID
    author_id: UUID
    slug: str
    view_count: int


class PostUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)
    content: Optional[str] = Field(default=None)
    excerpt: Optional[str] = Field(default=None, max_length=500)
    status: Optional[PostStatus] = Field(default=None)
    is_featured: Optional[bool] = Field(default=None)
    tag_names: Optional[List[str]] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    slug: str = Field(unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    posts: List[Post] = Relationship(back_populates="tags", link_model=PostTagLink)


class TagCreate(SQLModel):
    name: str = Field(max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)


class TagRead(SQLModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime


class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="posts.id")
    author_id: UUID = Field(foreign_key="users.id")
    content: str = Field(max_length=1000)
    is_approved: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    post: Post = Relationship(back_populates="comments")
    author: "User" = Relationship()


class CommentCreate(SQLModel):
    content: str = Field(max_length=1000)


class CommentRead(SQLModel):
    id: UUID
    post_id: UUID
    author_id: UUID
    content: str
    is_approved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime
import re

from app.posts.models import (
    Post, PostCreate, PostUpdate, PostStatus,
    Tag, TagCreate,
    Comment, CommentCreate,
    PostTagLink
)
from app.posts.schemas import (
    PostCreateRequest, PostUpdateRequest,
    TagCreateRequest, TagUpdateRequest,
    CommentCreateRequest
)
from app.auth.models import User
from app.exceptions import NotFoundError, UnauthorizedError, ConflictError


class PostService:
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s-]+', '-', slug)
        slug = slug.strip('-')
        return slug[:100]  # Limit length
    
    async def _ensure_unique_slug(self, session: AsyncSession, base_slug: str, post_id: Optional[UUID] = None) -> str:
        """Ensure slug is unique by adding number suffix if needed"""
        slug = base_slug
        counter = 1
        
        while True:
            query = select(Post).where(Post.slug == slug)
            if post_id:
                query = query.where(Post.id != post_id)
            
            result = await session.execute(query)
            existing_post = result.scalar_one_or_none()
            
            if not existing_post:
                return slug
            
            slug = f"{base_slug}-{counter}"
            counter += 1
    
    async def _get_or_create_tags(self, session: AsyncSession, tag_names: List[str]) -> List[Tag]:
        """Get existing tags or create new ones"""
        tags = []
        
        for tag_name in tag_names:
            tag_name = tag_name.strip().lower()
            if not tag_name:
                continue
            
            # Try to find existing tag
            result = await session.execute(select(Tag).where(Tag.name == tag_name))
            tag = result.scalar_one_or_none()
            
            if not tag:
                # Create new tag
                tag_slug = self._generate_slug(tag_name)
                tag_slug = await self._ensure_unique_tag_slug(session, tag_slug)
                
                tag = Tag(
                    name=tag_name,
                    slug=tag_slug
                )
                session.add(tag)
                await session.flush()  # Get the ID
            
            tags.append(tag)
        
        return tags
    
    async def _ensure_unique_tag_slug(self, session: AsyncSession, base_slug: str, tag_id: Optional[UUID] = None) -> str:
        """Ensure tag slug is unique"""
        slug = base_slug
        counter = 1
        
        while True:
            query = select(Tag).where(Tag.slug == slug)
            if tag_id:
                query = query.where(Tag.id != tag_id)
            
            result = await session.execute(query)
            existing_tag = result.scalar_one_or_none()
            
            if not existing_tag:
                return slug
            
            slug = f"{base_slug}-{counter}"
            counter += 1
    
    async def create_post(self, session: AsyncSession, post_data: PostCreateRequest, author: User) -> Post:
        """Create a new post"""
        # Generate slug
        slug = self._generate_slug(post_data.title)
        slug = await self._ensure_unique_slug(session, slug)
        
        # Set published_at if status is published
        published_at = datetime.utcnow() if post_data.status == PostStatus.PUBLISHED else None
        
        # Create post
        post = Post(
            title=post_data.title,
            content=post_data.content,
            excerpt=post_data.excerpt,
            status=post_data.status,
            is_featured=post_data.is_featured,
            slug=slug,
            author_id=author.id,
            published_at=published_at
        )
        
        session.add(post)
        await session.flush()  # Get the post ID
        
        # Handle tags
        if post_data.tag_names:
            tags = await self._get_or_create_tags(session, post_data.tag_names)
            post.tags = tags
        
        await session.commit()
        await session.refresh(post)
        return post
    
    async def get_post_by_id(self, session: AsyncSession, post_id: UUID) -> Optional[Post]:
        """Get post by ID with related data"""
        query = select(Post).options(
            selectinload(Post.author),
            selectinload(Post.tags)
        ).where(Post.id == post_id)
        
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_post_by_slug(self, session: AsyncSession, slug: str) -> Optional[Post]:
        """Get post by slug with related data"""
        query = select(Post).options(
            selectinload(Post.author),
            selectinload(Post.tags)
        ).where(Post.slug == slug)
        
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_posts(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        status: Optional[PostStatus] = None,
        author_id: Optional[UUID] = None,
        tag_slug: Optional[str] = None,
        search: Optional[str] = None,
        is_featured: Optional[bool] = None
    ) -> Tuple[List[Post], int]:
        """Get posts with filters and pagination"""
        query = select(Post).options(
            selectinload(Post.author),
            selectinload(Post.tags)
        )
        
        # Apply filters
        conditions = []
        
        if status:
            conditions.append(Post.status == status)
        
        if author_id:
            conditions.append(Post.author_id == author_id)
        
        if is_featured is not None:
            conditions.append(Post.is_featured == is_featured)
        
        if tag_slug:
            # Join with tags to filter by tag slug
            query = query.join(Post.tags).where(Tag.slug == tag_slug)
        
        if search:
            search_term = f"%{search}%"
            conditions.append(
                or_(
                    Post.title.ilike(search_term),
                    Post.content.ilike(search_term),
                    Post.excerpt.ilike(search_term)
                )
            )
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Get total count
        count_query = select(func.count(Post.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))
        if tag_slug:
            count_query = count_query.join(Post.tags).where(Tag.slug == tag_slug)
        
        total_result = await session.execute(count_query)
        total = total_result.scalar()
        
        # Get posts with pagination
        query = query.offset(skip).limit(limit).order_by(Post.created_at.desc())
        result = await session.execute(query)
        posts = result.scalars().unique().all()
        
        return list(posts), total
    
    async def update_post(
        self,
        session: AsyncSession,
        post_id: UUID,
        post_data: PostUpdateRequest,
        current_user: User
    ) -> Post:
        """Update post"""
        post = await self.get_post_by_id(session, post_id)
        if not post:
            raise NotFoundError("Post not found")
        
        # Check permissions
        if post.author_id != current_user.id and not current_user.is_superuser:
            raise UnauthorizedError("Not enough permissions")
        
        # Update fields
        update_data = post_data.model_dump(exclude_unset=True, exclude={'tag_names'})
        
        # Handle slug update if title changed
        if 'title' in update_data:
            new_slug = self._generate_slug(update_data['title'])
            if new_slug != post.slug:
                new_slug = await self._ensure_unique_slug(session, new_slug, post.id)
                update_data['slug'] = new_slug
        
        # Handle status change to published
        if 'status' in update_data and update_data['status'] == PostStatus.PUBLISHED and post.status != PostStatus.PUBLISHED:
            update_data['published_at'] = datetime.utcnow()
        
        # Update post fields
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            for field, value in update_data.items():
                setattr(post, field, value)
        
        # Handle tags
        if post_data.tag_names is not None:
            tags = await self._get_or_create_tags(session, post_data.tag_names)
            post.tags = tags
        
        await session.commit()
        await session.refresh(post)
        return post
    
    async def delete_post(self, session: AsyncSession, post_id: UUID, current_user: User) -> bool:
        """Delete post"""
        post = await self.get_post_by_id(session, post_id)
        if not post:
            raise NotFoundError("Post not found")
        
        # Check permissions
        if post.author_id != current_user.id and not current_user.is_superuser:
            raise UnauthorizedError("Not enough permissions")
        
        await session.delete(post)
        await session.commit()
        return True
    
    async def increment_view_count(self, session: AsyncSession, post_id: UUID) -> bool:
        """Increment post view count"""
        post = await self.get_post_by_id(session, post_id)
        if not post:
            return False
        
        post.view_count += 1
        await session.commit()
        return True


post_service = PostService()
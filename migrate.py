#!/usr/bin/env python3
"""
Database migration script for PostgreSQL setup
"""

import asyncio
import sys
from sqlmodel import SQLModel
from app.database import engine
from app.config import settings

# Import all models to ensure they are registered with SQLModel
from app.auth.models import User
from app.posts.models import Post
from app.users.models import UserProfile


async def create_tables():
    """Create all database tables"""
    print(f"Creating tables for database: {settings.DB_NAME}")
    print(f"Database URL: {settings.database_url}")
    
    try:
        async with engine.begin() as conn:
            # Drop all tables (use with caution in production)
            # await conn.run_sync(SQLModel.metadata.drop_all)
            
            # Create all tables
            await conn.run_sync(SQLModel.metadata.create_all)
            
        print("✅ Database tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)
    
    finally:
        await engine.dispose()


async def drop_tables():
    """Drop all database tables"""
    print(f"Dropping tables for database: {settings.DB_NAME}")
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            
        print("✅ Database tables dropped successfully!")
        
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        sys.exit(1)
    
    finally:
        await engine.dispose()


async def reset_database():
    """Reset database by dropping and recreating all tables"""
    print("🔄 Resetting database...")
    await drop_tables()
    await create_tables()
    print("✅ Database reset completed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration script")
    parser.add_argument(
        "action", 
        choices=["create", "drop", "reset"], 
        help="Action to perform: create, drop, or reset tables"
    )
    
    args = parser.parse_args()
    
    if args.action == "create":
        asyncio.run(create_tables())
    elif args.action == "drop":
        asyncio.run(drop_tables())
    elif args.action == "reset":
        asyncio.run(reset_database())
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class UserPreferences(SQLModel, table=True):
    __tablename__ = "user_preferences"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)
    
    # Basic Info
    gender: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    age_min: Optional[int] = Field(default=None)
    age_max: Optional[int] = Field(default=None)
    location: Optional[str] = Field(default=None)
    
    # Lifestyle
    education: Optional[str] = Field(default=None)
    occupation: Optional[str] = Field(default=None)
    income: Optional[str] = Field(default=None)
    religion: Optional[str] = Field(default=None)
    smoking: Optional[str] = Field(default=None)
    drinking: Optional[str] = Field(default=None)
    exercise: Optional[str] = Field(default=None)
    
    # Relationship Goals
    relationship_type: Optional[str] = Field(default=None)
    children: Optional[str] = Field(default=None)
    pets: Optional[str] = Field(default=None)
    
    # Personality & Interests
    personality_type: Optional[str] = Field(default=None)
    hobbies: Optional[str] = Field(default=None)
    music_taste: Optional[str] = Field(default=None)
    movie_preference: Optional[str] = Field(default=None)
    
    # Text Preferences (Q14-22)
    communication_style: Optional[str] = Field(default=None)
    love_language: Optional[str] = Field(default=None)
    conflict_resolution: Optional[str] = Field(default=None)
    social_preference: Optional[str] = Field(default=None)
    travel_preference: Optional[str] = Field(default=None)
    food_preference: Optional[str] = Field(default=None)
    weekend_activity: Optional[str] = Field(default=None)
    financial_approach: Optional[str] = Field(default=None)
    future_goals: Optional[str] = Field(default=None)
    
    # Visual Test Results
    visual_test_completed: bool = Field(default=False)
    visual_preferences: Optional[str] = Field(default=None)  # JSON string
    
    # Completion Status
    basic_completed: bool = Field(default=False)
    text_completed: bool = Field(default=False)
    all_completed: bool = Field(default=False)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class UserPreferencesCreate(SQLModel):
    # Basic Info
    gender: Optional[str] = None
    age: Optional[int] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    location: Optional[str] = None
    
    # Lifestyle
    education: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[str] = None
    religion: Optional[str] = None
    smoking: Optional[str] = None
    drinking: Optional[str] = None
    exercise: Optional[str] = None
    
    # Relationship Goals
    relationship_type: Optional[str] = None
    children: Optional[str] = None
    pets: Optional[str] = None
    
    # Personality & Interests
    personality_type: Optional[str] = None
    hobbies: Optional[str] = None
    music_taste: Optional[str] = None
    movie_preference: Optional[str] = None
    
    # Text Preferences
    communication_style: Optional[str] = None
    love_language: Optional[str] = None
    conflict_resolution: Optional[str] = None
    social_preference: Optional[str] = None
    travel_preference: Optional[str] = None
    food_preference: Optional[str] = None
    weekend_activity: Optional[str] = None
    financial_approach: Optional[str] = None
    future_goals: Optional[str] = None
    
    # Visual Test
    visual_preferences: Optional[str] = None


class UserPreferencesRead(SQLModel):
    id: UUID
    user_id: UUID
    
    # Basic Info
    gender: Optional[str] = None
    age: Optional[int] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    location: Optional[str] = None
    
    # Lifestyle
    education: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[str] = None
    religion: Optional[str] = None
    smoking: Optional[str] = None
    drinking: Optional[str] = None
    exercise: Optional[str] = None
    
    # Relationship Goals
    relationship_type: Optional[str] = None
    children: Optional[str] = None
    pets: Optional[str] = None
    
    # Personality & Interests
    personality_type: Optional[str] = None
    hobbies: Optional[str] = None
    music_taste: Optional[str] = None
    movie_preference: Optional[str] = None
    
    # Text Preferences
    communication_style: Optional[str] = None
    love_language: Optional[str] = None
    conflict_resolution: Optional[str] = None
    social_preference: Optional[str] = None
    travel_preference: Optional[str] = None
    food_preference: Optional[str] = None
    weekend_activity: Optional[str] = None
    financial_approach: Optional[str] = None
    future_goals: Optional[str] = None
    
    # Visual Test
    visual_test_completed: bool = False
    visual_preferences: Optional[str] = None
    
    # Completion Status
    basic_completed: bool = False
    text_completed: bool = False
    all_completed: bool = False
    
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserPreferencesUpdate(SQLModel):
    # Basic Info
    gender: Optional[str] = None
    age: Optional[int] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    location: Optional[str] = None
    
    # Lifestyle
    education: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[str] = None
    religion: Optional[str] = None
    smoking: Optional[str] = None
    drinking: Optional[str] = None
    exercise: Optional[str] = None
    
    # Relationship Goals
    relationship_type: Optional[str] = None
    children: Optional[str] = None
    pets: Optional[str] = None
    
    # Personality & Interests
    personality_type: Optional[str] = None
    hobbies: Optional[str] = None
    music_taste: Optional[str] = None
    movie_preference: Optional[str] = None
    
    # Text Preferences
    communication_style: Optional[str] = None
    love_language: Optional[str] = None
    conflict_resolution: Optional[str] = None
    social_preference: Optional[str] = None
    travel_preference: Optional[str] = None
    food_preference: Optional[str] = None
    weekend_activity: Optional[str] = None
    financial_approach: Optional[str] = None
    future_goals: Optional[str] = None
    
    # Visual Test
    visual_preferences: Optional[str] = None
    visual_test_completed: Optional[bool] = None
    
    # Completion Status
    basic_completed: Optional[bool] = None
    text_completed: Optional[bool] = None
    all_completed: Optional[bool] = None
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL = "postgresql+asyncpg://postgres:fadlipsgr123@localhost:5432/uas-ml"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "fadlipsgr123"
    DB_NAME: str = "uas-ml"
    
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    DEBUG: bool = True
    PROJECT_NAME: str = "FastAPI Backend"
    APP_NAME: str = "FastAPI ML Project"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_HOSTS: list[str] = ["*"]
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    # Email/SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: str = "587"
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""
    
    # File Upload
    MAX_FILE_SIZE: str = "5242880"  # 5MB
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True 


settings = Settings()
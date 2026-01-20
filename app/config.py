"""Konfigurasi aplikasi akademik"""
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Settings untuk aplikasi akademik"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./akademik.db"
    SQLALCHEMY_ECHO: bool = False
    
    # Application
    APP_NAME: str = "Aplikasi Akademik"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # NIM Configuration
    NIM_BATCH_SIZE: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

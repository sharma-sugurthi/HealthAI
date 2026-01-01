"""
Application configuration management.
Centralizes all configuration settings with environment-specific support.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class"""
    
    # Application Settings
    APP_NAME: str = os.getenv('APP_NAME', 'HealthAI')
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database Settings
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///healthai.db')
    
    # Security Settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # JWT Settings
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '7'))
    
    # OpenRouter API Settings
    OPENROUTER_API_KEY: Optional[str] = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_BASE_URL: str = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    OPENROUTER_REFERER: str = os.getenv('OPENROUTER_REFERER', 'https://healthai.app')
    OPENROUTER_TITLE: str = os.getenv('OPENROUTER_TITLE', 'HealthAI Assistant')
    
    # AI Model Settings
    AI_MODEL: str = os.getenv('AI_MODEL', 'x-ai/grok-beta')
    AI_MAX_RETRIES: int = int(os.getenv('AI_MAX_RETRIES', '3'))
    AI_RETRY_DELAY: int = int(os.getenv('AI_RETRY_DELAY', '2'))
    AI_TEMPERATURE: float = float(os.getenv('AI_TEMPERATURE', '0.7'))
    AI_MAX_TOKENS: int = int(os.getenv('AI_MAX_TOKENS', '2000'))
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/healthai.log')
    
    # API Settings
    API_HOST: str = os.getenv('API_HOST', '0.0.0.0')
    API_PORT: int = int(os.getenv('API_PORT', '8000'))
    API_WORKERS: int = int(os.getenv('API_WORKERS', '4'))
    API_PREFIX: str = '/api/v1'
    
    # CORS Settings
    ALLOWED_ORIGINS: list = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:8501').split(',')
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration"""
        if not cls.OPENROUTER_API_KEY and cls.ENVIRONMENT == 'production':
            raise ValueError("OPENROUTER_API_KEY is required in production")
        
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production' and cls.ENVIRONMENT == 'production':
            raise ValueError("SECRET_KEY must be changed in production")
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development mode"""
        return cls.ENVIRONMENT == 'development'
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode"""
        return cls.ENVIRONMENT == 'production'
    
    @classmethod
    def is_testing(cls) -> bool:
        """Check if running in testing mode"""
        return cls.ENVIRONMENT == 'testing'


# Global config instance
config = Config()

# Validate configuration on import
if config.ENVIRONMENT != 'testing':
    config.validate()

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Email settings
    MAIL_USERNAME: str = Field(..., description="Email username")
    MAIL_PASSWORD: str = Field(..., description="Email password")
    MAIL_SERVER: str = Field(..., description="IMAP server address")
    
    # Telegram settings
    BOT_TOKEN: str = Field(..., description="Telegram bot token")
    CHAT_ID: str = Field(..., description="Telegram chat ID")
    
    # Application settings
    CHECK_INTERVAL: int = Field(default=300, description="Interval between email checks in seconds")
    RETRY_INTERVAL: int = Field(default=60, description="Interval between retries in case of error in seconds")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create global settings instance
settings = Settings() 
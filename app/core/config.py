from pydantic.v1 import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = 'Chatbot-AI-backend'
    DATABASE_URL: str = 'sqlite:///chatbot.db'
    OPENAI_API_KEY: str = ''
    SESSION_EXPIRE_HOURS: int = 24
    DEBUG: bool = False

    class Config:
        env_file = '.env'

settings = Settings()
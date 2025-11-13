from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = 'Chatbot-AI-backend'
    DATABASE_URL: str = 'sqlite:///chatbot.db'
    OPENAI_API_KEY: str = ''

    class Config:
        env_file = '.env'

settings = Settings()

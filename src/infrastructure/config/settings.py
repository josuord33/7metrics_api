from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    API_TITLE: str
    API_VERSION: str
    DEBUG: bool

    class Config:
        env_file = ".env"

settings = Settings()
